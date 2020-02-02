# @Created Date: 2020-02-02 04:22:28 pm
# @Filename: ShannonEntropyWeight.py
# @Email:  1730416009@stu.suda.edu.cn
# @Author: ZeFeng Zhu
# @Last Modified: 2020-02-02 04:23:12 pm
import pandas as pd
import numpy as np
import click, os


def nonNegative(dfrm: pd.core.frame.DataFrame):
    minOb = dfrm.min().min()
    if minOb >= 0:
        return dfrm
    else:
        return dfrm - minOb


def translation(dfrm: pd.core.frame.DataFrame, mod='greater'):
    def greater(x, maxOb, minOb):
        return (x-minOb)/(maxOb-minOb)+1

    def smaller(x, maxOb, minOb):
        return (maxOb-x)/(maxOb-minOb)+1

    if mod == 'greater':
        func = greater
    elif mod == 'smaller':
        func = smaller
    else:
        raise ValueError("mod should either be 'greater' or 'smaller'")

    for col in dfrm:
        cur = dfrm[col]
        maxOb = cur.max()
        minOb = cur.min()
        dfrm[col] = cur.apply(lambda x: func(x, maxOb, minOb))

    return dfrm


def getPossibilities(dfrm: pd.core.frame.DataFrame):
    for col in dfrm:
        cur = dfrm[col]
        sumOb = cur.sum()
        dfrm[col] = cur.apply(lambda x: x/sumOb)
    return dfrm


def getEntropy(dfrm: pd.core.frame.DataFrame):
    entropy = []
    for col in dfrm:
        cur = dfrm[col]
        k = 1/np.log(len(cur))
        dfrm[col] = cur.apply(lambda x: -x*np.log(x))
        entropy.append(k*dfrm[col].sum())
    return dfrm, np.array(entropy)


def getCV(entropy: np.ndarray):
    '''Get Coefficient Of Variation'''
    return 1 - entropy


def getWeight(cv: np.ndarray):
    return cv/cv.sum()


def getScore(dfrm: pd.core.frame.DataFrame, weight: np.ndarray, scoreColName='score'):
    dfrm[scoreColName] = dfrm.apply(lambda x: np.dot(weight, x), axis=1)
    return dfrm
    

@click.command()
@click.option('--inFile', help='File Path of Input File', type=str)
@click.option('--sep', default=',', help='Separator of File', type=str)
@click.option('--suffix', default='csv', type=str)
@click.option('--indexCol', default='index', help='Index Col Name', type=str)
@click.option('--outFolder', help='Folder of Output Files', type=str)
@click.option('--translationMod', default=None, type=str)
def main(infile, outfolder, sep, indexcol, suffix, translationmod):
    dfrm = pd.read_csv(infile, sep=sep, index_col=indexcol)
    dfrm = nonNegative(dfrm)
    if translationmod is not None:
        translation(dfrm, mod=translationmod)
    possibi = getPossibilities(dfrm).copy()
    _, entropy = getEntropy(dfrm)
    dfrm.to_csv(os.path.join(outfolder, f'entropyDfrm.{suffix}'), sep=sep)
    weight = getWeight(getCV(entropy))
    click.echo(f'Weight: {weight}')
    getScore(possibi, weight)
    possibi.to_csv(os.path.join(outfolder, f'possibiDfrm.{suffix}'), sep=sep)


if __name__ == '__main__':
    main()
