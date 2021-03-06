# Concepts Related to Metabolomics

```txt
Created Date: Wednesday, September 11th 2019, 10:26:40 am
Author: ZeFeng Zhu
```

## Initial

> Jeremy Nicholson 英国帝国理工 1999

## Basic Concepts

### 代谢组学

作为全局系统生物学的基础和系统生物学的一个重要组成部分，代谢组学
是以物理学基本原理为基础的分析化学、以数学计算与建模为基础的化学
计量学和以生物化学为基础的生命科学等学科的交叉学科。

### 代谢组学研究的意义

* 信号释放，能量传递，细胞间通信等内许多生命活动都是受代谢物调控的。
* 代谢物更多地反映了细胞所处环境，这与细胞的营养状态、药物和环境污染物的作用以及其它外界因素的影响密切相关。
* 基因组学和蛋白质组学能够说明可能发生的事件，而代谢组学则反映确实已经发生了的事情。

### Pipeline

1. 样品的采集与制备：足量的代表性样品
2. 数据采集和标志物识别: 常用色谱-质谱联用, NMR [分离+检测与鉴定]
3. 数据分析: PCA, PLS, ANN
4. 代谢途径分析: 代谢轮廓分析和代谢组学分析

### 高通量筛选(High Throughput Screening, HTS) V.S 虚拟筛选(Virtual Screening, VS)

高通量筛选（High Throughput Screening, HTS）和虚拟筛选（Virtual Screening, VS）旨在从数量巨大的化合物库中发现一系列具有生物活性且结构新颖的化合物；前者可以直接或者间接地探测到化合物样品库中小分子与靶标蛋白质之间的相互作用；而后者则通过基于规则或性质模式识别以及分子对接方法对虚拟化合物库进行过滤，这些化合物库可以是 来源于试剂供应商甚至是尚未合成的（虚拟）化合物。

尽管高通量筛选流程已经通过机器人系统实现了高度自动化，但是相对虚拟筛选而言消耗的时间和金钱仍 然巨大：使用虚拟筛选完成一个一百万个化合物的数据库的筛选一般只需数个小时或者数天，但是高通量 筛选同样规模的化合物库则至少需要数月之久。

除此之外，不断发展的计算机软硬件条件（包括更快的CPU、并行等高性能计算技术的采用、更加快速的 对接和药效团匹配算法的提出）都会使虚拟筛选的筛选速度在未来得到大大的提高。

### 虚拟筛选

根据对靶标生物大分子的三维结构依赖程度的不同，目前的方法可以分为两类:

* 基于配体 (Ligand-Based, LB)
* 基于受体 (Receptor-Based, RB)

#### Ligand-Based

LB方法一般用于靶标蛋白质三维结构未知的情况下，即从已有的活性或毒性小分子结构（二维或者三维）中提取特定的信息，进而从数据库中搜寻与此信息相符（或者类似）的结构不同的分子

* 从单一结构的活性分子中提取信息
  * 基于相似性搜索
* 从多个不同结构的分子中提取的共有特征信息
  * 基于数据挖掘及机器学习的方法
  * 基于药效团模型匹配的方法

#### 分子描述符

分子描述符是对分子特征的描述，这种描述不依赖于分子的实验性质和其它计算性质。分子描述符的计算和选择很大程度上影响着模型的质量和通用性。

描述符按性质可以分为定量和定性两种：

* 其中定量描述符主要是对理化性质、分子组成、拓扑性质、量化性质等特征的描述
* 定性描述符常见的是分子片段类描述符。

按照分子结构又可将描述符分为零维到三维描述符:

* 其中零维描述符主要描述分子的构成
* 一维描述符指分子片段相关描述符
* 二维描述符一般指分子拓扑性质
* 三维描述符则是对分子三维结构性质的描述

#### 类药五原则

类药五原则，是辉瑞公司资深药物化学家Christopher A. Lipinski在1997年提出的筛选类药分子的基本法则，符合Lipinski规则的化合物会有更好的药代动力学性质，在生物体内代谢过程中会有更高的生物利用度，因而也更有可能成为口服药物。

类药五原则（rule of five）也称为Lipinski规则, 其内容如下, 一个小分子药物中要具备以下性质:

1. 分子量小于500
2. 氢键给体数目小于5
3. 氢键受体数目小于10
4. 脂水分配系数小于5
5. 可旋转键的数量不超过10个

### 生物标志物

* 生物标志物是指用于表征患者体内异常状态存在的分子物质
* 生物标志物(Biomarker)是指“一种可客观检测和评价的特性，可作为正常生物学过程、病理过程或治疗干预药理学反应的指示因子”，作为个体化医疗 的“关键词”之一，寻找和发现有价值的生物标志物已经成为当前医学领域 的研究热点。
* 生物标志物可以是和特定疾病特征相关的基因类信息（如单核苷酸多态性 SNPs、 DNA的甲基化或者mRNA）、蛋白质（如前列腺特异性抗原）或 代谢物（如葡萄糖、胆固醇等）。


### 分析化学: 仪器分析

#### 色谱法

* 流动相
* 固定相

##### 气相色谱

* e.g 高效液相色谱
* 加温操作
* 流动相(载气)为色谱惰性，不参与分配平衡过程

##### 液相色谱

* 常温操作

#### 质谱法

##### 原理

1. 进样系统
  * 气体扩散
  * 直接进样
  * 气相色谱
2. 离子源
3. 质量分析器
4. 观测器

##### 碎片离子峰
