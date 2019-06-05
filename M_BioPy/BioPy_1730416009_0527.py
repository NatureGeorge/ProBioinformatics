# @Date:   2019-05-27T10:15:26+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioPy_1730416009_0527.py
# @Last modified time: 2019-05-27T14:31:37+08:00
import pandas as pd
from Bio.Cluster import treecluster


# Use pandas to read the excel-format file
dfrm = pd.read_excel('./ExpressionData.xlsx')
# Convert the table into a matrix/array
data_array = dfrm.drop('ID', axis=1).values
# Perform hierarchical clustering (For Gene/Protein)
tree_gene = treecluster(data_array, transpose=0, method='s', dist='e')
# Perform hierarchical clustering (For Experiment Condiction
# -> transpose=1,method=pairwise single-linkage clustering)
tree_exp = treecluster(data_array, transpose=1, method='m', dist='e')
# Output the result
with open('./Results.txt', 'wt') as outFile:
    outFile.write("# Cluster Tree of Exp Condiction\n")
    outFile.write(str(tree_exp) + '\n')
    outFile.write("# Cluster Tree of Gene\n")
    outFile.write(str(tree_gene) + '\n')
