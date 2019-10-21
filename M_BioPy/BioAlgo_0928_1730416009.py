# @Date:   2019-09-28T15:43:04+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioAlgo_0928_1730416009.py
# @Last modified time: 2019-10-21T14:32:51+08:00
# from functools import singledispatch


class MySeq:
    """ Class for biological sequences. """

    def __init__(self, seq, seq_type="DNA"):
        self.seq = seq.upper()
        self.seq_type = seq_type
        # self.validate()

    def __len__(self):
        return len(self.seq)

    def __getitem__(self, n):
        return self.seq[n]

    def __getslice__(self, i, j):
        return self.seq[i:j]

    def __str__(self):
        return self.seq

    def __repr__(self):
        return "MySeq(Sequence: %s, Biotype: %s)" % (self.seq, self.seq_type)

    def get_seq_biotype(self):
        return self.seq_type

    def alphabet(self):
        if self.seq_type == "DNA":
            return "ACGT"
        elif self.seq_type == "RNA":
            return "ACGU"
        elif self.seq_type == "PROTEIN":
            return "ACDEFGHIKLMNPQRSTVWY"
        else:
            return None

    def validate(self):
        alp = self.alphabet()
        res = True
        i = 0
        while i < len(self.seq) and res:
            if self.seq[i] not in alp:
                res = False
            else:
                i += 1
        return res


class MyAlign:
    def __init__(self, lseqs, gapSymbol="-"):
        self.listseqs = lseqs
        self.gapSymbol = gapSymbol

    def __len__(self):  # number of columns
        return len(self.listseqs[0])

    def __getitem__(self, n):
        if type(n) is tuple and len(n) == 2:
            i, j = n
            return self.listseqs[i][j]
        elif type(n) is int:
            return self.listseqs[n]
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
            res.append(self.listseqs[k][indice])
        return res

    def consensus(self):
        '''
        Get the sequence composed of that most frequent character
        * With equal frequence, select the first one
        '''
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


class PairwiseAlignment:
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
        for j in range(1, len(self.seq2) + 1):
            self.S[0].append(self.gap * j)
            self.T[0].append(3)
        # initialize gaps'column
        for i in range(1, len(self.seq1) + 1):
            self.S.append([self.gap * i])
            self.T.append([2])
        # apply the recurrence relation to fill the remaining of the matrix
        for i in range(len(self.seq1)):
            for j in range(len(self.seq2)):
                s1 = self.S[i][j] + self.score_pos(self.seq1[i], self.seq2[j])
                s2 = self.S[i][j + 1] + self.gap
                s3 = self.S[i + 1][j] + self.gap
                self.S[i + 1].append(max(s1, s2, s3))
                self.T[i + 1].append(PairwiseAlignment.max3t(s1, s2, s3))

    def smith_Waterman(self):
        '''
        Local Alignment
        * Dynamic Programming
        * optimized
        '''
        self.S = [[0]]  # Record the score
        self.T = [[0]]  # Record the orientation
        maxscore = 0
        for j in range(1, len(self.seq2) + 1):
            self.S[0].append(0)
            self.T[0].append(0)
        for i in range(1, len(self.seq1) + 1):
            self.S.append([0])
            self.T.append([0])
        for i in range(0, len(self.seq1)):
            for j in range(len(self.seq2)):
                s1 = self.S[i][j] + self.score_pos(self.seq1[i], self.seq2[j])
                s2 = self.S[i][j + 1] + self.gap
                s3 = self.S[i + 1][j] + self.gap
                b = max(s1, s2, s3)
                if b <= 0:
                    self.S[i + 1].append(0)
                    self.T[i + 1].append(0)
                else:
                    self.S[i + 1].append(b)
                    self.T[i + 1].append(PairwiseAlignment.max3t(s1, s2, s3))
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
                res[0] = self.seq1[i - 1] + res[0]
                res[1] = self.seq2[j - 1] + res[1]
                i -= 1
                j -= 1
            elif self.T[i][j] == 3:
                res[0] = self.gapSymbol + res[0]
                res[1] = self.seq2[j - 1] + res[1]
                j -= 1
            else:
                res[0] = self.seq1[i - 1] + res[0]
                res[1] = self.gapSymbol + res[1]
                i -= 1
        return MyAlign(res)

    def recover_align_local(self):
        '''Get the content of local alignment'''
        res = ["", ""]
        i, j = PairwiseAlignment.max_mat(self.S)
        while self.T[i][j] > 0:
            if self.T[i][j] == 1:
                res[0] = self.seq1[i - 1] + res[0]
                res[1] = self.seq2[j - 1] + res[1]
                i -= 1
                j -= 1
            elif self.T[i][j] == 3:
                res[0] = self.gapSymbol + res[0]
                res[1] = self.seq2[j - 1] + res[1]
                j -= 1
            elif self.T[i][j] == 2:
                res[0] = self.seq1[i - 1] + res[0]
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
        return "%s\n%s\n%s" % (sub_seq_a, "|" * len(sub_seq_b), sub_seq_b)


class MultipleAlignment:
    def __init__(self, seqs, alignseq):
        assert isinstance(seqs, list), "seqs should be a list"
        assert isinstance(
            alignseq, PairwiseAlignment), "alignseq should be a PairwiseAlignment"
        self.seqs = seqs
        self.alignpars = alignseq

    def add_seq_alignment(self, alignment, seq):
        res = []
        for i in range(len(alignment.listseqs) + 1):
            res.append("")

        cons = alignment.consensus()

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
                    res[k] += alignment[k, orig]
                orig += 1
        res[len(alignment.listseqs)] = align2.listseqs[1]
        return MyAlign(res)

    def align_consensus(self):
        score, alignment = self.alignpars.align(
            self.seqs[0], self.seqs[1], mode='global')

        print("Score:", score)
        print(self.alignpars.look_alignment(alignment))
        print("AlignScore", self.score_align(alignment), "\n")

        for i in range(2, len(self.seqs)):
            alignment = self.add_seq_alignment(alignment, self.seqs[i])
        return alignment

    def score_align(self, alignment):
        res = 0
        for i in range(len(alignment[0])):
            res += self.alignpars.score_pos(alignment[0][i], alignment[1][i])
        return res


class BinaryTree:
    def __init__(self, val, dist=0, left=None, right=None):
        self.value = val
        self.distance = dist
        self.left = left
        self.right = right

    def print_tree(self):
        # return str(self.print_tree_rec(0, "Root"))
        self.print_tree_rec(0, "Root")

    def print_tree_rec(self, level, side):
        tabs = ""
        for i in range(level):
            tabs += "\t"
        if self.value >= 0:
            # return tabs, side, " − value:", self.value
            print(tabs, side, " - value:", self.value)
        else:
            print(tabs, side, "- Dist.: ", self.distance)
            if self.left is not None:
                self.left.print_tree_rec(level + 1, "Left")
            if self.right is not None:
                self.right.print_tree_rec(level + 1, "Right")

            # return tabs, side, "− Dist.: ", self.distance

    def get_cluster(self):
        res = []
        if self.value >= 0:
            res.append(self .value)
        else:
            if self.left is not None:
                res.extend(self.left.get_cluster())
            if self.right is not None:
                res.extend(self.right.get_cluster())
        return res


class NumMatrix:
    def __init__(self, rows, cols):
        self.mat = []
        for i in range(rows):
            self.mat.append([])
            for j in range(cols):
                self.mat[i].append(0.0)

    def __getitem__(self, n):
        return self.mat[n]

    def num_rows(self):
        return len(self.mat)

    def num_cols(self):
        return len(self.mat[0])

    def get_value(self, i, j):
        if i > j:
            return self.mat[i][j]
        else:
            return self.mat[j][i]

    def set_value(self, i, j, value):
        if i > j:
            self.mat[i][j] = value
        else:
            self.mat[j][i] = value

    def print_mat(self):
        for r in self.mat:
            print(r)
        print()

    def min_dist_indexes(self):
        m = self.mat[1][0]
        res = (1, 0)
        for i in range(1, self.num_rows()):
            for j in range(i):
                if self.mat[i][j] < m:
                    m = self.mat[i][j]
                    res = (i, j)
        return res

    def add_row(self, newrow):
        self.mat.append(newrow)

    def add_col(self, newcol):
        for r in range(self .num_rows()):
            self.mat[r].append(newcol[r])

    def remove_row(self, ind):
        del self.mat[ind]

    def remove_col(self, ind):
        for r in range(self .num_rows()):
            del self.mat[r][ind]

    def copy(self):
        newm = NumMatrix(self.num_rows(), self.num_cols())
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                newm.mat[i][j] = self.mat[i][j]
        return newm


class HierarchicalClustering:
    def __init__(self, matdists):
        self.matdists = matdists

    def execute_clustering(self):
        # initialization of the tree leaves and matrix
        trees = []
        for i in range(self .matdists.num_rows()):
            t = BinaryTree(i)
            trees.append(t)
        tableDist = self.matdists.copy()
        # iterations
        for k in range(self.matdists.num_rows(), 1, -1):
            mins = tableDist.min_dist_indexes()  # minimum distance in D
            i, j = mins[0], mins[1]
            # create new tree joining clusters
            n = BinaryTree(-1, tableDist.get_value(i, j) /
                           2.0, trees[i], trees[j])
            if k > 2:
                # remove trees being joined from the list
                ti = trees.pop(i)
                tj = trees.pop(j)
                # calculating distances for new cluster
                dists = []
                for x in range(tableDist.num_rows()):
                    if x != i and x != j:
                        si = len(ti.get_cluster())
                        sj = len(tj.get_cluster())
                        d = (si * tableDist.get_value(i, x) + sj *
                             tableDist.get_value(j, x)) / (si + sj)
                        dists.append(d)
                # updating the matrix
                tableDist.remove_row(i)
                tableDist.remove_row(j)
                tableDist.remove_col(i)
                tableDist.remove_col(j)
                tableDist.add_row(dists)
                tableDist.add_col([0] * (len(dists) + 1))
                # add the new tree to the set to handle
                trees.append(n)
            else:
                return n


class UPGMA:
    def __init__(self, seqs, alseq=None):
        self.seqs = seqs
        self.alseq = alseq
        if self.checkSeqs():
            self.create_mat_dist()
        else:
            self.aln_create_mat_dist()

    '''
    @singledispatch
    def select_type(obj):
        print("UPGMA: Receive %s" % (type(obj)))
    '''

    def checkSeqs(self):
        if self.alseq is not None:
            return True
        for seq in self.seqs:
            if "-" in seq:
                return False
        return True

    # @select_type.register(MySeq)
    def create_mat_dist(self):
        self.matdist = NumMatrix(len(self.seqs), len(self.seqs))
        for i in range(len(self.seqs)):
            for j in range(i + 1, len(self.seqs)):
                s1 = self.seqs[i]
                s2 = self.seqs[j]
                _, alin = self.alseq.align(s1, s2, mode="global")
                print(alin, i, j, "\n")
                ncd = 0
                for k in range(len(alin)):
                    col = alin.column(k)
                    if (col[0] != col[1]):
                        ncd += 1
                self.matdist.set_value(i, j, ncd)

    def aln_create_mat_dist(self):
        self.matdist = NumMatrix(len(self.seqs), len(self.seqs))
        for i in range(len(self.seqs)):
            for j in range(i + 1, len(self.seqs)):
                s1 = self.seqs[i]
                s2 = self.seqs[j]
                alin = MyAlign([s1, s2])
                print(alin, i, j, "\n")
                ncd = 0
                for k in range(len(alin)):
                    col = alin.column(k)
                    if (col[0] != col[1]):
                        ncd += 1
                self.matdist.set_value(i, j, ncd)

    def run(self):
        ch = HierarchicalClustering(self.matdist)
        t = ch.execute_clustering()
        return t


def newMatrix(pwA, alphabet):
    for i in alphabet:
        for j in alphabet:
            if j == i:
                pwA.new_matrix((i, j), 1)
            else:
                pwA.new_matrix((i, j), -1)


def test_MSA():
    seq1 = "ATAGC"
    seq2 = "AAGC"
    seq3 = "ATGAC"
    # seq4 = "ATAAC"
    pwA = PairwiseAlignment()
    # '''
    for i in "ATCG":
        for j in "ATCG":
            if j == i:
                pwA.new_matrix((i, j), 1)
            else:
                pwA.new_matrix((i, j), -1)
    # '''
    msA = MultipleAlignment([seq1, seq2, seq3], pwA)
    al = msA.align_consensus()
    print(al)


def test_PWA():
    seq1 = "PHSWGPHSWG"
    seq2 = "HGWAGPHSWG"
    pwA = PairwiseAlignment()
    alignment = pwA.align(seq1, seq2, mode='global')
    print(pwA)
    print("Score:", alignment[0])
    print(pwA.look_alignment(alignment[1]))
    res = 0
    for i in range(len(seq1)):
        res += pwA.score_pos(alignment[1][0][i], alignment[1][1][i])
    print("AlignScore:", res)


def test_bt():
    a = BinaryTree(1)
    b = BinaryTree(2)
    c = BinaryTree(3)
    d = BinaryTree(4)
    e = BinaryTree(-1, 2.0, b, c)
    f = BinaryTree(-1, 1.5, d, a)
    g = BinaryTree(-1, 4.5, e, f)
    g.print_tree()
    print(f.get_cluster())
    print(g.get_cluster())


def test_UPGMA_1():
    seqType = "DNA"
    seq_li = ["ATAGCGAT", "ATAGGCCT", "CTAGGCCC", "CTAGGCCT"]
    # seq_li = ["ACATATCAT", "AGATATTAG", "AACAGATCT", "GCATCGATT"]
    seq_li = [MySeq(i, seqType) for i in seq_li]
    alseq = PairwiseAlignment()
    newMatrix(alseq, "ATCG")
    up = UPGMA(seq_li, alseq)
    arv = up.run()
    arv.print_tree()


def test_UPGMA_2():
    # from itertools import combinations
    seq_li = ["A-CATATC-AT-", "A-GATATT-AG-", "AACAGATC-T--", "G-CAT--CGATT"]
    # aln_li = [MyAlign(lseqs) for lseqs in combinations(seq_li, 2)]
    up = UPGMA(seq_li)
    arv = up.run()
    arv.print_tree()


if __name__ == "__main__":
    # test_PWA()
    # test_MSA()
    test_UPGMA_2()
