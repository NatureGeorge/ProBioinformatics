# @Date:   2019-09-28T15:43:04+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioAlgo_0928_1730416009.py
# @Last modified time: 2019-10-13T00:27:06+08:00


class MyAlign:
    def __init__(self , lseqs, gapSymbol="-"):
        self.listseqs = lseqs
        self.gapSymbol = gapSymbol

    def __len__(self): # number of columns
        return len(self.listseqs[0])

    def __getitem__(self, n):
        if type(n) is tuple and len(n) ==2:
            i, j = n
            return self.listseqs[i][j]
        elif type(n) is int: return self.listseqs[n]
        return None

    def __str__(self):
        res = ""
        for seq in self.listseqs:
            res += "\n" + seq
        return res

    def num_seqs(self):
        return len(self.listseqs)

    def column(self, indice):
        res = []
        for k in range(len(self.listseqs)):
            res.append( self.listseqs[k][indice])
        return res

    def consensus(self):
        cons = ""
        for i in range(len(self)):
            cont = {}
            for k in range(len(self.listseqs)):
                c = self.listseqs[k][i]
                if c in cont:
                    cont[c] = cont[c] + 1
                else:
                    cont[c] = 1
            maximum = 0
            cmax = None
            for ke in cont.keys():
                if ke != self.gapSymbol and cont[ke] > maximum:
                    maximum = cont[ke]
                    cmax = ke
            cons = cons + cmax
        return cons


class PairWiseAligner:
    '''
    # Pairwise Alignment
    * Global Alignment: Needleman-Wunsch
    * Local Alignment: Smith-Waterman
    '''

    def __init__(self):
        '''Set DefaultValues'''
        self.gapSymbol = "-"
        self.defaultValue = 0
        self.newMatrix = {}

    def __repr__(self):
        '''Show the Content of Matrix'''
        from numpy import array
        return "Matrix(S):\n%s\n\nMatrix(T):\n%s\n" % (array(self.S), array(self.T))

    @property
    def defaultMatrix(self):
        '''Get Blosum Matrix Via BioPython'''
        from Bio.SubsMat import MatrixInfo
        matrix = MatrixInfo.blosum62
        return matrix

    def score_pos(self, c1, c2):
        '''Get Score of particular position via given matrix'''
        if c1 == self.gapSymbol or c2 == self.gapSymbol:
            return self.gap
        else:
            try:
                result = self.matrix[(c1, c2)]
            except KeyError:
                try:
                    result = self.matrix[(c2, c1)]
                except KeyError:
                    print("Unexpected key for given matrix, return defaultValue.")
                    return self.defaultValue
        return result

    def max3t(v1, v2, v3):
        '''Get the optimized direction'''
        if v1 > v2:
            if v1 > v3:
                return 1
            else:
                return 3
        else:
            if v2 > v3:
                return 2
            else:
                return 3

    def max_mat(mat):
        '''Get the row and col of optimized values'''
        maxval = mat[0][0]
        maxrow = 0
        maxcol = 0
        for i in range(0, len(mat)):
            for j in range(0, len(mat[i])):
                if mat[i][j] > maxval:
                    maxval = mat[i][j]
                    maxrow = i
                    maxcol = j
        return maxrow, maxcol

    def needleman_Wunsch(self):
        '''
        Global Alignment
        * Dynamic Programming
        * optimized
        '''
        self.S = [[0]]  # Record the score
        self.T = [[0]]  # Record the orientation
        # initialize gaps'row
        for j in range(1, len(self.seq2)+1):
            self.S[0].append(self.gap * j)
            self.T[0].append(3)
        # initialize gaps'column
        for i in range(1, len(self.seq1)+1):
            self.S.append([self.gap * i])
            self.T.append([2])
        # apply the recurrence relation to fill the remaining of the matrix
        for i in range(len(self.seq1)):
            for j in range(len(self.seq2)):
                s1 = self.S[i][j] + self.score_pos(self.seq1[i], self.seq2[j])
                s2 = self.S[i][j+1] + self.gap
                s3 = self.S[i+1][j] + self.gap
                self.S[i+1].append(max(s1, s2, s3))
                self.T[i+1].append(PairWiseAligner.max3t(s1, s2, s3))

    def smith_Waterman(self):
        '''
        Local Alignment
        * Dynamic Programming
        * optimized
        '''
        self.S = [[0]]  # Record the score
        self.T = [[0]]  # Record the orientation
        maxscore = 0
        for j in range(1, len(self.seq2)+1):
            self.S[0].append(0)
            self.T[0].append(0)
        for i in range(1, len(self.seq1)+1):
            self.S.append([0])
            self.T.append([0])
        for i in range(0, len(self.seq1)):
            for j in range(len(self.seq2)):
                s1 = self.S[i][j] + self.score_pos(self.seq1[i], self.seq2[j])
                s2 = self.S[i][j+1] + self.gap
                s3 = self.S[i+1][j] + self.gap
                b = max(s1, s2, s3)
                if b <= 0:
                    self.S[i+1].append(0)
                    self.T[i+1].append(0)
                else:
                    self.S[i+1].append(b)
                    self.T[i+1].append(PairWiseAligner.max3t(s1, s2, s3))
                    if b > maxscore:
                        maxscore = b
        return maxscore

    def recover_align_global(self):
        '''Get the content of global alignment'''
        res = ["", ""]
        i = len(self.seq1)
        j = len(self.seq2)
        while i > 0 or j > 0:
            if self.T[i][j] == 1:
                res[0] = self.seq1[i-1] + res[0]
                res[1] = self.seq2[j-1] + res[1]
                i -= 1
                j -= 1
            elif self.T[i][j] == 3:
                res[0] = self.gapSymbol + res[0]
                res[1] = self.seq2[j-1] + res[1]
                j -= 1
            else:
                res[0] = self.seq1[i-1] + res[0]
                res[1] = self.gapSymbol + res[1]
                i -= 1
        return MyAlign(res)

    def recover_align_local(self):
        '''Get the content of local alignment'''
        res = ["", ""]
        i, j = PairWiseAligner.max_mat(self.S)
        while self.T[i][j] > 0:
            if self.T[i][j] == 1:
                res[0] = self.seq1[i-1] + res[0]
                res[1] = self.seq2[j-1] + res[1]
                i -= 1
                j -= 1
            elif self.T[i][j] == 3:
                res[0] = self.gapSymbol + res[0]
                res[1] = self.seq2[j-1] + res[1]
                j -= 1
            elif self.T[i][j] == 2:
                res[0] = self.seq1[i-1] + res[0]
                res[1] = self.gapSymbol + res[1]
                i -= 1
        return MyAlign(res)

    def is_legal_matrix(self, matrix):
        '''Check whether the dict-form of matrix is legal or not'''
        if not isinstance(matrix, dict):
            print("Not a Dict", type(matrix))
            return False
        else:
            for key, data in matrix.items():
                if len(key) != 2:
                    print("Invalid Key")
                    return False
                else:
                    try:
                        int(data)
                    except Exception:
                        print("Invalid Data")
                        return False
            return True

    def new_matrix(self, pairs, value):
        '''Create new matrix via input'''
        if not hasattr(self, 'matrix'):
            self.matrix = {}
        self.matrix[tuple(pairs)] = value

        assert self.is_legal_matrix(self.matrix), "Illegal Matrix !"

    def align(self, seq1, seq2, gap=-8, mode='global'):
        '''Do the alignment'''
        if not hasattr(self, 'matrix'):
            self.matrix = self.defaultMatrix

        assert self.is_legal_matrix(self.matrix), "Illegal Matrix !"

        self.seq1 = seq1
        self.seq2 = seq2
        self.gap = gap

        if mode == 'global':
            self.needleman_Wunsch()
            alig = self.S[len(seq1)][len(seq2)], self.recover_align_global()
        elif mode == 'local':
            alig = self.smith_Waterman(), self.recover_align_local()
        else:
            alig = None

        return alig

    def look_alignment(self, alignment, start=None, end=None):
        '''Access the detailed result of the alignment'''
        sub_seq_a = alignment[0][start:end]
        sub_seq_b = alignment[1][start:end]
        return "%s\n%s\n%s" % (sub_seq_a, "|"*len(sub_seq_b), sub_seq_b)


class MultipleAlignment():
    def __init__(self , seqs, alignseq):
        assert isinstance(seqs, list), "seqs should be a list"
        assert isinstance(alignseq, PairWiseAligner), "alignseq should be a PairWiseAligner"
        self.seqs = seqs
        self.alignpars = alignseq

    def add_seq_alignment (self, alignment, seq):
        res = []
        for i in range(len(alignment.listseqs)+1):
            res.append("")

        cons = alignment.consensus() # !

        new_score, align2 = self.alignpars.align(cons, seq, mode='global')

        print("Score:", new_score)
        print(self.alignpars.look_alignment(align2))
        print("AlignScore", self.score_align(align2), "\n")

        orig = 0
        for i in range(len(align2)):
            if align2[0, i] == self.alignpars.gapSymbol:
                for k in range(len(alignment.listseqs)):
                    res[k] += self.alignpars.gapSymbol
            else:
                for k in range(len(alignment.listseqs)):
                    res[k] += alignment[k,orig]
                orig +=1
        res[len(alignment.listseqs)] = align2.listseqs[1]
        return MyAlign(res)

    def align_consensus(self):
        score, alignment = self.alignpars.align(self.seqs[0], self.seqs[1], mode='global')

        print("Score:", score)
        print(self.alignpars.look_alignment(alignment))
        print("AlignScore", self.score_align(alignment), "\n")

        for i in range(2, len(self.seqs)):
            alignment = self.add_seq_alignment(alignment, self.seqs[i])
        return alignment

    def score_align(self, alignment):
        res = 0;
        for i in range(len(alignment[0])):
            res += self.alignpars.score_pos(alignment[0][i], alignment[1][i])
        return res



if __name__ == "__main__":
    # '''
    seq1 = "ATAGC"
    seq2 = "AACC"
    seq3 = "ATGAC"
    seq4 = "ATAAC"
    pwA = PairWiseAligner()

    for i in "ATCG":
        for j in "ATCG":
            if j == i:
                pwA.new_matrix((i, j), 1)
            else:
                pwA.new_matrix((i, j), -1)

    msA = MultipleAlignment([seq1, seq2, seq3, seq4], pwA)
    al = msA.align_consensus()
    print(al)
    # '''

    '''
    seq1 = "PHSWGPHSWG"
    seq2 = "HGWAGPHSWG"
    pwA = PairWiseAligner()
    alignment = pwA.align(seq1, seq2, mode='global')
    print(pwA)
    print("Score:", alignment[0])
    print(pwA.look_alignment(alignment[1]))
    res = 0;
    for i in range(len(seq1)):
        res += pwA.score_pos(alignment[1][0][i], alignment[1][1][i])
    print("AlignScore:", res)
    '''
