# @Date:   2019-10-28T14:02:28+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioAlgo_1028_1730416009.py
# @Last modified time: 2019-11-03T21:43:12+08:00
from Bio import SeqIO
from BioAlgo_0928_1730416009 import MySeq
from BioAlgo_1021_1730416009 import DeterministicMotifFinding


class MyMotifs:
    """
    Class to handle Probabilistic Weighted Matrix

    * Function

        * Create Position Weight Matrices
        * Define Data Structures For Motif
        * Return Motif Object

    """

    def __init__(self, seqs=[], pwm=[], alphabet=None):
        if seqs:
            self.size = len(seqs[0])
            self.seqs = seqs  # objet from class MySeq
            self.alphabet = seqs[0].alphabet()
            self.do_counts()
            self.create_pwm()
        else:
            self.pwm = pwm
            self.size = len(pwm[0])
            self.alphabet = alphabet

    def __len__(self):
        return self.size

    def create_matrix_zeros(nrows, ncols):
        res = []
        for i in range(0, nrows):
            res.append([0] * ncols)
        return res

    def do_counts(self):
        """
        Initialize the Counting Matrix
        """
        self.counts = MyMotifs.create_matrix_zeros(
            len(self.alphabet), self.size)
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1

    def create_pwm(self):
        """
        Probabilistic Weighted Matrix
        """
        if self.counts is None:
            self.do_counts()
        self.pwm = MyMotifs.create_matrix_zeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)

    def consensus(self):
        """
        returns the sequence motif obtained with the most frequent symbol at each position of the motif
        """
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self .alphabet[maxcoli]
        return res

    def masked_consensus(self):
        """
        returns the sequence motif obtained with the symbol that occurs in at least 50% of the input sequences
        """
        res = ""
        for j in range(self.size):
            maxcol = self .counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self .counts[i][j] > maxcol:
                    maxcol = self .counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self .alphabet[maxcoli]
            else:
                res += "− "
        return res

    def probability_sequence(self, seq):
        """
        Calculate the product of probabilities for each alphabet
        """
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res

    def probability_all_positions(self, seq):
        """
        Get the probabilities for all position via probability_sequence()
        """
        res = []
        for k in range(len(seq) - self.size + 1):
            res.append(self.probability_sequence(seq))
        return res

    def most_probable_sequence(self, seq):
        """
        Returns the index of the most probable sub−sequence of the input sequence
        """
        maximum = -1.0
        maxind = -1
        for k in range(len(seq) - self.size):
            p = self.probability_sequence(seq[k:k + self.size])
            if (p > maximum):
                maximum = p
                maxind = k
        return maxind

    def create_motif(self, seqs):
        """
        Use most_probable_sequence() to select the best subSeq
        """
        from MySeq import MySeq
        ll = []
        for s in seqs:
            ind = self.most_probable_sequence(s.seq)
            subseq = MySeq(s[ind:(ind + self.size)], s.get_seq_biotype())
            ll.append(subseq)
        return MyMotifs(ll)


class MotifFinding(DeterministicMotifFinding):
    """
    Inherited from parent class: ``DeterministicMotifFinding``

    Add new function:

        * ``new_create_motif_from_indexes()``
        * ``heuristic_stochastic()``
    """

    def new_create_motif_from_indexes(self, indexes):
        """
        Description::

            * A matrix is constructed from a set of motifs.
            * The number of columns is equal to the length of motif and the number of rows is equal to the size of alphabet.
            * Each cell of the matrix contains the frequency of the symbol in a given location

        """
        pseqs = []
        for i, ind in enumerate(indexes):
            pseqs.append(
                MySeq(self.seqs[i][ind:(ind + self.motif_size)], self.seqs[i].get_seq_biotype()))
        return MyMotifs(pseqs)

    def heuristic_stochastic(self):
        """
        Create a motif object from the randomly selected initial position on the input sequence,
        corresponding to PWM and scoring
        """
        from random import randint
        s = [0] * len(self.seqs)
        for k in range(len(s)):
            s[k] = randint(0, self.seq_size(k) - self.motif_size)
        motif = self.new_create_motif_from_indexes(s)
        motif.create_pwm()
        sc = self.score_multiplicative(s)
        bestsol = s
        improve = True
        while(improve):
            for k in range(len(s)):
                s[k] = motif.most_probable_sequence(self.seqs[k])
            if self.score_multiplicative(s) > sc:
                sc = self.score_multiplicative(s)
                bestsol = s
                motif = self.new_create_motif_from_indexes(s)
                motif.create_pwm()
            else:
                improve = False
        return bestsol


def motifSeqIO(fileName, format="fasta"):
    seqs = []
    for record in SeqIO.parse(fileName, format):
        seqs.append(MySeq(record.seq))
    return seqs


if __name__ == "__main__":
    seqs = motifSeqIO("./input.txt")
    motif = MotifFinding(8, seqs)
    print("Heuristic stochastic")
    sol = motif.heuristic_stochastic()
    print("Solution: ", sol)
    print("Score:", motif.score(sol))
    print("Score mult:", motif.score_multiplicative(sol))
    print("Consensus:", motif.new_create_motif_from_indexes(sol).consensus())
