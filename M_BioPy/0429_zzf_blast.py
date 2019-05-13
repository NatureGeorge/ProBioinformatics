#!/usr/bin/env python
# coding: utf-8

# # 实验题目：BLAST
# ## 实验内容
# * 通过本地版本或在线版的方式来寻找inputFasta文件中相似序列，保存为xml格式，命名为OutBlast.xml
# * 解析BLAST运行结果，提取所有e-value小于0.01的结果，保存到Results.txt文件中
# ### Import the packages

# In[]:


# @Date:   2019-04-29T11:11:49+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_BioPy
# @Last modified time: 2019-04-29T11:44:43+08:00

# Import packages
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML


# ### Def a function that use BioPy to collect data

# In[ ]:


def getBlastInfo(fasta_string, blastType, seqType):
    result_handle = NCBIWWW.qblast(blastType, seqType, fasta_string)
    with open("OutBlast.xml", "w") as save_file:
        save_file.write(result_handle.read())
        result_handle.close()
    result_handle = open("OutBlast.xml")
    return NCBIXML.parse(result_handle)


# ### Set Cutoff , Filter info and write output in main()

# In[ ]:


def main():
    fasta_string = open('inputFasta', 'rt').read()
    blast_record = getBlastInfo(fasta_string, "blastp", "pdbaa")
    E_VALUE_THRESH = 0.01
    with open('Results.txt', 'wt') as outputFile:
        for i in blast_record:
            for alignment in i.alignments:
                for hsp in alignment.hsps:
                    if hsp.expect < E_VALUE_THRESH:
                        outputFile.write('****Alignment****\n')
                        outputFile.write('sequence:%s\n' % (alignment.title))
                        outputFile.write('length%s\n:' % (alignment.length))
                        outputFile.write('e value:%s\n' % (hsp.expect))
                        outputFile.write('%s...\n' % (hsp.query[0:75]))
                        outputFile.write('%s...\n' % (hsp.match[0:75]))
                        outputFile.write('%s...\n' % (hsp.sbjct[0:75]))


# ### Main() when run codes individually

# In[ ]:


if __name__ == "__main__":
    main()
