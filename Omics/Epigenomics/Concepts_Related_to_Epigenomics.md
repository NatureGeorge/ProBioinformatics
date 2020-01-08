# Concepts Related to Epigenomics

> Last Modified Time 2019-09-05

## Epigenetic Landscape

* DNA-methylation
* Nucleosome position (MNase-Seq, ATAT-Seq)
* TF Binding (ChIP-Seq? DNase-Seq/FAIRE-Seq? ATAT-Seq?)
* Histone Modification
* Chromatin accessibility (ATAT-Seq)
* Higher order chromatin interactions
* Non-coding RNA
* ...

### DNA-methylation

* 富集区域: repetitive elements (CpG island e.g)
* Transferase:
* Heritable

#### DNA-methylation Detection

> ...

#### CpG island

> GC-rich regions that...

* The promoter regions of ~70% of genes have CpG islands.

##### Promoter Region

> The 1kb(or 2kb) upstream and downstream of TSS(Transcription Start Site).

### Histone Modification

* 甲基化
* 磷酸化
* 乙酰化
* 泛素化
* 磺酰化

#### Histone Code

Code | Description | Location
-|-|-
H3K9me3 | __Repress__ | Gene Body
H3K27ac | Activate | Enhancer
H3K27me3 | __Repress__ |Promoter(@ EZH2 酶+ DNA甲基化酶)
H3K7?me3 | __Repress__ |?
H3K4me3 | Activate | Promoter
H3K9ac | Activate | ?
H3K4me2 | Activate | Promoter,Enhancer

* Gene Body: H3K9me3(Repress)
* Promoter: H3K27me3(Repress) H3K4me2/3(Activate)
* Enhancer: H3K27ac(Activate) H3K4me2/1(Acivate)

> 位于组蛋白N末端, 不仅存在于H3上

##### Combination of Histone Code

* H3K4me3 + H3K36me3(transcription elongation) $\rightarrow$ Activate

### Non-coding RNA

* microRNA
* 长链非编码RNA

---

### ChIP-seq

> 染色质免疫共沉淀

#### 实验操作

1. Bacteria cell culture
2. Cross-linking (Fix with formaldehyde)
3. Sonication (DNA fragmentation)
4. Input (Only sonicated DNA)
5. Purification and quantification of ChIP-DNA

> 对照很重要

对照的作用：

* 降低背景噪声bias

#### 数据处理

```reads``` -> ```alignment``` -> ```signal construction``` -> ```peak calling``` -> 扫motif -> ?

#### 算法

* call peak: MACS算法 (泊松分布相关)
  * [link](https://www.jianshu.com/p/390f6d57488d "Link")
* reads 回帖
  * bowtie
  * tophat
  * BWA
* Tools for Motif Scan
  * MDScan
  * MEME
  * HOMER
  * MDSeqPos

> 计算转录水平: cufflinks

### TF

* Basal Transcription Regulation
* Differential enhancement of transcription
* Development
* Response to intercellular signals
* ...

#### Regulation

* Synthesis
* Nuclear localization
* Activation
* Accessibility of DNA-binding site
* Availability of other cofactors/transcription factors
* ...

#### TF Binding Motif DB / Motif Knowledgebase

* Jaspar

---
> 2019-10-10

1. ?
2. ?
3. ?
4. Conserve <-> functional ? => functional -> conserve
5. 多个TF相互作用
6. Cell Type-Specific Binding

Concepts:

* p值
* 控制错误发生率：控制p值更低
* Q值,校正P值
* BH法校正P值

Info:

1. 基因组版本
2. 物种
3. 基因
4. fastaq文件

### DNase-Seq, MNase-Seq

* DNase-Seq: identify the location of regulatory regions
  * 限制性内切酶 (DNase I)
  * 实验难做
  * 酶切时间不好控制
  * 细胞量要求大，也可单细胞
  * 在染色质致密区域，DNA链被致密结构很好地保护起来，使得内切酶无法接近这些区域，只能切割开放区域的DNA。同样，在开放区域，缠绕在核小体上的DNA被核小体结构所保护，只有核小体之间的DNA序列能够被DNase I切割，这些区域内能够被DNase切割的位点也被称为DHS，即DNase超敏感位点（DNase hypersensitive sites）
* MNase-Seq: 核小体排布,
  > __DNase-seq__ is DNase I digestion combined with high-throughput DNA sequencing to get sites of digestion at single base-pair resolution. It’s kind of the "yin" to MNase-seq’s "yang", providing inferred info on chromatin-binding proteins that lie between hypersensitive sites, whereas __MNase-seq__ maps protected regions. Both methods require another technique, such as ChIP-seq, for identifications of bound elements, though. (<https://epigenie.com/three-ways-to-get-intimate-with-epigenetic-marks/)>
  * 限制性外切酶
  * 和DNase-seq原理类似，探测区域互补；MNase-seq使用的酶是限制性外切酶，将不受保护的区域统统切除，只余下核小体上缠绕的DNA序列
  * MNase-Seq数据 不能用Macs call peak
  * 细胞量要求大
* FAIRE-Seq
  > FAIRE-Seq (Formaldehyde-Assisted Isolation of Regulatory Elements) is a method in molecular biology used for determining the sequences of DNA regions in the genome associated with regulatory activity. The technique was developed in the laboratory of Jason D. Lieb at the University of North Carolina, Chapel Hill. In contrast to DNase-Seq, the FAIRE-Seq protocol doesn't require the permeabilization of cells or isolation of nuclei, and can analyse any cell type. In a study of seven diverse human cell types, __DNase-seq and FAIRE-seq produced strong cross-validation__, with each cell type having 1-2% of the human genome as open chromatin.
  * 使用甲醛固定
  * 与chip-seq一样也用超声来打断
  * 信噪比低

### ATAT-Seq

> 全称Assay for Transposase Accessible Chromatin with high-throughput sequencing，即利用转座酶研究染色质可进入性的高通量测序技术。

* ATAC-seq出来的结果，和传统方法出来的结果具有很强的一致性
* 同时也和基于组蛋白修饰marker的ChIP-seq有较高的吻合程度
* 而相比起来，ATAC-seq的重复性，比MNase-seq和DNase-seq的更强，操作起来也更加简单，而且只需要很少的细胞/组织量
* 同时出来的信号更加漂亮
* 目前已经是研究染色质开放性首选的技术方法。
* (<https://www.zhihu.com/question/263776928/answer/273229159)>

* 同时具有MNase-Seq得到的核小体排布信息以及可由DNase-Seq/FAIRE-Seq得到调控区域信息
* 要考虑去除线粒体的问题

ATAC-Seq与ChIP-Seq的不同的是ATAC-Seq是全基因组范围内检测染色质的开放程度，可以得到全基因组范围内的蛋白质可能结合的位点信息，一般用于不知道特定的转录因子，用此方法与其他方法结合筛查感兴趣的特定调控因子；但是ChIP-Seq是明确知道感兴趣的转录因子是什么，根据感兴趣的转录因子设计抗体去做ChIP实验拉DNA，验证感兴趣的转录因子是否与DNA存在相互作用。ATAC-Seq、ChIP-Seq、Dnase-Seq、MNase-Seq、FAIRE-Seq整体的分析思路一致，找到富集区域，对富集区域进行功能分析。

### Super-Enhancer

> 2019/11/28

#### Feature

* 高表达
* 高调控
* 招募的TF数量众多
* 多个enhancer相互协作, 且较为密集

#### Conclusion

> Embryonic stem cell，ESCs

* Large Genomic Domains Occupied by Master Transcription Factors and Mediator in ESCs
* Super-Enhancers Are Associated with Key ESC Identity Genes
* Super-Enhancers Are Cell-Type Specific and Mark Key Cell Identity Genes

## Reference👩‍💻

1. 📺 [StatQuest: A gentle introduction to ChIP-Seq](https://www.youtube.com/watch?v=nkWGmaYRues)
2. 📺 [MIT 7.91J: 7. ChIP-seq Analysis; DNA-protein Interactions](https://www.youtube.com/watch?v=Ob9xGBPvr_s)