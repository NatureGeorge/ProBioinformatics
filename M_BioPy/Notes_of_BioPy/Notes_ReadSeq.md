# How BioPy Handel Biological Sequences?
Date: 20190325, By: ZeFengZhu
## Reference
> (https://biopython.org/wiki/Documentation)
> (http://biopython.org/DIST/docs/tutorial/Tutorial.html)
## Content
1. IUPAC
2. CodonTable
3. Seq & MutableSeq
4. SeqRecord
5. SeqIO
## 1. IUPAC
### import

```python
>>> from Bio.Alphabet import IUPAC
```

### Use

```python
# DNA基本字符集                              # RNA基本字符集
>>> IUPAC.unambiguous_dna.letters           >>> IUPAC.unambiguous_rna.letters
'GATC'                                      'GAUC'

# DNA模糊字符集                              # RNA模糊字符集
>>> IUPAC.ambiguous_dna.letters             >>> IUPAC.ambiguous_rna.letters
'GATCRYWSMKHBVDN'                           'GAUCRYWSMKHBVDN'

# 核苷酸扩展字母表
>>> IUPAC.ExtendedIUPACDNA.letters
'GATCBDSW'

# Protein基本字符集(20aa)
>>> IUPAC.IUPACProtein.letters
'ACDEFGHIKLMNPQRSTVWY'

# Protein字符集,含有不常见aa
>>> IUPAC.ExtendedIUPACProtein.letters
'ACDEFGHIKLMNPQRSTVWYBXZJUO'
```

## 2. CodonTable
### import

```python
>>> from Bio.Data import CodonTable
```

### Use

```python
>>> standard_table = CodonTable.unambiguous_dna_by_id[1]
>>> print(standard_table)
Table 1 Standard, SGC0
'''
  |  T      |  C      |  A      |  G      |
--+---------+---------+---------+---------+--
T | TTT F   | TCT S   | TAT Y   | TGT C   | T
T | TTC F   | TCC S   | TAC Y   | TGC C   | C
T | TTA L   | TCA S   | TAA Stop| TGA Stop| A
T | TTG L(s)| TCG S   | TAG Stop| TGG W   | G
--+---------+---------+---------+---------+--
C | CTT L   | CCT P   | CAT H   | CGT R   | T
C | CTC L   | CCC P   | CAC H   | CGC R   | C
C | CTA L   | CCA P   | CAA Q   | CGA R   | A
C | CTG L(s)| CCG P   | CAG Q   | CGG R   | G
--+---------+---------+---------+---------+--
A | ATT I   | ACT T   | AAT N   | AGT S   | T
A | ATC I   | ACC T   | AAC N   | AGC S   | C
A | ATA I   | ACA T   | AAA K   | AGA R   | A
A | ATG M(s)| ACG T   | AAG K   | AGG R   | G
--+---------+---------+---------+---------+--
G | GTT V   | GCT A   | GAT D   | GGT G   | T
G | GTC V   | GCC A   | GAC D   | GGC G   | C
G | GTA V   | GCA A   | GAA E   | GGA G   | A
G | GTG V   | GCG A   | GAG E   | GGG G   | G
--+---------+---------+---------+---------+--
'''

# 该id下的起始密码子
>>> standard_table.start_codons
['TTG', 'CTG', 'ATG']

# 该id下的终止密码子
>>> standard_table.stop_codons
['TAA', 'TAG', 'TGA']
```
## 3. Seq & MutableSeq
### import

```python
>>> from Bio import Seq
>>> from Bio.Alphabet import IUPAC
```

### Use
#### Seq

```python
# 以Seq.Seq类创建一个Seq对象                                  # 以Seq.Seq类创建一个Seq对象并指定字符集
>>> my_seq = Seq.Seq("AGCATCGTAGCATGCAC")                   >>> dna_seq = Seq.Seq("AGCATCGTAGCATGCAC", IUPAC.unambiguous_dna)
>>> my_seq                                                  >>> dna_seq
Seq('AGCATCGTAGCATGCAC')                                    Seq('AGCATCGTAGCATGCAC', IUPACUnambiguousDNA())
                                                            
# 转录(DNA ->> RNA)                                          # 转录(DNA ->> RNA)
>>> rnaSeq = my_seq.transcribe()                            >>> rna_seq = dna_seq.transcribe()
>>> rnaSeq                                                  >>> rna_seq
Seq('AGCAUCGUAGCAUGCAC', RNAAlphabet())                     Seq('AGCAUCGUAGCAUGCAC', IUPACUnambiguousRNA())
                                                            
# 逆转录(RNA ->> DNA)                                        # 逆转录(RNA ->> DNA)
>>> rnaSeq.back_transcribe()                                >>> rna_seq.back_transcribe()
Seq('AGCATCGTAGCATGCAC', DNAAlphabet())                     Seq('AGCATCGTAGCATGCAC', IUPACUnambiguousDNA())
                                                            
# 翻译(RNA ->> Protein)
>>> messenger_rna = Seq.Seq('AUGGCCAUUGUAAUGGGCCGCUGAAAGGGUGCCCGCCCGAUAGUA', IUPAC.unambiguous_rna)
>>> messenger_rna.translate()  # 若序列长度非3的倍数则会报错，但仍有结果
Seq('MAIVMGR*KGARPIV', HasStopCodon(IUPACProtein(), '*'))

# 翻译(DNA ->> Protein)
>>> coding_dna = messenger_rna.back_transcribe()
>>> coding_dna
Seq('ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGCCCGATAGTA', IUPACUnambiguousDNA())
>>> coding_dna.translate()
Seq('MAIVMGR*KGARPIV', HasStopCodon(IUPACProtein(), '*'))
```

```python
# Seq类如Str类的操作
>>> my_seq = Seq.Seq('AGCATCGTA GCATGCAC')
>>> my_seq
Seq('AGCATCGTA GCATGCAC')

>>> my_seq[:11]
Seq('AGCATCGTA G')

>>> my_seq.split('T')
[Seq('AGCA'), Seq('CG'), Seq('A GCA'), Seq('GCAC')]  # <class 'list'>

>>> my_seq.count('A')
5

>>> my_seq_1 = Seq.Seq('TAGATGCTAGGGGCGTCGTACAGC', IUPAC.unambiguous_dna)
>>> my_seq_2 = Seq.Seq('TATC', IUPAC.unambiguous_dna)
>>> my_seq_3 = my_seq_1 + my_seq_2
>>> my_seq_3
Seq('TAGATGCTAGGCGTCGTACAGCTATC', IUPACUnambiguousDNA())
>>> my_seq_3.find('AGCTATC')
21
```

#### MutableSeq
Seq对象与python中字符串类似，不可变。因此，若要改变序列，需要用到MutableSeq对象(可变的序列对象)。

```python
>>> my_seq = Seq.Seq('TAGATGCTAGGGGCGTCGTACAGC', IUPAC.unambiguous_dna)
>>> my_seq[:3] = 'AAA'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'Seq' object does not support item assignment

>>> my_seq = Seq.MutableSeq('TAGATGCTAGGGGCGTCGTACAGC', IUPAC.unambiguous_dna)
>>> my_seq[:3] = 'AAA'
>>> my_seq
MutableSeq('AAAATGCTAGGGGCGTCGTACAGC', IUPACUnambiguousDNA())

# Seq ->> MutableSeq
>>> my_seq = Seq.Seq('TAGATGCTAGGGGCGTCGTACAGC', IUPAC.unambiguous_dna)
>>> my_mut_seq = my_seq.tomutable()
>>> my_mut_seq
MutableSeq('TAGATGCTAGGGGCGTCGTACAGC', IUPACUnambiguousDNA())

# remove() & reverse()
>>> my_mut_seq.remove('T')
>>> my_mut_seq
MutableSeq('AGATGCTAGGGGCGTCGTACAGC', IUPACUnambiguousDNA())
>>> my_mut_seq.reverse()
>>> my_mut_seq
MutableSeq('CGACATGCTGCGGGGATCGTAGA', IUPACUnambiguousDNA())

# MutableSeq ->> Seq
>>> my_seq_t = my_mut_seq.toseq()
>>> my_seq_t
Seq('CGACATGCTGCGGGGATCGTAGA', IUPACUnambiguousDNA())
```

## 4. SeqRecord
提供序列及其注释容器(可能包括的特征)

{name, description, letter_annotations, annotations, features, dbxrefs}
### import

```python
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
```

### Use

```python
# 添加信息
sim_seq = Seq('GATC')
sim_seq_r = SeqRecord(sim_seq, id='Test123')
sim_seq_r.description = 'This is just a practice.'
sim_seq_r.annotations['RECORD1'] = '20190325'
sim_seq_r.annotations['RECORD2'] = '20190325,21:42'

# 转换文件格式
output = sim_seq_r.format('fasta')
print(output)
'''
>Test123 This is just a practice.
GATC
'''
```

## 5. SeqIO
### import

```python
from Bio import SeqIO
from Bio.Alphabet import generic_rna
from Bio.Seq import Seq
```

### Use

```python
# read and write the file (genebank ->> fasta)
with open("AY810830.gb", "r") as input_file:
    with open("AY810830.fasta", "w") as output_file:
        # 读入单序列: SeqIO.read(), 序列大文件:SeqIO.index()
        records = SeqIO.parse(input_file, "genbank")
        SeqIO.write(records, output_file, "fasta")

# read and write the file (fasta ->> genebank)
with open("AY810830_2.gb", "w") as output_file:
    with open("AY810830.fasta", "r") as fasta_file:
        records = SeqIO.read(fasta_file, "fasta")
        # print(records)
        print(type(str(records.seq)), str(records.seq))
        records.seq = Seq(str(records.seq), generic_rna)
        # print(records)
        SeqIO.write(records, output_file, "genbank")
```

