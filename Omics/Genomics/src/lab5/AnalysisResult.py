import argparse
from sklearn import metrics
import numpy as np
import os
import pandas as pd
from seaborn import set_style
import matplotlib.pyplot as plt
set_style("darkgrid")

default_cols = ['seqid', 'source', 'type', 'start',
                'end', 'score', 'strand', 'phase', 'attributes', 'pValue']


def plotSiteScore(dfrm, chrosLyst, folder, strand):
    if len(dfrm) == 0:
        return None
    plt.figure(figsize=(18, 8))
    for chro in chrosLyst:
        chr_c = dfrm[dfrm['seqid'] == chro]
        # plt.scatter(chr_c['start'], chr_c['score'], label=chro, s=chr_c['pValue']*30, marker='o', alpha=0.5)
        plt.plot(chr_c['start'], chr_c['score'], label=chro, alpha=0.5)
        print(chr_c['score'].describe())
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(folder, "siteScore_%s.png" % strand))


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


def labelHMM(dfrm, strandID, chrosLyst, exonLyst):
    for index, chro in enumerate(chrosLyst):
        chr_c = dfrm[(dfrm['seqid'] == chro) & (dfrm['strand'] == strandID)].index
        dfrm.loc[chr_c, "HMM_label"] = dfrm.loc[chr_c, ].apply(
            lambda x: getYN(x["start"], index, exonLyst), axis=1)


def label(gffPath, referPath, outputFolder, strands):
    # Input GFF Lyst
    dfLyst = [pd.read_csv(path, sep="\t", skiprows=2, names=default_cols) for path in gffPath.split(",")]
    chrosLyst = dfLyst[0]['seqid'].drop_duplicates().to_list()
    # Refer GFF
    gff = pd.read_csv(referPath, sep="\t", skiprows=7, names=default_cols[:-1])
    gff.dropna(inplace=True)
    # Get Refer info according to chrmosome
    chromIndex = gff[gff["type"] == "region"].index.to_list()
    chromInterval = [chromIndex[i:i+2] for i in range(len(chromIndex)-1)]
    chromInterval = [[i[0], i[1]-1] for i in chromInterval]
    chromInterval.append([chromInterval[-1][1]+1, None])

    def labelStrand(dfrm, strand, label="HMM_label"):
        dfrm[label] = np.nan
        exonLyst = []
        for interval in chromInterval:
            temp_df = gff.loc[interval[0]:interval[1]]
            exonStart = temp_df[(temp_df['type'] == 'gene') & (
                temp_df['strand'] == strand)]['start'].to_list()
            exonLyst.append(exonStart)

        labelHMM(dfrm, strand, chrosLyst, exonLyst)


def main(gffPath, referPath, outputFolder, strand):
    df = pd.concat([pd.read_csv(path, sep="\t", skiprows=2, names=default_cols) for path in gffPath.split(",")])
    chrosLyst = df['seqid'].drop_duplicates().to_list()

    plotSiteScore(df[df['strand']=='+'], chrosLyst, outputFolder, "+")
    plotSiteScore(df[df['strand'] == '-'], chrosLyst, outputFolder, "-")

    gff = pd.read_csv(referPath, sep="\t", skiprows=7, names=default_cols[:-1])
    gff.dropna(inplace=True)
    
    chromIndex = gff[gff["type"] == "region"].index.to_list()
    chromInterval = [chromIndex[i:i+2] for i in range(len(chromIndex)-1)]
    chromInterval = [[i[0], i[1]-1] for i in chromInterval]
    chromInterval.append([chromInterval[-1][1]+1, None])
    
    df["HMM_label"] = np.nan

    for strandID in strand:
        exonLyst = []
        for interval in chromInterval:
            temp_df = gff.loc[interval[0]:interval[1]]
            exonStart = temp_df[(temp_df['type'] == 'gene') & (temp_df['strand']==strandID)]['start'].to_list()
            exonLyst.append(exonStart)
        
        labelHMM(df, strandID, chrosLyst, exonLyst)
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

