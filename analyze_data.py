from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def validate_columns(df, required, filename):
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"{filename} is missing required columns: {missing}")
    if df.empty:
        raise ValueError(f"{filename} contains no rows.")
    return df

# --- Cyclic voltammetry ---
cv = pd.read_csv(DATA / "sample_cv_data.csv")
validate_columns(cv, ["potential_V", "current_uA", "scan_direction"], "CV data")
if cv[["potential_V", "current_uA"]].isna().any().any():
    raise ValueError("CV data contains missing numeric values.")
if not set(cv["scan_direction"].dropna().unique()).issubset({"forward", "reverse"}):
    raise ValueError("scan_direction must contain only 'forward' and/or 'reverse'.")

fig, ax = plt.subplots(figsize=(8, 5))
peak_rows = []
for direction, group in cv.groupby("scan_direction", sort=False):
    group = group.sort_values("potential_V", ascending=(direction == "forward"))
    x = group["potential_V"].to_numpy()
    y = group["current_uA"].to_numpy()
    ax.plot(x, y, label=f"{direction.title()} scan", linewidth=1.8)

    # Simple extrema search; thresholds are intentionally modest for this demo.
    if direction == "forward":
        peaks, _ = find_peaks(y, prominence=max(np.std(y) * 0.8, 0.5))
        if len(peaks):
            idx = peaks[np.argmax(y[peaks])]
            peak_rows.append({"scan_direction": direction, "peak_type": "anodic_candidate",
                              "potential_V": x[idx], "current_uA": y[idx]})
    else:
        peaks, _ = find_peaks(-y, prominence=max(np.std(y) * 0.8, 0.5))
        if len(peaks):
            idx = peaks[np.argmax(-y[peaks])]
            peak_rows.append({"scan_direction": direction, "peak_type": "cathodic_candidate",
                              "potential_V": x[idx], "current_uA": y[idx]})

ax.set(title="Cyclic Voltammetry — Synthetic Demonstration Data",
       xlabel="Potential (V)", ylabel="Current (µA)")
ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "cv_plot.png", dpi=180)
plt.close(fig)

pd.DataFrame(peak_rows).to_csv(OUT / "peak_summary.csv", index=False)

# --- Electrochemical impedance spectroscopy ---
eis = pd.read_csv(DATA / "sample_eis_data.csv")
validate_columns(eis, ["frequency_Hz", "z_magnitude_ohm", "phase_deg"], "EIS data")
if eis[["frequency_Hz", "z_magnitude_ohm", "phase_deg"]].isna().any().any():
    raise ValueError("EIS data contains missing numeric values.")
if (eis["frequency_Hz"] <= 0).any():
    raise ValueError("EIS frequencies must be positive.")

eis = eis.sort_values("frequency_Hz")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
ax1.loglog(eis["frequency_Hz"], eis["z_magnitude_ohm"], marker="o", markersize=3)
ax1.set_ylabel("|Z| (Ω)")
ax1.set_title("EIS Bode Plot — Synthetic Demonstration Data")
ax1.grid(True, which="both", alpha=0.3)
ax2.semilogx(eis["frequency_Hz"], eis["phase_deg"], marker="o", markersize=3)
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Phase (degrees)")
ax2.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "eis_bode_plot.png", dpi=180)
plt.close(fig)

print("Analysis complete.")
print(f"CV plot: {OUT / 'cv_plot.png'}")
print(f"EIS plot: {OUT / 'eis_bode_plot.png'}")
print(f"Peak summary: {OUT / 'peak_summary.csv'}")
print("\nPeak candidates (not a validated electrochemical interpretation):")
print(pd.DataFrame(peak_rows).to_string(index=False) if peak_rows else "No peaks found.")
