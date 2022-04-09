import argparse
from pathlib import Path

import moldmaker.moldmaker

def main():
    parser = argparse.ArgumentParser(description="Make mold.")
    parser.add_argument("param_file", type=Path)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--dist-dir", type=Path, default="./mold")
    moldmaker.moldmaker.make_mold(**vars(parser.parse_args()))
