---
layout: page
title: Cabibbo-Kobayashi-Maskawa 矩阵
permalink: /cpv_lectures/ch2/
nav: false
---

### 2.1. 幺正三角形

1) $n\times n$ 的复矩阵有 $2n^2$ 个实参数，幺正条件一共 $n^2$ 个约束；

2) 夸克相位可以任意选取，但全局相位无关紧要，所以可以去掉 $2n-1$ 个夸克相位；

因此CKM矩阵一共有 $2n^2-n^2-(2n-1)=(n-1)^2$ 个自由参数，可将这些参数划分为欧拉角和相位

3) 一个 $n\times n$的正交矩阵可以用 $\frac{1}{2}n(n-1)$ 个角度来描述；

4) 其余自由参数均为相位: $(n-1)^2-\frac{1}{2}n(n-1)=\frac{1}{2}(n-1)(n-2)$

在标准模型框架下CKM矩阵有三个欧拉角和一个相位，可以用来参数化CKM矩阵

$$
V_{CKM}=\begin{pmatrix}
c_{12}&s_{12}&0\\
-s_{12}&c_{12}&0\\
0&0&1
\end{pmatrix}
\begin{pmatrix}
c_{13}&0&s_{13}e^{-i\delta_{13}}\\
0&1&0\\
-s_{13}e^{i\delta_{13}}&0&c_{13}
\end{pmatrix}
\begin{pmatrix}
1&0&0\\
0&c_{23}&s_{23}\\
0&-s_{23}&c_{23}\\
\end{pmatrix}
$$

### 2.2. 矩阵元的大小