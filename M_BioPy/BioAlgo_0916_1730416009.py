# @Date:   2019-09-16T15:54:12+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioAlgo_0916_1730416009.py
# @Last modified time: 2019-09-22T01:36:55+08:00
import re
from Bio import Seq
from Bio.Alphabet import IUPAC
from Bio.Data.CodonTable import TranslationError

'''
Write and test a Python function that, given a DNA sequence,
returns the size of the first protein that can be encoded by
that sequence (in any of the three reading frames). The
function should return −1 if no protein is found.
'''


def translateIO(dnaSeq, startPattern='(?=M.+)'):
    pattern = re.compile(startPattern)
    subDnaSeq = (dnaSeq[i:] for i in range(0, 3))
    result_li = []
    proteinSeq_li = []
    for sub in subDnaSeq:
        try:
            dnaOb = Seq.Seq(sub, IUPAC.unambiguous_dna)
            proteinOb = dnaOb.translate()
        except TranslationError as e:
            print("Invalid DNA Sequence! [From Biopython]:", e)
            return proteinSeq_li, result_li

        proteinSeq = str(proteinOb[:])
        proteinSeq_li.append(proteinSeq)
        # result_li.append(pattern.findall(proteinSeq))
        result_li.append([i.span()[0] for i in pattern.finditer(proteinSeq)])

    return proteinSeq_li, result_li


def getProteinSizeFromDNA(dnaSeq, mode=1):
    proteinSeq_li, index_li = translateIO(dnaSeq)
    print(proteinSeq_li, index_li)
    re_li = []
    if mode == 1:
        for i in range(3):
            try:
                re_li.append(len(proteinSeq_li[i]) - index_li[i][0])
            except IndexError:
                re_li.append(-1)
        return re_li
    else:
        for i in range(3):
            re_li.append([len(proteinSeq_li[i]) - index_li[i][j] for j in range(len(index_li[i]))])
        return list(map(lambda x: x if x else -1, re_li))


if __name__ == '__main__':
    print(getProteinSizeFromDNA('ATGATCTTATGTAATGTCTTATTTATGGTC', mode=1))
    print(getProteinSizeFromDNA('ATGATCTTATGTAATGTCTTATTTATGGTC', mode=2))
    print(getProteinSizeFromDNA('ATCTTTATCTTATTTGTCTAATAGTGA', mode=1))
    print(getProteinSizeFromDNA('ATCTTTATCTTATTTGTC', mode=1))
