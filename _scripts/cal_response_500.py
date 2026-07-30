from pathlib import Path

import ROOT


INPUT_FILE = "root/IBD_flat500k.root"
TREE_NAME = "evt"
OUTPUT_DIR = Path("F:/桌面/南山清北")
OUTPUT_FILE = OUTPUT_DIR / "response_500.root"
FIGURE_DIR = OUTPUT_DIR
N_RESPONSE_BINS = 500


def require_root_object(obj, description):
    if not obj:
        raise RuntimeError(f"Cannot load {description}")
    return obj


def calculate_response(n_response_bins=N_RESPONSE_BINS):
    input_file = ROOT.TFile.Open(INPUT_FILE, "READ")
    if not input_file or input_file.IsZombie():
        raise OSError(f"Cannot open {INPUT_FILE}")

    tree = require_root_object(input_file.Get(TREE_NAME), f"tree '{TREE_NAME}'")
    tree.SetBranchStatus("*", 1)

    epsilon = 1.0e-9
    true_min = float(tree.GetMinimum("nu_energy")) - epsilon
    true_max = float(tree.GetMaximum("nu_energy")) + epsilon
    reco_min = float(tree.GetMinimum("prompt_smearedE")) - epsilon
    reco_max = float(tree.GetMaximum("prompt_smearedE")) + epsilon

    migration_counts = ROOT.TH2D(
        "h_migration_counts",
        "Migration counts;"
        "E_{#nu}^{true} [MeV];"
        "E_{prompt} [MeV]",
        n_response_bins,
        true_min,
        true_max,
        n_response_bins,
        reco_min,
        reco_max,
    )
    migration_counts.SetDirectory(0)
    migration_counts.Sumw2()

    for event in tree:
        migration_counts.Fill(
            float(event.nu_energy),
            float(event.prompt_smearedE),
        )

    input_file.Close()

    response = ROOT.TH2D(
        "h_response",
        "Normalized response matrix;"
        "E_{#nu}^{true} [MeV];"
        "E_{prompt} [MeV]",
        n_response_bins,
        true_min,
        true_max,
        n_response_bins,
        reco_min,
        reco_max,
    )
    response.SetDirectory(0)
    response.Sumw2()

    empty_true_bins = 0
    for true_bin in range(1, n_response_bins + 1):
        column_sum = sum(
            migration_counts.GetBinContent(true_bin, reco_bin)
            for reco_bin in range(1, n_response_bins + 1)
        )

        if column_sum <= 0.0:
            empty_true_bins += 1
            continue

        for reco_bin in range(1, n_response_bins + 1):
            count = migration_counts.GetBinContent(true_bin, reco_bin)
            probability = count / column_sum

            # For unit-weight MC, this is the binomial statistical uncertainty.
            probability_error = (
                probability * (1.0 - probability) / column_sum
            ) ** 0.5

            response.SetBinContent(true_bin, reco_bin, probability)
            response.SetBinError(true_bin, reco_bin, probability_error)

    if empty_true_bins:
        print(
            f"Warning: {empty_true_bins} true-energy bins contain no MC events; "
            "their response columns are left at zero."
        )

    return migration_counts, response


def save_results(output_filename, migration_counts, response):
    Path(output_filename).parent.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    output_file = ROOT.TFile.Open(str(output_filename), "RECREATE")
    if not output_file or output_file.IsZombie():
        raise OSError(f"Cannot create {output_filename}")

    output_file.cd()
    migration_counts.Write()
    response.Write()

    canvas_counts = ROOT.TCanvas(
        "c_migration_counts",
        "Migration counts",
        900,
        750,
    )
    canvas_counts.SetRightMargin(0.15)
    migration_counts.Draw("COLZ")
    canvas_counts.Write()
    canvas_counts.SaveAs(str(FIGURE_DIR / "migration_counts_500.pdf"))

    canvas_response = ROOT.TCanvas(
        "c_response",
        "Response matrix",
        900,
        750,
    )
    canvas_response.SetRightMargin(0.15)
    response.SetMinimum(0.0)
    response.Draw("COLZ")
    canvas_response.Write()
    canvas_response.SaveAs(str(FIGURE_DIR / "response_matrix_500.pdf"))

    output_file.Close()
    print(f"Saved {output_filename}")


if __name__ == "__main__":
    counts_histogram, response_histogram = calculate_response()
    save_results(OUTPUT_FILE, counts_histogram, response_histogram)
