# Chapter one: 随机事件及其概率
## 1.样本空间
## 2.事件
### 事件的运算与关系
* 和事件 (并集) A $\cup$ B = {x| x $\in$ A or x  $\in$ B} $\Leftrightarrow$ A与B至少有一发生
* 积事件 (交集) A $\cap$ B = {x| x  $\in$ A and x  $\in$ B} $\Leftrightarrow$ A与B同时发生
* $\bigcup^{n}_{i=1}A_i\Leftrightarrow$ 该和事件发生 $\Leftrightarrow A_1,A_2,...A_n$ 中至少有一发生
* $\bigcap^{n}_{i=1}A_i \Leftrightarrow$ 该积事件发生 $\Leftrightarrow A_1,A_2,...A_n$ 同时发生
* 当AB = $\varnothing$, 称事件A与B不相容或互斥
* 差事件 A - B = {x $\in$ A and x $\notin$ B}
* A的逆事件(对立事件) $A \cup \overline{A} = S, A\overline{A} = \varnothing, \overline{\overline{A}} = A$
* **引入逆事件后,A与B的差事件可表示为$A - B = A\overline{B} = A\cup B - B = A - AB$**

### 事件的运算定律(集合的运算定律)
* 交换律 $A \cup B = B \cup A, A \cap B = B \cap A$
* 结合律 $A \cup (B \cup C) = (A \cup B) \cup C, A \cap (B \cap C) = (A \cap B) \cap C$
* 分配律 $A \cup (B \cap C) = (A \cup B) \cap (A \cup C), A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$
* 对偶律 $\overline{A \cup B} = \overline{A} \cap \overline{B}, \overline{A \cap B} = \overline{A} \cup \overline{B}$
* 对偶律推广 $\overline{\bigcap^{n}_{i=1}A_i} = \bigcup^{n}_{i=1}\overline{A_i}, \overline{\bigcup^{n}_{i=1}A_i} = \bigcap^{n}_{i=1}\overline{A_i}$
* __Attention:__ $\overline{AB} \ne \overline{A} \overline{B}, \overline{AB} = \overline{A \cap B}, \overline{A} \overline{B} = \overline{A} \cap \overline{B}$
* $\overline{AB} = (\overline{A} \overline{B}) \cup A\overline{B} \cup \overline{A}B \Leftrightarrow A,B不同时发生 = A,B都不发生 \cup A发生而B不发生 \cup B发生而A不发生$

Summary:
1. 至少有一发生
    * 和事件
    * $A \cup B$
    * $\bigcup^{n}_{i=1}A_i$

2. 同时发生
    * 积事件
    * $A \cap B$
    * $\bigcap^{n}_{i=1}A_i$

3. 都不发生
    * 至少有一发生的逆事件
    * $\overline{A \cup B} = \overline{A} \cap \overline{B}$
    * $\overline{\bigcup^{n}_{i=1}A_i} = \bigcap^{n}_{i=1}\overline{A_i}$

4. 不同时发生 $\Leftrightarrow$ __至少有一事件不发生 $\Leftrightarrow$ 最多有n-1个事件发生__
    * 同时发生的逆事件
    * $\overline{A \cap B} = \overline{A} \cup \overline{B}$
    * $\overline{\bigcap^{n}_{i=1}A_i} = \bigcup^{n}_{i=1}\overline{A_i}$

## 3.频率
### 频率的稳定值 -> p -> 概率
## 4. 概率
### 概率的统计性定义
> 当试验的次数增加时,随机事件A发生的频率的稳定值p称为概率,记为P(A) = p

### 概率的公理化定义
> 设随机试验对应的样本空间为S,对每个事件A定义P(A)满足三公理：
* 非负性: $P(A) \ge 0$
* 规范性: $P(S) = 1$
* 可列可加性: $A_{i}A_{j} = \varnothing, i \ne j \Rightarrow P(\bigcup^{\infty}_{i=1}A_i) = \sum^{\infty}_{i=1}P(A_i)$

#### 公理化定义推导出的性质
1. $P(\varnothing) = 0$
2. $P(A) = 1 - P(\overline{A})$
3. (有限可加性) $A_1,A_2,...,A_n,A_{i}A_{j} = \varnothing, i \ne j \Rightarrow P(\bigcup^{n}_{i=1}A_i) = \sum^{n}_{i=1}P(A_i)$
4. $A \subset B \Rightarrow P(B-A) = P(B) - P(A) \ge 0$ ; 一般情况: $P(B-A) = P(B) - P(AB)$
5. 概率加法公式: $P(\bigcup^{n}_{i=1}A_i) = \sum^{n}_{i=1}P(A_i) - \sum_{1 \leq i < j \leq n}P(A_{i}A_{j}) + \sum_{1 \leq i < j \leq k < n}P(A_{i}A_{j}A_{k}) + ... + (-1)^{i-1}P(A_{1}A_{2}...A_{n}))$

### 古典概型(等可能概型)
样本点有限且等可能
> 基本就是数数问题

1. 抽球问题(放回/不放回)(考虑顺序/不考虑顺序)
2. 分房问题
3. 随机取数问题

### 条件概率
$P(B) \ne P(B|A)$
> 缩小的样本空间:事件$A$的发生改变了样本空间,使它由原来的$S$缩减为新的样本空间$S_A = A$

> 以A的视角来看待B事件: B在A中所占的比例
#### 定义
$P(B|A) = \cfrac{P(AB)}{P(A)}, P(A) > 0$
#### 性质
$P(\bullet|A)$ 是概率, 因而满足三性:
* 非负性: $P(B|A) \ge 0$
* 规范性: $P(S|A) = 1$
* 可列可加性: $B_1,B_2,...,B_{i}B_{j} = \varnothing, i \ne j \Rightarrow P(\bigcup^{\infty}_{i=1}B_i|A) = \sum^{\infty}_{i=1}P(B_i|A)$

进而满足上述所有的概率性质
* $P(B|A) = 1 - P(\overline{B}|A)$
* $P(B \cup C |A) = P(B|A) + P(C|A) - P(BC|A)$
* $B \supset C \Rightarrow P(B|A) \ge P(C|A)$
* ...

#### 乘法公式
$P(AB) = P(A) \cdot P(B|A) = P(B) \cdot P(A|B)$
$P(A_{1}A_{2}\ldots A_n) = P(A_1)P(A_2|A_1)P(A_3|A_{1}A_2)\ldots P(A_n|A_1\ldots A_{n-1})$


### 全概率公式
#### 定义
$P(A) = \sum^{n}_{j=1}P(B_j)\cdot P(A|B_j)$
#### 证明
$\because A = AS = AB_{1}\cup AB_{2}\cup \ldots \cup AB_n,$

$AB_{i}AB_{j} = \varnothing , i \ne j$

$\therefore P(A) = \sum^{n}_{j=1}P(AB_j) \Leftrightarrow P(A) = \sum^{n}_{j=1}P(B_j)\cdot P(A|B_j)$

#### 样本空间的变换
若设$P(B_j) = p_j, P(A|B_j) = q_j, j = 1,2,\ldots,n$

则
$P(A) = \sum^{n}_{j=1}p{j}q_{j}$

### Bayes公式
#### 定理
> $设B_1,B_2,\ldots,B_n为S的一个划分且P(B_i) > 0.对P(A) > 0有Bayes公式:$

$P(B_i|A) = \cfrac{P(B_i)P(A|B_i)}{\sum^{n}_{j=1}P(B_j)P(A|B_j)} = \cfrac{p_{i}q_{i}}{\sum^{n}_{j=1}p_{j}q_{j}}$

**分母即为全概率公式，分子由乘法公式得到** ; $P(B_i)$ 为先验概率, $P(B_i|A)$ 为后验概率
