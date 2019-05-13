# @Date:   2019-05-13T10:12:57+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: 0513_zzf_ncbi_search.py
# @Last modified time: 2019-05-13T11:15:41+08:00
from Bio import Entrez
from Bio import Medline
import pandas as pd


def collectPubmedInfo(email, term, record_dict, retmax, outputPath):
    Entrez.email = email
    # Use ESearch
    handle = Entrez.esearch(db="pubmed", term=term, retmax=retmax)
    record = Entrez.read(handle)
    count = record["Count"]
    idlist = record["IdList"]
    # Use pandas to save a formated file
    df_1 = pd.DataFrame({"PubmedIDs(%s)" % (count): idlist})
    df_1.to_csv(outputPath+"PubmedIDs_1.txt", sep="\t")
    # Use EFetch to collect id and use medline to get details
    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
    records = Medline.parse(handle)
    for record in records:
        for key in record_dict.keys():
            record_dict[key].append(record[key])
    # Use pandas to save a formated file
    df_2 = pd.DataFrame(record_dict)
    df_2.to_csv(outputPath+"Results_1.txt", sep="\t")


if __name__ == "__main__":
    email = "1730416009@stu.suda.edu.cn"
    term = "machine learning AND cancer"
    record_dict = {"TI": [], "SO": []}
    retmax = 100000
    outputPath = "./"
    collectPubmedInfo(email, term, record_dict, retmax, outputPath)
