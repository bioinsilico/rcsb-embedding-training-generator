import argparse
import pandas as pd

from tm_score_list import save_results_to_file, config_tm_score


def load_range_pairs(file_path, start_row, end_row):
    """
    Load rows from a CSV file in a specified range without reading the whole file.

    Parameters:
    file_path (str): The path to the CSV file.
    start_row (int): The starting row index (0-based).
    end_row (int): The ending row index (0-based, inclusive).

    Returns:
    DataFrame: A DataFrame containing the specified rows.
    """
    # Calculate the number of rows to read
    nrows = end_row - start_row + 1
    # Use skiprows to skip the rows before the start_row and nrows to limit the number of rows read
    return pd.read_csv(
        file_path,
        skiprows=range(1, start_row + 1),
        nrows=nrows,
        header=None
    ).iterrows()


def count_pairs(file_path):
    """
    Count the number of lines in a file.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    int: The number of lines in the file.
    """
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count


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
        "--pair_list_file",
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
    parser.add_argument(
        "--buffer_size",
        type=int,
        required=False,
        default=1000,
        help="Number of tasks",
    )
    cfg = parser.parse_args()
    tm_score = config_tm_score(cfg.us_align_bin, cfg.pdb_path)
    num_pairs = count_pairs(cfg.pair_list_file)

    rank = cfg.rank
    size = cfg.size

    # Determine the range of indices for which this process is responsible
    chunk_size = num_pairs // size
    start_idx = rank * chunk_size
    end_idx = (rank + 1) * chunk_size if rank != size - 1 else num_pairs

    print(f"Rank {rank}/{size} protein list [{start_idx}:{end_idx}] / {num_pairs} ")


    buffer = []
    buffer_chunk_size = cfg.buffer_size
    results_filename = f'{cfg.out_path}/tm_scores_pair_{rank}.csv'

    for (idx, (pdb_i, ch_i, pdb_j, ch_j)) in load_range_pairs(file_path=cfg.pair_list_file, start_row=start_idx, end_row=end_idx):
        similarity_score = tm_score(pdb_i, ch_i, pdb_j, ch_j)
        buffer.append(f"{pdb_i},{ch_i},{pdb_j},{ch_j},{similarity_score[0]},{similarity_score[1]}\n")
        if len(buffer) >= buffer_chunk_size:
            save_results_to_file(buffer, results_filename)
            buffer.clear()

    if buffer:
        save_results_to_file(buffer, results_filename)


if __name__ == "__main__":
    main()
