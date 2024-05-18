import re


def parse_tm_align(output):
    parsed_data = {}

    # Use regular expressions to find and extract the required data
    structure_1_match = re.search(r"Name of Structure_1:\s*(.+)", output)
    structure_2_match = re.search(r"Name of Structure_2:\s*(.+)", output)
    length_1_match = re.search(r"Length of Structure_1:\s*(\d+)\s*residues", output)
    length_2_match = re.search(r"Length of Structure_2:\s*(\d+)\s*residues", output)
    aligned_length_match = re.search(r"Aligned length=\s*(\d+)", output)
    rmsd_match = re.search(r"RMSD=\s*([\d.]+)", output)
    tm_score_1_match = re.search(r"TM-score=\s*([\d.]+) \(normalized by length of Structure_1", output)
    tm_score_2_match = re.search(r"TM-score=\s*([\d.]+) \(normalized by length of Structure_2", output)

    if structure_1_match:
        parsed_data['Structure_1'] = structure_1_match.group(1).strip()
    if structure_2_match:
        parsed_data['Structure_2'] = structure_2_match.group(1).strip()
    if length_1_match:
        parsed_data['Length_1'] = int(length_1_match.group(1))
    if length_2_match:
        parsed_data['Length_2'] = int(length_2_match.group(1))
    if aligned_length_match:
        parsed_data['Aligned_Length'] = int(aligned_length_match.group(1))
    if rmsd_match:
        parsed_data['RMSD'] = float(rmsd_match.group(1))
    if tm_score_1_match:
        parsed_data['TM_Score_1'] = float(tm_score_1_match.group(1))
    if tm_score_2_match:
        parsed_data['TM_Score_2'] = float(tm_score_2_match.group(1))

    return parsed_data
