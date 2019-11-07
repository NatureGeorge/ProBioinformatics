# @Date:   2019-10-21T14:15:14+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioAlgo_1021_1730416009.py
# @Last modified time: 2019-11-03T19:52:31+08:00
# import sys
# sys.append("./")
from BioAlgo_0928_1730416009 import MySeq
import numpy as np
# from collections import Counter


class DeterministicMotifFinding:
    """ Class for deterministic motif finding. """

    def __init__(self, size=8, seqs=None):
        self.motif_size = size
        if seqs is not None:
            assert isinstance(seqs[0], MySeq), "seqs contains MySeq object"
            self.seqs = seqs
            self.alphabet = seqs[0].alphabet()
        else:
            self.seqs = []

    def __len__(self):
        return len(self.seqs)

    def __getitem__(self, n):
        return self.seqs[n]

    def seq_size(self, i):
        return len(self.seqs[i])

    def read_file(self, fic, t):
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(), t))
        self.alphabet = self.seqs[0].alphabet()

    def create_motif_from_indexes(self, indexes):
        # pseqs = []
        res = [[0] * self.motif_size for i in range(len(self.alphabet))]
        for i, ind in enumerate(indexes):
            subseq = self.seqs[i][ind:(ind + self.motif_size)]
            for i in range(self.motif_size):
                for k in range(len(self.alphabet)):
                    if subseq[i] == self.alphabet[k]:
                        res[k][i] = res[k][i] + 1
        return res

    def score(self, s):
        score = 0
        mat = self.create_motif_from_indexes(s)
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score += maxcol
        return score

    def score_multiplicative(self, s):
        score = 1.0
        mat = self.create_motif_from_indexes(s)
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score = score * maxcol
        return score

    def next_solution(self, s):
        next_sol = [0] * len(s)
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seq_size(pos) - self.motif_size:
            pos -= 1
        if (pos < 0):
            next_sol = None
        else:
            for i in range(pos):
                next_sol[i] = s[i]
            next_sol[pos] = s[pos] + 1
            for i in range(pos + 1, len(s)):
                next_sol[i] = 0
        return next_sol

    def exhaustive_search(self):
        best_score = -1
        res = []
        s = [0] * len(self.seqs)
        while s is not None:
            sc = self.score(s)
            if (sc > best_score):
                best_score = sc
                res = s
            s = self.next_solution(s)
        return res

    def next_vertex(self, s):
        res = []
        if len(s) < len(self.seqs):  # internal node −> down one level
            for i in range(len(s)):
                res.append(s[i])
            res.append(0)
        else:  # bypass
            pos = len(s) - 1
            while pos >= 0 and s[pos] == self.seq_size(pos) - self.motif_size:
                pos -= 1
            if pos < 0:
                res = None  # last solution
            else:
                for i in range(pos):
                    res.append(s[i])
                res.append(s[pos] + 1)
        return res

    def bypass(self, s):
        res = []
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seq_size(pos) - self.motif_size:
            pos -= 1
        if pos < 0:
            res = None
        else:
            for i in range(pos):
                res.append(s[i])
            res.append(s[pos] + 1)
        return res

    def branch_and_bound(self):
        best_score = -1
        best_motif = None
        size = len(self.seqs)
        s = [0] * size
        while s is not None:
            if len(s) < size:
                # estimate the bound for current internal node
                # test if the best score can be reached
                optimum_score = self.score(
                    s) + (size - len(s)) * self.motif_size
                if optimum_score < best_score:
                    s = self.bypass(s)
                else:
                    s = self.next_vertex(s)
            else:
                # test if current leaf is a better solution
                sc = self.score(s)
                if sc > best_score:
                    best_score = sc
                    best_motif = s
                s = self.next_vertex(s)
        return best_motif

    def heuristic_consensus(self):
        res = [0] * len(self.seqs)
        max_score = -1
        partial = [0, 0]
        for i in range(self.seq_size(0) - self.motif_size):
            for j in range(self.seq_size(1) - self.motif_size):
                partial[0] = i
                partial[1] = j
                sc = self.score(partial)
                if(sc > max_score):
                    max_score = sc
                    res[0] = i
                    res[1] = j
        for k in range(2, len(self.seqs)):
            partial = [0]*(k + 1)
            for j in range(k):
                partial[j] = res[j]
            max_score = -1
            for i in range(self.seq_size(k) - self.motif_size):
                partial[k] = i
                sc = self.score(partial)
                if(sc > max_score):
                    max_score = sc
                    res[k] = i
        return res


def test():
    seqs = ['gtcaac', 'gtcgac', 'gttaac', 'gttgac', 'gtcaac']
    seqs_array = np.array([[i for i in seq.upper()] for seq in seqs])
    motif_len = len(seqs[0])
    alphabet = 'ACGT'
    li = []
    for i in range(motif_len):
        sub = seqs_array[:, i]
        li.append([len(sub[sub == a]) for a in alphabet])
    print(li)


def test2():
    seqs = ['gtcaac', 'gtcgac', 'gttaac', 'gttgac', 'gtcaac']
    motif_len = len(seqs[0])
    alphabet = 'acgt'
    res = [[0] * motif_len for i in range(4)]
    for subseq in seqs:
        for i in range(motif_len):
            for k in range(4):
                if subseq[i] == alphabet[k]:
                    res[k][i] = res[k][i] + 1
    print(res)


def test_full():
    seq1 = MySeq("ATAGAGCTGA", "DNA")
    seq2 = MySeq("ACGTAGATGA", "DNA")
    seq3 = MySeq("AAGATAGGGG", "DNA")
    mf = DeterministicMotifFinding(3, [seq1, seq2, seq3])
    print("Exhaustive:")
    sol = mf.exhaustive_search()
    print("Solution: ", sol)
    print("Score: ", mf.score(sol))
    print("\nBranch and Bound:")
    sol2 = mf.branch_and_bound()
    print("Solution: ", sol2)
    print("Score:", mf.score(sol2))
    print("\nHeuristic consensus: ")
    sol3 = mf.heuristic_consensus()
    print("Solution: ", sol3)
    print("Score:", mf.score(sol3))


if __name__ == "__main__":
    test_full()
