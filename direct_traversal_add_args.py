import os

def add_args(parser): 
    # parser.description = "Construct z path interpolating between anchor points"
    parser.add_argument("z", help="Input z.pkl embeddings")
    parser.add_argument(
        "--ind",
        metavar=".TXT",
        required=True,
        help="Text file containing indices of anchor points",
    )
    parser.add_argument(
        "-n",
        type=int,
        default=6,
        help="Number of points in between anchors, inclusive (default: %(default)s)",
    )
    parser.add_argument("--loop", action="store_true", help="Loop to first point")
    parser.add_argument(
        "-o",
        metavar="Z.PATH.TXT",
        type=os.path.abspath,
        required=True,
        help="Output .txt file for z-values",
    )



