#!/usr/bin/env python3
"""Plot V(C1) vs time for an exponential-like drop from Vin to Vx on [0, Ts/2]."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def vc1_profile(t: np.ndarray, ts: float, vin: float, vx: float, a: float) -> np.ndarray:
    """Endpoint-constrained exponential-like profile.

    Satisfies:
    - V(0) = Vin
    - V(Ts/2) = Vx
    """
    t_end = ts / 2.0
    exp_t = np.exp(-a * t)
    exp_end = np.exp(-a * t_end)
    return vx + (vin - vx) * (exp_t - exp_end) / (1.0 - exp_end)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plot V(C1) decreasing from Vin to Vx over 0..Ts/2 with an exponential trend."
    )
    parser.add_argument("--Ts", type=float, default=10e-6, help="Switching period Ts (seconds)")
    parser.add_argument("--Vin", type=float, default=1.2, help="Initial voltage Vin (V)")
    parser.add_argument("--Vx", type=float, default=0.35, help="Final voltage Vx at Ts/2 (V)")
    parser.add_argument("--a", type=float, default=7.0e5, help="Exponential factor a in exp(-a t)")
    parser.add_argument("--points", type=int, default=600, help="Number of sampled points")
    parser.add_argument(
        "--out",
        type=Path,
        default=(
            Path(__file__).resolve().parent.parent
            / "doc_thesis"
            / "figs"
            / "04"
            / "vc1_time_plot.png"
        ),
        help="Output image path",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    t = np.linspace(0.0, args.Ts / 2.0, args.points)
    v = vc1_profile(t, args.Ts, args.Vin, args.Vx, args.a)

    plt.figure(figsize=(7.5, 4.8))
    plt.plot(t, v, color="#1f77b4", linewidth=2.2, label="V(C1)")
    plt.scatter([0.0, args.Ts / 2.0], [args.Vin, args.Vx], color="#d62728", zorder=3)

    plt.title("V(C1) Exponential-Like Drop in 0 to Ts/2")
    plt.xlabel("Time (s)")
    plt.ylabel("V(C1) (V)")

    # Use symbolic tick labels to avoid presenting concrete numeric values.
    plt.xticks([0.0, args.Ts / 2.0], ["0", "Ts/2"])
    plt.yticks([args.Vx, args.Vin], ["Vx", "Vin"])

    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.out, dpi=180)
    print(f"Saved plot to: {args.out}")


if __name__ == "__main__":
    main()
