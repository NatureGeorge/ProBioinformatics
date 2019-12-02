# @Date:   2019-11-18T13:49:37+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioAlgo_1111_1730416009.py
# @Last modified time: 2019-11-25T15:16:21+08:00
from collections import defaultdict
import functools
from itertools import permutations, combinations
from time import perf_counter
from tqdm import tqdm
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


SYMBOL = {
    "rightArrow": "=>",
    "leftArrow": "<=",
    "leftRightArrow": "<==>"
}


class MyGraph:
    def __init__(self, g={}):
        """ Constructor - takes dictionary to fill the graph as input ; default is empty dictionary """
        self.graph = g
        self.nodes = None

    def print_graph(self):
        for v in self.graph.keys():
            print(v, "->", self.graph[v])

    # get basic information about the graph
    def get_nodes(self):
        if self.nodes is not None:
            return self.nodes
        else:
            return list(self.graph.keys())

    def set_nodes(self, nodes=None):
        if nodes is None:
            self.nodes = self.get_nodes()
        else:
            self.nodes = nodes
        
        self.nodePermutations = list(permutations(self.nodes, 2))

    def get_edges(self):
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d))
        return edges

    def size(self):
        """ Returns number of nodes, number of edges """
        return len(self.get_nodes()), len(self.get_edges())

    # add nodes and edges
    def add_vertex(self, v):
        """ Add a vertex to the graph Tests if vertex exists not adding if it does. """
        if v not in self.graph.keys():
            self.graph[v] = []

    def add_edge(self, o, d):
        """ Add edge to the graph. If vertices do not exist, they are added to the graph """
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]:
            self.graph[o].append(d)

    # successors, predecessors, adjacent nodes
    def get_successors(self, v):
        return list(self.graph[v])  # avoids list being overwritten

    def get_predecessors(self, v):
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res

    def get_adjacents(self, v):
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res:
                res.append(p)
        return res

    # degrees
    def out_degree(self, v):
        return len(self.graph[v])

    def in_degree(self, v):
        return len(self.get_predecessors(v))

    def degree(self, v):
        return len(self.get_adjacents(v))

    def all_degrees(self, deg_type="inout"):
        """ Computes the degree for all nodes. deg_type can be "in", "out", or "inout" Returns a dictionary: node −> degree."""
        degs = defaultdict(int)
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else:
                degs[v] = 0
            if deg_type == "in" or deg_type == "inout":
                for v in self.graph.keys():
                    for d in self.graph[v]:
                        if deg_type == "in" or v not in self.graph[d]:
                            degs[d] = degs[d] + 1
            return degs

    def highest_degrees(self, all_deg=None, deg_type="inout", top=10):
        if all_deg is None:
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()),
                         key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_deg[:top]))

    # topological metrics over degrees
    def mean_degree(self, deg_type="inout"):
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))

    def prob_degree(self, deg_type="inout"):
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res

    # BFS and DFS searches
    def reachable_bfs(self, v):
        lyst = [v]
        res = []
        while len(lyst) > 0:
            node = lyst.pop(0)
            if node != v:
                res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in lyst:
                    lyst.append(elem)
        return res

    def reachable_dfs(self, v):
        lyst = [v]
        res = []
        while len(lyst) > 0:
            node = lyst.pop(0)
            if node != v:
                res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in lyst:
                    lyst.insert(s, elem)
                    s += 1
        return res

    def distance(self, s, d):
        if s == d:
            return 0
        lyst = [(s, 0)]
        visited = [s]
        while len(lyst) > 0:
            node, dist = lyst.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return dist + 1
                elif elem not in visited:
                    lyst.append((elem, dist + 1))
                    visited.append(elem)
        return None

    @functools.lru_cache()
    def shortest_path(self, s, d):
        if s == d:
            return 0
        lyst = [(s, [])]
        visited = [s]
        while len(lyst) > 0:
            node, preds = lyst.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return preds + [node, elem]
                elif elem not in visited:
                    lyst.append((elem, preds + [node]))
                    visited.append(elem)
        return None

    @functools.lru_cache()
    def reachable_with_dist(self, s):
        res = []
        lyst = [(s, 0)]
        while len(lyst) > 0:
            node, dist = lyst.pop(0)
            if node != s:
                res.append((node, dist))
            for elem in self.graph[node]:
                # if not MyGraph.is_in_tuple_list(lyst, elem) and not MyGraph.is_in_tuple_list(res, elem):
                str_first_lyst = ','.join(i[0] for i in lyst)
                str_first_res = ','.join(i[0] for i in res)
                if not MyGraph.is_in_tuple_first_strList(str_first_lyst, elem) and not MyGraph.is_in_tuple_first_strList(str_first_res, elem):
                    lyst.append((elem, dist + 1))
        return res

    @staticmethod
    def is_in_tuple_list(tl, val):
        res = False
        for x, _ in tl:
            if val == x:
                return True
        return res

    @staticmethod
    @functools.lru_cache()
    def is_in_tuple_first_strList(string, elem):
        if elem in string:
            return True
        else:
            return False

    # mean distances ignoring unreachable nodes
    def mean_distances(self):
        tot = 0
        num_reachable = 0
        for k in self.graph.keys():
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        n = len(self.get_nodes())
        return meandist, float(num_reachable) / ((n - 1) * n)

    def closeness_centrality(self, node):
        print("closeness_centrality(%s): " % node, end="")
        print(perf_counter())
        dist = self.reachable_with_dist(node)
        if len(dist) == 0:
            return 0.0
        s = 0.0
        for d in dist:
            s += d[1]
        return len(dist) / s

    def highest_closeness(self, top=10):
        cc = {}
        for k in self.graph.keys():
            cc[k] = self.closeness_centrality(k)
        print(cc)
        ord_cl = sorted(list(cc.items()), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_cl[:top]))

    def betweenness_centrality(self, node):
        print("betweenness_centrality(%s): " % node, end="")
        print(perf_counter())
        total_sp = 0
        sps_with_node = 0
        '''
        for s in self.graph.keys():
            for t in self.graph.keys():
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t)
                    if sp is not None:
                        total_sp += 1
                        if node in sp:
                            sps_with_node += 1
        return sps_with_node / total_sp
        '''
        for s, t in tqdm(self.nodePermutations):
            if s == node or t == node:
                continue
            else:
                sp = self.shortest_path(s, t)
                if sp is not None:
                    total_sp += 1
                    if node in sp:
                        sps_with_node += 1
        return sps_with_node / total_sp

    # cycles
    def node_has_cycle(self, v):
        lyst = [v]
        res = False
        visited = [v]
        while len(lyst) > 0:
            node = lyst.pop(0)
            for elem in self.graph[node]:
                if elem == v:
                    return True
                elif elem not in visited:
                    lyst.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v):
                return True
        return res

    # clustering
    def clustering_coef(self, v):
        adjs = self.get_adjacents(v)
        if len(adjs) <= 1:
            return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]:
                        ligs = ligs + 1
        return float(ligs) / (len(adjs) * (len(adjs) - 1))

    def all_clustering_coefs(self):
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs

    def mean_clustering_coef(self):
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))

    def mean_clustering_perdegree(self, deg_type="inout"):
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys():
                degs_k[degs[k]].append(k)
            else:
                degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]:
                tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck


class MetabolicNetwork(MyGraph):

    def __init__(self, network_type="metabolite-reaction", split_rev=False, symbol=SYMBOL):
        MyGraph.__init__(self, {})
        self.net_type = network_type
        self.node_types = defaultdict(list)
        self.split_rev = split_rev
        self.symbol = symbol
        self.rightArrow = symbol["rightArrow"]
        self.leftRightArrow = symbol["leftRightArrow"]

    def add_vertex_type(self, v, nodetype):
        self.add_vertex(v)
        self.node_types[nodetype].append(v)

    def get_nodes_type(self, node_type):
        if node_type in self.node_types:
            return self.node_types[node_type]
        else:
            return None

    def load_from_file(self, filename):
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction")
        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else:
                raise Exception("Invalid line:")
            if self.leftRightArrow in rline:
                # print("Find leftRightArrow")
                left, right = rline.split(self.leftRightArrow)
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id + "_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id + "_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id + "_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
            elif self.rightArrow in line:
                # print("Find right Arrow")
                left, right = rline.split(self.rightArrow)
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else:
                raise Exception("Invalid line:")

        if self.net_type == "metabolite-reaction":
            self.graph = gmr.graph
            self.node_types = gmr.node_types
        elif self.net_type == "metabolite-metabolite":
            self.convert_metabolite_net(gmr)
        elif self.net_type == "reaction-reaction":
            self.convert_reaction_graph(gmr)
        else:
            self.graph = {}

    def convert_metabolite_net(self, gmr):
        for m in gmr.node_types["metabolite"]:
            self.add_vertex(m)
            sucs = gmr.get_successors(m)
            for s in sucs:
                sucs_r = gmr.get_successors(s)
                for s2 in sucs_r:
                    if m != s2:
                        self.add_edge(m, s2)

    def convert_reaction_graph(self, gmr):
        for r in gmr.node_types["reaction"]:
            self.add_vertex(r)
            sucs = gmr.get_successors(r)
            for s in sucs:
                sucs_r = gmr.get_successors(s)
                for s2 in sucs_r:
                    if r != s2:
                        self.add_edge(r, s2)

    # assessing metabolic potential

    def active_reactions(self, active_metabolites):
        if self.net_type != "metabolite-reaction" or not self.split_rev:
            return None
        res = []
        for v in self.node_types['reaction']:
            preds = set(self.get_predecessors(v))
            if len(preds) > 0 and preds.issubset(set(active_metabolites)):
                res.append(v)
        return res

    def produced_metabolites(self, active_reactions):
        res = []
        for r in active_reactions:
            sucs = self.get_successors(r)
            for s in sucs:
                if s not in res:
                    res.append(s)
        return res

    def all_produced_metabolites(self, initial_metabolites):
        mets = initial_metabolites
        cont = True
        while cont:
            cont = False
            reacs = self.active_reactions(mets)
            new_mets = self.produced_metabolites(reacs)
            for nm in new_mets:
                if nm not in mets:
                    mets.append(nm)
                    cont = True
        return mets

    # exercise 1 of chapter 14
    def final_metabolites(self):
        res = []
        for v in self.graph.keys():
            if v[0] == "M":
                if len(self.get_predecessors(v)) > 0:
                    if self.get_successors(v) == []:
                        res.append(v)
        return res

    # exercise 2 of chapter 14
    def shortest_path_product(self, initial_metabolites, target_product):
        if target_product in initial_metabolites:
            return []
        metabs = {}
        for m in initial_metabolites:
            metabs[m] = []
        reacs = self.active_reactions(initial_metabolites)
        cont = True
        while cont:
            cont = False
            for r in reacs:
                sucs = self.get_successors(r)
                preds = self.get_predecessors(r)
                for s in sucs:
                    if s not in metabs:
                        previous = []
                        for p in preds:
                            for rr in metabs[p]:
                                if rr not in previous:
                                    previous.append(rr)
                        metabs[s] = previous + [r]
                        if s == target_product:
                            return metabs[s]
                        cont = True
            if cont:
                reacs = self.active_reactions(metabs.keys())
        return None


def convertDict2Dfrm(dict):
    fromList, toList = [], []
    for key, values in dict.items():
        if not values:
            continue
        fromList.extend([key]*len(values))
        toList.extend(values)
    return pd.DataFrame({"source": fromList, "target": toList})


def useNetWorkX(dfrm):
    G = nx.from_pandas_edgelist(dfrm, source='source', target='target')
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()
    cValue = nx.closeness_centrality(G)
    bValue = nx.betweenness_centrality(G)
    kValue = dict(nx.degree(G))
    return pd.DataFrame([kValue, bValue, cValue]).T


def test():
    net = MetabolicNetwork(network_type="metabolite-metabolite", symbol={"rightArrow": "-->", "leftRightArrow": "<==>"})
    net.load_from_file(r"C:\Users\Nature\Desktop\M_BioAlgorithm\class\tec\MN.txt")
    net.set_nodes()
    nodes = pd.Series(net.get_nodes())
    bValues = nodes.apply(net.betweenness_centrality)
    cValues = nodes.apply(net.closeness_centrality)
    kValues = nodes.apply(net.degree)
    print(pd.DataFrame([nodes, kValues, bValues, cValues]).T)
    
    # result = useNetWorkX(convertDict2Dfrm(net.graph))
    # result.to_csv(r"C:\Users\Nature\Desktop\M_BioAlgorithm\self\Lab8\result.txt", sep="\t", header=["K", "B", "C"])


if __name__ == "__main__":
    test()
