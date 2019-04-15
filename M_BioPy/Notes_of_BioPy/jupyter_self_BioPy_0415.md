# 实验题目： 多序列比对
## 实验内容：
* 利用biopython调用序列比对软件
* 从比对文件中提取信息
* 利用biopython对比对文件进行分割

### Import the packages

```python
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO
```

### Prepare the input and output files

```python
base = r"C:\Users\Nature\Desktop\M_BioPy\exp\material\BioPy_exp4"
clustalw_exe = base + r"\clustalw2.exe"
in_file = base + r"\inputFasta"
out_file = base + r"\OutFasta.aln"
```

### Do the Alignment
本实验的序列文件为inputFasta.fasta。文件内有3条序列。
利用Bio.Align.Applications的ClustalwCommandline模块生成命令，并用clustalw_cline()向程序传输。

```python
clustalw_cline = ClustalwCommandline(clustalw_exe, infile=in_file, outfile=out_file)
clustalw_cline()
```

### Read the Alignment
利用Bio的AlignIO模块读取生成的比对文件。

```python
alignment = AlignIO.read(out_file, "clustal")
```

### Write the Annotation

```python
annotationOutFile = base + r"\OutAnnotation.txt"
with open(annotationOutFile, "wt") as outfile:
    for record in alignment:
        outfile.write(str(record) + "\n\n")
```

### Split the alignment
利用alignment[:, :10] + alignment[:, -10:]来提取相关列的比对信息。

```python
newAlignmentFile = base + r"\OutFasta2.aln"
newAlignment = alignment[:, :10] + alignment[:, -10:]
AlignIO.write(newAlignment, newAlignmentFile, "clustal")
```
