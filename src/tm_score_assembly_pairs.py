import csv
import argparse

from utils.parse_tm_align import parse_tm_align
from utils.run_command import run_command


if __name__ == "__main__":
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
        "--us_align_bin",
        type=str,
        required=True,
        help="List of PDB chains e.g. 101M.A",
    )
    parser.add_argument(
        "--pdb_path",
        type=str,
        required=True,
        help="List of PDB chains e.g. 101M.A",
    )
    parser.add_argument(
        "--out_file",
        type=str,
        required=True,
        help="List of PDB chains e.g. 101M.A",
    )
    cfg = parser.parse_args()
    US_ALIGN_BIN = cfg.us_align_bin
    PDB_PATH = cfg.pdb_path
    with open(cfg.out_file, 'w') as out:
        with open(cfg.list_file, 'r') as file:
            for row in file:
                (pdb_i, pdb_j, score) = row.strip().split("\t")
                cmd = f"{US_ALIGN_BIN} -mm 1 -ter 0 {PDB_PATH}/{pdb_i}.pdb {PDB_PATH}/{pdb_j}.pdb"
                stdout, stderr = run_command(cmd)
                tm_stdout = parse_tm_align(stdout)
                s = tm_stdout['TM_Score_1'] if tm_stdout['TM_Score_1'] > tm_stdout['TM_Score_2'] else tm_stdout['TM_Score_2']
                out.write(f"{pdb_i},{pdb_j},{score},{s}\n")