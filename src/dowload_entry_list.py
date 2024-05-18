import os
import requests


def download_file(url, folder_path, file_name=None):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Determine the file name from the URL if not provided
    if file_name is None:
        file_name = os.path.basename(url)

    # Full path to save the file
    file_path = os.path.join(folder_path, file_name)

    # Download the file
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Save the file
    with open(file_path, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    for row in open("../target/entry50_list.tsv"):
        entry_id = row.strip()
        print(f"Downloading {entry_id}")
        download_file(f"https://files.rcsb.org/download/{entry_id}.cif.gz", "/Users/joan/data/pdb")