# @Date:   2019-06-10T10:16:43+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioPy_zzf_0610.py
# @Last modified time: 2019-06-10T12:36:01+08:00
import re
import pandas as pd
from Bio.PDB import PDBList
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Polypeptide import is_aa


def mmcif_Method(pdbId_list, filePath, info_dict):
    def loadPDB_CIF_format(pdbId, filePath, pdbl):
        pdbFileSavePath = '%s%s.cif' % (filePath, pdbId)
        try:
            mmcif_dict = MMCIF2Dict(pdbFileSavePath)
        except IOError:
            # Get the file
            pdbl.retrieve_pdb_file(pdbId, file_format='mmCif', pdir=filePath)
            mmcif_dict = MMCIF2Dict(pdbFileSavePath)
        return mmcif_dict

    def getChainInfo_CIF(mmcif_dict, resListName, chainListName):
        dfrm = pd.DataFrame(
            {'res': mmcif_dict[resListName],
             'chain_id': mmcif_dict[chainListName]})
        chainInfo = ''
        for chain, df in dfrm.groupby('chain_id'):
            chainInfo += '%s: %s; ' % (chain,
                    len(list(filter(lambda x: x != '?', df['res']))))
        return chainInfo

    pdbl = PDBList()
    for pdbId in pdbId_list:
        mmcif_dict = loadPDB_CIF_format(pdbId, filePath, pdbl)
        info_dict['PDBID'].append(pdbId)
        info_dict['name'].append(mmcif_dict['_struct.title'])
        info_dict['PMID'].append(mmcif_dict['_citation.pdbx_database_id_PubMed'])
        info_dict['resolution'].append(mmcif_dict['_refine.ls_d_res_high'])
        info_dict['Chain Information'].append(getChainInfo_CIF(
            mmcif_dict, '_pdbx_poly_seq_scheme.pdb_mon_id', '_pdbx_poly_seq_scheme.pdb_strand_id'))
    return info_dict


def pdb_Method(pdbId_list, filePath, info_dict):
    def loadPDB_PDB_format(pdbId, filePath, parser, pdbl):
        try:
            structure = parser.get_structure(pdbId, filePath + "pdb%s.ent" % pdbId.lower())
        except IOError:
            pdbl.retrieve_pdb_file(pdbId, file_format='pdb', pdir=filePath)
            structure = parser.get_structure(
                pdbId, filePath + "pdb%s.ent" % pdbId.lower())
        return structure

    def getChainInfo_PDB(structure):
        model = structure[0]
        chainInfo = ''
        for chain in model.get_chains():
            chainInfo += '%s: %s; ' % (chain.id,
                                       len(list(filter(is_aa, chain))))
        return chainInfo

    parser = PDBParser(PERMISSIVE=1)
    pdbl = PDBList()
    findPMID = re.compile(r'PMID\s+([\d,]+)')
    for pdbId in pdbId_list:
        structure = loadPDB_PDB_format(pdbId, filePath, parser, pdbl)
        info_dict['PDBID'].append(pdbId)
        info_dict['name'].append(structure.header['name'])
        info_dict['PMID'].append(findPMID.findall(structure.header['journal']))
        info_dict['resolution'].append(structure.header['resolution'])
        info_dict['Chain Information'].append(getChainInfo_PDB(structure))
    return info_dict


if __name__ == '__main__':
    filePath = 'C:/Users/Nature/Desktop/M_BioPy/exp/homeWork/17生信_实验八/1730416009_朱泽峰/'
    pdbId_list = ['1B34', '1BLX', '1CGI', '1B3B', '1DEV', '1DQL']
    info_dict = {'PDBID': [], 'name': [], 'PMID': [],
                 'resolution': [], 'Chain Information': []}
    #result_dict = mmcif_Method(pdbId_list, filePath, info_dict)
    result_dict = pdb_Method(pdbId_list, filePath, info_dict)
    pd.DataFrame(result_dict).to_csv(filePath + 'Summary4.txt', index=False, sep='\t')
