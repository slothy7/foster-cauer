"""Plot foster network and compare to source curve"""

import matplotlib.pyplot as plt

from ..foster import Foster
from .utils.parsing import MyParser
from .utils.zthcsvread import read_zth_csv


def main():
    """main"""

    parser = MyParser(
        description=(
            "Generate Foster RC model component values "
            "from Zth vs. time CSV file and plot resulting fit."
        )
    )
    parser.add_argument(
        "csv_file", help="CSV file containing Zth [K/W] vs. time [s] data"
    )
    parser.add_argument(
        "norder",
        type=int,
        default=4,
        help=(
            "How many RC pairs to generate for model. "
            "Currently supporting 3, 4, 5 orders. Default is 4th order."
        ),
    )
    parser.add_argument(
        "--rmax",
        type=float,
        default=1_000,
        help="Maximum value for any R in model. Default = 1000 Ohms",
    )
    parser.add_argument(
        "--cmax",
        type=int,
        default=1_000,
        help="Maximum value for any C in model. Default = 1000 F",
    )
    args = parser.parse_args()

    csv_file = args.csv_file

    # raw data from csv to be used for comparison to model later
    t, zth = read_zth_csv(csv_file)

    norder = args.norder
    rmax = args.rmax
    cmax = args.cmax

    foster = Foster()

    rc_vals = foster.foster_fit(
        csv_file, (0, [rmax] * norder + [cmax] * norder), norder
    )

    # label_template = (
    #     "fit:\nr1={:.2e}\nr2={:.2e}\nr3={:.2e}\nr4={:.2e}\nr5={:.2e}\n"
    #     "c1={:.2e}\nc2={:.2e}\nc3={:.2e}\nc4={:.2e}\nc5={:.2e}"
    # )
    label_template = "fit:\n"
    for i in range(norder * 2):
        if i < norder:
            # resistors first
            label_template = f"{label_template}r{i+1}={{:.2e}}\n"
        else:
            # now caps
            label_template = f"{label_template}c{i+1-norder}={{:.2e}}\n"

    plt.loglog(t, zth, "b-", label="data")
    plt.loglog(
        t,
        foster.foster_zth_n(norder, t, rc_vals),
        "go--",
        label=label_template.format(*rc_vals),
    )
    plt.xlabel("time [s]")
    plt.ylabel("Zth [K/W]")
    plt.grid(visible=True, which="both")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
