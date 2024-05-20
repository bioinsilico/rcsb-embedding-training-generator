import os

import pymongo

from entity_50 import ENTITY_50
from entity_70 import ENTITY_70
from entity_30 import ENTITY_30


def collect_instances_from_entities(entity_list, thr):
    db_client = pymongo.MongoClient(
        "mongodb://updater:w31teQuerie5@10.20.2.171:27017/?connectTimeoutMS=3000000&socketTimeoutMS=3000000"
        # "mongodb://localhost:27017"
    )
    dw = db_client["dw"]
    core_entity = dw["core_polymer_entity"]
    entries = set({})

    with open(f'../target/instance{thr}_list.tsv', 'w') as file:
        for entity_id in entity_list:
            auth_asym_id = core_entity.find(
                {"rcsb_id": entity_id},
                {"rcsb_polymer_entity_container_identifiers.auth_asym_ids": 1}
            )[0]["rcsb_polymer_entity_container_identifiers"]["auth_asym_ids"][0]
            entries.add(entity_id.split('_')[0])
            print(f"{entity_id.split('_')[0]}.{auth_asym_id}")
            file.write(f"{entity_id.split('_')[0]}.{auth_asym_id}\n")

    with open(f'../target/entry{thr}_list.tsv', 'w') as file:
        for entry_id in entries:
            file.write(f"{entry_id}\n")


def split_file(file_path, n):
    if n < 1:
        raise ValueError("Number of chunks must be at least 1.")

    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    chunk_size = total_lines // n
    remainder = total_lines % n

    base_name, ext = os.path.splitext(file_path)

    chunks = []
    start = 0

    for i in range(n):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunk_lines = lines[start:end]
        chunk_file = f"{base_name}-{i+1}{ext}"
        with open(chunk_file, 'w') as chunk:
            chunk.writelines(chunk_lines)
        chunks.append(chunk_file)
        start = end

    return chunks


if __name__ == "__main__":
    thr = "50"
    entity_list = ENTITY_50
    collect_instances_from_entities(entity_list, thr)
    split_file(f"../target/instance{thr}_list.tsv", 100)
