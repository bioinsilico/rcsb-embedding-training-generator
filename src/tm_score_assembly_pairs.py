import csv
import argparse

from utils.parse_tm_align import parse_tm_align
from utils.run_command import run_command

US_ALIGN_BIN  = "/home/jseguramora/devel/rcsb-embedding-training-generator/resources/us-align/USalign"
PDB_PATH = "/home/jseguramora/jobs/lustre/structure-embedding/foldseek-assembly/pdb"

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
    cfg = parser.parse_args()
    with open(cfg.list_file, 'r') as file:
        csv_reader = csv.reader(file)
        for (pdb_i, pdb_j, score) in csv_reader:
            cmd = f"{US_ALIGN_BIN} -mm 1 -ter 0 {PDB_PATH}/{pdb_i}.pdb {PDB_PATH}/{pdb_j}.pdb"
            stdout, stderr = run_command(cmd)
            print(parse_tm_align(stdout))