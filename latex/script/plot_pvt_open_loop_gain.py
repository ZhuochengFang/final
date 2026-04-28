#!/usr/bin/env python3
#run by command "python script\plot_pvt_open_loop_gain.py"
"""Plot open-loop gain under different PVT conditions for CLS and non-CLS LVFIA."""

from pathlib import Path

import matplotlib.pyplot as plt


def main() -> None:
    # Data source:
    # doc_thesis/contents/04-2_MainBody.tex
    # Table: "不同PVT条件下的CLS电路开环增益"
    # Table: "不同PVT条件下无CLS的LVFIA电路开环增益"
    voltages = [0.7, 0.65, 0.6, 0.55, 0.5, 0.45]
    temperatures = [-40, 25, 80]

    cls_gain = {
        -40: [46.27, 49.55, 53.78, 56.47, 57.55, 57.55],
        25: [43.56, 46.50, 49.44, 53.13, 55.31, 55.31],
        80: [23.41, 32.84, 35.42, 37.04, 37.79, 37.79],
    }

    no_cls_gain = {
        -40: [23.65, 25.07, 26.16, 26.68, 26.68, 26.68],
        25: [20.13, 21.62, 22.51, 23.08, 23.33, 23.33],
        80: [12.67, 18.85, 20.65, 21.97, 22.91, 23.45],
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    markers = ["o", "s", "^"]
    datasets = [
        ("CLS Open-loop Gain", cls_gain),
        ("No-CLS LVFIA Open-loop Gain", no_cls_gain),
    ]

    for ax, (title, gain_data) in zip(axes, datasets):
        for idx, temp in enumerate(temperatures):
            ax.plot(
                voltages,
                gain_data[temp],
                marker=markers[idx % len(markers)],
                linewidth=2,
                label=f"T = {temp} degC",
            )
        ax.set_title(title)
        ax.set_xlabel("Supply Voltage VDD (V)")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.invert_xaxis()
        ax.legend(frameon=False)

    axes[0].set_ylabel("Open-loop Gain")
    fig.tight_layout()

    output_dir = Path(__file__).resolve().parent.parent / "doc_thesis" / "figs" / "04"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "pvt_open_loop_gain.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plot to: {output_path}")


if __name__ == "__main__":
    main()
