#!/usr/bin/env python3
#run by command "python script\plot_pvt_open_loop_gain.py"
"""Plot closed-loop gain comparison for CLS and non-CLS circuits."""

from pathlib import Path

import matplotlib.pyplot as plt


def main() -> None:
    # Data source:
    # doc_thesis/contents/04-2_MainBody.tex
    # Table: "CLS电路闭环增益"
    c1_c2 = [2, 10, 20, 40, 100, 200]
    gain_with_cls = [1.99, 8.74, 15.12, 24.30, 36.06, 42.58]
    gain_without_cls = [1.78, 6.73, 10.37, 14.26, 18.44, 20.22]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(c1_c2, gain_with_cls, marker="o", linewidth=2, label="With CLS")
    ax.plot(c1_c2, gain_without_cls, marker="s", linewidth=2, label="Without CLS")

    ax.set_xlabel("C1/C2")
    ax.set_ylabel("Gain")
    ax.set_title("Closed-loop Gain Comparison")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(frameon=False)
    fig.tight_layout()

    output_path = (
        Path(__file__).resolve().parent.parent
        / "doc_thesis"
        / "figs"
        / "04"
        / "cls_closed_loop_gain.png"
    )
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plot to: {output_path}")


if __name__ == "__main__":
    main()
