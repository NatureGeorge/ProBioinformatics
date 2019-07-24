# @Date:   2019-07-24T16:43:57+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: LearnAlgorithm_zzf_0724.py
# @Last modified time: 2019-07-24T23:23:04+08:00
from manimlib.imports import *
import numpy as np
from itertools import combinations


class ShowComplexityOrder(GraphScene):
    # --------------------------------------------------------------------------
    # Configuaion
    # --------------------------------------------------------------------------
    xlim = (0, 18)
    ylim = xlim
    CONFIG = {
        "x_min": xlim[0],
        "x_max": xlim[1],
        "y_min": ylim[0],
        "y_max": ylim[1],
        "graph_origin": ORIGIN,
        "axes_color": GREEN,
        "x_labeled_nums": range(xlim[0], xlim[1], 4),
        "y_labeled_nums": range(ylim[0], ylim[1], 4),
        "x_tick_frequency": 1,
        "y_tick_frequency": 1,
        "graph_origin": LEFT*6+DOWN*3,
    }
    content_di = {
        "Exponential order": [RED, lambda x: np.exp2(x)-1, "y = 2^{x}-1", 20],
        "Square order": [BLUE, lambda x: x*x, "y = x^{2}", 15],
        "Linear order": [GRAY, lambda x: x, "y = x", 10],
        "Logarithmic order": [YELLOW, lambda x: np.log2(x+1), "y = \\log_{2}(x+1)", 5]
        }

    def construct(self):
        commonObject = self.setCommonObject()
        self.addIntroduction(*commonObject)
        self.addGraph()
        self.addExplanation(*commonObject)

    def setCommonObject(self):
        contentObject_li = [TextMobject(i, color=j[0]) for i,j in self.content_di.items()]
        return contentObject_li

    def addIntroduction(self, *commonObject):
        # ----------------------------------------------------------------------
        # Object
        # ----------------------------------------------------------------------
        ## Title
        title = TextMobject("Learning Algorithm")
        title.scale(2)
        title.bg = SurroundingRectangle(title,color=BLUE, fill_color=BLUE, fill_opacity=.5)
        sub_title = TextMobject("[Examples of some order of complexity]")
        ## Content
        contentObject_li = commonObject
        # contentObject_tp = (TextMobject(i, color=j[0]) for i,j in self.content_di.items())
        ## Description
        text = TextMobject("This Video Is Powered By Manim\n(2019)", color=BLUE)
        text.scale(0.7)
        ## Shapes
        line = Line(np.array([-4,0,0]), np.array([4,0,0]), color=BLUE)

        # ----------------------------------------------------------------------
        # Position
        # ----------------------------------------------------------------------
        ## Title
        title_group = VGroup(title.bg, title)
        ## Content
        contentObject_li[0].next_to(title_group, DOWN)
        start = 0
        for i in combinations(contentObject_li, 2):
            if start != i[0]:
                i[1].next_to(i[0], DOWN)
                start = i[0]
        contentObject_tp = tuple(contentObject_li)
        content_group = VGroup(*contentObject_tp)
        ## Description & Shapes
        text.shift(UP)
        line.shift(UP)

        # ----------------------------------------------------------------------
        # Animation
        # ----------------------------------------------------------------------
        ## Description & Shapes
        self.play(ShowCreation(line))
        self.wait(0.5)
        self.play(Transform(line, text))
        self.wait(0.8)
        ## Title
        self.play(FadeIn(title_group))
        self.wait(1.6)
        self.play(ApplyMethod(title_group.shift, 2.5*UP))
        ## SubTitle
        self.play(Write(sub_title))
        self.wait(0.5)
        ## Content
        self.play(Write(content_group))
        self.wait(0.5)

        ## Move and prepare for graphs
        out_group = VGroup(title_group, line, text, sub_title)
        self.play(FadeOutAndShiftDown(out_group))
        self.play(ApplyMethod(content_group.shift, 5*RIGHT+2.2*UP))


    def addGraph(self):
        # ----------------------------------------------------------------------
        # Object
        # ----------------------------------------------------------------------
        self.setup_axes(animate=True)
        func_graph_li = [[self.get_graph(i[1], i[0]), i[2], i[0], i[3]] for i in self.content_di.values()]
        '''
        func_graph_exp = self.get_graph(lambda x: np.exp2(x)-1, RED)
        func_graph_du = self.get_graph(lambda x: x*x, BLUE)
        func_graph_linear = self.get_graph(lambda x: x, GRAY)
        func_graph_log = self.get_graph(lambda x: np.log2(x+1), YELLOW)
        '''
        # Add label
        graph_lab_li = [self.get_graph_label(i[0], label=i[1], x_val=0.5, color=i[2], direction=i[3]) for i in func_graph_li]
        '''
        graph_lab_exp = self.get_graph_label(func_graph_exp, label="y = 2^{x}-1", x_val=0.5, color=RED, direction=20)
        graph_lab_du = self.get_graph_label(func_graph_du, label="y = x^{2}", x_val=0.5, color=BLUE, direction=15)
        graph_lab_linear = self.get_graph_label(func_graph_du, label="y = x", x_val=0.5, color=GRAY, direction=10)
        graph_lab_log = self.get_graph_label(func_graph_du, label="y = \\log_{2}(x+1)", x_val=0.5, color=YELLOW, direction=5)
        '''
        # ----------------------------------------------------------------------
        # Animation
        # ----------------------------------------------------------------------
        for i in range(0, len(func_graph_li)):
            self.play(ShowCreation(func_graph_li[i][0]), ShowCreation(graph_lab_li[i]))
        self.wait(4)
        '''
        self.play(ShowCreation(func_graph_exp), ShowCreation(graph_lab_exp))
        self.play(ShowCreation(func_graph_du), ShowCreation(graph_lab_du))
        self.play(ShowCreation(func_graph_linear), ShowCreation(graph_lab_linear))
        self.play(ShowCreation(func_graph_log), ShowCreation(graph_lab_log))
        '''
        ## Move and prepare for detailed examples
        graph_tp = tuple(func_graph_li[i][0] for i in range(0, len(func_graph_li))) +\
                   tuple(graph_lab_li[i] for i in range(0, len(func_graph_li)))
        graph_group = VGroup(*graph_tp, self.axes)
        self.play(FadeOut(graph_group))
        self.wait(0.5)

    def addExplanation(self, *commonObject):
        # ----------------------------------------------------------------------
        # Object
        # ----------------------------------------------------------------------
        ## Title (Used to be Content)
        titleObject_tp = commonObject
        ## Content (New Content)
        sub_title = TextMobject("Nested-loop")
        sub_content =  TextMobject("When the inner loop's number of steps is not affected by the outter loop's steps, the ")

        # ----------------------------------------------------------------------
        # Position
        # ----------------------------------------------------------------------


        # ----------------------------------------------------------------------
        # Animation & Position
        # ----------------------------------------------------------------------
        temp_tp = tuple([titleObject_tp[0]]) + titleObject_tp[2:]
        title_group = VGroup(*temp_tp)
        self.play(FadeOutAndShiftDown(title_group))
        self.play(ApplyMethod(titleObject_tp[1].to_edge, TOP+LEFT))
        start = titleObject_tp[1]
        for title in titleObject_tp[2:]:
            title.to_edge(TOP+LEFT)
            self.wait(1)
            self.play(Transform(start, title))
            self.wait(1)
