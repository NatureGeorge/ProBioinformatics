# @Date:   2019-07-24T16:43:57+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: LearnAlgorithm_zzf_0724.py
# @Last modified time: 2019-07-25T10:22:44+08:00
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
        "axes_color": GREEN,
        "x_labeled_nums": range(xlim[0], xlim[1], 4),
        "y_labeled_nums": range(ylim[0], ylim[1], 4),
        "x_tick_frequency": 1,
        "y_tick_frequency": 1,
        "graph_origin": LEFT*6+DOWN*3,
    }
    content_di = {
        "Exponential Order": [RED, lambda x: np.exp2(x)-1, "2^{x}-1", 20, "$O(2^{n}})$"],
        "Square Order": [BLUE, lambda x: x*x, "x^{2}", 15, "$O(n^{2})$"],
        "Linear Order": [GRAY, lambda x: x, "x", 10, "$O(n)$"],
        "Logarithmic Order": [YELLOW, lambda x: np.log2(x+1), "\\log_{2}(x+1)", 5, "$O(n*\\log_{2}n)$"]
        }
        # func, graph_label_tex, graph_label_x_val, color
        # 1,2,3,0

    def construct(self):
        commonObject = self.setCommonObject()
        self.addIntroduction(*commonObject)
        self.addGraph()
        # self.addExplanation(*commonObject)

    def setCommonObject(self):
        contentObject_li = [TextMobject(i, color=j[0]) for i,j in self.content_di.items()]
        return contentObject_li

    def setContentGroup(self, contentObject_li, topObject):
        if topObject:
            contentObject_li[0].next_to(topObject, DOWN)

        start = 0
        for i in combinations(contentObject_li, 2):
            if start != i[0]:
                i[1].next_to(i[0], DOWN)
                start = i[0]
        contentObject_tp = tuple(contentObject_li)
        content_group = VGroup(*contentObject_tp)
        return content_group


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
        piCreature = PiCreature(color=BLUE_C, height = 1)

        # ----------------------------------------------------------------------
        # Position
        # ----------------------------------------------------------------------
        ## Title
        title_group = VGroup(title.bg, title)
        ## Content
        '''
        contentObject_li[0].next_to(title_group, DOWN)
        start = 0
        for i in combinations(contentObject_li, 2):
            if start != i[0]:
                i[1].next_to(i[0], DOWN)
                start = i[0]
        contentObject_tp = tuple(contentObject_li)
        content_group = VGroup(*contentObject_tp)
        '''
        content_group = self.setContentGroup(contentObject_li, title_group)
        ## Description & Shapes
        text.shift(UP)
        line.shift(UP)
        piCreature.next_to(line, LEFT)

        # ----------------------------------------------------------------------
        # Animation
        # ----------------------------------------------------------------------
        ## Description & Shapes
        self.play(FadeInFrom(piCreature, LEFT), ApplyMethod(piCreature.look_at, line))
        piCreature.look_at(line)
        self.wait(0.2)
        self.play(ShowCreation(line), Blink(piCreature))
        # self.play(piCreature.change, "happy")
        self.wait(0.5)
        self.play(Transform(line, text))
        self.wait(0.5)
        ## Title
        self.play(FadeIn(title_group), FadeOut(piCreature, RIGHT))
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
        self.play(ApplyMethod(content_group.shift, 5*RIGHT+3.2*UP))


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


class CompareGraph(ShowComplexityOrder):
        CONFIG = {
            "x_axis_label": "",
            "y_axis_label": "",
            "x_min" : 0,
            "x_max" : 100,
            "x_labeled_nums" : list(range(0, 100, 20)),
            "x_tick_frequency" : 10,
            "y_min" : 0,
            "y_max" : 10000,
            "y_tick_frequency" : 1000,
            "y_labeled_nums" : list(range(1000, 10000, 2000)),
            "dots_x": list(range(0,100,20)),
            "showCoord_dots": [2],
            "graph_origin": 1.5*DOWN+0.5*RIGHT,
            "chart_width": 7,
            "chart_height": 2,
            "axes_color": GRAY,
        }
        content_di = {
            "Exponential Order": [RED, lambda x: np.exp2(x)-1, "2^{x}-1", 90, "$O(2^{n}})$"],
            "Square Order": [BLUE, lambda x: x*x, "x^{2}", 90, "$O(n^{2})$"],
            "Linear Order": [GRAY, lambda x: 30*x, "30x", 90, "$O(n)$"],
            "Logarithmic Order": [YELLOW, lambda x: 5*x*np.log2(x+1), "5n\\log_{2}(x+1)", 90, "$O(n\\log_{2}n)$"]
            }

        def construct(self):
            commonObject = self.setCommonObject()
            content_group = self.setContentGroup(commonObject, False)
            self.addExplanation(content_group)
            # self.show_graph()
            # self.show_bg_graph()
            # self.set_Dots()
            # self.addDescription()

        def addExplanation(self, content_group):
            # ----------------------------------------------------------------------
            # Object
            # ----------------------------------------------------------------------
            ## Title (Used to be Content)
            titleObject = content_group
            ## Content (New Content)
            new_title_group = VGroup(*[TextMobject("An Algorithm On %s Means ..." % i,
                                        color=self.content_di[i][0]).scale(0.7)
                                        for i in self.content_di.keys()])
            # ----------------------------------------------------------------------
            # Position
            # ----------------------------------------------------------------------
            titleObject.shift(5*RIGHT+2.2*UP)
            new_title_group.to_edge(2*TOP+LEFT)
            # ----------------------------------------------------------------------
            # Animation & Position
            # ----------------------------------------------------------------------
            self.add(titleObject)
            title_group = VGroup(titleObject[0], titleObject[2:])
            self.play(FadeOutAndShiftDown(title_group))
            self.play(ApplyMethod(titleObject[1].to_edge, TOP+LEFT))
            self.setup_axes(animate=True)
            self.play(ApplyMethod(self.axes.scale, 0.5))

            start = titleObject[1]
            num = 1
            def getDiLi(di, num):
                key_li = list(di.keys())
                return di[key_li[num]]

            screen = True
            for title in new_title_group[1:]:
                self.title = title
                title.to_edge(TOP+LEFT)
                self.wait(1)
                self.play(Transform(start, title))
                self.wait(1)
                li = getDiLi(self.content_di, num)
                num += 1
                self.show_graph(li[1], li[2], li[3], li[0])
                self.wait(1)
                # self.show_bg_graph(li[1], li[0])
                self.set_Dots(self.graph, li[1])
                if not screen:
                    screen = True
                    screen_rect = ScreenRectangle(height=2).next_to(self.title, 3*DOWN).shift(DOWN+RIGHT)
                    self.play(ShowCreation(screen_rect))
                self.addDescription(10, li[4])
                # self.play(FadeOut(VGroup(graph, graph_label), RIGHT))
                # break
            self.play(FadeOut(VGroup(self.title, self.axes), DOWN))
            close_1 = TextMobject("\\texttt{{Made By ZeFeng Zhu}}", color=BLUE_D).scale(1.2)
            close_2 = TextMobject("\\texttt{{Last modified time: 2019-07-27T21:40:34+08:00}}").scale(0.8).next_to(close_1, DOWN)
            self.play(ShowCreation(VGroup(close_1, close_2)))
            self.wait()



        def addDescription(self, num, tex):
            coord = self.coord_groups[0]
            self.play(FadeOut(VGroup(*coord[2:])))
            x = coord[0]
            y = coord[1]

            rect = Rectangle(
                width = self.chart_width,
                height = self.chart_height
            ).next_to(self.title, 2.5*DOWN).shift(0.5*RIGHT)

            label = TextMobject(tex).next_to(rect.get_top(), 0.7*DOWN).scale(0.7)
            des_x = TextMobject("Workload", color=GREEN).scale(0.8)
            des_y = TextMobject("Steps", color=PURPLE).scale(0.8)
            des_group = VGroup(des_x, des_y).next_to(label, DOWN)
            des_x.next_to(rect.get_left())
            des_y.next_to(rect.get_right(), 5*LEFT)
            num_x  =TextMobject("%s"%num).scale(0.5).next_to(des_x, DOWN)
            new_tex = tex[2:-1].replace('n', str(num))
            num_y  =TextMobject("$\\approx C*%s \\texttt{{ at most}}$"%new_tex).scale(0.5).next_to(des_y, DOWN)
            # num_group = VGroup(num_x, num_y).next_to(des_group, DOWN)
            self.play(FadeOutAndShiftDown(x), FadeInFrom(VGroup(des_x, num_x), UP), ShowCreation(rect))
            self.play(FadeOutAndShiftDown(y), FadeInFrom(VGroup(des_y, num_y), UP))
            self.wait()
            arrow = Arrow(des_x.get_right(), des_y.get_left()).scale(0.7)
            # label.scale(0.7).next_to(arrow, 0.5*UP)
            self.play(GrowArrow(arrow), ShowCreation(label))
            self.wait(5)
            self.play(FadeOut(VGroup(rect, self.graph, self.graph_label, self.dots, arrow, label, des_group, num_x, num_y), UP))
            self.wait()

        def show_graph(self, func, graph_label_tex, graph_label_x_val, color):
            # func_graph_li = [[self.get_graph(i[1], i[0]), i[2], i[0], i[3]] for i in self.content_di.values()]

            graph = self.get_graph(func, color=color)

            graph_label = self.get_graph_label(
                graph, graph_label_tex,
                direction = LEFT,
                x_val = graph_label_x_val,
            ).scale(0.7)

            self.play(ShowCreation(graph), Write(graph_label))
            self.wait(1)
            self.graph = graph
            self.graph_label = graph_label

        def show_bg_graph(self, func, color):
            bg_graph = self.get_graph(func, color=color)
            origin = self.coords_to_point(0, 0)
            h_line, v_line = [
                Line(origin, origin, color = color, stroke_width = 2)
                for color in (YELLOW, BLUE_E)
            ]

            def h_update(h_line, proportion = 1):
                end = bg_graph.point_from_proportion(proportion)
                t_axis_point = end[0]*RIGHT + origin[1]*UP
                h_line.put_start_and_end_on(t_axis_point, end)

            def v_update(v_line, proportion = 1):
                end = bg_graph.point_from_proportion(proportion)
                d_axis_point = origin[0]*RIGHT + end[1]*UP
                v_line.put_start_and_end_on(d_axis_point, end)

            self.play(ShowCreation(bg_graph, run_time=3),
                      UpdateFromFunc(h_line, h_update),
                      UpdateFromFunc(v_line, v_update))
            self.wait(0.4)
            self.play(FadeOut(VGroup(h_line, v_line), RIGHT))

        def getChangingCoord(self, mob, func):
            decimal_x = DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=1,
                include_sign=False,
            )
            decimal_y = DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=0,
                include_sign=False,
            )
            decimal_x.add_updater(lambda d: d.set_value(self.x_axis.point_to_number(mob.get_center())))
            decimal_y.add_updater(lambda d: d.set_value(func(self.x_axis.point_to_number(mob.get_center()))))

            text = [TextMobject(i) for i in "(,)"]
            decimal_x.next_to(text[0], RIGHT)
            text[1].next_to(decimal_x, 2*RIGHT+0.0625*DOWN)
            decimal_y.next_to(text[1], RIGHT+0.0625*UP)
            text[2].next_to(decimal_y, 5*RIGHT)

            tp = tuple([decimal_x, decimal_y]) + tuple(text)
            coord_group = VGroup(*tp)
            coord_group.scale(0.6)
            return coord_group

        def set_Dots(self, graph, func):
            def update_dot(dot, dt):
                x = self.x_axis.point_to_number(dot.get_center())
                slope = self.slope_of_tangent(dot.temp_x - x, graph)
                x += slope*dt*50
                dot.move_to(self.input_to_graph_point(x, graph))

            dots = VGroup(*[
                Dot().move_to(self.input_to_graph_point(x, graph))
                for x in self.dots_x
            ])
            dots.set_color_by_gradient(YELLOW, RED)

            for dot in dots:
                dot.temp_x = self.x_axis.point_to_number(dot.get_center())
                dot.move_to(self.input_to_graph_point(0, graph))

            coord_groups = VGroup(*[self.getChangingCoord(dots[i], func)
                for i in self.showCoord_dots]).next_to(self.axes, 3*LEFT)
            self.play(ShowCreation(dots), ShowCreation(coord_groups))
            self.wait(1)
            self.add(*[
                Mobject.add_updater(dot, update_dot)
                for dot in dots
            ])
            self.wait(9)
            # return coord_groups
            self.dots = dots
            self.coord_groups = coord_groups
