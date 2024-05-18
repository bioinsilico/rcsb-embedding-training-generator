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


if __name__ == "__main__":
    collect_instances_from_entities(ENTITY_50, "50")
