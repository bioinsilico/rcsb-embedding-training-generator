import csv

from utils.parse_tm_align import parse_tm_align
from utils.run_command import run_command

US_ALIGN_BIN  = "/home/jseguramora/devel/rcsb-embedding-training-generator/resources/us-align/USalign"
if __name__ == "__main__":
    with open('data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for (pdb_i, pdb_j, score) in csv_reader:
            cmd = f"{US_ALIGN_BIN} -mm 1 -ter 0 {pdb_i}.pdb {pdb_j}.pdb"
            stdout, stderr = run_command(cmd)
            print(parse_tm_align(stdout))