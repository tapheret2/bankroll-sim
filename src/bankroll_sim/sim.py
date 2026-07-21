from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Literal

Mode = Literal["flat", "prop", "kelly"]


@dataclass
class Result:
    mode: str
    final: float
    peak: float
    max_drawdown: float
    ruined: bool
    path: list[float]


def _kelly_f(p: float, b: float) -> float:
    q = 1.0 - p
    return max(0.0, (p * b - q) / b)


def simulate(
    p: float,
    b: float,
    bankroll: float,
    n: int,
    mode: Mode = "prop",
    stake: float = 10.0,
    frac: float = 0.02,
    kelly_mult: float = 0.5,
    seed: int | None = None,
) -> Result:
    rng = random.Random(seed)
    br = bankroll
    path = [br]
    peak = br
    max_dd = 0.0
    kf = _kelly_f(p, b) * kelly_mult

    for _ in range(n):
        if br <= 0:
            break
        if mode == "flat":
            s = min(stake, br)
        elif mode == "prop":
            s = br * frac
        else:
            s = br * kf
        if s <= 0:
            break
        if rng.random() < p:
            br = br + s * b
        else:
            br = br - s
        if br < 0:
            br = 0.0
        path.append(br)
        peak = max(peak, br)
        dd = (peak - br) / peak if peak > 0 else 0.0
        max_dd = max(max_dd, dd)

    return Result(
        mode=mode,
        final=br,
        peak=peak,
        max_drawdown=max_dd,
        ruined=br <= 1e-9,
        path=path,
    )


def compare_modes(p: float, b: float, bankroll: float, n: int, seed: int = 0) -> list[Result]:
    return [
        simulate(p, b, bankroll, n, mode="flat", stake=bankroll * 0.02, seed=seed),
        simulate(p, b, bankroll, n, mode="prop", frac=0.02, seed=seed),
        simulate(p, b, bankroll, n, mode="kelly", kelly_mult=0.5, seed=seed),
    ]


def ruin_probability(
    p: float,
    b: float,
    bankroll: float,
    n: int,
    mode: Mode = "prop",
    trials: int = 200,
    **kwargs,
) -> float:
    """Monte Carlo estimate of ruin frequency over *trials* paths."""
    ruined = 0
    for i in range(trials):
        seed = kwargs.get("seed")
        s = None if seed is None else seed + i
        res = simulate(p, b, bankroll, n, mode=mode, seed=s, **{k: v for k, v in kwargs.items() if k != "seed"})
        if res.ruined:
            ruined += 1
    return ruined / trials if trials else 0.0


def growth_factor(final: float, initial: float) -> float:
    """Return final/initial bankroll ratio (0 if initial <= 0)."""
    if initial <= 0:
        return 0.0
    return final / initial


def median_final_bankroll(
    p: float,
    b: float,
    bankroll: float,
    n: int,
    mode: Mode = "prop",
    trials: int = 101,
    **kwargs,
) -> float:
    """Median terminal bankroll across independent Monte Carlo paths."""
    finals: list[float] = []
    seed = kwargs.pop("seed", None)
    for i in range(trials):
        s = None if seed is None else int(seed) + i
        res = simulate(p, b, bankroll, n, mode=mode, seed=s, **kwargs)
        finals.append(float(res.final))
    finals.sort()
    return finals[len(finals) // 2] if finals else 0.0


def percentile_final_bankroll(
    p: float,
    b: float,
    bankroll: float,
    n: int,
    q: float = 0.1,
    mode: Mode = "prop",
    trials: int = 101,
    **kwargs,
) -> float:
    """Empirical q-quantile of terminal bankroll (q in [0, 1])."""
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be in [0, 1]")
    finals: list[float] = []
    seed = kwargs.pop("seed", None)
    for i in range(trials):
        s = None if seed is None else int(seed) + i
        res = simulate(p, b, bankroll, n, mode=mode, seed=s, **kwargs)
        finals.append(float(res.final))
    finals.sort()
    if not finals:
        return 0.0
    idx = min(len(finals) - 1, max(0, int(q * (len(finals) - 1))))
    return finals[idx]
