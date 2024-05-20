"""CSV to Cauer RC thermal network CLI"""

from ..cauer import Cauer
from .utils.parsing import MyParser


def main() -> None:
    """main"""
    # Foster network components
    # Expand to as many RC pairs as necessary as shown in comments

    parser = MyParser(
        description="Generate Cauer RC model component values from Zth vs. time CSV file",
        epilog="ssherbrook@apple.com",
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
    norder = args.norder
    rmax = args.rmax
    cmax = args.cmax

    cauer = Cauer()
    cauer_rcs = cauer.get_cauer_rcs(csv_file, norder, rmax, cmax)

    for comp, val in cauer_rcs.items():
        print(f".param {comp} = {val}")


if __name__ == "__main__":
    main()
