# Requirements of Final Record and Report

```txt
Created Date: Tuesday, January 7th 2020, 1:22:57 pm
Author: ZeFeng Zhu
```

## Content

根据整个授课内容和实验讲义的教学要求和设计方案, 完成一个已知基因组的 __测序模拟、组装、注释和可视化分析工作__

### 分析记录文档:30

1. 文档结构与排版:5
2. 内容的完整度:10
3. 文档内容详尽程度:10
4. 问题记录和解决记录:5

### 分析总结文档:60

1. 文档结构与排版:10
2. 内容完整度(至少包括摘要、材料和方法、结果、讨论):10
3. 摘要:10
4. 材料和方法:10
5. 结果:10
6. 讨论:10

### 实验项目

1. 基因组测序模拟
2. 序列组装
3. 基因组注释之同源搜索
4. 基因组注释之从头预测与结构建模
5. 基因组注释之启动子分析和预测
6. 基因组可视化

## Flowchart

### Overall

```viz
digraph flowchart {
    size="6,4"; ratio = fill;
    node [style="filled,setlinewidth(3)", color="#8383cc", fontname="Courier New", shape="Mrecord",fixedsize=true,width=2.5,fillcolor="#d9e7ee"];
    edge [color="0.635 0.707 0.707", fontname="Courier New"];
    step1[label="基因组测序模拟"];
    step2[label="序列组装"];
    step3[label="基因组注释"];
    step4[label="基因组可视化"];
    step1->step2;
    step2->step3;

    subgraph cluster_0 {
        style=filled;
        color=lightgrey;
        node [color=white];
        step31[label="同源搜索"];
        step32[label="从头预测与结构建模"];
        step33[label="启动子分析和预测"];
        step3 -> step31;
        step3 -> step32;
        step3 -> step33;
    }

    step31->step4;
    step32->step4;
    step33->step4;
}
```

### 基因组测序模拟

```viz
digraph flowchart_1 {
    # rankdir=LR;
    fontname="Courier New";
    size="6,4"; ratio = fill;
    node [style="filled,setlinewidth(3)", color="#8383cc", fontname="Courier New", shape="Mrecord",fixedsize=true,width=2.5,fillcolor="#d9e7ee"];
    edge [color="0.635 0.707 0.707", fontname="Courier New"];
    label="基因组测序模拟";
    step1[label="art_illumina调研"];
    step2[label="基因组数据下载"];
    step3[label="基因组测序模拟"];

    sub_step1->step1;
    step1->sub_step2;
    sub_step2->step2;
    step2->step3;
    step3->sub_step31;

    subgraph cluster_1 {
        style=filled;
        color=lightgrey;
        sub_step1[label="文献调研"];
        sub_step2[label="软件的安装和测试"];
        label="拓展内容";
        subgraph cluster_2{
            color=grey;
            sub_step31[label="基因组测序数据下载"];
            sub_step32[label="相关的统计计算"];
            sub_step33[label="art_profile_illumina"];
            sub_step34[label="对比profile"];
            sub_step31->sub_step32->sub_step33->sub_step34;
            label="数据模型的创建";
        }
    }
}
```

### 序列组装

```viz
digraph flowchart_2 {
    # rankdir=LR;
    fontname="Courier New";
    size="12,8"; ratio = fill;
    node [style="filled,setlinewidth(3)", color="#8383cc", fontname="Courier New", shape="Mrecord",fixedsize=true,width=2.5,fillcolor="#d9e7ee"];
    edge [color="0.635 0.707 0.707", fontname="Courier New"];
    label="序列组装";
    step1[label="数据准备"];
    step2[label="fastqc质控分析"];
    # step3[label="与参考基因组的比对"];
    # step4[label="序列组装及结果分析"];

subgraph cluster_1{
    style=filled;
    color=lightgrey;
    node [color=white];
    subgraph cluster_01 {
        color=grey;
        label="art_illumina 模拟双末端测序"
        sub_c1_1[label="短插入片段库"];
        sub_c1_2[label="长插入片段库"];
    }
    label="数据准备"
    sub_c1_3[label="参考基因组文件创建"];
}
    sub_c1_1->sub_c1_3;
    sub_c1_2->sub_c1_3;

    subgraph cluster_0 {
        style=filled;
        color=lightgrey;
        sub_step1[label="文献调研"];
        sub_step2[label="软件的安装和测试"];
        sub_step3[label="序列组装练习"];
        label="拓展内容";
        sub_step1->sub_step2->sub_step3;
    }

    subgraph cluster_2 {
        style=filled;
        color=lightgrey;
        node [color=white];
        sub_c2_step1[label="bowtie2对比"];
        sub_c2_step2[label="samtools统计分析"];
        sub_c2_step3[label="plot-bamstats可视化"];
        label="与参考基因组的比对";
        sub_c2_step1->sub_c2_step2->sub_c2_step3;
    }

    subgraph cluster_3 {
        style=filled;
        color=lightgrey;
        node [color=white];
        sub_c3_step1[label="SOAPdenovo组装"];
        sub_c3_step2[label="Quast分析"];
        label="序列组装及结果分析";
        sub_c3_step1->sub_c3_step2;
    }

    step1->sub_c1_1;
    step1->sub_c1_2;
    sub_step3->step1;
    sub_c1_3->step2[label="bowtie2 -build"];
    step2->sub_c2_step1;
    sub_c2_step3->sub_c3_step1
}
```

### 基因组注释之同源搜索

```viz
digraph flowchart_3 {
    # rankdir=LR;
    fontname="Courier New";
    size="6,4"; ratio = fill;
    node [style="filled,setlinewidth(3)", color="#8383cc", fontname="Courier New", shape="Mrecord",fixedsize=true,width=2.5,fillcolor="#d9e7ee"];
    edge [color="0.635 0.707 0.707", fontname="Courier New"];
    label="基因组注释之同源搜索";
    # step1[label="数据准备及预处理"];
    step2[label="创建本地BLAST DB"];
    step3[label="全基因组同源基因搜索"];
    step4[label="同源搜索结果评估"];

    subgraph cluster_1{
        style=filled;
        color=lightgrey;
        node [color=white];
        label="数据准备及预处理"
        sub_c1_1[label="基因组序列"];
        sub_c1_2[label="已知蛋白序列"];
    }

    sub_c2_0[label="原始GFF文档", color=white];
    sub_c1_1->step2[label="makeblastdb"];
    step2->step3;
    sub_c1_2->step3[label="tblastn"];
    "code1" [ style = "filled" penwidth = 1 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">blast92gff3.pl</font></td></tr><tr><td align="left" port="r3">perl code</td></tr></table>> ];
    "code2" [ style = "filled" penwidth = 1 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">blast2gff.py</font></td></tr><tr><td align="left" port="r3">python code</td></tr></table>> ];
    step3->code1;
    step3->code2;
    code1->step4;
    code2->step4;
    sub_c2_0->step4[label="gffcompare"];
}
```

### 基因组注释之从头预测与结构建模

```viz
digraph flowchart_4 {
    # rankdir=LR;
    fontname="Courier New";
    size="6,4"; ratio = fill;
    node [style="filled,setlinewidth(3)", color="#8383cc", fontname="Courier New", shape="Mrecord",fixedsize=true,width=2.5,fillcolor="#d9e7ee"];
    edge [color="0.635 0.707 0.707", fontname="Courier New"];
    label="基因组注释之从头预测与结构建模";
    # step1[label="数据准备"];
    step2[label="全基因组从头基因预测"];
    # step3[label="从头基因预测结果的鉴别"];
    step4[label="从头预测结果的评估"];

    subgraph cluster_1{
        style=filled;
        color=lightgrey;
        node [color=white];
        label="数据准备"
        sub_c1_1[label="基因组序列"];
        sub_c1_2[label="已知蛋白序列"];
        sub_c1_3[label="原始GFF文档"];
    }

    subgraph cluster_2{
        style=filled;
        color=lightgrey;
        node [color=white];
        label="从头基因预测结果的鉴别"
        sub_c2_1[label="创建本地BLAST DB"];
        sub_c2_2[label="提取蛋白序列"];
        sub_c2_3[label="鉴别预测出来的基因"];
        sub_c2_4[label="预测结果合并"];
    }

    sub_c1_1->step2[label="Augustus"];
    sub_c1_2->sub_c2_1[label="makeblastdb"];
    step2->sub_c2_2[label="GFF file"];
    sub_c2_2->sub_c2_3;
    sub_c2_1->sub_c2_3;
    sub_c2_3->sub_c2_4;
    step2->sub_c2_4[label="GFF file"];
    sub_c2_4->step4[label="gffcompare"];
    # sub_c1_3->step4;
}
```

### 基因组注释之启动子分析和预测

```viz
digraph flowchart_5 {
    # rankdir=LR;
    fontname="Courier New";
    size="6,4"; ratio = fill;
    node [style="filled,setlinewidth(3)", color="#8383cc", fontname="Courier New", shape="Mrecord",fixedsize=true,width=2.5,fillcolor="#d9e7ee"];
    edge [color="0.635 0.707 0.707"];
    label="基因组注释之启动子分析和预测";
    step1[label="数据准备"];
    step2[label="启动子元件HMM数据"];
    # step3[label="DNA元件的计算鉴别"];
    step4[label="与原GFF文件进行对比"];
    step5[label="分值结果可视化"];
    step6[label="ROC曲线绘制"];
    step7[label="据最佳阈值进一步筛选"];

    subgraph cluster_1{
        style=filled;
        color=lightgrey;
        node [color=white];
        label="DNA元件的计算鉴别"
        sub_c1_1[label="计算原始得分"];
        sub_c1_2[label="bootstrap & shuffle"];
        sub_c1_3[label="根据p值进行过滤"];
        sub_c1_1->sub_c1_2->sub_c1_3;
    }
    step1->step2->sub_c1_1;
    sub_c1_3->step4->step5->step6->step7->sub_c1_3;
}
```

### 基因组可视化

```viz
digraph flowchart_6 {
    # rankdir=LR;
    size="6,4"; ratio = fill;
    node [style="filled,setlinewidth(3)", color="#8383cc",shape=box,fixedsize=true,width=1.9,fillcolor="#d9e7ee"];
    edge [color="0.635 0.707 0.707"];
    label="基因组可视化";
    step1[label="文献调研"];
    step2[label="基因组可视化"];
    step1->step2;
}
```

### Overall Detail

```viz
digraph flowchart_detail {
    # rankdir=LR;
    size="11,9"; ratio = fill;
    fontname="Courier New";
    node[style="filled,setlinewidth(3)", color="#8383cc", fontname="Courier New", shape="Mrecord",fixedsize=true,width=1.9,fillcolor="#d9e7ee"];
    edge[color="0.635 0.707 0.707", fontname="Courier New"];
    label="基因组信息学flowchart";

    fnaFile[label="基因组序列", fillcolor="#FFFFF0", color="#EEE8AA"];
    gffFile[label="原始GFF文档", fillcolor="#FFFFF0", color="#EEE8AA"];
    proFile[label="UniProt得蛋白序列", fillcolor="#FFFFF0", color="#EEE8AA"];

    subgraph cluster_1{
        label="基因组测序模拟";
        style=dashed;
        color=gray;
        lab1_1[label="art_illumina调研"];
        lab1_2[label="基因组测序模拟"];

        subgraph cluster_pairSeq {
            color=lightgrey;
            style=filled;
            node[fillcolor=white];
            label="art_illumina 模拟双末端测序";
            sub_pairSeq_1[label="短插入片段库"];
            sub_pairSeq_2[label="长插入片段库"];
        }
    }

    lab1_1->lab1_2[color="#FF8C00"];
    fnaFile->lab1_2[color="#FF8C00"];
    lab1_2->sub_pairSeq_1[label="-p", color="#FF8C00"];
    lab1_2->sub_pairSeq_2[label="-mp", color="#FF8C00"];

    subgraph cluster_2{
        label="序列组装";
        style=dashed;
        color=gray;
        lab2_1[label="参考基因组文件创建"];
        lab2_2[label="fastqc质控分析"];

        subgraph cluster_compare {
            style=filled;
            color=lightgrey;
            node[fillcolor=white, width=2.6];
            sub_compare_1[label="bowtie2对比"];
            sub_compare_2[label="samtools统计分析"];
            sub_compare_3[label="plot-bamstats可视化"];
            label="与参考基因组的比对";
            sub_compare_1->sub_compare_2->sub_compare_3[color="#00FFFF"];
        }

        subgraph cluster_seqAssembly {
            style=filled;
            color=lightgrey;
            node[fillcolor=white];
            sub_seqAss_1[label="SOAPdenovo组装"];
            sub_seqAss_2[label="Quast分析"];
            label="序列组装及结果分析";
            sub_seqAss_1->sub_seqAss_2[color="#00FFFF"];
        }
    }

    fnaFile->lab2_1[label="bowtie2 -build", color="#00FFFF"];
    sub_pairSeq_1->lab2_2[color="#00FFFF"];
    sub_pairSeq_2->lab2_2[color="#00FFFF"];
    lab2_2->sub_compare_1[color="#00FFFF"];
    lab2_1->sub_compare_1[color="#00FFFF"];
    sub_pairSeq_1->sub_seqAss_1[color="#00FFFF"];
    sub_pairSeq_2->sub_seqAss_1[color="#00FFFF"];
    gffFile->sub_seqAss_2[color="#00FFFF"];
    fnaFile->sub_seqAss_2[color="#00FFFF"];

    subgraph cluster_3{
        label="基因组注释之同源搜索";
        style=dashed;
        color=gray;
        lab3_2[label="创建本地BLAST DB"];
        lab3_3[label="全基因组同源基因搜索"];
        lab3_4[label="同源搜索结果评估"];
        "code1" [ style = "filled" penwidth = 1 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">blast92gff3.pl</font></td></tr><tr><td align="left" port="r3">perl code</td></tr></table>> ];
        "code2" [ style = "filled" penwidth = 1 fillcolor = "white" fontname = "Courier New" shape = "Mrecord" label =<<table border="0" cellborder="0" cellpadding="3" bgcolor="white"><tr><td bgcolor="black" align="center" colspan="2"><font color="white">blast2gff.py</font></td></tr><tr><td align="left" port="r3">python code</td></tr></table>> ];
    }

    fnaFile->lab3_2[label="makeblastdb", color="#FF1493"];
    proFile->lab3_3[label="tblastn", color="#FF1493"];
    lab3_2->lab3_3[color="#FF1493"];
    lab3_3->code1[color="#FF1493"];
    lab3_3->code2[color="#FF1493"];
    gffFile->lab3_4[color="#FF1493"];
    code1->lab3_4[color="#FF1493"];
    code2->lab3_4[color="#FF1493"];

    subgraph cluster_4{
        label="基因组注释之从头预测与结构建模";
        style=dashed;
        color=gray;
        lab4_1[label="全基因组从头基因预测"];
        lab4_3[label="从头预测结果的评估"]

        subgraph cluster_iden{
            style=filled;
            color=lightgrey;
            node[fillcolor=white];
            label="从头基因预测结果的鉴别"
            sub_iden_1[label="创建本地BLAST DB"];
            sub_iden_2[label="提取蛋白序列"];
            sub_iden_3[label="鉴别预测出来的基因"];
            sub_iden_4[label="预测结果合并"];
        }
    }

    fnaFile->lab4_1[label="Augustus", color="#00FF00"];
    lab4_1->sub_iden_2[label="GFF File", color="#00FF00"];
    sub_iden_2->sub_iden_3[color="#00FF00"];
    sub_iden_3->sub_iden_4[color="#00FF00"];
    lab4_1->sub_iden_4[color="#00FF00"];
    proFile->sub_iden_1[label="makeblastdb", color="#00FF00"];
    sub_iden_1->sub_iden_3[color="#00FF00"];
    sub_iden_4->lab4_3[label="gffcompare", color="#00FF00"];
    gffFile->lab4_3[color="#00FF00"];

    subgraph cluster_5{
        label="基因组注释之启动子分析和预测";
        style=dashed;
        color=gray;
        lab5_1[label="启动子元件HMM数据"];
        lab5_3[label="与原GFF文件进行对比"];
        lab5_4[label="分值结果可视化"];
        lab5_5[label="ROC曲线绘制"];
        lab5_6[label="据最佳阈值进一步筛选"];

        subgraph cluster_ele{
            style=filled;
            color=lightgrey;
            node [fillcolor=white,width=2.7];
            label="DNA元件的计算鉴别"
            sub_ele_1[label="计算原始得分"];
            sub_ele_2[label="bootstrap & shuffle"];
            sub_ele_3[label="根据p值进行过滤"];
        }
    }

    lab5_1->sub_ele_1;
    sub_ele_1->sub_ele_2->sub_ele_3;
    sub_ele_3->lab5_3->lab5_4->lab5_5->lab5_6->sub_ele_3;
    gffFile->lab5_3;
    gffFile->lab5_5;
    fnaFile->sub_ele_1;

    subgraph cluster_6{
        label="基因组可视化";
        style=dashed;
        color=gray;
        lab6_1[label="文献调研"];
        lab6_2[label="基因组可视化"];
    }

    lab6_1->lab6_2[color="#8B4513"];
    fnaFile->lab6_2[color="#8B4513"];
    gffFile->lab6_2[color="#8B4513"];
    sub_iden_4->lab6_2[color="#8B4513"];
    code2->lab6_2[color="#8B4513"];
}
```