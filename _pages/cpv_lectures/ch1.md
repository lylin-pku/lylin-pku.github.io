---
layout: page
title: 标准模型中的CP破坏
permalink: /cpv_lectures/ch1/
nav: false
---

## 1.1. 宇称变换

考虑一个标量波函数$\psi(t,x,y,z)$，宇称变换作用于波函数得到

$$P\psi(t,x,y,z)=\psi(t,-x,-y,-z)$$

宇称变换可以视作相对于一个平面的镜像对称，然后绕垂直于这个平面的一根轴转动$\pi$角度. 由于角动量守恒，因此宇称变换反映了在镜面对称下物理量的变换. 宇称守恒意味着任何物理过程在镜面对称操作下保持不变.

众所周知，自旋是一个赝矢量，即在宇称变换下保持不变. 如果能找到一个相对于自旋方向能产生不对称分布的过程，就说明这个过程不满足宇称守恒.

另一种考察宇称是否守恒的方式是考虑粒子的螺旋度

$$h=\frac{1}{2}\vec{\sigma}\cdot\hat{p}$$

螺旋度在宇称变换下反号($P\hat{p}=-\hat{p}$)，因此若某个过程在产生粒子时存在一个偏好的螺旋度就说明这个过程宇称不守恒.

### 1.1.1 宇称破坏

1957年，Lederman等人利用$\mu$子衰变验证了在弱相互作用中宇称不守恒. $pp$对撞产生的$\pi$介子衰变产生$\mu$子

$$\pi^+\to\mu^++\nu_\mu$$

根据粒子物理的基本知识，$\nu_\mu$只具有一种螺旋度，由于$\pi$的自旋为0，因此$\mu$子也只具有一种螺旋度(自旋方向与动量方向相反). 发射的$\mu$子被石墨靶吸收停留下来.对石墨施加垂直于$\mu$子前进方向的磁场，$\mu$子在磁场中发生进动，在一定时间后发生衰变

$$
\mu^+\to e^++\nu_e+\bar{\nu}_\mu
$$

在某一特定方向探测衰变产生的正电子，记录一定时间内的电子数. 改变磁场大小，$\mu$子的拉莫尔进动频率发生变化，自旋相对于原始入射方向的转角发生变化，由于$\mu$子的螺旋度是唯一的，探测到的电子数会随着磁场变化呈现周期性振荡. 而如果$\pi$介子衰变过程宇称守恒，$\mu$子的自旋方向均匀分布，探测到的电子数不会呈现周期变化而是一个常数. 实验结果显示$\pi$介子衰变产生$\mu$子的过程确实破坏了宇称.

## 1.2 QED中的离散对称性：C,P,T

本小节中我们将推导$P,C,T$的算符表达式. 根据定义，变换后的波函数$\psi_P(\vec{x},t),\psi_C(\vec{x},t),\psi_T(\vec{x},t)$满足与自由场$\psi(\vec{x},t)$相同的运动方程. 

考虑狄拉克方程

$$\Big(i\gamma^\mu\frac{\partial}{\partial x_\mu}-\gamma^\mu eA_\mu-m\Big)~\psi(\vec{x},t)=0$$

展开为

$$\Big(\gamma^0[i\frac{\partial}{\partial t}-e\phi(\vec{x},t)]-\gamma^i[i\frac{\partial}{\partial x^i}-eA^i(\vec{x},t)]-m\Big)~\psi(\vec{x},t)=0$$

在宇称变换下

$$\Big(\gamma^0[i\frac{\partial}{\partial t}-e\phi(-\vec{x},t)]-\gamma^i[i\frac{\partial}{\partial (-x^i)}+eA^i(-\vec{x},t)]-m\Big)~\psi(-\vec{x},t)=0$$

注意到$(\gamma^0)^2=1,{\gamma^\mu,\gamma^\nu}=2g^{\mu\nu}$，因此$\gamma^0\gamma^i=-\gamma^i\gamma^0$，在上式左侧乘一个$\gamma^0$

$$\Big(\gamma^0[i\frac{\partial}{\partial t}-e\phi(-\vec{x},t)]-\gamma^i[i\frac{\partial}{\partial x^i}-eA^i(-\vec{x},t)]-m\Big)~\gamma^0\psi(-\vec{x},t)=0$$

满足原始的狄拉克方程，因此可以得知狄拉克旋量在宇称操作下的变换

$$
\boxed{\psi(\vec{x},t)\xrightarrow{\text{P}}\psi_P(\vec{x},t)=\gamma^0\psi(-\vec{x},t)=P\psi(-\vec{x},t)}
$$

注意可以保留一个任意相位$e^{i\phi}\gamma^0\psi(-\vec{x},t)$.

考虑电荷共轭变换$e\to -e$，狄拉克方程满足

$$
\Big(\gamma^0[i\frac{\partial}{\partial t}+e\phi(\vec{x},t)]-\gamma^i[i\frac{\partial}{\partial x^i}+eA^i(\vec{x},t)]-m\Big)~\psi_C(\vec{x},t)=0
$$

注意到$\gamma^0=\gamma^{0 *},\gamma^1=\gamma^{1 *},\gamma^2=-\gamma^{2 *},\gamma^3=\gamma^{3 *}$，对原始狄拉克方程取复共轭

$$
\Big(-\gamma^0[i\frac{\partial}{\partial t}+e\phi(\vec{x},t)]+\gamma^1[i\frac{\partial}{\partial x^1}+eA^1(\vec{x},t)]-\gamma^2[i\frac{\partial}{\partial x^2}+eA^2(\vec{x},t)]+\gamma^3[i\frac{\partial}{\partial x^3}+eA^3(\vec{x},t)]-m\Big)~\psi^*(\vec{x},t)=0
$$

左侧乘以$\gamma^2$得到

$$
\Big(\gamma^0[i\frac{\partial}{\partial t}+e\phi(\vec{x},t)]-\gamma^1[i\frac{\partial}{\partial x^1}+eA^1(\vec{x},t)]-\gamma^2[i\frac{\partial}{\partial x^2}+eA^2(\vec{x},t)]-\gamma^3[i\frac{\partial}{\partial x^3}+eA^3(\vec{x},t)]-m\Big)~\gamma^2\psi^*(\vec{x},t)=0
$$

考虑一个额外相位$i$得到

$$\psi_C(\vec{x},t)=i\gamma^2\psi^*(\vec{x},t)$$

利用$\bar{\psi}^T=(\psi^\dagger\gamma^0)^T=\gamma^0\psi^*$得到

$$
\boxed{\psi(\vec{x},t)\xrightarrow{C}\psi_C(\vec{x},t)=i\gamma^2\gamma^0\bar{\psi}^T(\vec{x},t)=C\bar{\psi}^T(\vec{x},t)}
$$

对时间反演后的复共轭狄拉克方程左侧乘$\gamma^1\gamma^3$

$$
\Big(-\gamma^0[i\frac{\partial}{\partial (-t)}+e\phi(\vec{x},-t)]-\gamma^1[i\frac{\partial}{\partial x^1}-eA^1(\vec{x},-t)]-\gamma^2[i\frac{\partial}{\partial x^2}-eA^2(\vec{x},-t)]-\gamma^3[i\frac{\partial}{\partial x^3}-eA^3(\vec{x},-t)]-m\Big)~\gamma^1\gamma^3\psi^*(\vec{x},-t)=0
$$

得到时间反演算符

$$
\boxed{\psi(\vec{x},t)\xrightarrow{T}\psi_T(\vec{x},t)=i\gamma^1\gamma^3\psi^*(\vec{x},-t)=T\psi^*(\vec{x},-t)}
$$

对于CP操作有

$$
CP\psi(\vec{x},t)=ie^{i\phi}\gamma^2\gamma^0\psi^*(-\vec{x},t)
$$

对于CPT操作有

$$
CPT\psi(\vec{x},t)=e^{i\phi}\gamma^5\psi(-\vec{x},-t)
$$

## 1.3.标准模型与CP破坏

### 1.3.1.Yukawa耦合与夸克混合

标准模型包括了$SU(3)\times SU(2)\times U(1)$规范相互作用，拉氏量由三个部分组成

$$
\mathcal{L}_{SM}=\mathcal{L}_{kinetic}+\mathcal{L}_{Higgs}+\mathcal{L}_{Yukawa}
$$

运动学部分描述了旋量场

$$
\mathcal{L}_{kinetic}=i\bar{\psi}(\partial^\mu\gamma_\mu)\psi
$$

其中$\psi$为三代费米子，分为五类

$$
Q_{Li}^I(3,2,+1/6),~~~u_{Ri}^I(3,1,+2/3),~~~d_{Ri}^I(3,1,-1/3),~~~L_{Li}^I(1,2,-1/2),~~~l_{Ri}^I(1,1,-1)
$$

$Q_{Li}$代表三代左手夸克，参与强相互作用，对应于$\mathfrak{su}(3)$的标准表示$\mathbf{3}$；同时参与弱相互作用，对应于$\mathfrak{su}(2)$的标准表示$\mathbf{2}$；对应的$\mathfrak{u}(1)$超荷为$1/6$.

$u_{Ri}$代表三代右手上夸克，参与强相互作用，对应于$\mathfrak{su}(3)$的标准表示$\mathbf{3}$；但不参与弱相互作用，对应于$\mathfrak{su}(2)$的平庸表示$\mathbf{1}$；对应的$\mathfrak{u}(1)$超荷为$2/3$.

$d_{Ri}$代表三代右手下夸克，参与强相互作用，对应于$\mathfrak{su}(3)$的标准表示$\mathbf{3}$；但不参与弱相互作用，对应于$\mathfrak{su}(2)$的平庸表示$\mathbf{1}$；对应的$\mathfrak{u}(1)$超荷为$-1/3$.

$L_{Li}$代表三代左手轻子，包括左手的$e,\mu,\tau$和对应的左手中微子，不参与强相互作用，对应于$\mathfrak{su}(3)$的平庸表示$\mathbf{1}$；参与弱相互作用，对应于$\mathfrak{su}(2)$的标准表示$\mathbf{2}$；对应的$\mathfrak{u}(1)$超荷为$-1/2$.

$l_{Ri}$代表三代右手轻子，包括右手的$e,\mu,\tau$，不参与强相互作用，对应于$\mathfrak{su}(3)$的平庸表示$\mathbf{1}$；也不参与弱相互作用，对应于$\mathfrak{su}(2)$的平庸表示$\mathbf{1}$；对应的$\mathfrak{u}(1)$超荷为$-1$.

例如其中$Q_{Li}^I(3,2,+1/6)$代表了

$$
\begin{pmatrix}
u_g^I&u_r^I&u_b^I \\
d_g^I&d_r^I&d_b^I
\end{pmatrix}_i=\begin{pmatrix}
u_g^I&u_r^I&u_b^I \\
d_g^I&d_r^I&d_b^I
\end{pmatrix},
\begin{pmatrix}
c_g^I&c_r^I&c_b^I \\
s_g^I&s_r^I&s_b^I
\end{pmatrix},
\begin{pmatrix}
t_g^I&t_r^I&t_b^I \\
b_g^I&b_r^I&b_b^I
\end{pmatrix}

$$


规范相互作用来源于将动能项的导数替换为协变导数

$$
\mathcal{L}_{kinematic}=i\bar{\psi}(D^\mu\gamma_\mu)\psi
$$

标准模型中协变导数定义为

$$
D^\mu=\partial^\mu+ig_sG^\mu_aL_a+igW_b^\mu\sigma_b+ig'B^\mu Y
$$

其中$L_a$为Gell-Mann矩阵，$\sigma_b$为Pauli矩阵. $G_a^\mu, W_b^\mu和B^\mu$分别为8个胶子场，自发对称性破缺前的三个弱相互作用玻色子和一个超荷玻色子. 

$$
\begin{aligned}
g: (\mathbf{8},\mathbf{1})_0\\
~\\
W^\pm,W^0: (\mathbf{1},\mathbf{3})_0\\
~\\
B: (\mathbf{1},\mathbf{1})_0
\end{aligned}
$$

可以写出左手夸克的带电流相互作用拉氏量

$$
\begin{aligned}
\mathcal{L}_{kinematic,weak}(Q_L) 
&=i\overline{Q^I_{Li}}\gamma_\mu(\partial^\mu+\frac{i}{2}gW^\mu_b\sigma_b)Q^I_{Li} \\ 
&=i\overline{(u~~d)^I_{iL}}\gamma_\mu(\partial^\mu+\frac{i}{2}gW^\mu_b\sigma_b)
\begin{pmatrix}
u \\
d
\end{pmatrix}
^I_{Li}
\end{aligned}
$$

$W$和$Z$玻色子通过自发对称性破缺获得质量. 考虑希格斯场

$$
H: (\mathbf{1},\mathbf{2})_{\frac{1}{2}}
$$

其拉氏量可以写为

$$
\mathcal{L}_{Higgs}=(D_\mu\phi)^\dagger(D^\mu\phi)-\mu^2\phi^\dagger\phi-\lambda(\phi^\dagger\phi)^2
$$

其中$\phi$是一个同位旋二重态

$$
\phi(x)=
\begin{pmatrix}
\phi^+ \\
\phi^0
\end{pmatrix}
$$

Higgs场与规范玻色子的相互作用来源于协变导数，而Higgs场与费米子的相互作用则来源于所谓的Yukawa相互作用

$$
\begin{aligned}
-\mathcal{L}_{Yukawa} 
&= Y_{ij}\overline{\psi_{Li}}\phi\psi_{Rj}+h.c. \\
&= Y_{ij}^d~\overline{Q^I_{Li}}~\phi~d^I_{Rj} + Y_{ij}^u~\overline{Q^I_{Li}}~\tilde{\phi}~u^I_{Rj}+ Y^l_{ij}~\overline{L^I_{Li}}~\phi~l^I_{Rj} +h.c.
\end{aligned}
$$

其中

$$
\tilde{\phi}=i\sigma_2\phi^*
$$

矩阵$Y_{ij}$是味空间中任意的复矩阵，给出了不同代费米子(轻子)之间的耦合，或夸克(轻子)混合. Yukawa耦合实际上给出了费米子的质量项，例如由于中微子不存在右手分量，所以在标准模型框架下中微子就没有质量.

下面我们关注味物理相关的项$Y_{ij}^d~\overline{Q^I_{Li}}~\phi~d^I_{Rj}$.

$$
\begin{aligned}
Y_{ij}^d~\overline{Q^I_{Li}}~\phi~d^I_{Rj}
&= Y_{ij}^d~\overline{(u~~d)^I_{Li}}~\phi~d^I_{Rj}\\
&=
\begin{pmatrix}
Y_{11}~\overline{(u~~d)^I_L}\begin{pmatrix}\phi^+\\ \phi^0\end{pmatrix} & Y_{12}~\overline{(u~~d)^I_L}\begin{pmatrix}\phi^+\\ \phi^0\end{pmatrix} & Y_{13}~\overline{(u~~d)^I_L}\begin{pmatrix}\phi^+\\ \phi^0\end{pmatrix} \\
Y_{21}~\overline{(c~~s)^I_L}\begin{pmatrix}\phi^+\\ \phi^0\end{pmatrix}& Y_{22}~\overline{(c~~s)^I_L}\begin{pmatrix}\phi^+\\ \phi^0\end{pmatrix} & Y_{11}~\overline{(u~~d)^I_L}\begin{pmatrix}\phi^+\\ \phi\end{pmatrix} \\
Y_{31}~\overline{(t~~b)^I_L}\begin{pmatrix}\phi^+\\ \phi^0\end{pmatrix} & Y_{32}~\overline{(t~~b)^I_L}\begin{pmatrix}\phi^+\\ \phi^0\end{pmatrix} & Y_{33}~\overline{(t~~b)^I_L}\begin{pmatrix}\phi^+\\ \phi^0\end{pmatrix}
\end{pmatrix}\cdot
\begin{pmatrix}
d^I_R\\ s^I_R\\ b^I_R
\end{pmatrix}
\end{aligned}
$$

在自发对称性破缺后

$$
\phi(x)=\begin{pmatrix}
\phi^+\\
\phi^0
\end{pmatrix}\xrightarrow{sym.breaking}\frac{1}{\sqrt{2}}\begin{pmatrix}
0\\
v+h(x)
\end{pmatrix}
$$

得到了费米子场的质量项

$$
\begin{aligned}
-\mathcal{L}_{Yukawa}^{quarks}
&= Y_{ij}^d~\overline{Q^I_{Li}}~\phi~d^I_{Rj} + Y_{ij}^u~\overline{Q^I_{Li}}~\tilde{\phi}~u^I_{Rj} + h.c. \\
&= Y_{ij}^d~\overline{d^I_{Li}}~\frac{v}{\sqrt{2}}~d^I_{Rj} + Y_{ij}^u~\overline{u^I_{Li}}~\frac{v}{\sqrt{2}}~u^I_{Rj} + h.c. + \mathrm{interaction terms} \\
&= M_{ij}^d~\overline{d^I_{Li}}~d^I_{Rj} + M_{ij}^u~\overline{u^I_{Li}}~u^I_{Rj} + h.c. + \mathrm{interaction terms}
\end{aligned}
$$

为了获得物理的质量项，需要将$M_{ij}$对角化

$$
\begin{aligned}
M^d_{diag}=V^d_LM^dV^{d\dagger}_R \\
M^u_{diag}=V^u_LM^uV^{u\dagger}_R
\end{aligned}
$$

拉氏量重写为

$$
\begin{aligned}
-\mathcal{L}_{Yukawa}^{quarks}
&= \overline{d^I_{Li}}~M_{ij}^d~d^I_{Rj} + \overline{u^I_{Li}}~M_{ij}^u~u^I_{Rj} + h.c. + \mathrm{interaction terms} \\
&= \overline{d^I_{Li}}~V^{d\dagger}_L~V^d_L~M_{ij}^d~V^{d\dagger}_R~V^d_R~d^I_{Rj} + \overline{u^I_{Li}}~V^{u\dagger}_L~V^u_L~M_{ij}^u~V^{u\dagger}_R~V^u_R~u^I_{Rj} + h.c. + \mathrm{interaction terms} \\
&= \overline{d_{Li}}~(M_{ij}^d)_{diag}~d_{Rj} + \overline{u_{Li}}~(M_{ij}^u)_{diag}~u_{Rj} + h.c. + \mathrm{interaction terms}
\end{aligned}
$$

由此得到夸克质量本征态与相互作用本征态的关系

$$
\begin{aligned}
d_{Li}=(V_L^d)_{ij}d^I_{Lj}~~~d_{Ri}=(V_R^d)_{ij}d^I_{Rj} \\
u_{Li}=(V_L^u)_{ij}u^I_{Lj}~~~u_{Ri}=(V_R^u)_{ij}u^I_{Rj}
\end{aligned}
$$

注意到物理传播的夸克都是质量本征态，并且右手夸克不参与弱相互作用，那么左手弱带电流相互作用写为

$$
\begin{aligned}
\mathcal{L}_{c.c.}&=\frac{g}{\sqrt{2}}\overline{u^I_{iL}}\gamma_\mu W^{-\mu}d^I_{iL}+\frac{g}{\sqrt{2}}\overline{d^I_{iL}}\gamma_\mu W^{+\mu}u^I_{iL}+... \\
&=\frac{g}{\sqrt{2}}\overline{u_{iL}}(V_L^uV_L^{d\dagger})_{ij} \gamma_\mu W^{-\mu}d_{iL}+\frac{g}{\sqrt{2}}\overline{d_{iL}}(V_L^dV_L^{u\dagger})_{ij}\gamma_\mu W^{+\mu}u_{iL}+...
\end{aligned}
$$

其中幺正矩阵$(V_L^uV_L^{d\dagger})_{ij}$即为Cabibbo-Kobayashi-Maskawa矩阵.