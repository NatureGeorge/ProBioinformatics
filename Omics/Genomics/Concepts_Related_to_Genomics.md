# Concepts Related to Genomics
> Last Modified Time 2019-09-05

[toc]

## Genome Map

### Genetic Mapping

#### 基因标记
* allele
  * ABO血型
  * 人白细胞抗原

#### DNA标记
* RFLP(限制性长度多态性) $\rightarrow$ 1980, 第一代DNA分子标记技术
* SSLP(简单序列长度多态性)
  * 小卫星序列
  * 微卫星序列
* SNP

### Physical Map
优点:
* 比遗传图分辨率高
* 比遗传图覆盖率更高 (其因随机交换限制)
* 比遗传图分子标记更准确

#### Method
* 限制性酶切作图 (Restriction Map)
* 基于克隆的基因组作图
  * BAC 细菌人工染色体
  * YAC 酵母人工染色体
* 染色体细胞图 (原位杂交)
* STS作图
  * 距离模型: Maximum likelihood approach
* 辐射杂交作图

## 测序
### WGS(全基因组测序)策略
#### 作图法测序
> Up to Dowm
1. 高密度分子标记遗传图和大分子DNA克隆重叠群
2. 将单个大分子DNA克隆逐个测序
3. 序列组装

#### 鸟枪法测序
> Bottom to Up
1. 全基因组鸟枪法随机测序 (小片段)
2. 搭建重叠群, 并到大分子克隆内
3. 以分子标记为基点将其锚定到染色体上

### 测序方法
* 链终止法/Sanger法 (一代测序方法/Sanger测序技术, 易于机械操作与程序化控制 $\rightarrow$ 快速自动化测序)
* 化学降解法
* 聚丙烯酰胺凝胶电泳
* 荧光染料标记
  * 由荧光显微镜捕获信息, 计算机图像解析
  * 但是信号捕捉存在缺陷
    * 不同荧光间的干扰
    * 荧光激发时间的不同
* 光点测序 (Pryosequencing)
* DNA芯片测序 (局限性大 $\rightarrow$ __Deprecated__)
* NGS (Next Generation Sequence)
  * SBS
  * SBL
* 单分子测序技术 (测序长度更长, 以kb为单位)

#### 二代测序特点
* 单端测序
* 双端测序
  * $\le 300bp$
* Read Mapping (Cost a lot)
  * Raw FastQ -> Mapped SAM -> Mapped BED
  * output: SAM/BAM or BED
  * SAM/BAM (处于alignment阶段)
  * SAM $\leftrightarrow$ BAM
  * SAM $\leftrightarrow$ FastQ
  * BWA

##### ChIP-seq
> 染色质免疫共沉淀

```reads``` -> ```alignment``` -> ```signal construction``` -> ```peak calling```

##### ATCG-seq
一套数据，两种处理方式,分别得到：
1. 染色质可及性
2. 核小体排布

#### 三代测序


### 需注意的问题
* 基因组测序的覆盖面 $P_0 = e^{-m}$
  * $P_0$: 丢失概率
  * $e$: 自然对数底数
  * $m$: 覆盖面(单倍体基因组数)
* Physical Gap $\rightarrow$ 构建基因组文库时丢失的DNA序列
* Sequence Gap $\rightarrow$

### 常用数据库
* GOLD (Genome OnLine Database)

### 测序模拟 (NGS read simulator)
* 用以评估测序仪正确率
* 利用经验模型(Error Model, 根据已有数据得出, 与一代测序数据比对得到统计信息)

#### 软件(e.g)
* ART
* Wessim
* ...


## 序列组装（Genome Assembly）
### 原理
* Multiple copies of Genome
* (碎片化)
* Sheared random fragments
* (电泳过滤)
* Size fractionated fragments
* (BAC/YAC)
* 建库
* Reads (双末端测序)
* (Overlap)
* Contigs
* Scaffolds (mate-pair reads)

### 组装策略
* 从头组装
  * 可以发现基因组装中...
  * 基因组的覆盖度容易受到非编码区域重复序列变化的影响
  * 重复序列也在基因组装配形成重叠群时产生歧义
* 有参组装 (但无法解释可变剪切)
  * ...

#### 二组学的组装
_基因组组装与转录组组装的方法不一样_
Difference：
1. 基因组的测序深度在基因组中通常(?)是相同的 (例外@GC偏移)
2. 在基因组测序中两条链都会被测序
3. 转录组的测序深度可能变化很大
4. RNA-seq 是链特异性的
5. 歧义问题： 同一个基因的不同转录变异体其中有共同的外显子

### 组装遇到的难点
* 测序错误
* 重复序列
* 多态性变异
* 倒位
* 覆盖率

### 组装软件
* 转录组: Trinity
  > de novo transcriptome assembly from RNA-Seq data. Trinity assembles transcript sequences from Illumina RNA-Seq data.
* 转录组: TopHat
  > TopHat is a fast splice junction mapper for RNA-Seq reads. It aligns RNA-Seq reads to mammalian-sized genomes using the ultra high-throughput short read aligner Bowtie, and then analyzes the mapping results to identify splice junctions between exons.
* 基因组: Bowtie/Bowtie2
* 基因组: SOAPDenovo

### 组装算法
__Greedy Algotithm__
* De novo
  * Hamilton path
* 比较组装
  * Eulerian path

> SSAKE

#### 算法流程1
1. Overlap Discovery (所有Reads 两两比较)
2. 启发式算法
  * K-mer size
  * Minimum overlap length
  * Minimum ..
  * 参数越大，组装越精确但contigs也越短
3. overlap graph 的
4. 多序列比对，确定readout

#### 算法思想1
* 把每个Reads看作一个节点
* 若两reads存在overlap(符合阈值)， 就在相应节点之间建立一条边
* 所有reads通过overlap关联，构造有向图
* 通过寻找图中经过每个节点一次且仅一次的路径

#### 算法流程2
> de Bruijn graph

1. 构建k-mers
2. k-mer 之间

##### 问题
1. 错误Reads
2. 分支问题 (需过滤)
3. Gaps


#### 算法思想2

### 基因组建模 (20191114)

#### ```GT...AG``` Rule
> 用以识别内含子范围:前体RNA中参与内含子剪接的两个特殊位点，即在内含子和外显子交界处有两个相当短的保守序列:5'端为GT, 3'端为 AG,称为GT-AG规律。GT-AG规则主要适用于(或是全部)真核生物基因的剪接位点。
