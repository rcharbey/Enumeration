# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('%s/Egopol/Graphs' % os.path.expanduser("~"))
import index_degree
from igraph import Graph

PT = []
PS = []

def create_list_neighbors(graph):
    for v in graph.vs:
        v['list_neighbors'] = []
    for e in graph.es:
        if not e.source in graph.vs[e.target]['list_neighbors']:
            graph.vs[e.target]['list_neighbors'].append(e.source)
        if not e.target in graph.vs[e.source]['list_neighbors']:
            graph.vs[e.source]['list_neighbors'].append(e.target)
    for v in graph.vs:
        v['list_neighbors'].sort(reverse = True)

def in_neighborhood_vsub(graph, list_neighbors, length_vsub):
    for n in list_neighbors:
        if graph.vs[n]['id_sub'] != -1 and graph.vs[n]['id_sub'] != length_vsub-1:
            return True
    return False

def add_vertex(graph, vertex):
    vertex['id_sub'] = len(graph.vs)
    graph.add_vertex(name = vertex['name'], **{'id_principal' : vertex.index})

def extend_subgraph(graph, k, graph_sub, v, vext):
    if len(graph_sub.es) > 0 :
        index_degree.index_pattern(graph_sub, PT, PS)
    if len(graph_sub.vs) == k:
        return
    while vext:
        w = vext.pop()
        vext2 = list(vext)
        add_vertex(graph_sub, w)
        for nei in w['list_neighbors']:
            u = graph.vs[nei]
            if u.index >= v.index:
                if u['id_sub'] == -1 :
                    if not in_neighborhood_vsub(graph, u['list_neighbors'], len(graph_sub.vs)):
                        vext2.append(u)
                else:
                    graph_sub.add_edge(len(graph_sub.vs) - 1, u['id_sub'])
            else:
                break

        extend_subgraph(graph, k, graph_sub, v, vext2)
        graph_sub.delete_vertices(w['id_sub'])
        w['id_sub'] = -1

def characterize_with_patterns(graph, k):
    create_list_neighbors(graph)
    global PT
    global PS    
    size_pt_per_k = {2:1, 3:3, 4:9, 5:30}
    size_ps_per_k = {2:1, 3:4, 4:15, 5:73}
    
    PT = size_pt_per_k[k]*[0]
    PS = []
    
    for v in graph.vs:
        PS.append(size_ps_per_k[k]*[0])
        v['id_sub'] = -1
    for v in graph.vs:
        graph_sub = Graph.Formula()
        v['id_sub'] = 0
        if not 'name' in v.attributes():
            v['name'] = str(v.index)
        graph_sub.add_vertex(name = v['name'], **{'id_principal' : v.index, 'evol_class' : 1, 'pattern_sub' : 0, 'neighbors_evol_classes' : []})

        vext = []
        for nei in v['list_neighbors']:
            if nei > v.index:
                vext.append(graph.vs[nei])

        if len(vext) > 0:
            extend_subgraph(graph, k, graph_sub, v, vext)
        v['id_sub'] = -1
    return (PT, PS)