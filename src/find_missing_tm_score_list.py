import argparse
import os
import csv

from tm_score_list import load_results_from_file, generate_pairs, build_key
from utils.parse_tm_align import parse_tm_align

from utils.run_command import run_command


def main():
    parser = argparse.ArgumentParser(
        description="Use compute_tm_score_list \
        to calculate TM-score between structure chains of a query and target lists",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--list_file",
        type=str,
        required=True,
        help="List of PDB chains e.g. 101M.A",
    )
    parser.add_argument(
        "--tm_score_path",
        type=str,
        required=True,
        help="Output folder ",
    )
    parser.add_argument(
        "--tm_score_missing_list_file",
        type=str,
        required=True,
        help="Output folder ",
    )
    cfg = parser.parse_args()
    proteins = [(r.strip().split(".")[0], r.strip().split(".")[1]) for r in open(cfg.list_file)]
    num_proteins = len(proteins)

    local_results = set({})
    for n in range(0,1000):
        local_results.update(load_results_from_file(f"{cfg.tm_score_path}/tm_scores_rank_{n}.csv"))

    with open(cfg.tm_score_missing_list_file, 'w', newline='') as f:
        for ((pdb_i, ch_i), (pdb_j, ch_j)) in generate_pairs(proteins, 0, num_proteins):
            if build_key(pdb_i, ch_i, pdb_j, ch_j) not in local_results:
                f.write(f"{pdb_i},{ch_i},{pdb_j},{ch_j}\n")


if __name__ == "__main__":
    main()
