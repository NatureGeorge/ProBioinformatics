# @Date:   2019-11-19T15:08:04+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: ExtractSequence.py
# @Last modified time: 2019-11-19T17:27:45+08:00
import re
from collections import Iterable, Iterator


def ExtractSeqFromGFF(text, startwith=r"# protein sequence = \[([A-z]+)", content="# ([A-z]+)", endwith="end gene ([a-z0-9]+)"):
    # endwith="end gene ([a-z0-9]+)"
    startwith = re.compile(startwith)
    content = re.compile(content)
    endwith = re.compile(endwith)
    flag, seq, seqDict = 0, "", {}

    for line in text:
        startToken = startwith.findall(line)
        if startToken:
            flag = 1
            seq += startToken[0]
            continue
        if flag:
            endToken = endwith.findall(line)
            if endToken:
                seqDict[endToken[0]] = seq
                flag, seq = 0, ""
                continue
            seq += content.findall(line)[0]

    for key, value in seqDict.items():
        print("{key}:{value}".format(key=key, value=value))


def ExtractSeqFromGFF2(text, startwith=r"# protein sequence = \[([A-z]+)", content="# ([A-z]+)", endwith=r"([A-z]+)]", endKey="end gene ([A-z0-9]+)"):
    assert isinstance(text, (Iterable, Iterator)), "Invalid Object"

    startwith, content, endwith, endKey = (re.compile(i) for i in (startwith, content, endwith, endKey))
    flag, endToken, seq, seqDict = 0, 0, "", {}

    for line in text:
        startToken = startwith.findall(line)
        if startToken:
            flag = 1
            seq += startToken[0]
            # continue
        if flag:
            endToken = endwith.findall(line)
            if endToken:
                flag = 0
            if not startToken:
                seq += content.findall(line)[0]
        elif endToken:
            key = endKey.findall(line)
            if key:
                seqDict[key[0]] = seq
                endToken, seq = 0, ""
    # """
    for key, value in seqDict.items():
        print("{key}:{value}".format(key=key, value=value))
    # """
    # return seqDict


def ExtractSeqFromGFF3(text, startwith=r"# protein sequence = \[([A-z]+)", content="# ([A-z]+)", endwith="([A-z]+)]", endKey="end gene ([A-z0-9]+)"):
    assert isinstance(text, (Iterable, Iterator)), "Invalid Object"

    startwith, content, endwith, endKey = (re.compile(i) for i in (startwith, content, endwith, endKey))
    flag, endToken, seq = 0, 0, ""

    for line in text:
        startToken = startwith.findall(line)
        if startToken:
            flag = 1
            seq += startToken[0]
        if flag:
            endToken = endwith.findall(line)
            if endToken:
                flag = 0
            if not startToken:
                seq += content.findall(line)[0]
        elif endToken:
            key = endKey.findall(line)
            if key:
                yield key[0], seq
                endToken, seq = 0, ""


def toFASTA(name, seq):
    return ">{name}\n{seq}\n".format(name=name, seq=seq)


def script(inPath, outPath):
    with open(inPath, "rt") as inFile:
        with open(outPath, "wt") as outFile:
            g = ExtractSeqFromGFF3(inFile, startwith=r"# coding sequence = \[([a-z]+)")
            for name, seq in g:
                outFile.write(toFASTA(name, seq[:-1]))


if __name__ == "__main__":
    text1 = """
    # coding sequence = [atgtctagattagaaagattgacctcattaaacgttgttgctggttctgacttgagaagaacctccatcattggtacca
    # tcggtccaaagaccaacaacccagaaaccttggttgctttgagaaaggctggtttgaacattgtccgtatgaacttctctcacggttcttacgaatac
    # cacaagtctgtcattgacaacgccagaaagtccgaagaattgtacccaggtagaccattggccattgctttggacaccaagggtccagaaatcagaac
    # tggtaccaccaccaacgatgttgactacccaatcccaccaaaccacgaaatgatcttcaccaccgatgacaagtacgctaaggcttgtgacgacaaga
    # tcatgtacgttgactacaagaacatcaccaaggtcatctccgctggtagaatcatctacgttgatgatggtgttttgtctttccaagttttggaagtc
    # gttgacgacaagactttgaaggtcaaggctttgaacgccggtaagatctgttcccacaagggtgtcaacttaccaggtaccgatgtcgatttgccagc
    # tttgtctgaaaaggacaaggaagatttgagattcggtgtcaagaacggtgtccacatggtcttcgcttctttcatcagaaccgctaacgatgttttga
    # ccatcagagaagtcttgggtgaacaaggtaaggacgtcaagatcattgtcaagattgaaaaccaacaaggtgttaacaacttcgacgaaatcttgaag
    # gtcactgacggtgttatggttgccagaggtgacttgggtattgaaatcccagccccagaagtcttggctgtccaaaagaaattgattgctaagtctaa
    # cttggctggtaagccagttatctgtgctacccaaatgttggaatccatgacttacaacccaagaccaaccagagctgaagtttccgatgtcggtaacg
    # ctatcttggatggcgctgactgtgttatgttgtctggtgaaaccgccaagggtaactacccaatcaacgccgttaccactatggctgaaaccgctgtc
    # attgctgaacaagctatcgcttacttgccaaactacgatgacatgagaaactgtactccaaagccaacctccaccaccgaaaccgtcgctgcctccgc
    # tgtcgctgctgttttcgaacaaaaggccaaggctatcattgtcttgtccacttccggtaccaccccaagattggtttccaagtacagaccaaactgtc
    # caatcatcttggttaccagatgcccaagagctgctagattctctcacttgtacagaggtgtcttcccattcgttttcgaaaaggaacctgtctctgac
    # tggactgatgatgttgaagcccgtatcaacttcggtattgaaaaggctaaggaattcggtatcttgaagaagggtgacacttacgtttccatccaagg
    # tttcaaggccggtgctggtcactccaacactttgcaagtctctaccgtttaa]
    # protein sequence = [MSRLERLTSLNVVAGSDLRRTSIIGTIGPKTNNPETLVALRKAGLNIVRMNFSHGSYEYHKSVIDNARKSEELYPGRP
    # LAIALDTKGPEIRTGTTTNDVDYPIPPNHEMIFTTDDKYAKACDDKIMYVDYKNITKVISAGRIIYVDDGVLSFQVLEVVDDKTLKVKALNAGKICSH
    # KGVNLPGTDVDLPALSEKDKEDLRFGVKNGVHMVFASFIRTANDVLTIREVLGEQGKDVKIIVKIENQQGVNNFDEILKVTDGVMVARGDLGIEIPAP
    # EVLAVQKKLIAKSNLAGKPVICATQMLESMTYNPRPTRAEVSDVGNAILDGADCVMLSGETAKGNYPINAVTTMAETAVIAEQAIAYLPNYDDMRNCT
    # PKPTSTTETVAASAVAAVFEQKAKAIIVLSTSGTTPRLVSKYRPNCPIILVTRCPRAARFSHLYRGVFPFVFEKEPVSDWTDDVEARINFGIEKAKEF
    # GILKKGDTYVSIQGFKAGAGHSNTLQVSTV]
    # end gene g25
    ###
    # coding sequence = [atggctatcacccctgacaaacagaagaaagaacaacagcatcaaccacagaacggaccgctcgactatgctcacatat
    # gcaagtgtattgcaatgttctttgtcgttgcgggcgtggtgctgatgttcttcgagaccgggttggacccagaacaaaaagagcaaatcaagcgtctc
    # caccagttggacggcattcctcacgcttga]
    # protein sequence = [MAITPDKQKKEQQHQPQNGPLDYAHICKCIAMFFVVAGVVLMFFETGLDPEQKEQIKRLHQLDGIPHA]
    # end gene g292
    ###
    """.split("\n")

    # text2 = open(r"C:\OmicData\YJM1342\YJM1342_augustus\augustus.gff", "rt")

    # ExtractSeqFromGFF2(text1)
    # ExtractSeqFromGFF2(text1, startwith=r"# coding sequence = \[([a-z]+)")

    '''
    g = ExtractSeqFromGFF3(text2)
    count = 0
    for key, value in g:
        print("{key}:{value}".format(key=key, value=value))
        count += 1
        if count > 10:
            break
    text2.close()
    '''

    script(r"C:\OmicData\YJM1342\YJM1342_augustus\augustus.gff", r"C:\OmicData\YJM1342\YJM1342_augustus\augustus_gene.fasta")
