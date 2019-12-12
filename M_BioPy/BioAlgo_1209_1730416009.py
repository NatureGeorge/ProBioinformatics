# @Date:   2019-12-09T13:35:37+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioAlgo_1111_1730416009.py
# @Last modified time: 2019-12-09T13:36:30+08:00
"""
Requirement:
Write a version of this function that can handle non-connected graphs
(still balanced). This function should allow to calculate all Eulerian
cycles of the different connected components
"""
from BioAlgo_1111_1730416009 import MyGraph
from collections import defaultdict


class MyGraph2Eulerian(MyGraph):
    def check_balanced_node(self, node):
        return self.in_degree(node) == self.out_degree(node)

    def check_balanced_graph(self):
        for n in self.graph.keys():
            if not self.check_balanced_node(n):
                return False
        return True

    def check_nearly_balanced_graph(self):
        res = None, None
        for n in self.graph.keys():
            indeg = self.in_degree(n)
            outdeg = self.out_degree(n)
            if indeg - outdeg == 1 and res[1] is None:
                res = res[0], n
            elif indeg - outdeg == -1 and res[0] is None:
                res = n, res[1]
            elif indeg == outdeg:
                pass
            else:
                return None, None
        return res

    def is_connected(self):
        total = len(self.graph.keys()) - 1
        for v in self.graph.keys():
            reachable_v = self.reachable_bfs(v)
            if (len(reachable_v) < total):
                return False
        return True

    def eulerian_cycle(self):
        if not self.is_connected() or not self.check_balanced_graph():
            return None
        edges_visit = list(self.get_edges())
        res = []
        while edges_visit:
            pair = edges_visit[0]
            i = 1
            if res != []:
                while pair[0] not in res:
                    pair = edges_visit[i]
                    i = i + 1
            edges_visit.remove(pair)
            start, nxt = pair
            cycle = [start, nxt]
            while nxt != start:
                for suc in self.graph[nxt]:
                    if (nxt, suc) in edges_visit:
                        pair = (nxt, suc)
                        nxt = suc
                        cycle.append(nxt)
                        edges_visit.remove(pair)
            if not res:
                res = cycle
            else:
                pos = res.index(cycle[0])
                for i in range(len(cycle)-1):
                    res.insert(pos + i + 1, cycle[i+1])
        return res

    def eulerian_path(self):
        unb = self.check_nearly_balanced_graph()
        if unb[0] is None or unb[1] is None:
            return None
        # Deliberate modification: transform a path to a circle
        self.graph[unb[1]].append(unb[0])
        cycle = self.eulerian_cycle()
        for i in range(len(cycle)-1):
            if cycle[i] == unb[1] and cycle[i+1] == unb[0]:
                break
        path = cycle[i+1:] + cycle[1:i+1]
        return path


def suffix(seq):
    return seq[1:]


def prefix(seq):
    return seq[:-1]


def composition(k, seq):
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    res.sort()
    return res


class DeBruijnGraph(MyGraph2Eulerian):

    def __init__(self, frags):
        MyGraph2Eulerian.__init__(self, {})
        self.create_deBruijn_graph(frags)

    # override
    def add_edge(self, o, d):
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        self.graph[o].append(d)

    # override
    def in_degree(self, v):
        res = 0
        for k in self.graph.keys():
            if v in self.graph[k]:
                res += self.graph[k].count(v)
        return res
    
    def create_deBruijn_graph(self, frags):
        for seq in frags:
            suf = suffix(seq)
            self.add_vertex(suf)
            pref = prefix(seq)
            self.add_vertex(pref)
            self.add_edge(pref, suf)

    def seq_from_path(self, path):
        seq = path[0]
        for i in range(1, len(path)):
            nxt = path[i]
            seq += nxt[-1]
        return seq

    @staticmethod
    def test(orig_sequence="ATGCAATGGTCTG", kmer=3):
        frags = composition(kmer, orig_sequence)
        print("frags: %s" % frags)
        dbgr = DeBruijnGraph(frags)
        dbgr.print_graph()
        print("-"*100)
        print(dbgr.check_nearly_balanced_graph())
        print("-"*100)
        p = dbgr.eulerian_path()
        print(p)
        print("-"*100)
        print(dbgr.seq_from_path(p))
        print("-"*100)


def merge_common(lists):
    """
    Merge all sublist having common elements

    Reference: https://www.geeksforgeeks.org/python-merge-list-with-common-elements-in-a-list-of-lists/
    """
    neigh = defaultdict(set)
    visited = set()
    for each in lists:
        for item in each:
            neigh[item].update(each)

    def comp(node, neigh=neigh, visited=visited, vis=visited.add):
        nodes = set([node])
        next_node = nodes.pop
        while nodes:
            node = next_node()
            vis(node)
            nodes |= neigh[node] - visited
            yield node
    for node in neigh:
        if node not in visited:
            yield sorted(comp(node))


def findConnectedComponent(graph_dict):
    """
    This function find out every connected component
    in the inputed graph which stored in a python
    dictionary

    :param dict graph_dict: graph which stored in a dictionary
    """
    if not isinstance(graph_dict, dict):
        raise ValueError("Invalid input, graph_dict should be a dict")

    group = []
    
    '''
    group = defaultdict(list)
    group_count = 1
    for index, (node, others) in enumerate(graph_dict.items()):
        vSet = set([node] + others)
        if index == 0:
            group[group_count] = list(vSet)
            continue
        groupKeys = list(group.keys())
        for key in groupKeys:
            overlap = vSet & set(group[key])
            if overlap:
                group[key].extend(list(vSet-overlap))
            else:
                group_count += 1
                group[group_count] = list(vSet)
    lystS = list(group.values())
    '''
    
    for node, others in graph_dict.items():
        group.append(list(set([node] + others)))

    return list(merge_common(group))


if __name__ == "__main__":
    # DeBruijnGraph.test()
    frags = ["ATA", "ACC", "CAT", "CCA", "TAA", "TTG", "TGG", "GGC", "GCT"]
    newfrags = ['AAT', 'ATG', 'ATG', 'CAA', 'CTG',
             'GCA', 'GGT', 'GTC', 'TCT', 'TGC',
             'TGG',
             'XXY', 'XYO', 'XYO', 'ZXX', 'ZYO',
             'OZX', 'OOY', 'OYZ', 'YZY', 'YOZ',
             'YOO']
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    allGraph = dbgr.graph.copy()
    lystL = findConnectedComponent(allGraph)
    for lyst in lystL:
        print(lyst)
        cur_graph = {key: value for key, value in allGraph.items() if key in lyst}
        dbgr.graph = cur_graph
        dbgr.print_graph()
        print("-"*100)
        print(dbgr.check_nearly_balanced_graph())
        print("-"*100)
        p = dbgr.eulerian_path()
        print(p)
        print("-"*100)
        print(dbgr.seq_from_path(p))
        print("="*100)
    
