sentiment-influencer-app
==============================

Social network influencer app to identify communities, network statistics, with real time sentiment analyzer for Twitter.

Produces multiple files to feed into Sigma.js and React analytics dashboard 

How to Use
==============================
`$ twecoll3 init datafox`

`$ twecoll3 fetch datafox`

`$ twecoll3 edgelist daatfox`

`TODO:` Upgarde to Python 3.7
==============================

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org
    
    
Network Statistic Definitions
-----------

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
    size = nx.degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='size', values=size)

    """
    Definition: Degree centrality assigns an importance score based purely on the number of links held by each node. 
    
    What it tells us: How many direct, ‘one hop’ connections each node has to other nodes within the network.
    
    When to use it: For finding very connected individuals, popular individuals, individuals who are likely to hold
    most information or individuals who can quickly connect with the wider network.
    
    A bit more detail: Degree centrality is the simplest measure of node connectivity. Sometimes it’s useful to look 
    at in-degree (number of inbound links) and out-degree (number of outbound links) as distinct measures, 
    for example  when looking at transactional data or account activity.
    """

    idc = nx.in_degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='idc', values=idc)

    odc = nx.out_degree_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='odc', values=odc)

    # eigen-vector centrality
    edc = nx.eigenvector_centrality(di_graph)
    nx.set_node_attributes(di_graph, name='edc', values=edc)
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
    
    
    
    
    
