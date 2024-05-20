import argparse

from utils.parse_tm_align import parse_tm_align
from utils.ready_pairs import ReadyPairs
from utils.run_command import run_command
from concurrent.futures import ThreadPoolExecutor, as_completed




def tm_align(entry_a, ch_a, entry_b, ch_b):
    cmd = f"{US_CMD} {PDB_PATH}/{entry_a}.cif.gz {PDB_PATH}/{entry_b}.cif.gz -chain1 {ch_a} -chain2 {ch_b}"
    stdout, stderr = run_command(cmd)
    return parse_tm_align(stdout)


def tm_score(entry_a, ch_a, entry_b, ch_b):
    tm_stdout = tm_align(entry_a, ch_a, entry_b, ch_b)
    return max(tm_stdout['TM_Score_1'], tm_stdout['TM_Score_2'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Use compute_tm_score_list \
        to calculate TM-score between structure chains of a query and target lists",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--pdb_path",
        type=str,
        required=True,
        help="Folder with PDB files",
    )
    parser.add_argument(
        "--us_align_bin",
        type=str,
        required=True,
        help="US-align exec",
    )
    parser.add_argument(
        "--query_list_file",
        type=str,
        required=True,
        help="List of PDB chains e.g. 101M.A",
    )
    parser.add_argument(
        "--target_list_file",
        type=str,
        required=True,
        help="List of PDB chains e.g. 101M.A",
    )
    parser.add_argument(
        "--out_path",
        type=str,
        required=True,
        help="Output folder ",
    )
    cfg = parser.parse_args()

    US_CMD = cfg.us_align_bin
    PDB_PATH = cfg.pdb_path

    query_list = [(r.strip().split(".")[0], r.strip().split(".")[1]) for r in open(cfg.query_list_file)]
    target_list = [(r.strip().split(".")[0], r.strip().split(".")[1]) for r in open(cfg.target_list_file)]

    ready_pairs = ReadyPairs()

    for (pdb_i, ch_i) in query_list:
        executor = ThreadPoolExecutor(max_workers=6)
        future_to_command = {}
        for (pdb_j, ch_j) in target_list:
            if ready_pairs.is_ready(pdb_i, ch_i, pdb_j, ch_j):
                continue
            k = executor.submit(tm_score, pdb_i, ch_i, pdb_j, ch_j)
            future_to_command[k] = (pdb_i, ch_i, pdb_j, ch_j)
        with open(f'{cfg.out_path}/{pdb_i}.{ch_i}.tm_score.csv', 'w') as file:
            for future in as_completed(future_to_command):
                (pdb_i, ch_i, pdb_j, ch_j) = future_to_command.get(future)
                try:
                    result = future.result()
                    file.write(f"{pdb_i}.{ch_i},{pdb_j}.{ch_j},{result}\n")
                except Exception as exc:
                    raise Exception(f"{pdb_i}.{ch_i},{pdb_j}.{ch_j},{tm_score(pdb_i, ch_i, pdb_j, ch_j)}")
        break
