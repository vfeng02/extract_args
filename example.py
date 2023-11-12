import argparse
import os
import os.path

def add_args(parser): 
    parser.add_argument(
        "workdir", type=os.path.abspath, help="Directory with cryoDRGN results"
    )
    parser.add_argument(
        "epoch",
        type=int,
        help="Epoch number N to analyze (0-based indexing, corresponding to z.N.pkl, weights.N.pkl)",
    )
    parser.add_argument("--device", type=int, help="Optionally specify CUDA device")

def main(parser):
    print(parser._actions[-1].option_strings)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Example parser')
    main(parser)


