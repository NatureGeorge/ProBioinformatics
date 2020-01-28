# Mathematical Modeling🌀🔥⚡

```txt
Created Date: Thursday, September 5th 2019, 10:57:07 am
Author: ZeFeng Zhu
```

## Progress

> 👶 👦 🧒 👨 👴

|   |Mathematical Modeling|Pattern Recognition|Machine Learning|
|---|---|---|---|
|Basic Knowledge|👦|👦|👶|
|Introduction|👦|👦|👶|
|Practice|👶|👶|👶|
|Pro|👶|👶|👶|

## Some Note

> Noted that following note may be error-prone

### Entropy (Measuring Information)

#### Definition of Shannon's Entropy

* 信息中有
  * 有意义信息(非冗余)
  * 无意义信息
  * 冗余信息
* Bit作为信息量(Information)的衡量方式
  * Bit = 0 or 1 (是或不是, 天然等概率)
  * Bit = Uncertainty divided by 2
* 对于Bit计算方法的两种直观理解方式
  * N种情况(state) -> log计算 -> 得到信息量 $\log_{2}^{N}$
    * 可以这样理解，N种情况等可能(Uncertainty divided by N, N is uncertainty reduction factor)，把所有情况赋予二进制编码, 为了完整描述每一情况，需要的二进制位数即是传递该情况所需的信息量
    * 在此种理解方式下
      * N只能为正整数?
      * 只适用于各个情况(state)<可能性/概率>均等的情况?
  * 直接log化概率 (MORE GENERAL) $-log_2^{p}$
* 从log计算来看, 对于概率越大的事件, 其对应信息bit越低; state越少对应信息bit也越低。反之越大。意味着越确定的事情bit越低(信息量越少)，反之越大。
* Measure the average amount of information
  * 相当于数学期望
  * $-\sum_{i}p_{i}log_{2}(p_{i})$
  * That's it, the formula calculates the entropy, which measures the uncertainty.
  * $H(\text{p}) = -\sum_{i}p_{i}log_{2}(p_{i})$, $\text{p}$为概率分布
    * it tells how unpredictable the probability distribution is.
    * 且在这里的信息都是有意义信息，无意义或冗余信息可以看作是为传递有意义信息而产生的成本，传递的信息的集合称为消息(message)

|Index|Weather|Possibility|Code|Information|Message|
|---|---|---|---|---|---|
|0  |🌞 |0.125|000|3 bits|3 bits|
|1  |⛅ |0.125|001|3 bits|3 bits|
|2  |☁ |0.125|010|3 bits|3 bits|
|3  |🌨 |0.125|011|3 bits|3 bits|
|4  |🌧 |0.125|100|3 bits|3 bits|
|5  |🌩 |0.125|101|3 bits|3 bits|
|6  |🌪 |0.125|110|3 bits|3 bits|
|7  |🌫 |0.125|111|3 bits|3 bits|

表1

* Cross-Entropy
  * 可以理解为传递消息(message)所需的期望信息量?
  * 表2中 $\text{Entropy} = 2.23 \,\text{bits},\, \text{Cross-Entropy} = 3\,\text{bits}$
  * 表3中 $\text{Cross-Entropy} = 2.42\,\text{bits}$
  * $H(\text{p, q})=-\sum_{i}p_{i}\log_{2}(q_{i})$, $\text{p}$为true概率分布, $\text{q}$为predicted概率分布
  * 提及的二表的Message列即为predicted distribution，由Code列决定
  * predicted possibility加和不一定为1
  * 如果预测良好(两distribution相等)，则Cross-Entropy与Entropy计算数值相等; 如果predicted distribution与true distribution存在差异，则Cross-Entropy将会比Entropy大(在message进行合理编码的情况下?)
    * $\text{Cross-Entropy}-\text{Entropy} \Rightarrow \text{Relative Entropy} \Rightarrow \text{Kullback-Leibler divergence}$
    * $\text{Cross-Entropy} = \text{Entropy} + \text{K-L divergence}$
  * K-L divergence:
    * $D_{KL}(\text{p}||\text{q})=H(\text{p, q})-H(\text{p})=-\sum_{i}p_{i}\log_{2}(q_{i})+\sum_{i}p_{i}\log_{2}(p_{i})=\sum_{i}p_{i}[log_{2}(p_{i})-log_2(q_{i})]=\sum_{i}p_{i}\log_{2}^{\cfrac{p_{i}}{q_{i}}}$
    * 特殊情形: $D(p||q)=p\log^{\cfrac{p}{q}}+(1-p)\log^{\cfrac{1-p}{1-q}}$
  * Cross-Entropy can act as a Cost Function: log Loss/Cross-Entropy Loss
    * $H(\text{p, q})=-\sum_{i}p_{i}\log(q_{i})$
    * 采用自然底数
    * 换底公式: $log_2(x)=log(x)/log(2)$

|Index|Weather|Possibility|Code|Information|Message|
|---|---|---|---|---|---|
|0  |🌞 |0.35|000|1.51 bits|3 bits|
|1  |⛅ |0.35|001|1.51 bits|3 bits|
|2  |☁ |0.1|010|3.32 bits|3 bits|
|3  |🌨 |0.1|011|3.32 bits|3 bits|
|4  |🌧 |0.04|100|4.64 bits|3 bits|
|5  |🌩 |0.04|101|4.64 bits|3 bits|
|6  |🌪 |0.01|110|6.64 bits|3 bits|
|7  |🌫 |0.01|111|6.64 bits|3 bits|

表2

|Index|Weather|Possibility|Code|Information|Message|
|---|---|---|---|---|---|
|0  |🌞 |0.35|00|1.51 bits|2 bits|
|1  |⛅ |0.35|01|1.51 bits|2 bits|
|2  |☁ |0.1|100|3.32 bits|3 bits|
|3  |🌨 |0.1|101|3.32 bits|3 bits|
|4  |🌧 |0.04|1100|4.64 bits|4 bits|
|5  |🌩 |0.04|1101|4.64 bits|4 bits|
|6  |🌪 |0.01|11100|6.64 bits|5 bits|
|7  |🌫 |0.01|11101|6.64 bits|5 bits|

表3 (unambiguous code)

|Code|Bit|Note|
|---|---|---|
|00 |2  |  |
|01 |2  |  |
|100    |3  |前2位已被上一级占，采用进位生成新前2位|
|101    |3  |  |
|1100   |4  |前3位已被上一级占，采用进位生成新前3位|
|1101   |4  |  |
|11100  |5  |前4位已被上一级占，采用进位生成新前4位|
|11101  |5  |  |

表4

#### Reference

1. [📺 Entropy, Cross-Entropy and KL-Divergence](https://www.youtube.com/watch?v=ErfnhcEV1O8)
