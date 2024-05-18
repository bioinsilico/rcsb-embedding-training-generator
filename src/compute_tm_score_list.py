from utils.parse_tm_align import parse_tm_align
from utils.run_command import run_command
from concurrent.futures import ThreadPoolExecutor, as_completed

US_CMD = "/Users/joan/devel/rcsb-embedding-training-generator/resources/us-align/USalign"
PDB_PATH = "/Users/joan/data/pdb"


def tm_align(entry_a, ch_a, entry_b, ch_b):
    cmd = f"{US_CMD} {PDB_PATH}/{entry_a}.cif.gz {PDB_PATH}/{entry_b}.cif.gz -chain1 {ch_a} -chain2 {ch_b}"
    stdout, stderr = run_command(cmd)
    return parse_tm_align(stdout)


def tm_score(entry_a, ch_a, entry_b, ch_b):
    tm_stdout = tm_align(entry_a, ch_a, entry_b, ch_b)
    return max(tm_stdout['TM_Score_1'], tm_stdout['TM_Score_2'])


if __name__ == "__main__":
    instance_list = [(r.strip().split(".")[0], r.strip().split(".")[1]) for r in open('../target/test_lit.tsv')]
    future_to_command = {}
    executor = ThreadPoolExecutor(max_workers=6)

    (pdb_i, ch_i) = instance_list.pop()
    while len(instance_list) > 0:
        for (pdb_j, ch_j) in instance_list:
            k = executor.submit(tm_score, pdb_i, ch_i, pdb_j, ch_j)
            future_to_command[k] = (pdb_i, ch_i, pdb_j, ch_j)
        (pdb_i, ch_i) = instance_list.pop()

    for future in as_completed(future_to_command):
        (pdb_i, ch_i, pdb_j, ch_j) = future_to_command[future]
        try:
            result = future.result()
            print(f"{pdb_i}.{ch_i},{pdb_j}.{ch_j},{result}")
        except Exception as exc:
            raise Exception(f"{pdb_i}.{ch_i},{pdb_j}.{ch_j},{tm_score(pdb_i,ch_i,pdb_j,ch_j)}")
