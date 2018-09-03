#!/usr/bin/env python

# convert gml to json and add basic network statistics

# TODO: fix relative file paths for file input and export
# TODO: move definitions of algorithms to README.md

# import libraries
import numpy as np
import json
import networkx as nx
from modularity_maximization import partition
from modularity_maximization.utils import get_modularity
import matplotlib.pyplot as plt
import re
# from fa2 import ForceAtlas2


def analyze_convert(gmlfile, outputfile, outputfile_format='json'):
    """
    Converts GML file to json while adding statistics and community information
    coloring, node size and edge weight included

    using modularity_maximization.

    JSON output is usable with D3 force layout and GEXF with sigmajs
    # see: https://cambridge-intelligence.com/keylines-faqs-social-network-analysis/
    """

    print(outputfile_format.upper(), 'output file selected')
    print('\nReading GML file:', gmlfile)
    di_graph = nx.read_gml('../../../data/interim/' + gmlfile, label='id')

    # re-assign node id as attr
    node_id_dict = {}
    for id in di_graph.node:
        node_id_dict[id] = int(id)
    nx.set_node_attributes(di_graph, name='id', values=node_id_dict)

    # find communities and assign
    print('Identifying communities...')
    comm_dict = partition(di_graph)

    print('\nModularity of such partition for network is %.3f' % \
          get_modularity(di_graph, comm_dict))

    print('\nAssigning Communities...')

    # get unique set of communities
    comm_unique_set = set()
    for n, d in di_graph.nodes(data=True):
        d['mc'] = comm_dict[n]
        comm_unique_set.add(d['mc'])

    # create colormap
    cmap = plt.get_cmap('cool')
    colors = (cmap(np.linspace(0, 1, len(comm_unique_set)))) * 255
    colors = np.round(colors, decimals=0)

    # assign colors to each community group
    color_mapping = {}
    counter = 0
    for i in list(comm_unique_set):
        color_mapping[i] = colors[counter]
        counter += 1

    # applying colors to nodes iteratively
    for n, d in di_graph.nodes(data=True):
        for group in color_mapping.keys():
            if d['mc'] == group:
                d['color'] = re.sub(r'\s+', '', np.array2string(color_mapping[group], separator=','))
                d['color'] = str.replace(d['color'], '255.]', '1)')
                d['color'] = str.replace(d['color'], '[', 'rgba(')
                d['color'] = str.replace(d['color'], '.', '')

    # loop through nodes and edges, if edge source == node id then color same
    for n, node_d in di_graph.nodes(data=True):
        for source, target, edge_d in di_graph.edges(data=True):
            if source == n:
                edge_d['color'] = node_d['color']
                edge_d['color'] = edge_d['color'].replace(',1)', ',0.1)')



    # set positions of nodes using layout algorithm
    print('\nCreating layout...')
    # forceatlas2 = ForceAtlas2(
    #     # Behavior alternatives
    #     outboundAttractionDistribution=False,  # Dissuade hubs
    #     linLogMode=False,  # NOT IMPLEMENTED
    #     adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
    #     edgeWeightInfluence=1.0,
    #
    #     # Performance
    #     jitterTolerance=1.0,  # Tolerance
    #     barnesHutOptimize=True,
    #     barnesHutTheta=1.2,
    #     multiThreaded=False,  # NOT IMPLEMENTED
    #
    #     # Tuning
    #     scalingRatio=2.0,
    #     strongGravityMode=False,
    #     gravity=1.0,
    #
    #     # Log
    #     verbose=True)
    #
    # positions = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=2000)
    pos = nx.spring_layout(G=di_graph, iterations=100, weight='weight', scale=1, k=5)

    # positions from layout applied to node attributes
    for node, (x, y) in pos.items():
        di_graph.node[node]['x'] = float(x)
        di_graph.node[node]['y'] = float(y)

    print('\nCalculating network statistics...')

    # betweeness centrality
    bc = nx.betweenness_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='bc', values=bc)

    """
    Definition: Betweenness centrality measures the number of times a node lies on the shortest path between other 
    nodes.

    What it tells us: This measure shows which nodes act as ‘bridges’ between nodes in a network. It does this by 
    identifying all the shortest paths and then counting how many times each node falls on one.
    
    When to use it: For finding the individuals who influence the flow around a system.
    
    A bit more detail: Betweenness is useful for analyzing communication dynamics, but should be used with care. A high 
    betweenness count could indicate someone holds authority over, or controls collaboration between, disparate 
    clusters in a network; or indicate they are on the periphery of both clusters.
    
    """
    # degree centrality
    dc = nx.degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='dc', values=dc)

    """
    Definition: Degree centrality assigns an importance score based purely on the number of links held by each node. 
    
    What it tells us: How many direct, ‘one hop’ connections each node has to other nodes within the network.
    
    When to use it: For finding very connected individuals, popular individuals, individuals who are likely to hold
    most information or individuals who can quickly connect with the wider network.
    
    A bit more detail: Degree centrality is the simplest measure of node connectivity. Sometimes it’s useful to look 
    at in-degree (number of inbound links) and out-degree (number of outbound links) as distinct measures, 
    for example  when looking at transactional data or account activity.
    """
    # TODO: check size of node in html file
    size = nx.in_degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='size', values=size)

    odc = nx.out_degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='odc', values=odc)

    # eigen-vector centrality
    edc = nx.eigenvector_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='odc', values=edc)
    """
    Definition: Like degree centrality, EigenCentrality measures a node’s influence based on the number of links it 
    has to other nodes within the network. EigenCentrality then goes a step further by also taking into account how 
    well connected a node is, and how many links their connections have, and so on through the network.

    What it tells us: By calculating the extended connections of a node, EigenCentrality can identify nodes with 
    influence over the whole network, not just those directly connected to it.

    When to use it: EigenCentrality is a good ‘all-round’ SNA score, handy for understanding human social networks, 
    but also for understanding networks like malware propagation.

    A bit more detail: KeyLines calculates each node’s EigenCentrality by converging on an eigenvector using the power 
    iteration method. Learn more.
    """
    # closeness centrality
    cc = nx.closeness_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='cc', values=cc)
    """
    Definition: This measure scores each node based on their ‘closeness’ to all other nodes within the network.
    
    What it tells us: This measure calculates the shortest paths between all nodes, then assigns each node a score 
    based 
    on its sum of shortest paths.
    
    When to use it: For finding the individuals who are best placed to influence the entire network most quickly.
    
    A bit more detail: Closeness centrality can help find good ‘broadcasters’, but in a highly connected network 
    you will often find all nodes have a similar score. What may be more useful is using Closeness to find influencers 
    within a single cluster.
    
    """

    # page rank
    pr = nx.pagerank(di_graph)
    nx.set_node_attributes(di_graph, name='pr', values=pr)
    """
    Definition: PageRank is a variant of EigenCentrality, also assigning nodes a score based on their connections,
    and their connections’ connections. The difference is that PageRank also takes link direction and weight into 
    account – so links can only pass influence in one direction, and pass different amounts of influence.
    
    What it tells us: This measure uncovers nodes whose influence extends beyond their direct connections into the 
    wider network.
    
    When to use it: Because it factors in directionality and connection weight, PageRank can be helpful for 
    understanding citations and authority.
    
    """

    # giant component filter

    # giant = max(nx.connected_component_subgraphs(G), key=len)

    if outputfile_format.upper() == 'JSON':

        print('\nExporting ' + outputfile + '.json')

        # create a dictionary in a node-link format that is suitable for JSON serialization
        with open('../../../data/processed/' + outputfile + '.json', 'w') as outfile1:
            outfile1.write(json.dumps(nx.readwrite.json_graph.node_link_data(G=di_graph, attrs={'link': 'edges',
                                                                                                'name': 'id',
                                                                                                'source': 'source',
                                                                                                'target': 'target'})))
        print('Complete!')

    elif outputfile_format.upper() == 'GEXF':
        print('\nExporting GEXF file...', outputfile, '.gexf')
        nx.write_gexf(di_graph, '../../../data/processed/' + outputfile + '.gexf')
        print('\nComplete!')

    else:
        print('Please enter a valid output file format: JSON or GEXF')


analyze_convert('TheDataFox.gml', 'TheDataFox', outputfile_format='json')
