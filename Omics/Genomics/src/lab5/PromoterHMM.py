import argparse
from collections import defaultdict, Counter
import os
from numpy.random import shuffle
import pandas as pd
from tqdm import tqdm
from time import perf_counter
from scipy.special import comb


WEIGHTED = {
    "A": [-1.02, -3.05, 0.00, -4.61, 0.00, 0.00, 0.00, 0.00, -0.01, -0.94, -0.54, -0.48, -0.48, -0.74, -0.62],
    "C": [-0.28, -2.06, -5.22, -3.49, -5.17, -4.63, -4.12, -3.74, -1.13, -0.05, 0.00, -0.05, -0.11, -0.28, -0.40],
    "G": [0.00, -2.74, -4.28, -4.61, -3.77, -4.73, -2.65, -1.50, 0.00, 0.00, -0.09, 0.00, 0.00, 0.00, 0.00],
    "T": [-1.68, 0.00, -2.28, 0.00, -2.34, -0.52, -3.65, -0.37, -1.40, -0.97, -1.40, -0.82, -0.66, -0.54, -0.61]}

WEIGHT = {
    "A": [61, 16, 352, 3, 354, 268, 360, 222, 155, 56, 83, 82, 82, 68, 77],
    "C": [145, 46, 0, 10, 0, 0,	3, 2, 44, 135, 147, 127, 118, 107, 101],
    "G": [152, 18, 2, 2, 5, 0, 20, 44, 157,150, 128, 128, 128, 139, 140],
    "T": [31,309, 35, 374, 30, 121, 6, 121, 33, 48, 31, 52,	61,	75,	71]
    }

WEIGHT_HMM = {
    'A': [21.4, 15.9, 3.7, 91.1, 0.0, 94.5, 67.3, 97.3, 52.1, 40.7, 16.5, 23.6],
    'C': [22.7, 39.3, 9.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.1, 34.8, 37.1],
    'G': [28.2, 35.2, 2.9, 0.0, 0.0, 0.0, 0.0, 2.7, 12.0, 40.2, 38.0, 30.4],
    'T': [27.7, 9.6, 83.6, 8.9, 100.0, 5.5, 32.7, 0.0, 35.9, 10.0, 10.7, 8.9]
    }

WEIGHT = {key: [sv/100 for sv in value] for key, value in WEIGHT.items()}

DEFAULT_FILE = "C:/OmicData/YJM1342/GCA_000977265.3_Sc_YJM1342_v1_genomic.fna"

class HMMPredProm:

    def __init__(self, path, chroNum, length=12, weight=WEIGHT, bootstrapNum=70, pValue=0.05):
        if os.path.exists(path):
            self.path = path
        else:
            raise ValueError("Invalid File Path !")
        
        self.length = length
        self.weight = weight
        self.bootstrapNum = bootstrapNum
        self.pValue = pValue
        self.chroNum = chroNum

    @staticmethod
    def getFileRows(path):
        with open(path, 'rt') as file:
            rows = 0
            for line in file:
                rows += 1
        return rows

    @classmethod
    def seqIO(cls, path):
        name, seq = '', ''
        rows = cls.getFileRows(path)
        with open(path, 'rt') as seqFile:
            for index, line in enumerate(seqFile):
                if line.startswith(">"):
                    if index != 0:
                        yield name, seq
                        seq = ''
                    name = line[:-1]
                else:
                    seq += line[:-1].upper()
                    if index + 1 == rows:
                        yield name, seq

    def subSeq(self, str):
        for i in range(0, len(str)-self.length+1):
            yield i, str[i:i+self.length]

    def scoreSeq(self, seq, inb=False):
        score = 1
        for index, base in enumerate(seq):
            try:
                score *= self.weight[base][index]
            except KeyError:
                score = 0
                break
            except IndexError:
                print(seq, index, base)
                raise IndexError("Invalid length for inputed seq")
        
        if not inb:
            return score, self.bootstrapping(score, seq)
        else:
            return score

    @staticmethod
    def checkRunTime(start, cutoff=1):
        if perf_counter() - start >= cutoff:
            raise RuntimeError("Spend too much time !")

    def bootstrapping(self, score, seq):
        if score == 0:
            return None
        elif len(set(seq)) == 1:
            return 0
        else:
            pass

        recordDict = {}
        start = perf_counter()
        
        seq_len = len(seq)
        m = seq_len
        record, allPosNum = Counter(seq), 1
        for x in record.values():
            allPosNum *= comb(m, x)
            m -= x
        
        testNum = min(self.bootstrapNum, allPosNum)
        
        try:
            while len(recordDict) < testNum:
                seq_var = list(seq)
                self.seq = seq
                shuffle(seq_var)
                seq_var = ''.join(seq_var)
                if seq_var in recordDict.keys():
                    self.checkRunTime(start)
                    continue
                        
                recordDict[seq_var] = self.scoreSeq(seq_var, inb=True)
                self.checkRunTime(start)
        except RuntimeError:
            print("skip")
            pass
        
        count = 0
        for varScore in record.values():
            if varScore > score:
                count += 1
        
        return count/testNum

    def grouper(self, seq, dict, key):
        while True:
            subSeq = yield from self.subSeq(seq)
            dict[key].append(self.scoreSeq(subSeq))

    def main(self, reverse=False):
        '''
        for name, seq in seqs:
            group = self.grouper(seq, result, name)
            next(group)
            group.send(None)
        return result
        '''
        seqs = self.seqIO(self.path)
        result = defaultdict(list)
        for count, (name, seq) in enumerate(seqs):
            
            seq_len = len(seq)
            
            if reverse:
                seq = reverseCom(seq)
                def index_func(x): return seq_len - index
            else:
                def index_func(x): return x+1

            subSeqs = self.subSeq(seq)
            for index, sseq in tqdm(subSeqs, total=seq_len-self.length+1):
                sp = self.scoreSeq(sseq)
                if sp[1] is not None:
                    result[name].append((index_func(index), *sp))
            print(name)
            
            if count+1 == self.chroNum:
                break
        
        return result

    @staticmethod
    def filteringResult(pV, dict):
        return {chro: [(locus, score, pValue) for locus, score, pValue in value if pValue <= pV] for chro, value in dict.items()}
    
    def toDataFrame(self, dict, strand='+'):
        """convert the dict to a dataframe"""
        dfLyst = []
        allCols = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'pValue']
        for chro, data in dict.items():
            df = pd.DataFrame(data, columns=["start", "score", "pValue"])
            # df['attributes'] = df['pValue'].apply(lambda x: 'p-value={}'.format(x))
            df["seqid"] = ' '.join(chro[1:].split(' ')[0:1])
            df["strand"] = strand
            df["end"] = df["start"]+self.length-1
            for col in allCols:
                if col not in df.columns:
                    df[col] = '.'
            dfLyst.append(df)
        return pd.concat(dfLyst)[allCols]


completement = {"A": "T", "C":"G", "G": "C", "T": "A"}


def reverseCom(seq):
    reverse = seq[::-1]
    seq = ''.join(completement.get(i, i) for i in reverse)
    return seq



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HMM Prediction Result of Promoter')
    parser.add_argument('-f', '--fasta', type=str,
                        default=DEFAULT_FILE,
                        help='File path of fasta file; default = %s'
                        % DEFAULT_FILE)
    parser.add_argument('-b', '--bootstrapNum', type=int,
                        default=50,
                        help='Number of bootstrap test')
    parser.add_argument('-p', '--pValue', type=float,
                        default=0.05)
    parser.add_argument('-c', '--chroNum', type=int,
                        default=2)
    parser.add_argument('-o', '--outputFolder', type=str,
                        default='C:/OmicData/YJM1342/')
    parser.add_argument('-r', '--reverse', type=bool,
                        default=True)
    parser.add_argument('-t', '--tage', type=str,
                        default='')
    args = parser.parse_args()
    test = HMMPredProm(args.fasta, chroNum=args.chroNum, bootstrapNum=args.bootstrapNum, pValue=args.pValue)
    
    resultDict = test.filteringResult(test.pValue, test.main())
    fin = test.toDataFrame(resultDict)
    outputPath = os.path.join(args.outputFolder, "output_%s_%s.gff3" % (args.bootstrapNum, args.tage))
    
    with open(outputPath, 'w+') as out:
        out.write("##gff-version 3\n")
    fin.to_csv(outputPath, sep="\t", index=False, header=False, mode='a+')

    if args.reverse:
        resultDict = test.filteringResult(test.pValue, test.main(reverse=True))
        fin = test.toDataFrame(resultDict, '-')
        outputPath = os.path.join(args.outputFolder, "output_reverse_%s_%s.gff3" % (args.bootstrapNum, args.tage))

        with open(outputPath, 'w+') as out:
            out.write("##gff-version 3\n")
        fin.to_csv(outputPath, sep="\t", index=False, header=False, mode='a+')
    
    
