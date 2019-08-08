# @Date:   2019-08-08T20:09:56+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: 0808_zzf_AnalysisDSSP.py
# @Last modified time: 2019-08-08T20:10:05+08:00
import re
import numpy as np
import json
import requests
import time
import os


def getDSSPcontent(filePath, return_dict=False):
    info = []
    with open(filePath, 'rt') as inFile:
        for line in inFile:
            if line[2] =='#' or info:
                info.append(line[16])
    da = tuple(list(i) for i in np.unique(info, return_counts=True))
    loop_content = da[1][da[0].index(' ')]/sum(da[1])
    if return_dict:
        info_dict = dict(zip(*da))
        return loop_content, info_dict
    else:
        return loop_content

def pdb_to_hssp(pdb_file_path, dssp_file_path,rest_url='https://www3.cmbi.umcn.nl/xssp/'):
    session = requests.Session()
    session.hooks = {
        'response': lambda r, *args, **kwargs: r.raise_for_status()
    }


    files = {'file_': open(pdb_file_path, 'rb')}

    url_create = '{}api/create/pdb_file/dssp/'.format(rest_url)
    r = session.post(url_create, files=files)
    # r.raise_for_status()

    job_id = json.loads(r.text)['id']
    print("Job submitted successfully. Id is: '{}'".format(job_id))

    ready = False
    while not ready:
        url_status = '{}api/status/pdb_file/dssp/{}/'.format(rest_url,
                                                                  job_id)
        r = session.get(url_status)
        # r.raise_for_status()

        status = json.loads(r.text)['status']
        print("Job status is: '{}'".format(status))

        if status == 'SUCCESS':
            ready = True
        elif status in ['FAILURE', 'REVOKED']:
            raise Exception(json.loads(r.text)['message'])
        else:
            time.sleep(5)
    else:
        url_result = '{}api/result/pdb_file/dssp/{}/'.format(rest_url,
                                                                  job_id)
        r = session.get(url_result)
        # r.raise_for_status()
        result = json.loads(r.text)['result']

        with open(dssp_file_path, 'wt') as outFile:
            outFile.write(result)


if __name__ == "__main__":
    pdb_file_folder = r'C:\Users\Nature\Desktop\Report_StructDDG\CompareModel\0503'
    dssp_file_folder = pdb_file_folder
    for pdb_file_path in os.listdir(pdb_file_folder):
        full_pdb_file_path = os.path.join(pdb_file_folder,pdb_file_path)
        if pdb_file_path[-4:] == '.pdb':
            print(pdb_file_path)
            dssp_file_path = r'%s\%s.dssp' % (dssp_file_folder, pdb_file_path[:-4])
            result = pdb_to_hssp(full_pdb_file_path, dssp_file_path)
            da = getDSSPcontent(dssp_file_path, return_dict=True)
            print(da)
