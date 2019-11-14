# @Date:   2019-11-03T16:45:17+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: ComplexityAGuidedTour.py
# @Last modified time: 2019-11-04T10:17:12+08:00
import numpy as np
from enum import IntEnum, unique
import random
from multiprocessing.dummy import Pool
# import multiprocessing as mp
# import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("darkgrid")


@unique
class Gene(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
    STAY = 4
    PICK = 5
    RANDOM = 6


@unique
class State(IntEnum):
    TRUE_COLLECT = 10
    FALSE_COLLECT = -1
    COLLISION = -5
    MISS = 0


@unique
class Environment(IntEnum):
    WALL = -1
    JAR = 1
    EMPTY = 0


environment = [(north, south, west, east, central)
               for north in Environment
               for south in Environment
               for west in Environment
               for east in Environment
               for central in Environment]


class Robe:
    Count = 1

    def __init__(self, go, genes=None, length=243, string=True):
        if genes is None:
            self.genes = Robe.create_individual(length, string)
        else:
            self.genes = genes
        # self.finalScore = []
        # self.finalPosition = []
        if go:
            self.multiGo()
            self.avgScore = self.getAvgScore()
            print("Robe: Complete Search [%s]" % Robe.Count)
            Robe.Count += 1

    def create_individual(length, string):
        if string:
            return ''.join(str(random.randint(min(Gene), max(Gene))) for i in range(length))
        else:
            return [random.randint(min(Gene), max(Gene)) for i in range(length)]

    def lookEnvironment(task, position):
        def get(x):
            for sit in Environment:
                if x == sit:
                    return sit
        i, j = position
        bound = len(task) - 1
        if j == 0:
            west = Environment.WALL
        else:
            west = get(task[i, j - 1])

        if j == bound:
            east = Environment.WALL
        else:
            east = get(task[i, j + 1])

        if i == 0:
            north = Environment.WALL
        else:
            north = get(task[i - 1, j])

        if i == bound:
            south = Environment.WALL
        else:
            south = get(task[i + 1, j])

        central = get(task[i, j])

        return north, south, west, east, central

    def action(gene, position):
        i, j = position
        gene = int(gene)
        if gene == Gene.NORTH:
            return (i - 1, j), False
        elif gene == Gene.SOUTH:
            return (i + 1, j), False
        elif gene == Gene.WEST:
            return (i, j - 1), False
        elif gene == Gene.EAST:
            return (i, j + 1), False
        elif gene == Gene.STAY:
            return position, False
        elif gene == Gene.PICK:
            return position, True
        elif gene == Gene.RANDOM:
            return random.choice([(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]), False

    def score(task, oldPosition, newPosition, pick):
        if pick:
            if task[oldPosition] == Environment.JAR:
                task[oldPosition] = 0
                return oldPosition, State.TRUE_COLLECT
            else:
                return oldPosition, State.FALSE_COLLECT
        else:
            bound = len(task) - 1
            x, y = newPosition
            if x < 0 or y < 0 or x > bound or y > bound:
                return oldPosition, State.COLLISION
            else:
                return newPosition, State.MISS

    def go(self, task, position=(0, 0), steps=200):
        s = 0
        step = 0
        while step < steps:
            gene = self.genes[environment.index(
                Robe.lookEnvironment(task, position))]
            newPosition, pick = Robe.action(gene, position)
            position, curScore = Robe.score(task, position, newPosition, pick)
            s += curScore
            step += 1
        # self.finalScore.append(s)
        # self.finalPosition.append(position)
        return s

    def generateTask(size=10):
        return np.array([[random.randint(0, 1) for i in range(size)] for j in range(size)])

    def multiGo(self, num=100):
        def register(task):
            return self.go(task)

        pool = Pool(processes=20)

        self.tasks = [Robe.generateTask() for i in range(num)]
        """
        for task in self.tasks:
            self.go(task)
        """
        self.finalScore = pool.map(register, self.tasks)
        pool.close()

    def getAvgScore(self):
        return sum(self.finalScore) / len(self.finalScore)


class RobeGroup:
    Count = 1

    def __init__(self, group=None, num=200):

        # self.group = []
        # self.scores = []
        pool = Pool(processes=20)
        # queue = mp.Queue()

        def register(genes):
            # self.group.append(Robe(True, genes=genes))
            return Robe(True, genes=genes)
            # queue.put(Robe(True, genes=genes))

        if group is None:
            # self.group = [Robe(True) for i in range(num)]
            group = [None]*num
        # else:
            # self.group = [Robe(True, genes=genes) for genes in group]
        self.group = pool.map(register, group)
        pool.close()
        """
        process = mp.Process(target=register, args=(queue, group, ))
        process.start()
        process.join()
        while not queue.empty():
            res = queue.get()
            self.group.append(res)
            self.scores.append(res.avgScore)
        """

        self.scores = [robe.avgScore for robe in self.group]
        max_s, min_s = max(self.scores), min(self.scores)
        self.normScores = np.array(
            [(score - min_s) / (max_s - min_s) for score in self.scores])
        self.prob = (self.normScores / self.normScores.sum()).tolist()
        print("RobeGroup: New Group [%s]" % RobeGroup.Count)
        RobeGroup.Count += 1

    def selectParent(self):
        np.random.seed()
        self.parent = np.random.choice(
            self.group, p=self.prob, size=2, replace=False)

    def selectBest(self):
        return self.group[self.prob.index(max(self.prob))]

    def getChild12(self):
        parent1, parent2 = self.parent[0], self.parent[1]
        index = random.randint(0, len(parent1.genes))
        child1 = RobeGroup.muta(parent1.genes[:index] + parent2.genes[index:])
        child2 = RobeGroup.muta(parent2.genes[:index] + parent1.genes[index:])
        self.children.append(child1)
        self.children.append(child2)

    def getChildren(self, pairs=99):
        self.best = self.selectBest().genes
        self.children = [self.best, self.best]
        for i in range(pairs):
            self.selectParent()
            self.getChild12()
        return self.children

    def muta(child, maxMuta=5, p=[0.9, 0.025, 0.025, 0.025, 0.025]):
        np.random.seed()
        num = np.random.choice(list(range(maxMuta)), p=p)
        for i in range(num):
            index = random.randint(0, len(child))
            child = child[:index] + \
                str(int(random.choice(
                    [gene for gene in Gene]))) + child[index + 1:]
        return child


def demo(num=99):
    max_scores = []
    initial = RobeGroup()
    max_scores.append(max(initial.scores))
    new = initial
    for i in range(num):
        new = RobeGroup(group=new.getChildren())
        maxNew = max(new.scores)
        print(maxNew)
        max_scores.append(maxNew)
    return max_scores, initial, new


if __name__ == "__main__":
    max_scores, initial, new = demo(2)
    print([robe.genes for robe in new.group])
    print(max_scores)
    plt.figure(figsize=(10, 8))
    a = plt.plot(list(range(len(max_scores))), max_scores)
    plt.show()
    plt.savefig('./Robe.png')
