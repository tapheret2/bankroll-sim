from __future__ import annotations

import argparse
import json
import sys

from .sim import compare_modes, simulate


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="bankroll-sim")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run")
    r.add_argument("--p", type=float, required=True)
    r.add_argument("--odds", type=float, required=True)
    r.add_argument("--bankroll", type=float, default=1000)
    r.add_argument("--n", type=int, default=200)
    r.add_argument("--mode", choices=["flat", "prop", "kelly"], default="prop")
    r.add_argument("--stake", type=float, default=20.0)
    r.add_argument("--frac", type=float, default=0.02)
    r.add_argument("--kelly-mult", type=float, default=0.5)
    r.add_argument("--seed", type=int, default=None)
    r.add_argument("--json", action="store_true")

    c = sub.add_parser("compare")
    c.add_argument("--p", type=float, required=True)
    c.add_argument("--odds", type=float, required=True)
    c.add_argument("--bankroll", type=float, default=1000)
    c.add_argument("--n", type=int, default=200)
    c.add_argument("--seed", type=int, default=0)

    args = p.parse_args(argv)
    b = args.odds - 1.0

    if args.cmd == "run":
        res = simulate(
            args.p, b, args.bankroll, args.n,
            mode=args.mode, stake=args.stake, frac=args.frac,
            kelly_mult=args.kelly_mult, seed=args.seed,
        )
        payload = {
            "mode": res.mode, "final": res.final, "peak": res.peak,
            "max_drawdown": res.max_drawdown, "ruined": res.ruined,
        }
        print(json.dumps(payload, indent=2) if args.json else payload)
        return 0

    rows = compare_modes(args.p, b, args.bankroll, args.n, seed=args.seed)
    for res in rows:
        print(f"{res.mode:6} final={res.final:10.2f} mdd={res.max_drawdown:6.1%} ruined={res.ruined}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
