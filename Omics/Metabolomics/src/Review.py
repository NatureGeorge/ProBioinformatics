# @Created Date: 2019-12-25 03:07:10 pm
# @Filename: Review.py
# @Email:  1730416009@stu.suda.edu.cn
# @Author: ZeFeng Zhu
# @Last Modified: 2019-12-25 03:07:19 pm

class Definition:
    def __init__(self):
        self.Metabolomics = "代谢组学(Metabonomics / Metabolomics)是关于生物体内源性代谢物质的整体及其变换规律的科学。是在后基因组学时代兴起的一门跨领域学科，其主要目标是定量的研究生命体对 外界刺激、病理生理变化、以及本身基因突变而产生的其体内代谢物水平的多元动态反应"
        self.content = [
            "代谢物靶标分析(Metabolite target analysis)", 
            "代谢物指纹分析(Metabolic finger printing)", 
            "代谢轮廓(谱)分析(Metabolic profiling)", 
            "代谢组学(Metabolomics)"]

    def display(self):
        for item in self.__dict__.items():
            print("[%s]:\n%s\n" % item)
