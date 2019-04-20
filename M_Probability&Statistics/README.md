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
