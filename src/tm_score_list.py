import argparse
import os
import csv

from utils.parse_tm_align import parse_tm_align

from utils.run_command import run_command


def config_tm_score(us_cmd, pdb_path):
    def __tm_align(entry_a, ch_a, entry_b, ch_b):
        cmd = f"{us_cmd} {pdb_path}/{entry_a}.cif.gz {pdb_path}/{entry_b}.cif.gz -chain1 {ch_a} -chain2 {ch_b}"
        stdout, stderr = run_command(cmd)
        return parse_tm_align(stdout)

    def __tm_score(entry_a, ch_a, entry_b, ch_b):
        tm_stdout = __tm_align(entry_a, ch_a, entry_b, ch_b)
        return tm_stdout['TM_Score_1'], tm_stdout['TM_Score_2']

    return __tm_score


def generate_pairs(proteins, start, end):
    """Generate pairs on-the-fly within the specified range."""
    for i in range(start, end):
        for j in range(i + 1, len(proteins)):
            yield proteins[i], proteins[j]


def save_results_to_file(results, filename):
    """Save results to a CSV file."""
    with open(filename, 'a', newline='') as f:
        for res in results:
            f.write(res)


def load_results_from_file(filename):
    """Load results from a CSV file."""
    results = set({})
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                pair = build_key(row[0], row[1], row[2], row[3])
                results.add(pair)
        print(f"Found file: {filename} with {len(results)} pairs")
    return results


def build_key(pdb_i, ch_i, pdb_j, ch_j):
    return f"{pdb_i}.{ch_i}:{pdb_j}.{ch_j}"


def main():
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
        "--list_file",
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
    parser.add_argument(
        "--rank",
        type=int,
        required=True,
        help="Task rank",
    )
    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="Number of tasks",
    )
    cfg = parser.parse_args()
    tm_score = config_tm_score(cfg.us_align_bin, cfg.pdb_path)
    proteins = [(r.strip().split(".")[0], r.strip().split(".")[1]) for r in open(cfg.list_file)]
    num_proteins = len(proteins)

    rank = cfg.rank
    size = cfg.size

    # Determine the range of indices for which this process is responsible
    chunk_size = num_proteins // size
    start_idx = rank * chunk_size
    end_idx = (rank + 1) * chunk_size if rank != size - 1 else num_proteins

    print(f"Rank {rank}/{size} protein list [{start_idx}:{end_idx}] / {num_proteins} ")

    # Load previously saved results if they exist
    results_filename = f'{cfg.out_path}/tm_scores_rank_{rank}.csv'
    local_results = load_results_from_file(results_filename)

    buffer = []
    buffer_chunk_size = 1000

    for ((pdb_i, ch_i), (pdb_j, ch_j)) in generate_pairs(proteins, start_idx, end_idx):
        if build_key(pdb_i, ch_i, pdb_j, ch_j) in local_results:
            continue
        similarity_score = tm_score(pdb_i, ch_i, pdb_j, ch_j)
        buffer.append(f"{pdb_i},{ch_i},{pdb_j},{ch_j},{similarity_score[0]},{similarity_score[1]}\n")
        if len(buffer) >= buffer_chunk_size:
            save_results_to_file(buffer, results_filename)
            buffer.clear()

    if buffer:
        save_results_to_file(buffer, results_filename)


if __name__ == "__main__":
    main()
