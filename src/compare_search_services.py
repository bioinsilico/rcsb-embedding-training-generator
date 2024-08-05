import json
import requests


# Function to load a JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def request_assemblies(service_url, pdb_id):
    url = f"{service_url}/search/assembly/{pdb_id}/1"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def extract_assemblies(docs):
    return [
        (item['total_score'], f"{item['rcsb_shape_container_identifiers']['entry_id']}-{item['rcsb_shape_container_identifiers']['assembly_id']}")
        for item in docs
    ]


def main():
    assemblies = load_json("../resources/homomeric_assembly_sizes_all.json")
    for pdb_id, num_chains in assemblies.items():
        if 1 < num_chains < 7:
            embedding_search = [a for s,a in extract_assemblies(request_assemblies("http://embedding-search.rcsb.org", pdb_id))]
            bio_zernike = [a for s,a in extract_assemblies(request_assemblies("https://shapesearch.rcsb.org/", pdb_id)) if s >= 70.]
            observed = set()
            coverage = [f"{pdb_id} - {len(embedding_search)} / {len(bio_zernike)} :"]
            for idx, assembly_id in enumerate(embedding_search):
                if assembly_id in bio_zernike:
                    observed.add(assembly_id)
                if len(observed) >= 0.25 * len(bio_zernike) and len(coverage) == 1:
                    coverage.append(str(idx+1))
                if len(observed) >= 0.5 * len(bio_zernike) and len(coverage) == 2:
                    coverage.append(str(idx+1))
                if len(observed) >= 0.75 * len(bio_zernike) and len(coverage) == 3:
                    coverage.append(str(idx+1))
                if len(observed) >= 0.90 * len(bio_zernike) and len(coverage) == 4:
                    coverage.append(str(idx+1))
                if len(observed) == len(bio_zernike):
                    coverage.append(str(idx+1))
                    break
            if len(observed) < len(bio_zernike):
                coverage.append("0")
            print("\t".join(coverage + [a for a in bio_zernike if a not in observed][0:5] + ["||"] + [a for a in embedding_search if a not in bio_zernike][0:5]))


if __name__ == "__main__":
    main()
