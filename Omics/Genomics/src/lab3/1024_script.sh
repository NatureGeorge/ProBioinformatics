# @Date:   2019-10-24T13:36:27+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: 1024_script.sh
# @Last modified time: 2019-10-24T15:07:34+08:00

# 文件准备
# 1. 基因组序列： .fa + .gff
workDir="/home/student/s24/zeFengZhu/Gen/lab3"
fastaFile="$workDir/GCA_000977265.3_Sc_YJM1342_v1_genomic.fna"
gffFile="$workDir/GCA_000977265.3_Sc_YJM1342_v1_genomic.gff"

# 2. 下载蛋白序列
# 根据基因组序列的物种来源，从UniProt数据库搜索、下载近缘物种所有已知蛋白序列（reviewed）【如：所有真菌（fungi）已知蛋白】，保存序列条数以及FASTA格式序列，用于全基因组的同源搜索
# uniprot-taxonomy_fungi+NOT+_saccharomyces+cerevisiae_+AND+reviewed_yes.fasta -> protein.fasta
unpFastaFile="$workDir/protein.fasta"
# 3. 创建本地 BLAST 数据库 (work dir: /home/student/s24/zeFengZhu/Gen/lab3/)
makeblastdb -in $fastaFile -input_type fasta -title Sc_gDNA -dbtype nucl -out Sc_gDNA

: '
Building a new DB, current time: 10/24/2019 14:22:05
New DB name:   /home/student/s24/zeFengZhu/Gen/lab3/Sc_gDNA
New DB title:  Sc_gDNA
Sequence type: Nucleotide
Keep Linkouts: T
Keep MBits: T
Maximum file size: 1000000000B
Adding sequences from FASTA; added 17 sequences in 0.468456 seconds.
'

# 全基因组的同源基因搜索
# 注意在远程连接服务器编辑shell脚本时，要提前改好换行符，切换到UNIX格式,否则shell脚本无法正常运行
:set ff=unix
tblastn -query $unpFastaFile -db SC_gDNA -out ./blastx_results.outfmt6 -evalue 1e-5 -outfmt 6 -max_target_seqs 1 -num_threads 10
tblastn -query $unpFastaFile -db SC_gDNA -out ./blastx_results.outfmt7 -evalue 1e-5 -outfmt 7 -max_target_seqs 1 -num_threads 10

# 使用 blast92gff3.pl 和 blast2gff.py 程序，分别把结果转成 GFF3 格式；
blast92gff3.pl Sc_blastx_results.outfmt6 > Sc_perl.gff3
blast2gff.py -b Sc_blastx_results.outfmt6 > Sc_python.gff3

# 比较两个程序转换结果的异同之处；
# 排除 blast 比对结果中的冗余项：【可选内容，视完成度加分，最多加 10 分】 （1）不同物种的同源蛋白在基因组上的匹配位置存在的重叠问题； （2）同一蛋白家族的不同成员在基因组上的匹配位置存在的重叠问题； （3）同一个蛋白在基因组上的不同位置的高相似区域问题；
