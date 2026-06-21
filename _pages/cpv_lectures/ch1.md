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

### 1.2 QED中的离散对称性：C,P,T

本小节中我们将推导$P,C,T$的算符表达式. 根据定义，变换后的波函数$\psi_P(\vec{x},t),\psi_C(\vec{x},t),\psi_T(\vec{x},t)$满足与自由场$\psi(\vec{x},t)$相同的运动方程. 

考虑狄拉克方程

$$\Big(i\gamma^\mu\frac{\partial}{\partial x_\mu}-\gamma^\mu eA_\mu-m\Big)~\psi(\vec{x},t)=0$$

展开为

$$\Big(\gamma^0[i\frac{\partial}{\partial t}-e\phi(\vec{x},t)]-\gamma^i[i\frac{\partial}{\partial x^i}-eA^i(\vec{x},t)]-m\Big)~\psi(\vec{x},t)=0$$

在宇称变换下

$$\Big(\gamma^0[i\frac{\partial}{\partial t}-e\phi(-\vec{x},t)]-\gamma^i[i\frac{\partial}{\partial (-x^i)}+eA^i(-\vec{x},t)]-m\Big)~\psi(-\vec{x},t)=0$$

注意到$(\gamma^0)^2=1,\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}$，因此$\gamma^0\gamma^i=-\gamma^i\gamma^0$，在上式左侧乘一个$\gamma^0$

$$\Big(\gamma^0[i\frac{\partial}{\partial t}-e\phi(-\vec{x},t)]-\gamma^i[i\frac{\partial}{\partial x^i}-eA^i(-\vec{x},t)]-m\Big)~\gamma^0\psi(-\vec{x},t)=0$$

满足原始的狄拉克方程，因此可以得知狄拉克旋量在宇称操作下的变换

$$
\boxed{\psi(\vec{x},t)\xrightarrow{\text{P}}\psi_P(\vec{x},t)=\gamma^0\psi(-\vec{x},t)=P\psi(-\vec{x},t)}
$$

注意可以保留一个任意相位$e^{i\phi}\gamma^0\psi(-\vec{x},t)$.

考虑电荷共轭变换$e\to -e$，狄拉克方程满足
$$\Big(\gamma^0[i\frac{\partial}{\partial t}+e\phi(\vec{x},t)]-\gamma^i[i\frac{\partial}{\partial x^i}+eA^i(\vec{x},t)]-m\Big)~\psi_C(\vec{x},t)=0$$

注意到$\gamma^0=\gamma^{0*},\gamma^1=\gamma^{1*},\gamma^{2*}=-\gamma^2,\gamma^3=\gamma^{3*}$，对原始狄拉克方程取复共轭

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