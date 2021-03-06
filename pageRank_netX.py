__author__ = 'Qin'

import networkx as nx

# Graph creation
G = nx.DiGraph()

# Define pagerank function
def pagerank(graph, damping_factor=0.85, max_iterations=100,
             min_delta=0.00001):
    """
    Compute and return the PageRank in an directed graph.

    @type  graph: digraph
    @param graph: Digraph.

    @type  damping_factor: number
    @param damping_factor: PageRank dumping factor.

    @type  max_iterations: number
    @param max_iterations: Maximum number of iterations.

    @type  min_delta: number
    @param min_delta: Smallest variation required for a new iteration.

    @rtype:  Dict
    @return: Dict containing all the nodes PageRank.
    """

    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}
    # value for nodes without inbound links
    min_value = (1.0 - damping_factor) / graph_size

    # itialize the page rank dict with 1/N for all nodes
    # pagerank = dict.fromkeys(nodes, 1.0/graph_size)
    pagerank = dict.fromkeys(nodes, 1.0)

    for i in range(max_iterations):
        diff = 0  # total difference compared to last iteraction
        # computes each node PageRank based on inbound links
        for node in nodes:
            rank = min_value
            for referring_page in graph.predecessors(node):
                rank += damping_factor * pagerank[referring_page] / \
                        len(graph.neighbors(referring_page))

            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank

        # print('This is NO.%s iteration' % (i+1))
        #        print(pagerank)
        #        print('')

        # stop if PageRank has converged
        if diff < min_delta:
            break

    return pagerank


# Add nodes and edges
with open('nodes', mode='r', encoding='utf8') as nodesfile:
    for node in nodesfile:
        G.add_node(node.strip())

with open('edges', mode='r', encoding='utf8') as edgesfile:
    for edge in edgesfile:
        from_edge, to_edge = edge.split('\t')
        G.add_edge(from_edge.strip(), to_edge.strip())

pagerank = pagerank(G)
with open('pagerank', mode='w', encoding='utf8') as pagerankfile:
    for (key,value) in sorted(pagerank.items(),key=lambda x:x[1], reverse=True):
        pagerankfile.write('{0}\t{1}\n'.format(value,key))

# draw the graph
# import matplotlib.pyplot as plt
# nx.draw(G)
# plt.savefig("nodes.png")