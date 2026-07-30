from array import array
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import ROOT


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

E_THR = 1.806  # MeV
OSCILLATION_MAX_ENERGY = 12.0  # MeV
FIXED_DELTA_M32 = 2.40e-3  # eV^2

N_FIT_BINS = 200
FIT_ENERGY_MIN = 0.0  # MeV
FIT_ENERGY_MAX = 10.0  # MeV

# Start with 41 for a quick check; use 81, 101, or 121 for the final plot.
N_SCAN_POINTS = 81
SCAN_NSIGMA_RANGE = 5.0

MC_SPECTRUM_FILE = "root/nu_spec_OSC_noME.root"
MC_SPECTRUM_NAME = "totalprob2"
RESPONSE_FILE = Path("F:/桌面/南山清北/response_500.root")
RESPONSE_NAME = "h_response"
DATA_FILE = "root/IBD_OSC100k_noME.root"
DATA_TREE_NAME = "evt"

OUTPUT_DIR = Path("F:/桌面/南山清北")
OUTPUT_ROOT = OUTPUT_DIR / "confidence_contour_fixed_dm32.root"
OUTPUT_PDF = OUTPUT_DIR / "confidence_contour_fixed_dm32.pdf"
OUTPUT_PNG = OUTPUT_DIR / "confidence_contour_fixed_dm32.png"


def open_root_file(filename):
    root_file = ROOT.TFile.Open(str(filename), "READ")
    if not root_file or root_file.IsZombie():
        raise OSError(f"Cannot open {filename}")
    return root_file


def get_root_object(root_file, name):
    obj = root_file.Get(name)
    if not obj:
        raise RuntimeError(
            f"Cannot load '{name}' from {root_file.GetName()}"
        )
    return obj


def axis_edges(axis):
    n_bins = axis.GetNbins()
    return np.asarray(
        [axis.GetBinLowEdge(i) for i in range(1, n_bins + 1)]
        + [axis.GetBinUpEdge(n_bins)],
        dtype=np.float64,
    )


def centers_to_edges(centers):
    edges = np.empty(len(centers) + 1, dtype=np.float64)
    edges[1:-1] = 0.5 * (centers[:-1] + centers[1:])
    edges[0] = centers[0] - 0.5 * (centers[1] - centers[0])
    edges[-1] = centers[-1] + 0.5 * (centers[-1] - centers[-2])
    return edges


def build_overlap_rebin_matrix(source_edges, target_edges):
    """
    Construct R such that target_counts = R @ source_counts.

    Counts in a fine reconstructed-energy bin are distributed according to
    geometric overlap with the 0--10 MeV, 200-bin fit grid.
    """
    source_low = source_edges[:-1][None, :]
    source_high = source_edges[1:][None, :]
    target_low = target_edges[:-1][:, None]
    target_high = target_edges[1:][:, None]

    overlap = np.maximum(
        0.0,
        np.minimum(source_high, target_high)
        - np.maximum(source_low, target_low),
    )
    return overlap / (source_high - source_low)


def make_quadrature(true_edges, spectrum):
    """Precompute an 8-point Gauss-Legendre grid in every true-energy bin."""
    unit_nodes, unit_weights = np.polynomial.legendre.leggauss(8)
    n_true_bins = len(true_edges) - 1

    nodes = np.zeros((n_true_bins, len(unit_nodes)), dtype=np.float64)
    weights = np.zeros_like(nodes)
    flux = np.zeros_like(nodes)

    for true_bin in range(n_true_bins):
        low = max(float(true_edges[true_bin]), E_THR)
        high = min(
            float(true_edges[true_bin + 1]),
            OSCILLATION_MAX_ENERGY,
        )
        if high <= low:
            continue

        half_width = 0.5 * (high - low)
        midpoint = 0.5 * (high + low)
        nodes[true_bin, :] = midpoint + half_width * unit_nodes
        weights[true_bin, :] = half_width * unit_weights
        flux[true_bin, :] = [
            float(spectrum.Eval(float(energy)))
            for energy in nodes[true_bin, :]
        ]

    return nodes, weights, flux


def make_scan_axis(best, error, hard_min, hard_max):
    hard_width = hard_max - hard_min
    if not np.isfinite(error) or error <= 0.0:
        error = 0.1 * hard_width

    half_width = max(
        SCAN_NSIGMA_RANGE * error,
        0.05 * hard_width,
    )
    scan_min = max(hard_min, best - half_width)
    scan_max = min(hard_max, best + half_width)
    return np.linspace(
        scan_min,
        scan_max,
        N_SCAN_POINTS,
        dtype=np.float64,
    )


# ---------------------------------------------------------------------------
# Load flux, fine response, and data.
# ---------------------------------------------------------------------------

file_mc = open_root_file(MC_SPECTRUM_FILE)
f_mc = get_root_object(file_mc, MC_SPECTRUM_NAME)

file_response = open_root_file(RESPONSE_FILE)
response_histogram = get_root_object(file_response, RESPONSE_NAME)

n_true_response_bins = response_histogram.GetNbinsX()
n_reco_response_bins = response_histogram.GetNbinsY()
nu_edges_fine = axis_edges(response_histogram.GetXaxis())
prompt_edges_fine = axis_edges(response_histogram.GetYaxis())

response_fine = np.empty(
    (n_reco_response_bins, n_true_response_bins),
    dtype=np.float64,
)
for reco_bin in range(1, n_reco_response_bins + 1):
    for true_bin in range(1, n_true_response_bins + 1):
        response_fine[reco_bin - 1, true_bin - 1] = (
            response_histogram.GetBinContent(true_bin, reco_bin)
        )

fit_edges = np.linspace(
    FIT_ENERGY_MIN,
    FIT_ENERGY_MAX,
    N_FIT_BINS + 1,
    dtype=np.float64,
)
reco_rebin = build_overlap_rebin_matrix(prompt_edges_fine, fit_edges)
response_for_fit = reco_rebin @ response_fine

quadrature_nodes, quadrature_weights, quadrature_flux = make_quadrature(
    nu_edges_fine,
    f_mc,
)

file_data = open_root_file(DATA_FILE)
tree = get_root_object(file_data, DATA_TREE_NAME)
tree.SetBranchStatus("*", 1)

h_data = ROOT.TH1D(
    "h_data",
    "Data;E_{prompt} [MeV];Events",
    N_FIT_BINS,
    array("d", fit_edges),
)
h_data.SetDirectory(0)
h_data.Sumw2()

for event in tree:
    energy = float(event.prompt_smearedE)
    if FIT_ENERGY_MIN <= energy < FIT_ENERGY_MAX:
        h_data.Fill(energy)

data_counts = np.asarray(
    [h_data.GetBinContent(i) for i in range(1, N_FIT_BINS + 1)],
    dtype=np.float64,
)
data_sum = float(np.sum(data_counts))
if data_sum <= 0.0:
    raise RuntimeError("No data events are present in the 0--10 MeV range")


# ---------------------------------------------------------------------------
# Prediction and chi-square with fixed delta_m32.
# ---------------------------------------------------------------------------

def calculate_true_spectrum(delta_m21, sin2_theta12):
    energy = quadrature_nodes
    valid = quadrature_weights != 0.0

    delta_m31 = delta_m21 + FIXED_DELTA_M32
    baseline = 52.5e3  # m

    ue3_sq = 0.02
    ue1_sq = (1.0 - sin2_theta12) * (1.0 - ue3_sq)
    ue2_sq = sin2_theta12 * (1.0 - ue3_sq)

    probability = np.ones_like(energy)
    phase21 = np.zeros_like(energy)
    phase31 = np.zeros_like(energy)
    phase32 = np.zeros_like(energy)

    phase21[valid] = 1.267 * delta_m21 * baseline / energy[valid]
    phase31[valid] = 1.267 * delta_m31 * baseline / energy[valid]
    phase32[valid] = 1.267 * FIXED_DELTA_M32 * baseline / energy[valid]

    probability[valid] -= (
        4.0 * ue1_sq * ue2_sq * np.sin(phase21[valid]) ** 2
        + 4.0 * ue1_sq * ue3_sq * np.sin(phase31[valid]) ** 2
        + 4.0 * ue2_sq * ue3_sq * np.sin(phase32[valid]) ** 2
    )

    return np.sum(
        quadrature_weights * quadrature_flux * probability,
        axis=1,
    )


def calculate_prediction(delta_m21, sin2_theta12):
    true_prediction = calculate_true_spectrum(
        delta_m21,
        sin2_theta12,
    )
    reco_prediction = response_for_fit @ true_prediction

    prediction_sum = float(np.sum(reco_prediction))
    if not np.isfinite(prediction_sum) or prediction_sum <= 0.0:
        raise FloatingPointError("Prediction is empty or non-finite")

    # Shape-only normalization inside the fitted 0--10 MeV interval.
    reco_prediction *= data_sum / prediction_sum
    return reco_prediction


def calculate_chi2(delta_m21, sin2_theta12):
    try:
        prediction = calculate_prediction(delta_m21, sin2_theta12)
    except (FloatingPointError, ValueError):
        return 1.0e100

    positive = prediction > 0.0
    if np.any((~positive) & (data_counts > 0.0)):
        return 1.0e100

    residual = data_counts[positive] - prediction[positive]
    chi2 = np.sum(residual**2 / prediction[positive])
    return float(chi2) if np.isfinite(chi2) else 1.0e100


class BinnedChiSquare:
    def __init__(self):
        self.ncalls = 0

    def __call__(self, parameters):
        self.ncalls += 1
        return calculate_chi2(
            float(parameters[0]),
            float(parameters[1]),
        )


# ---------------------------------------------------------------------------
# First obtain the unconstrained two-parameter best fit.
# ---------------------------------------------------------------------------

chi2_function = BinnedChiSquare()
minimizer = ROOT.Math.Factory.CreateMinimizer("Minuit2", "Migrad")
minimizer.SetMaxFunctionCalls(100000)
minimizer.SetMaxIterations(10000)
minimizer.SetTolerance(1.0e-6)
minimizer.SetStrategy(1)
minimizer.SetPrintLevel(1)
minimizer.SetErrorDef(1.0)

minuit_functor = ROOT.Math.Functor(chi2_function, 2)
minimizer.SetFunction(minuit_functor)
minimizer.SetLimitedVariable(
    0,
    "delta_m21",
    7.5e-5,
    1.0e-8,
    5.0e-5,
    1.0e-4,
)
minimizer.SetLimitedVariable(
    1,
    "sin2_theta12",
    0.30,
    1.0e-5,
    0.10,
    0.50,
)

print("\n========== Two-parameter fit with fixed delta_m32 ==========")
fit_success = bool(minimizer.Minimize())
try:
    minimizer.Hesse()
except Exception as error:
    print(f"HESSE failed: {error}")

best_delta_m21 = float(minimizer.X()[0])
best_sin2_theta12 = float(minimizer.X()[1])
error_delta_m21 = float(minimizer.Errors()[0])
error_sin2_theta12 = float(minimizer.Errors()[1])
minimum_chi2 = float(minimizer.MinValue())

number_of_used_bins = int(
    np.count_nonzero(
        calculate_prediction(
            best_delta_m21,
            best_sin2_theta12,
        )
        > 0.0
    )
)
# Two fitted physics parameters and one data-normalization constraint.
ndof = number_of_used_bins - 2 - 1
p_value = (
    float(ROOT.TMath.Prob(minimum_chi2, ndof))
    if ndof > 0
    else float("nan")
)

print(f"Fit success: {fit_success}")
print(f"Minuit status: {minimizer.Status()}")
print(f"Function calls: {chi2_function.ncalls}")
print(f"Minimum chi2: {minimum_chi2:.8f}")
print(f"NDOF: {ndof}")
print(f"chi2/NDOF: {minimum_chi2 / ndof:.6f}")
print(f"p-value: {p_value:.8g}")
print(
    f"delta_m21 = ({best_delta_m21:.8e} "
    f"+/- {error_delta_m21:.3e}) eV^2"
)
print(
    f"sin^2(theta12) = {best_sin2_theta12:.8f} "
    f"+/- {error_sin2_theta12:.3e}"
)
print(f"delta_m32 fixed at {FIXED_DELTA_M32:.8e} eV^2")


# ---------------------------------------------------------------------------
# Direct two-dimensional scan. No nuisance-parameter minimization is needed
# because delta_m32 is fixed and the normalization is handled analytically.
# ---------------------------------------------------------------------------

delta_m21_scan = make_scan_axis(
    best_delta_m21,
    error_delta_m21,
    5.0e-5,
    1.0e-4,
)
sin2_theta12_scan = make_scan_axis(
    best_sin2_theta12,
    error_sin2_theta12,
    0.10,
    0.50,
)

chi2_surface = np.empty(
    (N_SCAN_POINTS, N_SCAN_POINTS),
    dtype=np.float64,
)

print(
    "\n========== Direct two-dimensional scan ==========\n"
    f"Grid: {N_SCAN_POINTS} x {N_SCAN_POINTS}\n"
    f"delta_m21: "
    f"[{delta_m21_scan[0]:.8e}, {delta_m21_scan[-1]:.8e}] eV^2\n"
    f"sin^2(theta12): "
    f"[{sin2_theta12_scan[0]:.6f}, {sin2_theta12_scan[-1]:.6f}]"
)

for sin_index, sin2_value in enumerate(sin2_theta12_scan):
    for delta_index, delta_m21_value in enumerate(delta_m21_scan):
        chi2_surface[sin_index, delta_index] = calculate_chi2(
            float(delta_m21_value),
            float(sin2_value),
        )

    if (sin_index + 1) % 10 == 0 or sin_index == 0:
        print(f"Scan row {sin_index + 1}/{N_SCAN_POINTS}")

delta_chi2_surface = np.maximum(
    chi2_surface - minimum_chi2,
    0.0,
)

# Joint confidence thresholds for two scanned parameters.
contour_levels = [2.30, 6.18, 11.83]
contour_labels = {
    2.30: r"$1\sigma$ (68.27%)",
    6.18: r"$2\sigma$ (95.45%)",
    11.83: r"$3\sigma$ (99.73%)",
}
contour_colors = ["tab:blue", "tab:orange", "tab:red"]

finite_delta_chi2 = delta_chi2_surface[
    np.isfinite(delta_chi2_surface)
]
if finite_delta_chi2.size == 0:
    raise RuntimeError("The complete chi-square scan is non-finite")

if float(np.max(finite_delta_chi2)) < contour_levels[-1]:
    print(
        "Warning: the scan does not reach Delta chi2 = 11.83. "
        "Increase SCAN_NSIGMA_RANGE."
    )


# ---------------------------------------------------------------------------
# Draw the delta-chi-square surface and confidence contours.
# ---------------------------------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

figure, axis = plt.subplots(figsize=(8.5, 7.2))

color_maximum = min(
    20.0,
    max(contour_levels[-1], float(np.max(finite_delta_chi2))),
)
filled_levels = np.linspace(0.0, color_maximum, 41)
filled_contours = axis.contourf(
    delta_m21_scan * 1.0e5,
    sin2_theta12_scan,
    delta_chi2_surface,
    levels=filled_levels,
    cmap="viridis",
    extend="max",
)
colorbar = figure.colorbar(filled_contours, ax=axis)
colorbar.set_label(r"$\Delta\chi^2$")

line_contours = axis.contour(
    delta_m21_scan * 1.0e5,
    sin2_theta12_scan,
    delta_chi2_surface,
    levels=contour_levels,
    colors=contour_colors,
    linewidths=2.2,
)
axis.clabel(
    line_contours,
    fmt=contour_labels,
    inline=True,
    fontsize=10,
)

axis.plot(
    best_delta_m21 * 1.0e5,
    best_sin2_theta12,
    marker="*",
    markersize=15,
    color="white",
    markeredgecolor="black",
    markeredgewidth=0.8,
    label="Best fit",
)
axis.set_xlabel(
    r"$\Delta m^2_{21}\ [10^{-5}\ {\rm eV}^2]$"
)
axis.set_ylabel(r"$\sin^2\theta_{12}$")
axis.set_title(
    "Two-dimensional confidence contours\n"
    rf"$\Delta m^2_{{32}}={FIXED_DELTA_M32:.4e}\ "
    r"{\rm eV}^2$ fixed"
)
axis.grid(alpha=0.2)
axis.legend()
figure.tight_layout()
figure.savefig(OUTPUT_PDF, bbox_inches="tight")
figure.savefig(OUTPUT_PNG, dpi=250, bbox_inches="tight")
plt.close(figure)


# ---------------------------------------------------------------------------
# Save the numerical scan surface and best-fit prediction to ROOT.
# ---------------------------------------------------------------------------

delta_m21_edges = centers_to_edges(delta_m21_scan)
sin2_theta12_edges = centers_to_edges(sin2_theta12_scan)

h_delta_chi2 = ROOT.TH2D(
    "h_delta_chi2_dm21_sin2theta12",
    "Fixed-#Delta m_{32}^{2} scan;"
    "#Delta m_{21}^{2} [eV^{2}];"
    "sin^{2}#theta_{12}",
    N_SCAN_POINTS,
    array("d", delta_m21_edges),
    N_SCAN_POINTS,
    array("d", sin2_theta12_edges),
)
h_delta_chi2.SetDirectory(0)

for sin_index in range(N_SCAN_POINTS):
    for delta_index in range(N_SCAN_POINTS):
        h_delta_chi2.SetBinContent(
            delta_index + 1,
            sin_index + 1,
            float(delta_chi2_surface[sin_index, delta_index]),
        )

best_prediction = calculate_prediction(
    best_delta_m21,
    best_sin2_theta12,
)
h_best_fit = ROOT.TH1D(
    "h_best_fit",
    "Best fit with fixed #Delta m_{32}^{2};"
    "E_{prompt} [MeV];Events",
    N_FIT_BINS,
    array("d", fit_edges),
)
h_best_fit.SetDirectory(0)
for fit_bin, value in enumerate(best_prediction, start=1):
    h_best_fit.SetBinContent(fit_bin, float(value))

output_file = ROOT.TFile.Open(str(OUTPUT_ROOT), "RECREATE")
if not output_file or output_file.IsZombie():
    raise OSError(f"Cannot create {OUTPUT_ROOT}")
output_file.cd()
h_data.Write()
h_best_fit.Write()
h_delta_chi2.Write()
output_file.Close()

print("\nOutput files:")
print(f"  {OUTPUT_ROOT}")
print(f"  {OUTPUT_PDF}")
print(f"  {OUTPUT_PNG}")

file_data.Close()
file_response.Close()
file_mc.Close()
