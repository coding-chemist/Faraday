"""Declarative chemistry fit rules — same pattern as FilterRule in repositories.

Instead of stacked `if ...: fit += X` blocks in each seeder, each rule is one declarative
entry. Adding a chemistry condition = one line in the rules list. The seeder's generate()
method never grows.
"""
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FitRule:
    """One declarative fit rule.

    When `when(ctx)` is True for the current condition context, adds `delta` to the
    aggregate score. `reason` is the chemistry rationale, kept inline for explainability
    (used in logs / debug output, never a code branch).
    """
    when: Callable[[Any], bool]
    delta: float
    reason: str = ""


def compute_fit(ctx: Any, rules: list[FitRule], lo: float = -1.0, hi: float = 1.0) -> float:
    """Aggregate fit score from declarative rules, clamped to [lo, hi].

    A `ctx` is whatever the seeder's context dataclass exposes — typically the chosen
    substrate, reagents, solvent, base, plus any boolean flags (e.g. use_hobt). Each rule's
    `when` lambda reads from that context.
    """
    score = sum(rule.delta for rule in rules if rule.when(ctx))
    return max(lo, min(hi, score))


def explain_fit(ctx: Any, rules: list[FitRule]) -> list[tuple[str, float]]:
    """Return the (reason, delta) tuples for rules that fired. Useful for debugging
    why a generated experiment got the yield bias it did."""
    return [(rule.reason, rule.delta) for rule in rules if rule.when(ctx)]
