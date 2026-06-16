"""Declarative filter rules — repositories declare what fields map to what SQL clauses,
the generic applier handles the WHERE/JOIN plumbing.

Adding a new filter is one tuple in the rules list. The repository's list() method
never grows.
"""
from dataclasses import dataclass
from operator import eq, ge, gt, le, lt
from typing import Any, Callable

from pydantic import BaseModel
from sqlalchemy import ColumnElement, Select

# Re-export operators so rule definitions don't need a separate import
__all__ = ["FilterRule", "apply_filter_rules", "eq", "ge", "gt", "le", "lt", "like_op"]


def like_op(column: ColumnElement[Any], value: str) -> ColumnElement[bool]:
    """Convenience LIKE wrapper — auto-wraps with % unless already provided."""
    if "%" not in value:
        value = f"%{value}%"
    return column.like(value)


@dataclass(frozen=True)
class FilterRule:
    """Declarative spec: when `field` on a filters object is non-None, apply `op(column, value)`.

    Optional join + extra_where for filters that need related-table predicates
    (e.g. catalyst_name filters ReagentORM.name with an implicit role=catalyst).
    """
    field: str                                            # attribute on the BaseModel filters
    column: ColumnElement[Any]                            # SQLAlchemy column to filter on
    op: Callable[[Any, Any], ColumnElement[bool]] = eq    # operator: eq, ge, le, gt, lt, like_op
    transform: Callable[[Any], Any] | None = None         # e.g. enum -> str
    join: Any | None = None                               # SQLAlchemy entity or relationship to join
    extra_where: ColumnElement[bool] | None = None        # extra constraint applied with this rule


def apply_filter_rules(
    stmt: Select,
    filters: BaseModel,
    rules: list[FilterRule],
) -> Select:
    """Apply each rule's WHERE clause if the corresponding filter field is set.

    Joins and extra_where constraints are deduplicated by object identity so multiple
    rules can share the same join (e.g. yield_min + yield_max both join ResultORM once).
    """
    joined: set[int] = set()
    applied_extras: set[int] = set()

    for rule in rules:
        value = getattr(filters, rule.field, None)
        if value is None:
            continue

        if rule.join is not None and id(rule.join) not in joined:
            stmt = stmt.join(rule.join)
            joined.add(id(rule.join))

        if rule.extra_where is not None and id(rule.extra_where) not in applied_extras:
            stmt = stmt.where(rule.extra_where)
            applied_extras.add(id(rule.extra_where))

        if rule.transform is not None:
            value = rule.transform(value)

        stmt = stmt.where(rule.op(rule.column, value))

    return stmt
