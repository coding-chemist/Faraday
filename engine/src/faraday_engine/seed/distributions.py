"""Probability distributions used across seeders. Pure functions, deterministic given an rng.

Yields are NOT independent of conditions — `correlated_yield()` shifts the mean based on a
condition-fit score so a good catalyst/solvent/base combination produces believably high
yields and a bad combination produces believably bad ones.
"""
import math
from collections.abc import Sequence
from random import Random
from typing import TypeVar

T = TypeVar("T")


def weighted_choice(rng: Random, items: Sequence[tuple[T, float]]) -> T:
    """Pick one item with weights. Items: [(value, weight), ...]."""
    total = sum(w for _, w in items)
    r = rng.uniform(0, total)
    cum = 0.0
    for value, weight in items:
        cum += weight
        if r <= cum:
            return value
    return items[-1][0]


def skewed_yield(rng: Random, mu: float = 72.0, sigma: float = 15.0, low: float = 10.0, high: float = 99.0) -> float:
    """Right-skewed normal — most yields cluster around mu, with a fat low-yield tail.

    Mimics real medchem yield distributions where most reactions are decent but failures
    exist. Returns a value in [low, high].
    """
    # Sample from skew-normal-ish via reflecting low tail
    raw = rng.gauss(mu, sigma)
    if raw > high:
        raw = high - rng.uniform(0, 3)
    if raw < low:
        raw = low + rng.uniform(0, 5)
    return round(raw, 1)


def correlated_yield(
    rng: Random,
    fit_score: float,
    base_mu: float = 72.0,
    base_sigma: float = 12.0,
) -> float:
    """Yield biased by condition fit. fit_score in [-1, 1]: -1=bad fit, +1=excellent fit.

    Shifts mean by up to ±18%. Mediocre score (0) gives base distribution.
    """
    mu = base_mu + 18.0 * fit_score
    sigma = max(6.0, base_sigma - 4.0 * abs(fit_score))  # confident yields when fit is clear
    return skewed_yield(rng, mu=mu, sigma=sigma)


def lognormal_time(rng: Random, median_h: float = 12.0, sigma: float = 0.5) -> float:
    """Reaction time in minutes — lognormal so most reactions are around the median with a
    long tail toward overnighters."""
    hours = rng.lognormvariate(math.log(median_h), sigma)
    hours = max(0.5, min(48.0, hours))
    return round(hours * 60, 0)


def gaussian_clamped(rng: Random, mu: float, sigma: float, low: float, high: float) -> float:
    """Normal sample clamped to [low, high]. For temperature, etc."""
    return max(low, min(high, rng.gauss(mu, sigma)))


def date_in_last_n_months(rng: Random, n: int, recency_bias: float = 1.3):
    """Returns a datetime within the last n months, biased toward recent dates.

    recency_bias > 1.0 means more samples near now; 1.0 = uniform.
    """
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    days_span = n * 30
    # Sample uniformly then bias by raising to power
    u = rng.random() ** (1.0 / recency_bias)
    days_back = days_span * (1.0 - u)
    hour = rng.randint(8, 19)
    minute = rng.randint(0, 59)
    return (now - timedelta(days=days_back)).replace(hour=hour, minute=minute, second=0, microsecond=0)
