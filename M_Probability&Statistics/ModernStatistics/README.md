# Basic Concepts of Modern Statistics🐱‍🏍

```txt
Created Date: Sunday, December 29th 2019, 4:00:12 pm
Author: ZeFeng Zhu
```

## Basic Statistical Test

### Key🎯

* 统计与变异性
  * 根本上，统计学处理变异性及变异性不同的原因
  * 对于生物学中许多来源的变异性定量化是很重要的
    * 包括实验的不精确
    * 同一物种不同生物个体间的差异
    * 环境中的差异
* 检验的统计学意义
  * 统计学显著性检验的目的是辨别具有真正(生物学 etc.)意义的随机变化所导致的影响
* t-检验与替换
  * t-检验的目的是检验正态分布数据的平均值之间差异的显著性
  * Wilcoxon Test/Mann-Whitney Test for non-norm dist etc.
* 方差分析
  * 实验中有两组以上数据时，量化组平均值差异的显著性
* 卡方检验(Chi-square test)与Fisher精确检验(Fisher's exact test)
  * 经常用于用关联表表示的离散“计数”型数据
  * 目的是评价：如果零假设是真的，期望的计数之间的统计学意义，以及每个类别中的实际观察计数
* 基于再取样的检验
  * 为了计算p值，假定零假设是真的，替换大多数的统计检验，并且通常包含数据的随机化取样
* 多重检验
  * 当进行一次以上的统计检验时，有必要对多个采样进行校正，能给出一个不正确的小p值
  * Bonferroni校正
  * Benjamini-Hochberg校正

### 统计与变异性

* 描述性统计
* 算术平均值
* 中位数
* 标准差
* 异常值
* 四分位数

### 检验的统计学意义

__A frequently asked question:__ 大量的变异性是否归因于一个特定的因素?

__For instance:__

* 糖尿病患者与无该病的患者相比是否血糖水平有所不同? $\Leftrightarrow$ 两组患者之间测量的血糖变异性是否明显区别于其他因素的变异性?

__How to solve:__

* 利用统计显著性检验来区分随机发生的变异性(, 来看是否数据能够给出血糖水平差异的确实证据)
* 统计显著性检验基于零假设，即“观察到的效应是由于随机发生”的假设
* 进一步计算**在零假设为真的条件下**的概率，称该概率为p-value
  * 如果p-value足够小，那么零假设就不成立，效应就不是随机发生
  * 若零假设的p-value小于0.05(95%显著性水平)或更小，小于0.01(99%显著性水平)，这种情况常**被**认为效应是显著的
  * 表明显著性水平的p-value是由试验者来设定的，p-value越小，假阳性(随机效应被归于真)概率越小，但假阴性(真效应被归于随机)概率会增加

### t-检验与替换

* t-test基本假设是数据符合正态分布
* t-test (Student's t-test)是对样本均值进行的显著性检验
* 单因素t-test: 检验一个样本的均值与一些确定值是否存在显著性差异
  * e.g 检验溶液的蛋白质浓度，可以用标准的已知浓度作为参考物, 单因素t-test被用于检验用相同检测方法重复的测量是否与已知浓度存在差异
* 双因素t-test: 两个样本的均值与其他每一个值之间是否存在显著性差异
* Paired t-test: 
  * e.g 5个志愿者餐前餐后测量的血糖水平数据可分为2组，数据不是相互独立的；同一人的数据是配对的；paired t-test就是把5个人的10个数据转化为5个餐前与餐后的血糖水平之差，然后用单因素t-test，看该差值的均值是否与0存在显著性差异
* 当数据不是正态分布时，可使用Wilcoxon检验，进行非参数检验

__Some details about the answer of the mentioned question:__

1. 检验数据是否符合正态分布
2. 如若不是则尝试剔除异常值再检验是否符合正态分布，若符合则进行下一步
3. 双因素t-test
4. 采用标准差作为变异度，且得到p-value
5. 进行判断

### 方差分析

* 与t-test一样也检验数据组均值之间是否存在统计显著性差异，但是其可以用于超过2组的数据检验
* 以方差为测量变异度的指标
* Summary:
  * 首先把所有数据混起来作为一组数据，计算总体均值与总体方差
  * 总体方差分解为两部分：
    * 组内方差 (每组数据各自的方差)
    * 组间方差 (不同组均值间的方差)
  * 如果组间方差比组内方差更高，那么表示效应更显著；反之随机因素更显著
  * 零假设：所有组的数据均满足相同均值的正态分布
  * 也有表示零假设概率的p-value

__Sample problem:__ 研究10种药物对血糖的影响，每一组有20人服用同一种药物(包括对照组)，(更复杂的分组：20人一组中男女各10名的子组等)

__How to solve:__

1. 方差分析，看组内方差与组间方差的大小关系😀
2. t-test两两比较45次，多重检验校正p-value😨

### Chi-square test & Fisher's exact test

__The reason to perform Chi-square test:__ 一些变量例如血糖水平是连续变化的，原则上可以取任意值；但**分类变量**只能取一系列离散值。分类变量可以用于定义t-test和方差分析组，但有时需要当作因变量，并对它们的值进行统计显著性检验，常用的方法就是Chi-square($\chi^{2}$) test。

__Sample Problem:__ 

* 表中数据是一种植物的3个变异体遭受的旱灾应激
* 实验观察到的基因数目符合正态分布
* 问题：变异体是否对应激有不同的反应
* 零假设：这些变异体对应激没有不同的反应
* 斜体数字给出每个种类期望的基因数，期望值建立在零假设为真的基础上 (e.g $43.8 = \frac{130}{178}*55$)

|   |变异体A|变异体B|变异体C|总合|
|---|---|---|---|---|
|相关上调基因应激数|55 (*43.8*)|30 (*46.0*)|45 (*40.2*)|130|
|无变化表达数|5 (*16.2*)|33 (*17.0*)|10 (*14.8*)|48|
|总合|60|63|55|178|

* 统计检验关注的就是观察计数(O)与期望计数(E)相互之间是否存在显著性差异
* step:
  * 先计算6格总合的$\chi^{2}$统计量$(O-E)^{2}/E$
    * 这个总合越大说明零假设为真的概率越大
  * p-value由$\chi^{2}$统计量的概率分布函数得到
* 若2*2分类表的数据小于等于5，则不能用卡方检验，可以用费歇尔精确检验提替代

## Nonparametric tests

### Key🎯

* 拟合优度检验
  * Q-Q plot `qqnorm(), qqline(), qqplot()`
  * 正态性W检验方法
    * 利用Shapiro-Wilk的W统计量作正态性检验
    * `shapiro.test()`提供W统计量以及p-value
    * 零假设: 样本来自于正态分布的总体
    * Large p-value does not prove that the distribution is normal - just not significantly differnet from normal
    * But it is too sensitive - one should use histogram/Q-Q plot when assessing t test/ANOVA assumptions
  * 经验分布的Kolmogorov-Smirnov检验方法
    * `ks.test()`
    * 单个总体的检验
      * 零假设: X具有分布F
      * 理论上可以检验任何分布
      * 经验分布函数$F_n(x)$是总体分布函数$F(x)$的估计
      * 经验分布拟合检验的方法是检验$F_n(x)$与假设的总体分布函数$F_0(x)$之间的差异
      * KS统计量: $D=\text{sup}_{-\infty \lt x \lt \infty} |F_n(x)-F_0(x)|$
    * 两个总体的检验
      * 零假设: $F(x)=G(x)$
    * 与Pearson$\chi^{2}$检验相比
      * 不需要将样本分组，少一个任意性
      * 但是只能用在理论分布为**一维连续分布且分布完全已知**的情况下，适用面更小
      * 但在可用场合下其功效一般略优于Pearson检验
  * Neyman-Pearson拟合优度$\chi^{2}$检验
    * `chisq.test(x, p=p)`
    * 理论分布已知
      * 零假设: X具有分布F 
      * 分组后每组的频数要大于等于5，否则需要合并组或采用其他方法(Fisher's exact test)
    * 理论分布未知，依赖于若干个未知参数
      * 通过样本做出各个参数的最大似然估计，再检验假设: $H: \text{X具有分布}F(x,\hat{\theta_{1}},\hat{\theta_{2}},...,\hat{\theta_{r}})$
      * 然后再按理论分布已知的情况进行处理
      * 但是自由度变为$m-1-r$，即自由度减少了r
* 列联表(Contingency table)数据的独立性检验
  * Pearson$\chi^{2}$检验
    * 输入列联表数据，`chisq.test()`即可作独立性检验
  * Fisher's exact test
    * 应用: 样本较小(单元的期望频数小于(等于)4)
    * 最初是针对2*2这种特殊列联表提出
    * 建立在超几何分布的基础上
    * `fisher.test()`
* 符号检验 (Sign test)
  * 检验一个样本是否来自某个总体
    * ie. `binom.test(sum(X>99), length(X), al="l")`
  * 用成对样本来检验两个总体间是否存在差异
    * ie. `binom.test(sum(x<y), length(x))`
* 秩检验
  * 秩统计量 (Rank statistics)
    * 分布无关性 (distribution-freeness)
  * 秩相关检验
    * Spearman秩相关检验
    * Kendall相关检验
  * Wilcoxon秩检验
    * 对来自一个总体样本的检验
    * 非成对样本的秩次和检验

### Sign test⚫⚪

#### 检验一个样本是否来自某个总体

假设某个总体的中位数为$M_0$,如果样本中位数$M=M_0$，我们就接受样本
来自某个总体的假设。

其具体的检验方法是这样的:

* 首先从每个样本观察值中减去总体中位数$M_0$，得出的正、负差额用正(+)、负(-)号加以表示
* 若总体中位数等于样本中位数，即$M=M_0$，那么，样本观察值在中位数上、下的数目应各占一半，因现时出现正号或负号的概率应各占1/2
* 设样本容量为n就可以用二项分布$B(n,1/2)$来计算出现负号（或正号）个数的概率
* 从而根据一定的显著性水平作出是否接受原假设$H_0: M=M_0$的判定

#### 用成对样本来检验两个总体间是否存在差异

符号检验法也可用于以成对随机样本观察值来检验两个总体之间是否存在
显著差异。

如果两个总体无显者差异，则两个成对随机样本观察值正、负差额的个数应大体相等．假定$x_i-y_i\gt 0$用正号表示，$x_i-y_i\lt 0$用负号表示，则如果两个总体无显显著差异，那么出现正号和负号的概率各占1/2，和上面检验样本是否来自某个总体一样，可用二项分布$B(n,1/2)$，根据一定的显著性水平和正号（或负号）的个数，作出接受或拒绝两个总体无显著差异的判断

### 秩检验🎢

#### 秩相关检验

> Pearson相关检验针对于正态分布总体的数据，秩相关检验并不要求所检验的数据来自正态分布的总体

* a measure of the strength and direction of **the monotonic relationship** between two variables
* Monotonicity is less restrictive than that of a linear relationship

##### Spearman秩相关检验

* measures the strength and direction of monotonic association between two variables
* But a monotonic relationship is **not** strictly an assumption of Spearman's correlation. One can run a Spearman's correlation on a non-monotonic relationship to determinine if there is a monotonic component to the association
* For linear relationships, Pearson and Spearman correlations are nearly same
* For non-linear relationships, Pearson and Spearman correlations are different

##### Kendall相关检验

* A coefficient that represents the degree of concordance between two columns of ranked data
* The greater the number of "inversions" the smaller the coefficient will be

#### Wilcoxon秩检验 (Wilcoxon Signed Rank Test)

* 弥补符号检验的不足，在一定程度上考虑样本观察值与总体中位数之间的差额，不仅是符号(表征位于中心位置的哪一边)还有值来表征距离中心位置的远近
* 假设
  * 总体分布是连续的
  * 总体对其中位数是对称的
* `wilcox.test(x, y=NULL, alternative=c("two.sided", "less", "greater"), mu=0, paired=FALSE, exact=NULL, ...)`
  * mu: 待检参数，如中位数

##### 对来自一个总体样本的检验

* 检验一个样本是否来自某个总体 `wilcox.test(X, mu=140, alternative="less", comf.int=TRUE)`
* 用于对成对样本的检验，从而说明两个总体是否存在显著差异 `wilcox.test(x, y, akternative="greater", paired=TRUE)`

##### 非成对样本的秩次和检验

* 两非成对样本要检验其对应两个总体的中位数是否想等(若中位数相等，则认为两个总体无差异)
* Wilcoxon-Mann-Whitney统计量U
* 两组样本可以不平衡
* `wilcox.test(x, y, alternative="less", exact=FALSE, correct=FALSE)`

## 多元数据的数据特征与相关分析

### 协方差

* 协方差(corvarience)能分辨出两变量的关系:
  * 正相关 OR
  * 负相关 OR
  * 无相关
* But covariance is a **computational stepping stone** to something that is interesting, like correlation and PCA...
* Covariance values are **sensitive to the scale of data** and this makes them difficult to interpret
  * Covariance does not tell if the points are relatively close the line and if the slope is steep or not

### 相关系数 (Coeffcient of Correlation)

* Quantity the strength of the relationship(i.e bewteen X and Y) with correlation
  * Not 'CAUSE & EFFECT', just 'RELATION'
  * the more closer the data are to the line, the more X can tell about Y (given a x value, we might guess that the value for y falls in a smaller range)
* Maximum value for correlation is 1, minimum value is -1
* Does **not depend on the scale of data** (due to the denominator)
* But does not show the slope and need enough data to increase confidence
* Note: when talks about correlation, only use straight line
* For correlation, a p-value tells us the probability that randomly drawn dots will result in a similarly relationship, or stronger
* p-value越小，对预测结果的confidence越大
* 样本点的增加本质上是增加confidence，相关系数不一定增加

> $R^{2}$将会来解决两个相关关系哪个更好的问题(单看相关系数无法判断)

### 二元数据的数据特征与相关系数

* 二元总体$(X,Y)^{T}$

$$
A = \begin{bmatrix} 
x_{1} & x_{2} & ... & x_{n} \\
y_{1} & y_{2} & ... & y_{n} \\
\end{bmatrix}
$$

* 观测样本的协方差阵

$$
S = \begin{bmatrix} 
s_{xx} & s_{xy}\\
s_{xy} & s_{yy}\\
\end{bmatrix}
$$

* 观测样本的相关系数

$$r=\cfrac{s_{xy}}{\sqrt{s_{xx}}\sqrt{s_{yy}}}$$


* R函数
  * 计算协方差阵: `cov(x, y=NULL, use="all.obs", method=c("pearson", "kendall", "spearman"))`
  * 计算相关系数矩阵: `cor(x, y=NULL, use="all.obs", method=c("pearson", "kendall", "spearman"))`

### 二元数据的相关性检验

* 总体的相关系数

$$\rho(X,Y)=\cfrac{\text{cov}(X,Y)}{\sqrt{\text{var(X)var(Y)}}}$$

* 当样本个数n充分大时，$r_{xy}$可以作为$\rho(X,Y)$的估计
* Question: 当样本个数n至少取到多少时，样本相关才能保证总体相关
* Anwser: 确认总体是否相关最有效办法是作总体$(X,Y)^{T}$的相关性检验
  * 可以证明，若$(X,Y)^{T}$是二元正态总体，且$\rho(X,Y)=0$，则统计量 $t=\cfrac{r_{xy}\sqrt{n-2}}{\sqrt{1-r_{xy}^{2}}}$服从自由度为n-2的t分布
  * 利用上述性质即可进行X和Y的相关性检验
  * 此时相关系数$r_{xy}$被称为Pearson相关系数，因此被称为Pearson相关性检验
* `cor.test(x, y, alternative=c("two.sided", "less", "greater"), method=c("pearson", "kendall", "spearman"), exact=NULL, conf.level=0.95, ...)`

## Linear Regression

### 一元线性回归

* 回归参数的估计
  * 最小二乘法
  * ...
* 回归方程的显著性检验
  * t-test
  * F-test
  * 相关系数检验
* Related R function: `lm(), summary(), anova(), predict()`
* 参数$\beta_{0}, \beta_{1}$的区间估计
* 预测
* 控制

### 多元线性回归

* 回归系数的估计
* 显著性检验
  * 回归系数的显著性检验
  * 回归方程的显著性检验
* 参数$\beta$的区间估计
* 预测
* 修正拟合模型

### 逐步回归

* `step()`

### 回归诊断

* WHAT
* 残差分析
  * 残差图
* 影响分析
* 多重共线性

## 方差分析

### one-way ANOVA

* `aov(formula, data=NULL, ...)`
* 均值的多重比较
  * 多重t-test
    * `pairwise.t.test(x, g, p.adjust.method)`
  * p-value的修正
    * `p.adjust(p, method)`
* 方差的齐次性检验
  * 可加性
  * 独立正态性
    * `shapiro.test()`
  * 方差齐性
    * `bartlett.test()`
* Kruskal-Wallis秩和检验
  * 两样本的Wilcoxon方法在多于两样本时的推广
  * `kruskal.test(x, g)`
* Friedman秩和检验
  * paired(配伍组)设计中，多个样本的比较，若它们的总体不能满足正态性和方差齐次性的要求，可采用Friedman秩和检验
  * `fireman.test(y, groups, blocks, ...)`

### two-way ANOVA

* 不考虑交互作用
  * `aov(Y ~ A+B, data=data)`
* 考虑交互作用
  * `aov(Y ~ A+B+A:B, data=data)`
* 方差的齐次性检验 (same as one-way ANOVA)

## Reference👩‍💻

1. 📚 BIOINFORMATICS (2nd Edition) _T.Charlie Hodgman, Andrew French, David R.Westhead..._
2. 📚 统计建模与R软件 _薛毅, 陈立萍 清华大学出版社_
3. 📺 [StatQuest: P Values, clearly explained](https://www.youtube.com/watch?v=5Z9OIYA8He8)
4. 📺 [P-values and significance tests | AP Statistics | Khan Academy](https://www.youtube.com/watch?v=KS6KEWaoOOE) or [Hypothesis testing and p-values | Inferential statistics | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=-FtlH4svqx4)
5. 📺 [One-tailed and two-tailed tests | Inferential statistics | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=mvye6X_0upA)
6. 📺 [Z-statistics vs. T-statistics | Inferential statistics | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=5ABpqVSx33I)
7. 📺 [Pearson's chi square test (goodness of fit) | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=2QeDRsxSF9M)
8. 📺 [Contingency table chi-square test | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=hpWdDmgsIRE)
9. 📺 [StatQuest: Covariance and Correlation Part 1: Covariance](https://www.youtube.com/watch?v=qtaqvPAeEJY)
10. 📺 [StatQuest: Covariance and Correlation Part 2: Pearson's Correlation](https://www.youtube.com/watch?v=xZ_z8KWkhXE)
11. 📺 [Spearman Rank Correlation using R](https://www.youtube.com/watch?v=3R3z5uOFUic)
12. 📺 [Kendall's tau - Explained Simply + Examples (part 1)](https://www.youtube.com/watch?v=oXVxaSoY94k)
13. 📺 [9: Shapiro-Wilk test](https://www.youtube.com/watch?v=dRAqSsgkCUc)
