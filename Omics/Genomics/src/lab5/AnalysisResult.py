import argparse
from sklearn import metrics
import numpy as np
import os
import pandas as pd
from seaborn import set_style
import matplotlib.pyplot as plt
set_style("darkgrid")

default_cols = ['seqid', 'source', 'type', 'start',
                'end', 'score', 'strand', 'phase', 'attributes']


def plotSiteScore(dfrm, chrosLyst, folder):
    plt.figure(figsize=(18, 8))
    for chro in chrosLyst:
        chr_c = dfrm[dfrm['seqid'] == chro]
        # plt.scatter(chr_c['start'], chr_c['score'], label=chro, s=chr_c['pValue']*30, marker='o', alpha=0.5)
        plt.plot(chr_c['start'], chr_c['score'], label=chro, alpha=0.5)
        print(chr_c['score'].describe())
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(folder, "siteScore.png"))


def plotROC(dfrm, folder):
    plt.figure(figsize=(14, 8))
    fpr, tpr, threshold = metrics.roc_curve(dfrm['HMM_label'], dfrm['score'])
    roc_auc = metrics.auc(fpr, tpr)
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig(os.path.join(folder, "ROC.png"))
    return fpr, tpr, threshold, roc_auc


def getYN(site, index, exonLyst, cutoff=100):
    lyst = exonLyst[index]
    for i in lyst:
        if i - site < cutoff:
            return True
    return False


def labelHMM(dfrm, chrosLyst, exonLyst, colName="HMM_label"):
    dfrm[colName] = np.nan
    for index, chro in enumerate(chrosLyst):
        chr_c = dfrm[dfrm['seqid'] == chro].index
        dfrm.loc[chr_c, "HMM_label"] = dfrm.loc[chr_c, ].apply(
            lambda x: getYN(x["start"], index, exonLyst), axis=1)


def main(gffPath, referPath, outputFolder, strand):
    df = pd.read_csv(gffPath, sep="\t", skiprows=1, names=default_cols)
    chrosLyst = df['seqid'].drop_duplicates().to_list()

    plotSiteScore(df, chrosLyst, outputFolder)

    gff = pd.read_csv(referPath, sep="\t", skiprows=7, names=default_cols)
    gff.dropna(inplace=True)
    
    chromIndex = gff[gff["type"] == "region"].index.to_list()
    chromInterval = [chromIndex[i:i+2] for i in range(len(chromIndex)-2)]
    chromInterval = [[i[0], i[1]-1] for i in chromInterval]
    chromInterval.append([chromInterval[-1][1]+1, None])
    
    exonLyst = []
    for interval in chromInterval:
        temp_df = gff.loc[interval[0]:interval[1]]
        exonStart = temp_df[(temp_df['type'] == 'gene') & (temp_df['strand'] == strand)]['start'].to_list()
        exonLyst.append(exonStart)
    
    labelHMM(df, chrosLyst, exonLyst)
    # fpr, tpr, threshold, roc_auc = 
    plotROC(df, outputFolder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Analysis the result of HMM Promoter Prediction')
    parser.add_argument('-i', '--gffFile', type=str)
    parser.add_argument('-r', '--referenceGff', type=str)
    parser.add_argument('-o', '--outputFolder', type=str)
    parser.add_argument('-s', '--strand', type=str, default='+')
    args = parser.parse_args()
    main(args.gffFile, args.referenceGff, args.outputFolder, args.strand)

