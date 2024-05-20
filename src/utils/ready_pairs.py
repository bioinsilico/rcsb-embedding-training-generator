
class ReadyPairs:
    ready_pairs = set({})

    def is_ready(self, pdb_i, ch_i, pdb_j, ch_j):
        if pdb_i == pdb_j and ch_j == ch_i:
            return True
        if f"{pdb_i}.{ch_i}:{pdb_j}.{ch_j}" in self.ready_pairs:
            return True
        if f"{pdb_j}.{ch_j}:{pdb_i}.{ch_i}" in self.ready_pairs:
            return True
        else:
            self.ready_pairs.add(f"{pdb_i}.{ch_i}:{pdb_j}.{ch_j}")
            return False
