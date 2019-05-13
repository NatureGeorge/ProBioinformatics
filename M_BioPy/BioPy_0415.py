# @Date:   2019-04-15T10:20:24+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_BioPy
# @Last modified time: 2019-04-15T11:53:16+08:00
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO

# Set the File Path
base = r"C:\Users\Nature\Desktop\M_BioPy\exp\material\BioPy_exp4"
clustalw_exe = base + r"\clustalw2.exe"
in_file = base + r"\inputFasta"
out_file = base + r"\OutFasta.aln"

# Do the Alignment
clustalw_cline = ClustalwCommandline(clustalw_exe, infile=in_file, outfile=out_file)
clustalw_cline()

# Read the Alignment
alignment = AlignIO.read(out_file, "clustal")

# Write the Annotation
annotationOutFile = base + r"\OutAnnotation.txt"
with open(annotationOutFile, "wt") as outfile:
    for record in alignment:
        outfile.write(str(record) + "\n\n")

# Split the alignment
newAlignmentFile = base + r"\OutFasta2.aln"
newAlignment = alignment[:, :10] + alignment[:, -10:]
AlignIO.write(newAlignment, newAlignmentFile, "clustal")
