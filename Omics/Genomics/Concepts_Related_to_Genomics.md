# Concepts Related to Genomics
> Last Modified Time 2019-09-05

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
