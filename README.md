Electrochemical Sensor Data Analysis

A portfolio project for analyzing electrochemical sensor measurements using Python. It demonstrates data cleaning, cyclic voltammetry (CV) visualization, peak extraction, and electrochemical impedance spectroscopy (EIS) visualization.

The included dataset is synthetic and generated for demonstration. It is not experimental evidence and must not be presented as measured laboratory data.


Load and validate electrochemical measurement data.
Plot cyclic voltammograms (current versus potential).
Estimate oxidation and reduction peak positions and currents.
Visualize impedance magnitude and phase against frequency.
Export plots and a small summary table for a reproducible workflow.

Python 3.10+ is recommended.

1. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt

2. Run the analysis script from the repository root:

   ```bash
   python src/analyze_data.py

3. Review the generated figures and `outputs/peak_summary.csv`.

Data formats

CV data (data/sample_cv_data.csv)

| Column           | Meaning             | Unit |

| `potential_V`   | Applied potential     | V |
| `current_uA`    | Measured current     | µA |
| `scan_direction` | Forward or reverse scan label | dimensionless |

EIS data (`data/sample_eis_data.csv`)

| Column             | Meaning                                 | Unit |

| `frequency_Hz`     | Measurement frequency               | Hz |
| `z_real_ohm`       | Real component of impedance         | Ω |
| `z_imag_ohm`       | Imaginary component of impedance     | Ω |
| `z_magnitude_ohm`  | Impedance magnitude                 | Ω |
| `phase_deg`        | Impedance phase angle               | degrees |

Interpretation

Peak finding is a numerical estimate. Baseline correction, smoothing, electrode chemistry, reference-electrode choice, scan rate, and replicate variability can change reported peak values.
A CV peak separation should only be interpreted electrochemically when the scan protocol, redox chemistry, reference electrode, and measurement conditions are known.
EIS plots are descriptive. Equivalent-circuit fitting is intentionally not performed by this starter project; fitting requires a justified circuit model and appropriate validation.
The sample files are synthetic examples created to demonstrate the workflow. Replace them with properly documented data before drawing scientific conclusions.

MIT License. See `LICENSE`.
