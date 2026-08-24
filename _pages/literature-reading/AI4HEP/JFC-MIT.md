---
layout: page
title: AI Agent Can Already Autonomously Perform Experimental High Energy Physics
permalink: /literature-reading/AI4HEP/JFC-MIT/
nav: false
---


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

##### 2.1 Agents for data analysis

Gendreau-Distler[10]等人提出了一个基于LLM-agent驱动的数据分析框架。他们将一个基于LLM的agent与Snakemake工作流管理器结合，自动化地利用ATLAS的开放数据集测量了Higgs到双光子的产生截面。工作流管理器执行可重复性和确定性，而agent产生、执行并迭代修改分析代码。作者对多个主流大语言模型进行了基准测试。值得注意的是，作者指出“多步任务规划超出了当前系统的能力”，并提到agent是工作在一个固有的、预先定义好的框架下执行任务。


Diefenbacher[8]等人利用LHC Olympics数据集研究了大模型agent在反常探测方面的表现，证明了agents可以开发和测试与人类提出的方法相媲美的实验分析方法。

Menzo等人提出了HEPTAPOD框架，这一框架让大语言模型能够与主流的HEP攻击交互，构建模拟工作流，并管理多步的研究流程。HEPTAPOD专注于上游模拟工作以及工作流管理而非端到端的数据分析，强调整个过程中人为监督的作用。

Badea等人利用LEP的开放数据集与AI-物理学家agent合作，进行了一个概念验证测量。他们的方法依赖于一个迭代的人在回路中的循环，在这个循环中，物理学家在每个agent尝试之后提供详细的反馈，引导分析走向正确的结果。

##### 2.2 Agents for simulation and experiment design

GRACE专注于上游的实验设计问题而非数据分析。在给定一个自然语言的prompt或者实验论文，GRACE可以提取出这个实验的结构，构造模拟，并利用MC对实验设计进行优化。

##### 2.3 LLM-assisted toolkits

CoLLM提供了一个端到端的管道，从纯语言分析规范到经过训练的深度学习分类器，用于对撞机分析。虽然它使用大语言模型在物理约束下生成分析代码，但它更像是一个带有图形用户界面的人工智能辅助工具包，而不是一个完全自主的代理，并且专门关注分析的深度学习分类步骤。

##### 2.4 Benchmarks and community efforts

CelloAI基准测试提供了一个用于评估HEP环境下的AI助手的框架，重点关注代码文档和生成任务。值得注意的是，CelloAI基准套件尚未包括物理分析任务，使得本领域在评估AI在高能物理最具有潜力的应用上存在一个巨大的gap。

##### 2.5 Knowledge retrieval for physics analysis

对于自动化分析agent而言，一个关键的困难在于如何从已有的文献中提取并应用已有的知识。标准的检索增强生成(Retrieval-Augmented Generation, RAG)在读取科学论文时存在一定的困难，因为在这类文章中，关联的信息通常会遍布不同的小节、图片甚至多篇文章。

##### 2.6 Summary and gaps

下面这张表总结了以上讨论的所有agent系统。

<img src="{{ '/assets/images/literature-reading/JFC-MIT-1.png' | relative_url }}" alt="JFC-MIT-1" width="350">

现有的agent系统呈现出一下特点：首先，现有的大部分agent系统都是工作在预先规划好的框架下的，仅在有限的地方进行coding；第二，目前没有现存的系统能够将自动化多步骤规划、专业知识检索和多智能体review结合在一起；第三，高能物理实验领域缺乏对现实的、端到端的物理分析智能体的基准测试(benchmark)，基于以上所有困境，MIT的研究人员提出了后文中的$JFC$框架。

#### **3 The $JFC$ Framework**

$JFC$是一个自动执行高能物理实验分析的智能体框架。一个协调智能体(orchestrator agent)将不同的执行和审查工作在不同的阶段(phase)分配给不同的智能体。每个phase都会生成一个文稿并在进入下一个phase前必须要通过审查。

##### 3.1 Architecture overview

$JFC$框架基于Claude Code，底层模型使用的是claude-opus-4-6。