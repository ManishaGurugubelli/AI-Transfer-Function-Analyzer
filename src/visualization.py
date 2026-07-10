import os
import numpy as np
import matplotlib

# Streamlit backend
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from scipy import signal

# ==========================================================
# CONFIGURATION
# ==========================================================

PLOT_DIR = "../plots"
os.makedirs(PLOT_DIR, exist_ok=True)


# ==========================================================
# BUILD TRANSFER FUNCTION
# ==========================================================

def build_system(numerator, denominator):

    num = list(numerator)
    den = list(denominator)

    while len(num) > 1 and abs(num[0]) < 1e-12:
        num.pop(0)

    while len(den) > 1 and abs(den[0]) < 1e-12:
        den.pop(0)

    return signal.TransferFunction(num, den)


# ==========================================================
# POLE ZERO MAP
# ==========================================================

def plot_pole_zero(poles):

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)

    real = np.real(poles)
    imag = np.imag(poles)

    xmin = min(real) - 2
    xmax = max(real) + 2

    ymin = min(imag) - 2
    ymax = max(imag) + 2

    # Stable region
    ax.axvspan(
        xmin,
        0,
        color="#dff7df",
        alpha=0.45
    )

    # Unstable region
    ax.axvspan(
        0,
        xmax,
        color="#ffe1e1",
        alpha=0.45
    )

    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)

    ax.scatter(
        real,
        imag,
        marker="x",
        color="red",
        s=180,
        linewidths=3
    )

    for i, pole in enumerate(poles):

        ax.annotate(
            f"P{i+1}",
            (np.real(pole), np.imag(pole)),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=10,
            weight="bold"
        )

    if np.any(real > 0):
        banner = "❌ UNSTABLE SYSTEM"
        colour = "red"
    else:
        banner = "✅ STABLE SYSTEM"
        colour = "green"

    ax.text(
        0.02,
        0.96,
        banner,
        transform=ax.transAxes,
        fontsize=12,
        color=colour,
        weight="bold",
        bbox=dict(
            facecolor="white",
            edgecolor=colour,
            alpha=0.9
        )
    )

    ax.set_title("Pole Map")
    ax.set_xlabel("Real Axis")
    ax.set_ylabel("Imaginary Axis")

    ax.grid(True)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    fig.tight_layout()
    fig.canvas.draw()

    return fig


# ==========================================================
# STEP RESPONSE
# ==========================================================

def step_response(system):

    t, y = signal.step(system)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)

    ax.plot(
        t,
        y,
        color="royalblue",
        linewidth=2.5,
        label="Step Response"
    )

    ax.set_title("Step Response")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")

    ax.grid(True)
    ax.legend()

    fig.tight_layout()
    fig.canvas.draw()

    return fig, t, y


# ==========================================================
# IMPULSE RESPONSE
# ==========================================================

def impulse_response(system):

    t, y = signal.impulse(system)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=120)

    ax.plot(
        t,
        y,
        color="darkorange",
        linewidth=2.5,
        label="Impulse Response"
    )

    ax.set_title("Impulse Response")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")

    ax.grid(True)
    ax.legend()

    fig.tight_layout()
    fig.canvas.draw()

    return fig, t, y
# ==========================================================
# PERFORMANCE METRICS
# ==========================================================

def calculate_metrics(t, y, poles):

    t = np.asarray(t).flatten()
    y = np.asarray(y).flatten()

    # ------------------------------------------------------
    # Unstable System
    # ------------------------------------------------------

    if np.any(np.real(poles) > 0):

        return {

            "Final Value": "Divergent",

            "Peak Value": "N/A",

            "Peak Time": "N/A",

            "Rise Time": "N/A",

            "Settling Time": "N/A",

            "Overshoot (%)": "N/A",

            "Steady State Error": "Divergent"

        }

    # ------------------------------------------------------
    # Stable System
    # ------------------------------------------------------

    final_value = float(y[-1])

    peak_index = np.argmax(y)

    peak_value = float(y[peak_index])

    peak_time = float(t[peak_index])

    # -------------------------------
    # Overshoot
    # -------------------------------

    if abs(final_value) < 1e-12:

        overshoot = "N/A"

    else:

        overshoot = max(
            0,
            (peak_value - final_value) / abs(final_value) * 100
        )

        overshoot = round(float(overshoot), 2)

    # -------------------------------
    # Rise Time
    # -------------------------------

    rise_time = "N/A"

    try:

        t10 = t[np.where(y >= 0.1 * final_value)[0][0]]

        t90 = t[np.where(y >= 0.9 * final_value)[0][0]]

        rise_time = round(float(t90 - t10), 4)

    except:

        pass

    # -------------------------------
    # Settling Time
    # -------------------------------

    settling_time = "N/A"

    try:

        tolerance = abs(final_value) * 0.02

        settling = t[-1]

        for i in range(len(y) - 1, -1, -1):

            if abs(y[i] - final_value) > tolerance:

                if i + 1 < len(t):

                    settling = t[i + 1]

                break

        settling_time = round(float(settling), 4)

    except:

        pass

    return {

        "Final Value": round(final_value, 4),

        "Peak Value": round(peak_value, 4),

        "Peak Time": round(peak_time, 4),

        "Rise Time": rise_time,

        "Settling Time": settling_time,

        "Overshoot (%)": overshoot,

        "Steady State Error": round(abs(1 - final_value), 4)

    }

# ==========================================================
# STEP RESPONSE WITH ANNOTATIONS
# ==========================================================

def annotated_step_response(system):

    fig, t, y = step_response(system)

    metrics = calculate_metrics(
        t,
        y,
        system.poles
    )

    ax = fig.axes[0]

    unstable = np.any(np.real(system.poles) > 0)

    # ------------------------------------------------------
    # UNSTABLE SYSTEM
    # ------------------------------------------------------

    if unstable:

        ax.text(
            0.02,
            0.95,
            "❌ UNSTABLE SYSTEM",
            transform=ax.transAxes,
            fontsize=13,
            color="red",
            weight="bold",
            bbox=dict(
                facecolor="white",
                alpha=0.9
            )
        )

        ax.text(
            0.02,
            0.80,
            "System response diverges.\nPerformance metrics are not applicable.",
            transform=ax.transAxes,
            fontsize=10,
            bbox=dict(
                facecolor="white",
                alpha=0.85
            )
        )

    # ------------------------------------------------------
    # STABLE SYSTEM
    # ------------------------------------------------------

    else:

        ax.text(
            0.02,
            0.95,
            "✅ STABLE SYSTEM",
            transform=ax.transAxes,
            fontsize=13,
            color="green",
            weight="bold",
            bbox=dict(
                facecolor="white",
                alpha=0.9
            )
        )

        peak_time = metrics["Peak Time"]
        peak_value = metrics["Peak Value"]

        if (
            isinstance(peak_time, (int, float))
            and isinstance(peak_value, (int, float))
        ):

            ax.scatter(
                peak_time,
                peak_value,
                color="red",
                s=80,
                zorder=5
            )

            ax.annotate(
                f"Peak = {peak_value:.4f}",
                xy=(peak_time, peak_value),
                xytext=(30, -25),
                textcoords="offset points",
                arrowprops=dict(
                    arrowstyle="->",
                    lw=2
                ),
                bbox=dict(
                    facecolor="white",
                    alpha=0.9
                )
            )

    # ------------------------------------------------------
    # PERFORMANCE SUMMARY
    # ------------------------------------------------------

    info = (
        f"Rise Time : {metrics['Rise Time']} s\n"
        f"Settling Time : {metrics['Settling Time']} s\n"
        f"Overshoot : {metrics['Overshoot (%)']} %"
    )

    ax.text(
        0.68,
        0.80,
        info,
        transform=ax.transAxes,
        fontsize=10,
        bbox=dict(
            facecolor="white",
            alpha=0.9
        )
    )

    fig.tight_layout()
    fig.canvas.draw()

    return fig, metrics
# ==========================================================
# COMPLETE VISUALIZATION
# ==========================================================

def visualize_system(numerator, denominator, poles):

    system = build_system(
        numerator,
        denominator
    )

    pole_fig = plot_pole_zero(poles)

    step_fig, metrics = annotated_step_response(system)

    impulse_fig, _, _ = impulse_response(system)

    return {

        "pole_plot": pole_fig,

        "step_plot": step_fig,

        "impulse_plot": impulse_fig,

        "metrics": metrics

    }


# ==========================================================
# PRINT METRICS
# ==========================================================

def print_metrics(metrics):

    print("\n" + "=" * 60)
    print("SYSTEM PERFORMANCE")
    print("=" * 60)

    for key, value in metrics.items():

        print(f"{key:<22}: {value}")


# ==========================================================
# MAIN ANALYSIS
# ==========================================================

def analyze_and_visualize(
    numerator,
    denominator,
    poles
):

    results = visualize_system(
        numerator,
        denominator,
        poles
    )

    print_metrics(results["metrics"])

    return results


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    numerator = [0, 0, 0, 0, 0, 5]

    denominator = [0, 0, 1, 10, 120, 500]

    poles = np.roots([1, 10, 120, 500])

    analysis = analyze_and_visualize(
        numerator,
        denominator,
        poles
    )

    print("\nReturned Metrics\n")

    for key, value in analysis["metrics"].items():

        print(f"{key:<22}: {value}")

    plt.show()
