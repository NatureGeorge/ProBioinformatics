# @Date:   2019-04-01T11:00:55+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: FilterModel
# @Last modified time: 2019-04-01T11:06:06+08:00
# coding: utf-8

# In[1]: import the packages


from Bio import SeqIO
from Bio.Alphabet import generic_dna
from Bio.Seq import Seq


# In[2]: prepare the input and output files


file_in = open('InputFiles.fasta', 'rt')
file_out_1 = open('OutputGenebank.gb', 'a+')
file_out_2 = open('OutputInfo.txt', 'wt')
file_out_2.write('SeqID\tLength\tIndex[AACACGTGA]\n')


# In[3]: Use SeqIO to read the fasta file


records = SeqIO.parse(file_in, "fasta")


# In[4]: Deal with the <generator> type


for i in records:
    # output_1
    i.seq = Seq(str(i.seq), generic_dna)
    SeqIO.write(i, file_out_1, "genbank")
    # output_2
    seq_length = len(i.seq)
    seq_ID = i.id
    seq_index = i.seq.find('AACACGTGA')
    file_out_2.write(('%s\t%s\t%s\n') % (seq_ID, seq_length, seq_index))
file_out_1.close()
file_out_2.close()
