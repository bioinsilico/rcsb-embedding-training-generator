## RCSB PDB Embedding Training Generator
Collection of scripts to generated training set based on TM-score for training embedding search.

### MPI test
```shell
python tm_score_list.py \
  --pdb_path /Users/joan/data/pdb \
  --us_align_bin /Users/joan/devel/rcsb-embedding-training-generator/resources/us-align/USalign \
  --list_file /Users/joan/devel/rcsb-embedding-training-generator/target/instance30_list.tsv \
  --out_path /Users/joan/tmp \
  --rank 0 \
  --size 4
```