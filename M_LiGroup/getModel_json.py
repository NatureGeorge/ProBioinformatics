# @Date:   2019-03-25T11:16:59+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: FilterModel
# @Last modified time: 2019-03-26T18:00:31+08:00
# -*- coding:utf-8 -*-
import re
from urllib import request
from urllib import error
from time import sleep
import xlrd
import pandas as pd
import json


class ModelX:

    def __init__(self, model_id):
        self.model_id = model_id
        self.info_dict = {}
        self.status = 0

    def addData_SMR(self, info, residueData):
        # self.info = info
        self.info_dict['seq_len'] = int(info[2])
        self.info_dict['cov_from'] = int(info[6])
        self.info_dict['cov_to'] = int(info[7])
        self.info_dict['seq_id'] = info[11]  # e.g '80.4234'
        self.info_dict['cov_len'] = (
            self.info_dict['cov_to'] - self.info_dict['cov_from'] + 1)
        self.info_dict['coverage'] = (
            float(self.info_dict['cov_len']) / float(self.info_dict['seq_len'])
            )
        self.info_dict['url'] = info[12]
        self.info_dict['otherInfo'] = ('qmean:%s&qmean_norm:%s') % (info[9], info[10])
        self.rangeSet = residueData
        self.rangeInterval = getInterval(self.rangeSet)
        self.provider = 'SMR'

    def addData_ModB(self, info, residueData):
        self.provider = 'ModBase'
        self.rangeSet = residueData
        self.rangeInterval = getInterval(self.rangeSet)
        self.info_dict['otherInfo'] = {}
        info_list = info.split('\n')
        for i in info_list:
            ilist = i.split('   ')
            cutList = i[40:].split(' ')
            try:
                num = float(cutList[0])
            except Exception:
                num = cutList[0]
            index = ilist[0]
            # print('addData_ModB()')
            if index == 'REMARK 220 SEQUENCE IDENTITY:':
                self.info_dict['seq_id'] = num
            elif index == 'REMARK 220 MODEL SCORE:':
                self.info_dict['otherInfo']['MODEL_SCORE'] = num
            elif index == 'REMARK 220 ModPipe Quality Score:':
                self.info_dict['otherInfo']['ModPipe_Quality_Score'] = num
            elif index == 'REMARK 220 zDOPE:':
                self.info_dict['otherInfo']['zDOPE'] = num
            elif index == 'REMARK 220 EVALUE:':
                self.info_dict['otherInfo']['EVALUE'] = num
            elif index == 'REMARK 220 TARGET LENGTH:':
                self.info_dict['seq_len'] = int(num)
            elif index == 'REMARK 220 TARGET BEGIN:':
                self.info_dict['cov_from'] = int(num)
            elif index == 'REMARK 220 TARGET END:':
                self.info_dict['cov_to'] = int(num)
            elif index == 'REMARK 220 MODPIPE MODEL ID:':
                self.info_dict['url'] = ('modelID:%s') % (num)
        self.info_dict['cov_len'] = (
            self.info_dict['cov_to'] - self.info_dict['cov_from'] + 1)
        self.info_dict['coverage'] = (
            float(self.info_dict['cov_len']) / float(self.info_dict['seq_len'])
            )

    def addData_Exp(self, info):
        null = '\\'
        self.info_dict['seq_len'] = null
        self.info_dict['cov_from'] = int(info[2])
        self.info_dict['cov_to'] = int(info[3])
        self.info_dict['cov_len'] = int(info[4])
        self.info_dict['seq_id'] = null
        self.info_dict['coverage'] = null
        self.info_dict['url'] = null
        self.info_dict['otherInfo'] = ('mutationChain:%s') % (info[1])
        self.rangeSet = info[5]
        self.rangeInterval = getInterval(self.rangeSet)
        self.provider = 'PDB'

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getRangeSet(self):
        return self.rangeSet

    def setDeltaMutaList(self, deltaMuta_list):
        temp = list(deltaMuta_list)
        temp.sort()
        self.deltaMuta_list = temp

    def getDeltaMutaList(self):
        return self.deltaMuta_list

    def getRangeInterval(self):
        return self.rangeInterval


class RepresentX:
    def __init__(self, representSet):
        self.representSet = representSet

    def addModel(self, model):
        self.representSet.append(model)

    def getRepresentSet(self):
        return self.representSet

    def setRangeSet(self):
        first = True
        for i in self.representSet:
            if first:
                self.rangeSet = i.getRangeSet()
                first = False
            else:
                self.rangeSet = self.rangeSet | i.getRangeSet()

    def getRangeSet(self):
        return self.rangeSet


def downloadFun(blocknum, blocksize, totalsize):
    percent = blocknum*blocksize/totalsize
    if percent > 1.0:
        percent = 1.0
    percent = percent*100
    print("download : %.2f%%" % (percent))


def getInterval(rangeSet):
    start = []
    interval_list = []
    true_interval_list = []
    maxRange = max(rangeSet)
    minRange = min(rangeSet)
    if len(rangeSet) == (maxRange + 1 - minRange):
        true_interval_list.append([minRange, maxRange])
    else:
        rangeSet_list = list(rangeSet)
        rangeSet_list.sort()
        for j in rangeSet_list:
            if not start:
                i = j
                start.append(j)
                i += 1
            else:
                if (i != j) or (j == max(rangeSet_list)):
                    if j == max(rangeSet_list):
                        if (i != j):
                            interval_list.append(start)
                            interval_list.append([j])
                            break
                        else:
                            start.append(j)
                    interval_list.append(start)
                    start = [j]
                    i = j + 1
                else:
                    start.append(j)
                    i += 1
        for li in interval_list:
            maxRange = max(li)
            minRange = min(li)
            true_interval_list.append([minRange, maxRange])
    return true_interval_list


# file_in:list_enstRef-UniprotAC.tab
# 假设/前提：'ENST00000262304 -> P98161-1'为'一对一'对应或'多对一'对应,不存在'一对多'
def getTranslation(file_in):
    readbook = xlrd.open_workbook(file_in)
    sheet = readbook.sheet_by_index(0)
    translate_dict = {}
    for line in range(sheet.nrows):
        if line == 0:
            continue
        else:
            list_1 = sheet.cell(line, 0).value.split(',')
            list_2 = sheet.cell(line, 1).value.split(',')
            if list_2[0] == '':
                translate_dict[sheet.cell(line, 2).value] = list_1
            else:
                for i in list_2:
                    temp_list = i.split(' ')
                    translate_dict[temp_list[2]] = []
                for i in list_2:
                    temp_list = i.split(' ')  # 待优化.
                    translate_dict[temp_list[2]].append(temp_list[0])
    return translate_dict


def getTranslate_dict(enstFile, refFile):
    translate_dict = {}
    translate_dict_enst = getTranslation(enstFile)
    translate_dict_ref = getTranslation(refFile)
    keySet_enst = set(translate_dict_enst.keys())
    keySet_ref = set(translate_dict_ref.keys())
    commonKeySet = keySet_enst & keySet_ref
    for key in commonKeySet:
        translate_dict[key] = translate_dict_enst[key] + translate_dict_ref[key]
    for key in (keySet_enst - commonKeySet):
        translate_dict[key] = translate_dict_enst[key].copy()
    for key in (keySet_ref - commonKeySet):
        translate_dict[key] = translate_dict_ref[key].copy()
    return translate_dict


# file_in:AccessionNumber_MutationAA_misssense_v85_enst-ref_only.csv
def getMuta(file_in, accessionNumber_list):
    f = open(file_in, 'rt')
    muta_dict = {}
    muta_list = set()
    for line in f:
        if line[:9] == 'Accession':
            continue
        else:
            line_list = line.split(',')
            accessionNumber = line_list[0]
            if accessionNumber in muta_dict.keys():
                muta_dict[accessionNumber].add(
                    int(line_list[1][3:-2]))
            elif accessionNumber in accessionNumber_list:
                muta_dict[accessionNumber] = set()
                muta_dict[accessionNumber].add(
                    int(line_list[1][3:-2]))
    for i in muta_dict.keys():  # 合并,去重
        muta_list = muta_list | muta_dict[i]
    f.close()
    return muta_list


def getMutaDict(file_in):
    f = open(file_in, 'rt')
    muta_dict = {}
    for line in f:
        if line[:9] == 'Accession':
            continue
        else:
            line_list = line.split(',')
            accessionNumber = line_list[0]
            if accessionNumber in muta_dict.keys():
                muta_dict[accessionNumber].add(int(line_list[1][1:-2]))
            else:
                muta_dict[accessionNumber] = set()
                muta_dict[accessionNumber].add(
                    int(line_list[1][1:-2]))
    f.close()
    return muta_dict


def getMutaList(muta_dict, accessionNumber_list):
    muta_list = set()
    for i in muta_dict.keys():
        if i in accessionNumber_list:
            muta_list = muta_list | muta_dict[i]
    return muta_list


# 要修改！！！！！！
def getResidueDataSet(fread, residue_info):
    residueData = set()
    allResidueData = residue_info.findall(fread.read())
    for i in allResidueData:
        temp_list = i.split(' ')
        try:
            aim = temp_list[-1]
            if aim[0].isalpha():
                residueData.add(int(aim[1:]))
            else:
                residueData.add(int(aim))
        except Exception:
            continue
    return residueData


def fileIO_SMR(sheet, targetUniprot, exp_rangeSet, residue_info_smr):
    def webDownload(out_fname, url):
        try:
            print('start to request')
            req = request.Request(url)
            print('start to getPage')
            page = request.urlopen(req).read()
            print('start to decode')
            page = page.decode('utf-8')
            with open(out_fname, 'wt') as outPut:
                outPut.write(page)
            print('start to writePage')
        except error.URLError as e:
            if hasattr(e, 'code'):
                print(e.code, 1)
            if hasattr(e, 'reason'):
                print(e.reason, 2)
            out_fname = 'null'
        finally:
            print('URLErrol')
        print('webDownload():', out_fname)
        return out_fname

    def newModel(iso_id, indexOfModelX, line_list, residue_info_smr):
        model_id = ('SMR_%s_%s') % (iso_id, indexOfModelX)
        residueData = getResidueData(model_id, line_list[12], residue_info_smr)
        if isinstance(residueData, bool):
            return False
        else:
            modelX = ModelX(model_id)
            modelX.addData_SMR(line_list, residueData)
            return modelX

    def getResidueData(model_id, url, residue_info_smr):
        out_fname = ('/root/Work/Filter_GetMaterials_1903/outFiles/SMR_modelSet_r/%s.pdb') % (model_id)
        try:
            print('fileIO_SMR:Trying to download the model.', url, model_id)
            out_fname = webDownload(out_fname, url)
            print('fileIO_SMR:FINISHED downloaded.')
            with open(out_fname, 'rt') as file:
                residueData = getResidueDataSet(file, residue_info_smr)
        except Exception as e:
            residueData = False
            print(e, url)
        return residueData

    modelSet_SMR = []
    indexOfModelX = 1
    for line in range(sheet.nrows):
        if line < 7:
            continue
        else:
            if sheet.cell(line, 5).value != 'SWISSMODEL':
                continue
            else:
                iso_id = sheet.cell(line, 1).value
                if iso_id == '':  # !!!
                    iso_id = sheet.cell(line, 0).value
                if iso_id != targetUniprot:
                    continue
                else:
                    seqFrom = int(sheet.cell(line, 6).value)
                    seqTo = int(sheet.cell(line, 7).value)
                    if((sheet.cell(line, 11).value >= 30.00) and (seqTo - seqFrom + 1 >= 20)):
                        if set(range(seqFrom, seqTo + 1)) <= exp_rangeSet:
                            continue
                        else:
                            print('fileIO_SMR:', iso_id)
                            line_list = sheet.row_values(line)
                            print('fileIO_SMR:Start to new a model from SMR.')
                            modelX = newModel(iso_id, indexOfModelX, line_list, residue_info_smr)
                            sleep(2)
                            print('fileIO_SMR:FINISHED newModel().')
                            if isinstance(modelX, bool):
                                continue
                            else:
                                modelSet_SMR.append(modelX)
                                indexOfModelX += 1
                    else:
                        continue
    return modelSet_SMR


def fileIO_ModB(uniprot, exp_rangeSet, reInfo_list, residue_info_modb):
    def getLineInfo(fread, info):
        text = info.findall(fread.read())[0]
        return text

    def newModel(uniprot, model_id, lineInfo, residueData):
        modelX = ModelX(model_id)
        modelX.addData_ModB(lineInfo, residueData)
        return modelX

    modelSet_ModB = []
    url = ('https://modbase.compbio.ucsf.edu/modbase-cgi/\
retrieve/modbase/?databaseID=%s') % (uniprot)
    print('fileIO_ModB:Start to get ModB Data.', uniprot)
    html = request.urlopen(url).read()
    html = html.decode('utf-8')
    modelInfo_list = reInfo_list[0].findall(html)
    if not modelInfo_list:
        print('fileIO_ModB: FINISHED')
        return modelSet_ModB
    else:
        filtered = []
        for model in modelInfo_list:
            a = float(reInfo_list[1].findall(model)[0].split('  ')[-1])
            b = int(reInfo_list[3].findall(model)[0].split('  ')[-1])
            c = int(reInfo_list[2].findall(model)[0].split('  ')[-1])
            if (a >= 30.00) and (b - c + 1) >= 20:
                if set(range(c, b + 1)) <= exp_rangeSet:
                    continue
                else:
                    filtered.append(model)
        for i in range(len(filtered)):
            model_id = ('modB_%s_%s') % (uniprot, i + 1)
            route = ('/root/Work/Filter_GetMaterials_1903/outFiles/ModBase_modelSet_r/%s.pdb') % (model_id)
            with open(route, 'wt') as fout:
                fout.write(filtered[i])
            with open(route, 'rt') as fread_1:
                residueData = getResidueDataSet(fread_1, residue_info_modb)
            try:
                with open(route, 'rt') as fread_2:
                    lineInfo = getLineInfo(fread_2, reInfo_list[4])
                modelX = newModel(uniprot, model_id, lineInfo, residueData)
                modelSet_ModB.append(modelX)
                print('fileIO_ModB: FINISHED')
            except Exception:
                continue
        return modelSet_ModB


def fileIO_PDB(uniprot, pdbId_dict):
    def newExp(info):
        pdbId = ('%s_%s') % (info[0], info[1])
        expX = ModelX(pdbId)
        expX.addData_Exp(info)
        return expX

    def getResidueData(pdb, chainInfo):
        residueData_mutiChain = {}
        url = ('http://files.rcsb.org/header/%s.pdb') % (pdb)
        print('fileIO_PDB:Start to get pdbData.', pdb, chainInfo)
        html = request.urlopen(url).read()
        html = html.decode('utf-8')
        # REMARK 465     \w{3} A  [0-9]*
        for index in range(len(chainInfo)):
            search = (r'REMARK 465     \w{3} %s\s*[0-9]*') % (chainInfo[index])
            residueInfo = re.compile(search)
            allResidueData = residueInfo.findall(html)
            residueData = set()
            for i in allResidueData:
                temp_list = i.split(' ')
                if temp_list[-1] == '':  # !
                    continue
                else:
                    residueData.add(int(temp_list[-1]))
            residueData_mutiChain[chainInfo[index]] = residueData
        return residueData_mutiChain

    expSet = []
    pdbInfo = pdbId_dict.get(uniprot, False)
    if isinstance(pdbInfo, bool):
        return expSet
    for pdb in pdbInfo.keys():
        residueData_mutiChain = getResidueData(pdb, pdbInfo[pdb][0])
        cov_from = int(pdbInfo[pdb][1][0])
        cov_to = int(pdbInfo[pdb][1][1])
        cov_len = cov_to - cov_from + 1
        alls = set(range(cov_from, cov_to+1))
        for chain in residueData_mutiChain.keys():
            rangeSet = alls - residueData_mutiChain[chain]
            info = [pdb, chain, cov_from, cov_to, cov_len, rangeSet]
            expX = newExp(info)
            expSet.append(expX)
        sleep(1)

    return expSet


def getPdbIdDict(pdbFile):
    pdbId_dict = {}  # {uniprot:{pdbId:[chainInfo, fromToList],},}
    expFile = open(pdbFile, 'rt')
    for line in expFile:
        if line[:4] == 'Gene':
            continue
        else:
            line_list = line.split('	')
            if line_list[4] == 'NONE':
                line_list[4] = line_list[5]
            uniprot = line_list[4]
            pdbId = line_list[6]
            if isinstance(pdbId_dict.get(uniprot, False), bool):
                pdbId_dict[uniprot] = {pdbId: [line_list[7], line_list[8:10]]}
            elif isinstance(pdbId_dict[uniprot].get(pdbId, False), bool):
                pdbId_dict[uniprot][pdbId] = [line_list[7], line_list[8:10]]
            else:
                continue
    expFile.close()
    return pdbId_dict


def mergeO(muta_list, expSet, modelSet, exp_rangeSet):
    def addMuta(structSet, muta_list):
        for struct in structSet:
            structRangeSet = struct.getRangeSet()
            structMuta_list = muta_list & structRangeSet
            struct.setDeltaMutaList(structMuta_list)

    if not modelSet:
        if not expSet:  # null
            return expSet
        else:  # only exp
            addMuta(expSet, muta_list)
            return expSet
    else:
        if not expSet:  # only model
            addMuta(modelSet, muta_list)
            return modelSet
        else:  # exp + model
            addMuta(expSet, muta_list)
            for model in modelSet:
                new_modelSet = []
                modelRangeSet = model.getRangeSet()
                alphaSet = modelRangeSet & exp_rangeSet
                deltaSet = modelRangeSet - alphaSet
                deltaMuta_list = deltaSet & muta_list
                model.setDeltaMutaList(deltaMuta_list)  # special
                new_modelSet.append(model)
            expSet.extend(new_modelSet)
            return expSet


def writeData(outPut, outPut_json, uniprot, representSet):
    if not representSet:
        outPut.write(('%s\t\n') % (uniprot))
        json_dict = {uniprot: ''}
        json_str = json.dumps(json_dict)
        outPut_json.write(json_str)
        outPut_json.write('\n')
    else:
        temp_dict = {}
        json_dict = {uniprot: temp_dict}
        for i in representSet:
            information = [
                i.model_id, i.provider, i.info_dict['seq_len'],
                i.info_dict['cov_len'], i.info_dict['cov_from'],
                i.info_dict['cov_to'], i.info_dict['seq_id'],
                i.info_dict['coverage'], i.getRangeInterval(),
                i.getDeltaMutaList(), i.info_dict['url'],
                i.info_dict['otherInfo']]
            outPut.write(('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n') % (
                uniprot, information[0], information[1], information[2],
                information[3], information[4],
                information[5], information[6],
                information[7], information[8],
                information[9], information[10],
                information[11]))
            temp_dict[information[0]] = i.info_dict.copy()
            temp_dict[information[0]]['provider'] = information[1]
            temp_dict[information[0]]['rangeSet'] = information[8]
            temp_dict[information[0]]['muta_list'] = information[9]
        json_str = json.dumps(json_dict)
        outPut_json.write(json_str)
        outPut_json.write('\n')


base = '/root/Work/Filter_GetMaterials_1903/'
smrFile = base+r'inFiles/INDEX_SMR_1902.xls'
# pdbFile = base + 'inFiles/mart_export_v85_missense_census_uniprot_2_pdbyes_2_2.txt'
enstFile = base + 'inFiles/uniprot-yourlist_enst_v86.xls'
refFile = base + 'inFiles/uniprot-yourlist_refseqANDothers_v86.xls'
mutaFile = base + 'inFiles/AccessionNumber_MutationAA_misssense_v86.csv'
# old_file_out_1 = base + 'outFiles/outFile0315_220.txt'
# old_file_out_2 = base + '/outFile0312.txt'
file_out = base + 'outFiles/outFile0325.txt'
file_out_json = base + 'outFiles/json_outFile0325.txt'
translate_dict = getTranslate_dict(enstFile, refFile)
muta_dict = getMutaDict(mutaFile)
# pdbId_dict = getPdbIdDict(pdbFile)

search_1 = (r'<content>([\s\S]*?)</content>')
search_2 = (r'REMARK 220 SEQUENCE IDENTITY:\s*[0-9]*\.[0-9]*')
search_3 = (r'REMARK 220 TARGET BEGIN:\s*[0-9]*')
search_4 = (r'REMARK 220 TARGET END:\s*[0-9]*')
search_5 = (r'REMARK 220 EXPERIMENTAL DETAILS([\s\S]*?)\nEXPDTA\s*')
search_smr = (r'ATOM\s*[0-9]*\s{2}\w*\s*\w{3}\s{1}\w\s*[0-9]*')
search_modb = (r'ATOM\s*[0-9]*\s{2}\w*\s*\w*\d*\s*\d*')
info_1 = re.compile(search_1)
seq_id_info = re.compile(search_2)
cov_from_info = re.compile(search_3)
cov_to_info = re.compile(search_4)
info_5 = re.compile(search_5)
residue_info_smr = re.compile(search_smr)
residue_info_modb = re.compile(search_modb)
reInfo_list = [info_1, seq_id_info, cov_from_info, cov_to_info, info_5]


def getOldSet(old_file_out):
        old_set = set()
        data = pd.read_csv(old_file_out, sep='\t', iterator=True)
        loop = True
        while loop:
            try:
                chunk = data.get_chunk(100000)
                info = chunk['UniProt']
                old_set = old_set | set(info)
            except StopIteration:
                loop = False
                print('[Info] Iteration is stopped.')
        return old_set


# old_set_1 = getOldSet(old_file_out_1)
# old_set_2 = getOldSet(old_file_out_2)
# new_translate_dictKeys = set(translate_dict.keys())  # - (old_set_1 | old_set_2)
old_set = getOldSet(file_out)
all_set = set(translate_dict.keys())
new_translate_dictKeys = all_set - old_set
totalSize = len(all_set)
tempSize = len(old_set)
readbook = xlrd.open_workbook(smrFile)
sheet = readbook.sheet_by_index(0)
outPutFile_json = open(file_out_json, 'a+')
outPutFile = open(file_out, 'a+')
'''outPutFile.write(
        'UniProt\tmodel_id\tprovider\tSeqLen\tCovLen\tfrom\tto\tseq_id\tcov\trangeSet\tmutaSite\t\
url\totherInfo\n')'''

expSet = []
exp_rangeSet = set()

for uniprot in new_translate_dictKeys:
    '''expSet = fileIO_PDB(uniprot, pdbId_dict)
    if expSet:
        representObject = RepresentX(expSet.copy())
        representObject.setRangeSet()
        exp_rangeSet = representObject.getRangeSet()
    else:
        exp_rangeSet = set()'''
    modelSet_SMR = fileIO_SMR(sheet, uniprot, exp_rangeSet, residue_info_smr)
    modelSet_ModB = fileIO_ModB(uniprot, exp_rangeSet, reInfo_list, residue_info_modb)  # need a test!
    modelSet_SMR.extend(modelSet_ModB)  # need a test!
    accessionNumber_list = translate_dict[uniprot]
    muta_list = getMutaList(muta_dict, accessionNumber_list)
    fakeRepresentSet = mergeO(muta_list, expSet, modelSet_SMR, exp_rangeSet)
    writeData(outPutFile, outPutFile_json, uniprot, fakeRepresentSet)
    tempSize += 1
    print(('<<SUMMARY:%s percent, temp:%s, total:%s>>') % (
        str((tempSize / totalSize) * 100), tempSize, totalSize))
outPutFile.close()
outPutFile_json.close()
