---
layout: post
title: sPlot方法
date: 2025-08-07 17:46:00+0800
description: notes for sPlot method
tags: statistics math
categories: math
related_posts: false
---

　　sPlot方法是高能物理实验中广泛应用的一种统计学方法，用于分析包含多种source的数据样本。例如，我们从探测器获得的data包含了signal和background两个部分，我们希望得到signal的各种变量的分布，可以通过质量谱提取signal的分布再通过sPlot方法得到其他变量的signal分布。本文将简述sPlot方法的基本原理以及一些例子，主要参考文献[arXiv:physics/0402083](https://arxiv.org/abs/physics/0402083)。

　　本方法用于分析包含了多种source（例如signal，部分重建本底，组合本底，misID等）的事件构成的数据样本。假设事件可以用一系列变量（例如B_M, B_IPCHI2OWNPV等）描述，这些变量可以被划分为两类。对于第一类变量，不同来源的事件的分布是已知的，我们称之为discriminating variable；第二类变量则是未知的，我们称之为control variable。

　　我们的目标是利用discriminating variable的信息推断不同source的control variable的分布而无需任何关于control variable的先验知识。sPlot方法的一个必要假设是control variable与discriminating variable是不相关的。

## 1. Basics

### 1.1 Likelihood method

　　考虑一个包含不同source的数据样本的扩展似然分析(extended Likelihood analysis)，对数似然函数可以写为：

\begin{equation}
\lable{eq:log-liklihood}
\mathcal{L} = \sum_{e=1}^N\ln \big[\sum_{i=1}^{N_s}N_if_i(y_e)\big]-\sum_{i=1}^{N_s}N_i
\end{equation}

其中
- $N$是样本中总的事件数；
- $N_s$是组成样本的事件的source的种数；
- $N_i$是第i类source的期望事件数（在扩展似然分析中总数是不定的）；
- $y$是discriminating variables的集合
- 
