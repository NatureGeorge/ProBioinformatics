# 实验题目： 序列格式转换：Fasta格式专成Genebank格式
## 实验内容
* 将InputFiles.fasta中的所有序列转换成Genebank的格式
* 生成Genebank的格式的文件
* 生成所有序列的综合信息，txt文件保存
### Import the packages

```python
from Bio import SeqIO
from Bio.Alphabet import generic_dna
from Bio.Seq import Seq
```

### Prepare the input and output files

```python
file_in = open('InputFiles.fasta', 'rt')
# file_out_1 = open('OutputGenebank.gb', 'a+')
# file_out_2 = open('OutputInfo.txt', 'wt')
# file_out_2.write('SeqID\tLength\tIndex[AACACGTGA]\n')
```

### Use SeqIO to read the fasta file
本实验的序列文件为InputFiles.fasta。文件内有多条序列，因此采用SeqIO.parse()来读取。

```python
records = SeqIO.parse(file_in, "fasta")
```

### Add Alphabet
读取后生成可迭代的genator对象，使用for循环遍历各个SeqRecord对象，并对各个Seq对象添加Alphabet。本实验中添加的Alphabet为generic_dna。

对Seq对象添加完Alphabet即可利用SeqIO.write(outputFileName,’genbank’)来输出Genebank格式的文件。本实验的genbank格式输出文件名为：OutputGenebank.gb。

在上述for遍历过程中，即利用SeqRecord对象提取seqID、Seq对象的长度以及利用find()得到的index信息。输出文件名为：OutputInfo.txt。

```python
for i in records:
    # output_1
    i.seq = Seq(str(i.seq), generic_dna)
    print(i)
    print(i.format('gb'))
    # SeqIO.write(i, file_out_1, "genbank")
    # output_2
    seq_i = i.seq
    seq_length = len(seq_i)
    seq_ID = i.id
    seq_index = i.seq.find('AACACGTGA')
    print(('seqID:%s\tlength:%s\tIndex[AACACGTGA]:%s\n\n') % (seq_ID, seq_length, seq_index))
    # file_out_2.write(('%s\t%s\t%s\n') % (seq_ID, seq_length, seq_index))
# file_out_1.close()
# file_out_2.close()
```

    ID: I1111
    Name: I1111
    Description: I1111 rank=0668881 x=2144.0 y=1105.0
    Number of features: 0
    Seq('ACGTCATGAGAGTTTGATCATGGCTCAGGACGAACGCTGGCGGCGTGCTTAACA...GCC', DNAAlphabet())
    LOCUS       I1111                    418 bp    DNA              UNK 01-JAN-1980
    DEFINITION  I1111 rank=0668881 x=2144.0 y=1105.0.
    ACCESSION   I1111
    VERSION     I1111
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 acgtcatgag agtttgatca tggctcagga cgaacgctgg cggcgtgctt aacacatgca
           61 agtcgaacga tgaagctcca gcttgctggg gtggattagt ggcgaacggg tgagtaacac
          121 gtgagtaacc tgcccttgac tctgggataa gcgttggaaa cgacgtctaa taccggatat
          181 gacgaccgat ggcatcatct ggttgtggaa agaattttgg tcaaggatgg actcgcggcc
          241 tatcaggtag ttggtgaggt aatggctcac caagcctacg acgggtagcc ggcctgagag
          301 ggtgaccggc cacactggga ctgagacacg gcccagactc ctacgggagg cagcagtggg
          361 gaatattgca caatgggcga aagcctgatg cagcaacgcc gcgtgaggga tgacggcc
    //
    
    seqID:I1111	length:418	Index[AACACGTGA]:115
    
    
    ID: I1112
    Name: I1112
    Description: I1112 rank=0320459 x=3829.0 y=3120.0
    Number of features: 0
    Seq('ACGTCATGAGAGTTTGATCCTGGCTCAGGATGAACGCTAGCGGCAGGCTTAACA...GCT', DNAAlphabet())
    LOCUS       I1112                    450 bp    DNA              UNK 01-JAN-1980
    DEFINITION  I1112 rank=0320459 x=3829.0 y=3120.0.
    ACCESSION   I1112
    VERSION     I1112
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 acgtcatgag agtttgatcc tggctcagga tgaacgctag cggcaggctt aacacatgca
           61 agtcgagggt agaaatagct tgctattttg agaccggcgc acgggtgcgt aacgcgtatg
          121 caatctgcct tttacagggg aatagcccag agaaatttgg attaatgccc catagcgctg
          181 cagggcggca tcgccgagca gctaaagtca caacggtaaa gatgagcatg cgtcccatta
          241 gctagttggt aaggtaacgg cttaccaagg cgatgatggg tagggtcctg agagggagat
          301 cccccacact ggtactgaga cacggaccag actcctacgg gaggcagcag tgaggaatat
          361 tggtcaatgg gcgcaagcct gaaccagcca tgccgcgtgc aggatgaagg ccttcgggtt
          421 gtaaactgct tttgacggaa cgaaaaagct
    //
    
    seqID:I1112	length:450	Index[AACACGTGA]:-1
    
    
    ID: I1113
    Name: I1113
    Description: I1113 rank=0668881 x=2144.0 y=1105.0
    Number of features: 0
    Seq('ACGTCATGAGAGTTTGATCATGGCTCAGGACGAACGCTGGCGGCGTGCTTAACA...GCC', DNAAlphabet())
    LOCUS       I1113                    374 bp    DNA              UNK 01-JAN-1980
    DEFINITION  I1113 rank=0668881 x=2144.0 y=1105.0.
    ACCESSION   I1113
    VERSION     I1113
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 acgtcatgag agtttgatca tggctcagga cgaacgctgg cggcgtgctt aacacatgca
           61 agtcgaacga tgaagctcca gctgtgagta acacgtgagt aacctgccct tgactctggg
          121 ataagcgttg gaaacgacgt ctaataccgg atatgacgac cgatggcgaa ttttggtcaa
          181 ggatggactc gcggcctatc aggtagttgg tgaggtaatg gctcaccaag cctacgacgg
          241 gtagccggcc tgagagggtg accggccaca ctgggactga gacacggccc agactcctac
          301 gggaggcagc agtggggaat attgcacaat gggcgaaagc ctgatgcagc aacgccgcgt
          361 gagggatgac ggcc
    //
    
    seqID:I1113	length:374	Index[AACACGTGA]:89
    
    
    ID: I1114
    Name: I1114
    Description: I1114 rank=0320459 x=3829.0 y=3120.0
    Number of features: 0
    Seq('ACGTCATGAGAGTTTGATCCTGGCTCAGGATGAACGCTAGCGGCAGGCTTAACA...GCT', DNAAlphabet())
    LOCUS       I1114                    450 bp    DNA              UNK 01-JAN-1980
    DEFINITION  I1114 rank=0320459 x=3829.0 y=3120.0.
    ACCESSION   I1114
    VERSION     I1114
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 acgtcatgag agtttgatcc tggctcagga tgaacgctag cggcaggctt aacacatgca
           61 agtcgagggt agaaatagct tgctattttg agaccggcgc acgggtgcgt aacgcgtatg
          121 caatctgcct tttacagggg aatagcccag agaaatttgg attaatgccc catagcgctg
          181 cagggcggca tcgccgagca gctaaagtca caacggtaaa gatgagcatg cgtcccatta
          241 gctagttggt aaggtaacgg cttaccaagg cgatgatggg tagggtcctg agagggagat
          301 cccccacact ggtactgaga cacggaccag actcctacgg gaggcagcag tgaggaatat
          361 tggtcaatgg gcgcaagcct gaaccagcca tgccgcgtgc aggatgaagg ccttcgggtt
          421 gtaaactgct tttgacggaa cgaaaaagct
    //
    
    seqID:I1114	length:450	Index[AACACGTGA]:-1
    
    
    ID: I1115
    Name: I1115
    Description: I1115 rank=0668881 x=2144.0 y=1105.0
    Number of features: 0
    Seq('ACGTCATGAGAGTTTGATCATGGCTCAGGACGAACGCTGGCGGCGTGCTTAACA...GCC', DNAAlphabet())
    LOCUS       I1115                    323 bp    DNA              UNK 01-JAN-1980
    DEFINITION  I1115 rank=0668881 x=2144.0 y=1105.0.
    ACCESSION   I1115
    VERSION     I1115
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 acgtcatgag agtttgatca tggctcagga cgaacgctgg cggcgtgctt aacacatgca
           61 agtcgaacga tgaagctcca gcttgctggg gtggattagt ggcgaacggg tgagtaacac
          121 gtgagtaacc tgcccttgac tctgggataa gcgttggaaa cgacgtctaa taccggatat
          181 gacgaccgat ggcatcatct ggttgtggaa agaattttgg tcaaggatgg actcgcggcc
          241 tatcaggtag ttggtgaggt aatggctcac caagccaatg ggcgaaagcc tgatgcagca
          301 acgccgcgtg agggatgacg gcc
    //
    
    seqID:I1115	length:323	Index[AACACGTGA]:115
    
    
    ID: I1116
    Name: I1116
    Description: I1116 rank=0320459 x=3829.0 y=3120.0
    Number of features: 0
    Seq('ACGCTAGCGGCAGGCTTAACACATGCAAGTCGAGGGTAGAAATAGCTTGCTATT...GGG', DNAAlphabet())
    LOCUS       I1116                    263 bp    DNA              UNK 01-JAN-1980
    DEFINITION  I1116 rank=0320459 x=3829.0 y=3120.0.
    ACCESSION   I1116
    VERSION     I1116
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 acgctagcgg caggcttaac acatgcaagt cgagggtaga aatagcttgc tattttgaga
           61 ccggcgcacg ggtgcgtaac gcgtatgcaa tctgcctttt acaggggaat agcccagaga
          121 aatttggatt aatgccccat agcgctgcag ggcggcatcg ccgagcagct aaagtcacaa
          181 cggtaaagat gagcatgcgt cccattagct agttggtaag gtaacggctt accaaggcga
          241 tgatgggtag ggtcctgaga ggg
    //
    
    seqID:I1116	length:263	Index[AACACGTGA]:-1
    
    
    ID: I1117
    Name: I1117
    Description: I1117 rank=0668881 x=2144.0 y=1105.0
    Number of features: 0
    Seq('ACGTCATGAGAGTTTGATCATGGCTCAGGACGAACGCTGGCGGCGTGCTTAACA...GCA', DNAAlphabet())
    LOCUS       I1117                    370 bp    DNA              UNK 01-JAN-1980
    DEFINITION  I1117 rank=0668881 x=2144.0 y=1105.0.
    ACCESSION   I1117
    VERSION     I1117
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 acgtcatgag agtttgatca tggctcagga cgaacgctgg cggcgtgctt aacacatgca
           61 agtcgaacga tgaagctcca gcttgctggg gtggattagt ggcgaacggg tgagtaacac
          121 gtgagtaacc tgcccttgac tctgggataa gcgttggaaa cgacgtctaa taccggatat
          181 gacgaccgat ggcatcatct ggttgtggaa agaattttgg tcaaggatgg actcgcggcc
          241 tatcaggtag ttggtgaggt aatggctcac caagcctacg acgggtagcc ggcctgagag
          301 ggtgaccggc cacactggga ctgagacacg gcccagactc ctacgggagg cagcagtggg
          361 gaatattgca
    //
    
    seqID:I1117	length:370	Index[AACACGTGA]:115
    
    
    ID: I1118
    Name: I1118
    Description: I1118 rank=0320459 x=3829.0 y=3120.0 length=512
    Number of features: 0
    Seq('ACGTCATGAGAGTTTGATCCTGGCTCAGGATGAACGCTAGCGGCAGGCTTAACA...GCT', DNAAlphabet())
    LOCUS       I1118                    302 bp    DNA              UNK 01-JAN-1980
    DEFINITION  I1118 rank=0320459 x=3829.0 y=3120.0 length=512.
    ACCESSION   I1118
    VERSION     I1118
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 acgtcatgag agtttgatcc tggctcagga tgaacgctag cggcaggctt aacacatgca
           61 agtcgagggt agaatgagca tgcgtcccat tagctagttg gtaaggtaac ggcttaccaa
          121 ggcgatgatg ggtagggtcc tgagagggag atcccccaca ctggtactga gacacggacc
          181 agactcctac gggaggcagc agtgaggaat attggtcaat gggcgcaagc ctgaaccagc
          241 catgccgcgt gcaggatgaa ggccttcggg ttgtaaactg cttttgacgg aacgaaaaag
          301 ct
    //
    
    seqID:I1118	length:302	Index[AACACGTGA]:-1
    
