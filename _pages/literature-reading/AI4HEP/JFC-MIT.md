---
layout: page
title: AI Agent Can Already Autonomously Perform Experimental High Energy Physics
permalink: /literature-reading/AI4HEP/JFC-MIT/
nav: false
---

### **AI Agent Can Already Autonomously Perform Experimental High Energy Physics**

本文原链接[https://arxiv.org/abs/2603.20179v1](https://arxiv.org/abs/2603.20179v1)

#### **Abstract**

当前基于大语言模型的AI agent已经能够自动地执行高能物理实验分析中的大部分步骤。MIT的研究人员发现在给定数据集、执行框架以及一套完整的先前实验文献的语料库的情况下，Claude Code可以自动化地执行包括事例筛选、本底估计、不确定度分析、统计推断以及撰写note等一系列标准分析流程。高能物理学界正在低估大语言模型的能力，并且当前大多数代理工作流都仅局限于一小部分分析板块而非让AI执行完整的分析流程。

MIT的研究人员提出了一个概念验证性(proof-of-concept)的框架——$Just~Furnish~Context (JFC)$。这一框架集成了包括文献知识检索和multi-agent review的自动分析agent，并利用ALEPH, DELPHI和CMS的公开数据集证明了其具备自动规划、执行以及记录一个完整的高能物理实验数据分析。

#### **1 Introduction**

一个典型的高能物理实验分析通常包括了以下步骤：

- 找到一个感兴趣的衰变道或新物理特征；
- 调研已有的文献并学习类似的测量是如何被执行的；
- 利用MC设计并验证一个事例筛选的流程，寻找可能的系统不确定度来源
- 揭盲真实实验数据并通过统计假设检验得到测量结果

这一过程通常会耗费一名研究生一年甚至更久的时间，并且会挤压他们思考更加重要的问题的精力和时间。本文中作者试图向读者证明AI agent可以完成这一枯燥的分析流程。研究人员向读者展示了，给定一个通用的框架，通过蒸馏大型HEP合作中实际使用分析流程和一个初始的高级物理prompt，Claude Code能够产生一个完整的分析：事件选择，背景估计，系统的不确定性评估，统计推断，以及一份的书面报告。与其他大部分类似研究不同的是，这一框架选择使用多个agent进行review而非进行持续的人为反馈，仅在揭盲阶段需要一次人为的评估，实现了一个近乎完全自动化的分析框架。

$JFC$框架大致可以分为三个独立的部分：

- $Methodology$ 

  研究团队对一个典型的粒子物理分析工作流程进行了编码。通常而言，这对应着一名研究生在科研中受到的训练。

  - $Review$

    在Methodology的部分存在一个独特的部分——review part——用于分析检验实验结果的可靠性，为了模拟这一流程，研究人员在每一个步骤后面都添加了检验的sub-agent。

- $General~agent~behavior$

  为了管理上下文窗口，Methodology中概述的分析步骤被发送给独立的sub-agent。然而，这些代理仍然需要知道整体的分析背景和计划。因此，研究人员对每个代理接收和输出的内容进行了严格的规范，并对日志进行了编码，使其能够被人类验证，也方便了代理级对复杂故障的调试。

- $Domain-specific~conventions$

  最后，在分析框架中指定了一组独立的约定，例如工具使用、可视化、或更模糊的或最近的分析技术。对这一基线水平的编码似乎是不可避免的，因为一般模型无法正确猜测不同领域差异较大的具体惯例。


#### **2 Related work**

