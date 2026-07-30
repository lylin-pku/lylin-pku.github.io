from array import array
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import ROOT


E_THR = 1.806  # MeV
OSCILLATION_MAX_ENERGY = 12.0  # MeV

N_FIT_BINS = 200
FIT_ENERGY_MIN = 0.0  # MeV
FIT_ENERGY_MAX = 10.0  # MeV

MC_SPECTRUM_FILE = "root/nu_spec_OSC_noME.root"
MC_SPECTRUM_NAME = "totalprob2"
OUTPUT_DIR = Path("F:/桌面/南山清北")
RESPONSE_FILE = OUTPUT_DIR / "response_500.root"
RESPONSE_NAME = "h_response"
DATA_FILE = "root/IBD_OSC100k_noME.root"
DATA_TREE_NAME = "evt"

OUTPUT_ROOT = OUTPUT_DIR / "binned_chi2_fit.root"
OUTPUT_PDF = OUTPUT_DIR / "binned_chi2_fit.pdf"
OUTPUT_PNG = OUTPUT_DIR / "binned_chi2_fit.png"
CONTOUR_PDF = OUTPUT_DIR / "confidence_contour_dm21_sin2theta12.pdf"
CONTOUR_PNG = OUTPUT_DIR / "confidence_contour_dm21_sin2theta12.png"

# Number of scan points along each axis. Increase to 101 or 121 for a smoother
# final contour after first checking the result with the default value.
N_CONTOUR_POINTS = 81
CONTOUR_NSIGMA_RANGE = 5.0


def open_root_file(filename):
    root_file = ROOT.TFile.Open(str(filename), "READ")
    if not root_file or root_file.IsZombie():
        raise OSError(f"Cannot open {filename}")
    return root_file


def get_root_object(root_file, name):
    obj = root_file.Get(name)
    if not obj:
        raise RuntimeError(
            f"Cannot load ROOT object '{name}' from {root_file.GetName()}"
        )
    return obj


def axis_edges(axis):
    n_bins = axis.GetNbins()
    return np.asarray(
        [axis.GetBinLowEdge(i) for i in range(1, n_bins + 1)]
        + [axis.GetBinUpEdge(n_bins)],
        dtype=np.float64,
    )


def build_overlap_rebin_matrix(source_edges, target_edges):
    """
    Return R such that target_counts = R @ source_counts.

    A source-bin count is divided according to geometric bin overlap. Because
    the response grid is fine (500 bins), the within-bin uniform approximation
    is small. Source-bin portions outside the target 0--10 MeV range are dropped.
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
    source_width = source_high - source_low
    return overlap / source_width


def make_quadrature(true_edges, spectrum):
    """Precompute an 8-point Gauss-Legendre integral grid for every true bin."""
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


# ---------------------------------------------------------------------------
# Load the fine response matrix. Its dimensions are read from the ROOT object,
# rather than being tied to the 200-bin fit.
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

# Convert the 500-bin reconstructed-energy axis to the fixed 200-bin fit axis.
# The true-energy axis stays fine.
reco_rebin = build_overlap_rebin_matrix(prompt_edges_fine, fit_edges)
response_for_fit = reco_rebin @ response_fine

column_acceptance = np.sum(response_for_fit, axis=0)
if np.any(column_acceptance > 1.0 + 1.0e-10):
    raise RuntimeError("Response aggregation produced a probability above one")

quadrature_nodes, quadrature_weights, quadrature_flux = make_quadrature(
    nu_edges_fine,
    f_mc,
)


# ---------------------------------------------------------------------------
# Data histogram: exactly 0--10 MeV in 200 bins, independent of the response
# matrix bin count and range.
# ---------------------------------------------------------------------------

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
data_errors = np.asarray(
    [h_data.GetBinError(i) for i in range(1, N_FIT_BINS + 1)],
    dtype=np.float64,
)
data_sum = float(np.sum(data_counts))
if data_sum <= 0.0:
    raise RuntimeError("The selected 0--10 MeV data range contains no events")


def calculate_true_spectrum(delta_m21, sin2_theta12, delta_m32):
    """Integrate flux times survival probability in every fine true-energy bin."""
    energy = quadrature_nodes
    valid = quadrature_weights != 0.0

    delta_m31 = delta_m21 + delta_m32
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
    phase32[valid] = 1.267 * delta_m32 * baseline / energy[valid]

    probability[valid] -= (
        4.0 * ue1_sq * ue2_sq * np.sin(phase21[valid]) ** 2
        + 4.0 * ue1_sq * ue3_sq * np.sin(phase31[valid]) ** 2
        + 4.0 * ue2_sq * ue3_sq * np.sin(phase32[valid]) ** 2
    )

    integrand = quadrature_flux * probability
    return np.sum(quadrature_weights * integrand, axis=1)


def calculate_prediction(
    delta_m21,
    sin2_theta12,
    delta_m32,
    return_true=False,
):
    true_prediction = calculate_true_spectrum(
        delta_m21,
        sin2_theta12,
        delta_m32,
    )
    reco_prediction = response_for_fit @ true_prediction

    prediction_sum = float(np.sum(reco_prediction))
    if not np.isfinite(prediction_sum) or prediction_sum <= 0.0:
        raise FloatingPointError("Prediction is empty or non-finite")

    # Shape-only fit: normalize the prediction inside the selected 0--10 MeV
    # window to the number of selected data events.
    scale = data_sum / prediction_sum
    reco_prediction *= scale

    if return_true:
        return reco_prediction, true_prediction * scale
    return reco_prediction


class BinnedChiSquare:
    def __init__(self):
        self.ncalls = 0
        self.last_prediction = None

    def __call__(self, parameters):
        self.ncalls += 1
        delta_m21 = float(parameters[0])
        sin2_theta12 = float(parameters[1])
        delta_m32 = float(parameters[2])

        try:
            prediction = calculate_prediction(
                delta_m21,
                sin2_theta12,
                delta_m32,
            )
        except (FloatingPointError, ValueError):
            return 1.0e100

        positive = prediction > 0.0
        if np.any((~positive) & (data_counts > 0.0)):
            return 1.0e100

        residual = data_counts[positive] - prediction[positive]
        chi2 = np.sum(residual**2 / prediction[positive])
        if not np.isfinite(chi2):
            return 1.0e100

        self.last_prediction = prediction.copy()
        return float(chi2)


chi2_function = BinnedChiSquare()
minimizer = ROOT.Math.Factory.CreateMinimizer("Minuit2", "Migrad")
minimizer.SetMaxFunctionCalls(100000)
minimizer.SetMaxIterations(10000)
minimizer.SetTolerance(1.0e-6)
minimizer.SetStrategy(1)
minimizer.SetPrintLevel(1)
minimizer.SetErrorDef(1.0)

# Keep this Python object alive while Minuit uses it.
minuit_functor = ROOT.Math.Functor(chi2_function, 3)
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
minimizer.SetLimitedVariable(
    2,
    "delta_m32",
    2.40e-3,
    1.0e-7,
    2.00e-3,
    3.00e-3,
)

print("\n========== Start Minuit fit ==========")
fit_success = bool(minimizer.Minimize())
try:
    minimizer.Hesse()
except Exception as error:
    print(f"HESSE failed: {error}")

best_delta_m21 = float(minimizer.X()[0])
best_sin2_theta12 = float(minimizer.X()[1])
best_delta_m32 = float(minimizer.X()[2])
error_delta_m21 = float(minimizer.Errors()[0])
error_sin2_theta12 = float(minimizer.Errors()[1])
error_delta_m32 = float(minimizer.Errors()[2])
minimum_chi2 = float(minimizer.MinValue())

best_reco_prediction, best_true_prediction = calculate_prediction(
    best_delta_m21,
    best_sin2_theta12,
    best_delta_m32,
    return_true=True,
)

number_of_used_bins = int(np.count_nonzero(best_reco_prediction > 0.0))
# Three physics parameters plus one degree of freedom used by normalizing the
# prediction to the observed event total.
ndof = number_of_used_bins - 3 - 1
p_value = (
    float(ROOT.TMath.Prob(minimum_chi2, ndof))
    if ndof > 0 and np.isfinite(minimum_chi2)
    else float("nan")
)

print("\n========== Fit result ==========")
print(f"Fit success: {fit_success}")
print(f"Minuit status: {minimizer.Status()}")
print(f"Function calls: {chi2_function.ncalls}")
print(f"EDM: {minimizer.Edm():.8e}")
print(f"Minimum chi2: {minimum_chi2:.8f}")
print(f"NDOF: {ndof}")
if ndof > 0:
    print(f"chi2/NDOF: {minimum_chi2 / ndof:.6f}")
    print(f"Goodness-of-fit p-value: {p_value:.8g}")
print(
    f"delta_m21 = ({best_delta_m21:.8e} "
    f"+/- {error_delta_m21:.3e}) eV^2"
)
print(
    f"sin^2(theta12) = {best_sin2_theta12:.8f} "
    f"+/- {error_sin2_theta12:.3e}"
)
print(
    f"delta_m32 = ({best_delta_m32:.8e} "
    f"+/- {error_delta_m32:.3e}) eV^2"
)

print("\nParameter covariance matrix:")
for i in range(3):
    print(
        " ".join(
            f"{minimizer.CovMatrix(i, j):14.6e}"
            for j in range(3)
        )
    )


# ---------------------------------------------------------------------------
# Two-dimensional profile-chi-square confidence contours.
#
# At every (delta_m21, sin^2(theta12)) point, those two parameters are fixed
# while delta_m32 is minimized again. The normalization is still profiled
# analytically inside calculate_prediction().
# ---------------------------------------------------------------------------

def make_scan_axis(best, error, hard_min, hard_max, n_points):
    hard_width = hard_max - hard_min
    if not np.isfinite(error) or error <= 0.0:
        error = 0.1 * hard_width

    # Five fitted standard deviations normally contain the 3-sigma contour.
    # The minimum span prevents an unrealistically narrow scan when HESSE
    # underestimates an uncertainty.
    half_width = max(
        CONTOUR_NSIGMA_RANGE * error,
        0.05 * hard_width,
    )
    scan_min = max(hard_min, best - half_width)
    scan_max = min(hard_max, best + half_width)
    return np.linspace(scan_min, scan_max, n_points, dtype=np.float64)


delta_m21_scan = make_scan_axis(
    best_delta_m21,
    error_delta_m21,
    5.0e-5,
    1.0e-4,
    N_CONTOUR_POINTS,
)
sin2_theta12_scan = make_scan_axis(
    best_sin2_theta12,
    error_sin2_theta12,
    0.10,
    0.50,
    N_CONTOUR_POINTS,
)

profile_chi2 = np.full(
    (N_CONTOUR_POINTS, N_CONTOUR_POINTS),
    np.nan,
    dtype=np.float64,
)
profiled_delta_m32 = np.full_like(profile_chi2, np.nan)

print(
    "\n========== Two-dimensional profile scan ==========\n"
    f"Grid: {N_CONTOUR_POINTS} x {N_CONTOUR_POINTS}\n"
    f"delta_m21 range: "
    f"[{delta_m21_scan[0]:.8e}, {delta_m21_scan[-1]:.8e}] eV^2\n"
    f"sin^2(theta12) range: "
    f"[{sin2_theta12_scan[0]:.6f}, {sin2_theta12_scan[-1]:.6f}]"
)

minimizer.SetPrintLevel(0)
for sin_index, sin2_value in enumerate(sin2_theta12_scan):
    # Alternating the scan direction gives nearby points nearby starting
    # conditions, without changing the stored array orientation.
    if sin_index % 2 == 0:
        delta_indices = range(N_CONTOUR_POINTS)
    else:
        delta_indices = range(N_CONTOUR_POINTS - 1, -1, -1)

    previous_delta_m32 = best_delta_m32
    for delta_index in delta_indices:
        delta_m21_value = delta_m21_scan[delta_index]

        minimizer.SetVariableValue(0, float(delta_m21_value))
        minimizer.SetVariableValue(1, float(sin2_value))
        minimizer.SetVariableValue(2, float(previous_delta_m32))
        minimizer.FixVariable(0)
        minimizer.FixVariable(1)

        try:
            scan_success = bool(minimizer.Minimize())
            scan_chi2 = float(minimizer.MinValue())
            scan_delta_m32 = float(minimizer.X()[2])

            if scan_success and np.isfinite(scan_chi2):
                profile_chi2[sin_index, delta_index] = scan_chi2
                profiled_delta_m32[sin_index, delta_index] = scan_delta_m32
                previous_delta_m32 = scan_delta_m32
        finally:
            minimizer.ReleaseVariable(0)
            minimizer.ReleaseVariable(1)

    if (sin_index + 1) % 10 == 0 or sin_index == 0:
        print(
            f"Profile scan row {sin_index + 1}/"
            f"{N_CONTOUR_POINTS}"
        )

minimizer.SetPrintLevel(1)

if not np.any(np.isfinite(profile_chi2)):
    raise RuntimeError("Every point in the two-dimensional profile scan failed")

# Use the unconstrained global minimum as the reference. Small negative values
# can occur from minimizer precision and are clipped to zero.
delta_chi2_surface = np.maximum(profile_chi2 - minimum_chi2, 0.0)

# Joint two-parameter confidence levels:
# 68.27% (1 sigma), 95.45% (2 sigma), 99.73% (3 sigma).
contour_levels = [2.30, 6.18, 11.83]
contour_labels = {
    2.30: r"$1\sigma$ (68.27%)",
    6.18: r"$2\sigma$ (95.45%)",
    11.83: r"$3\sigma$ (99.73%)",
}
contour_colors = ["tab:blue", "tab:orange", "tab:red"]

contour_figure, contour_axis = plt.subplots(figsize=(8, 7))
contours = contour_axis.contour(
    delta_m21_scan * 1.0e5,
    sin2_theta12_scan,
    delta_chi2_surface,
    levels=contour_levels,
    colors=contour_colors,
    linewidths=2.0,
)
contour_axis.clabel(
    contours,
    fmt=contour_labels,
    inline=True,
    fontsize=10,
)
contour_axis.plot(
    best_delta_m21 * 1.0e5,
    best_sin2_theta12,
    marker="*",
    markersize=14,
    color="black",
    label="Best fit",
)
contour_axis.set_xlabel(
    r"$\Delta m^2_{21}\ [10^{-5}\ {\rm eV}^2]$"
)
contour_axis.set_ylabel(r"$\sin^2\theta_{12}$")
contour_axis.set_title(
    r"Profile-$\chi^2$ confidence contours"
    "\n"
    r"$\Delta m^2_{32}$ profiled at every scan point"
)
contour_axis.grid(alpha=0.25)
contour_axis.legend()
contour_figure.tight_layout()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
contour_figure.savefig(CONTOUR_PDF, bbox_inches="tight")
contour_figure.savefig(CONTOUR_PNG, dpi=250, bbox_inches="tight")
plt.close(contour_figure)


# ---------------------------------------------------------------------------
# ROOT output
# ---------------------------------------------------------------------------

h_best_fit = ROOT.TH1D(
    "h_best_fit",
    "Best-fit prediction;E_{prompt} [MeV];Events",
    N_FIT_BINS,
    array("d", fit_edges),
)
h_best_fit.SetDirectory(0)
for reco_bin, value in enumerate(best_reco_prediction, start=1):
    h_best_fit.SetBinContent(reco_bin, float(value))

h_best_true = ROOT.TH1D(
    "h_best_true",
    "Best-fit true spectrum;E_{#nu} [MeV];Events",
    n_true_response_bins,
    array("d", nu_edges_fine),
)
h_best_true.SetDirectory(0)
for true_bin, value in enumerate(best_true_prediction, start=1):
    h_best_true.SetBinContent(true_bin, float(value))

# This is the effective 200 x 500 response used by the fit. X is true energy
# and Y is the 0--10 MeV fit energy, matching the original TH2 convention.
h_response_for_fit = ROOT.TH2D(
    "h_response_for_fit",
    "Response used by fit;E_{#nu}^{true} [MeV];E_{prompt} [MeV]",
    n_true_response_bins,
    array("d", nu_edges_fine),
    N_FIT_BINS,
    array("d", fit_edges),
)
h_response_for_fit.SetDirectory(0)
for fit_bin in range(N_FIT_BINS):
    for true_bin in range(n_true_response_bins):
        h_response_for_fit.SetBinContent(
            true_bin + 1,
            fit_bin + 1,
            float(response_for_fit[fit_bin, true_bin]),
        )


def centers_to_edges(centers):
    edges = np.empty(len(centers) + 1, dtype=np.float64)
    edges[1:-1] = 0.5 * (centers[:-1] + centers[1:])
    edges[0] = centers[0] - 0.5 * (centers[1] - centers[0])
    edges[-1] = centers[-1] + 0.5 * (centers[-1] - centers[-2])
    return edges


delta_m21_scan_edges = centers_to_edges(delta_m21_scan)
sin2_theta12_scan_edges = centers_to_edges(sin2_theta12_scan)

h_delta_chi2_dm21_sin2theta12 = ROOT.TH2D(
    "h_delta_chi2_dm21_sin2theta12",
    "Profile #Delta#chi^{2};"
    "#Delta m_{21}^{2} [eV^{2}];"
    "sin^{2}#theta_{12}",
    N_CONTOUR_POINTS,
    array("d", delta_m21_scan_edges),
    N_CONTOUR_POINTS,
    array("d", sin2_theta12_scan_edges),
)
h_delta_chi2_dm21_sin2theta12.SetDirectory(0)

h_profiled_delta_m32 = ROOT.TH2D(
    "h_profiled_delta_m32",
    "Profiled #Delta m_{32}^{2};"
    "#Delta m_{21}^{2} [eV^{2}];"
    "sin^{2}#theta_{12}",
    N_CONTOUR_POINTS,
    array("d", delta_m21_scan_edges),
    N_CONTOUR_POINTS,
    array("d", sin2_theta12_scan_edges),
)
h_profiled_delta_m32.SetDirectory(0)

for sin_index in range(N_CONTOUR_POINTS):
    for delta_index in range(N_CONTOUR_POINTS):
        delta_value = delta_chi2_surface[sin_index, delta_index]
        profiled_value = profiled_delta_m32[sin_index, delta_index]
        if np.isfinite(delta_value):
            h_delta_chi2_dm21_sin2theta12.SetBinContent(
                delta_index + 1,
                sin_index + 1,
                float(delta_value),
            )
        if np.isfinite(profiled_value):
            h_profiled_delta_m32.SetBinContent(
                delta_index + 1,
                sin_index + 1,
                float(profiled_value),
            )


# ---------------------------------------------------------------------------
# Plot only the requested 0--10 MeV fit interval.
# ---------------------------------------------------------------------------

fit_centers = 0.5 * (fit_edges[:-1] + fit_edges[1:])
fit_widths = fit_edges[1:] - fit_edges[:-1]
plot_errors = np.where(
    data_errors > 0.0,
    data_errors,
    np.sqrt(np.maximum(data_counts, 1.0)),
)

# Pearson standardized residual (often also called a pull):
#     (data - prediction) / sqrt(prediction)
standardized_residual = np.full(N_FIT_BINS, np.nan, dtype=np.float64)
positive_prediction = best_reco_prediction > 0.0
standardized_residual[positive_prediction] = (
    data_counts[positive_prediction]
    - best_reco_prediction[positive_prediction]
) / np.sqrt(best_reco_prediction[positive_prediction])

h_standardized_residual = ROOT.TH1D(
    "h_standardized_residual",
    "Standardized residual;"
    "E_{prompt} [MeV];"
    "(Data-Fit)/#sqrt{Fit}",
    N_FIT_BINS,
    array("d", fit_edges),
)
h_standardized_residual.SetDirectory(0)
for fit_bin, value in enumerate(standardized_residual, start=1):
    if np.isfinite(value):
        h_standardized_residual.SetBinContent(fit_bin, float(value))

figure, (spectrum_axis, residual_axis) = plt.subplots(
    2,
    1,
    figsize=(9, 8),
    sharex=True,
    gridspec_kw={
        "height_ratios": [3.0, 1.0],
        "hspace": 0.05,
    },
)

spectrum_axis.errorbar(
    fit_centers,
    data_counts,
    xerr=0.5 * fit_widths,
    yerr=plot_errors,
    fmt="o",
    markersize=3,
    color="black",
    label="Data",
)
spectrum_axis.stairs(
    best_reco_prediction,
    fit_edges,
    color="red",
    linewidth=2,
    label="Best-fit prediction",
)
spectrum_axis.set_ylabel("Events / bin")
spectrum_axis.set_title(
    rf"$\chi^2/\mathrm{{ndof}}={minimum_chi2:.2f}/{ndof}$, "
    rf"$p={p_value:.3g}$"
    "\n"
    rf"$\Delta m^2_{{21}}={best_delta_m21:.4e}$ eV$^2$, "
    rf"$\sin^2\theta_{{12}}={best_sin2_theta12:.4f}$, "
    rf"$\Delta m^2_{{32}}={best_delta_m32:.4e}$ eV$^2$"
)
spectrum_axis.legend()
spectrum_axis.grid(alpha=0.3)
spectrum_axis.tick_params(labelbottom=False)

# The shaded band marks +/-1 sigma; dashed lines mark +/-2 sigma.
residual_axis.axhspan(
    -1.0,
    1.0,
    color="tab:blue",
    alpha=0.12,
    linewidth=0,
)
residual_axis.axhline(0.0, color="black", linewidth=1.0)
residual_axis.axhline(
    2.0,
    color="gray",
    linestyle="--",
    linewidth=0.8,
)
residual_axis.axhline(
    -2.0,
    color="gray",
    linestyle="--",
    linewidth=0.8,
)
residual_axis.plot(
    fit_centers,
    standardized_residual,
    "o",
    markersize=3,
    color="black",
)
residual_axis.set_xlim(FIT_ENERGY_MIN, FIT_ENERGY_MAX)
residual_axis.set_xlabel(r"$E_{\rm prompt}$ [MeV]")
residual_axis.set_ylabel(
    r"$\frac{N_{\rm data}-N_{\rm fit}}{\sqrt{N_{\rm fit}}}$"
)
residual_axis.grid(alpha=0.3)

finite_residuals = standardized_residual[
    np.isfinite(standardized_residual)
]
if finite_residuals.size:
    residual_limit = max(
        3.0,
        1.15 * float(np.max(np.abs(finite_residuals))),
    )
    residual_axis.set_ylim(-residual_limit, residual_limit)

figure.align_ylabels((spectrum_axis, residual_axis))
figure.tight_layout()
figure.savefig(OUTPUT_PDF, bbox_inches="tight")
figure.savefig(OUTPUT_PNG, dpi=200, bbox_inches="tight")
plt.close(figure)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_file = ROOT.TFile.Open(str(OUTPUT_ROOT), "RECREATE")
if not output_file or output_file.IsZombie():
    raise OSError(f"Cannot create {OUTPUT_ROOT}")
output_file.cd()
h_data.Write()
h_best_fit.Write()
h_best_true.Write()
h_response_for_fit.Write()
h_standardized_residual.Write()
h_delta_chi2_dm21_sin2theta12.Write()
h_profiled_delta_m32.Write()
output_file.Close()

print("\nOutput files:")
print(f"  {OUTPUT_ROOT}")
print(f"  {OUTPUT_PDF}")
print(f"  {OUTPUT_PNG}")
print(f"  {CONTOUR_PDF}")
print(f"  {CONTOUR_PNG}")

file_data.Close()
file_response.Close()
file_mc.Close()
