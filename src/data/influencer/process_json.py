import json
import networkx as nx
from networkx.readwrite import json_graph
from random import randint as rand

def graphing(pair, node, word):
    word = word.lower()

    # Creates a primary word list and strips out the key word
    primary_list = [k.replace(" " + word, '') for k, v in pair.items() if v[1] == 'P']

    primary_list_test = [k.replace(" " + word, '') for k, v in pair.items()]

    # Creates a tertiary word list but retains the
    tertiary_list = [k.split() for k, v in pair.items() if v[1] == 'T']

    # Adds in words to the primary list
    for t in tertiary_list:
        for n in t:
            if n not in primary_list:
                primary_list.append(n)

    # Index used for providing an ID to the edge
    num = 1
    # creates a new NetworkX graph
    NG = nx.Graph()

    for k, v in pair.items():
        # Split the key into two words
        p = k.split(" ", 1)
        # Assign the weight variable
        w = v[0]/2
        # Add an edge with nodes, id, weight and color atributes
        NG.add_edge(p[0], p[1], id=num, weight=w, color='#bcdbf6', size=1)
        # Iterates the ID
        num = num + 1

    # Maximum weight value for scaling
    maxval = max(node.values(), key=lambda x: x)
    prim_co_ord = {}

    # Adds the central node with maximum size and centred into frame
    NG.add_node(word, size=maxval, label=word, x=3, y=3, color='#F6851F',
                borderColor='#bcdbf6', borderWidth=2)

    # Adds in the primary nodes
    for p in primary_list:
        val = node[p]
        # normalizes size of node. This can be modified or even removed
        v = ( (val / (maxval*0.6) * 12) + 12 )
        # Assigns unique random co-ordinates for the graph
        co_ord_x = rand(90, 110) / float(100)
        co_ord_y = rand(50, 200) / float(100)
        # Store these for later
        prim_co_ord[p] = [co_ord_x, co_ord_y]
        # Add node to graph with parameters
        NG.add_node(p, size=v, label=p, x=co_ord_x, y=co_ord_y, color='#F6851F',
                    borderColor='#bcdbf6', borderWidth=2)

    for t in tertiary_list:
        # Retrieves the word and it's pairs for tertiary nodes
        u=t[0]
        w=t[1]
        # The weight for the node of interest
        val = node[u]
        # normalizes size of node. This can be modified or even removed
        v = ((val / (maxval * 0.6) * 12) + 12)

        # Adds in x, y co-ords close to the primary node.
        try:
            tert_co_ord_x = prim_co_ord[w][0] + (rand(-5, 5) / float(100))
            tert_co_ord_y = prim_co_ord[w][1] + (rand(-5, 5) / float(100))
        except:
            tert_co_ord_x = prim_co_ord[u][0] + (rand(-5, 5) / float(100))
            tert_co_ord_y = prim_co_ord[u][1] + (rand(-5, 5) / float(100))

        # Adds in node with attributes
        NG.add_node(u, size=v, label=u, x=tert_co_ord_x, y=tert_co_ord_y,
                    color='#F6851F', borderColor='#bcdbf6', borderWidth=2)

    # Converts the Network graph to a JSON format
    fixNG = json_graph.node_link_data(NG)
    # Fixes the network so that edges use node names instead of integers
    fixNG['links'] = [
        {
            'source': fixNG['nodes'][link['source']]['id'],
            'target': fixNG['nodes'][link['target']]['id'],
            'id': link['id'], 'size': link['size'], 'color':'#bcdbf6'
        }
        for link in fixNG['links']]
    # Stringifies the json
    fixNG = str(json.dumps(fixNG))
    # Changes links to edges to comply with Sigma.JS
    rtnNG = fixNG.replace('links', 'edges')

    return rtnNG

def parse(listDB, word):        # Parses the data into dictionaries
    pairDict = {}
    nodeDict = {}
    # Separates primary nodes into their own list and sorts on count
    # A maximum of 15 nodes are selected from t
    pLst = [l for l in listDB if l[3] == 'P']
    pLst = sorted(pLst, key=lambda x: x[2], reverse=True)[:15]
    # A temp list for tertiary nodes linked to primary nodes
    m_pLst = [n[0] for n in pLst]

    # Separates tertiary nodes into their own list if in m_pLst
    tLst = [l for l in listDB if l[3] == 'T' and l[1] in set(m_pLst)]
    tLst = sorted(tLst, key=lambda x: x[2], reverse=True)[:20]

    for l in tLst:
        pLst.append(l)

    for lst in pLst:
        # Defines 1st word, 2nd word and count
        x = lst[0].lower()
        y = lst[1].lower()
        z = lst[2]
        if x and y:
            # Defines key and swapped order key for pairs
            key = (x+" "+y)
            varkey = (y+" "+x)
            val = lst[2], lst[3]
            val = list(val)
            # If these don't exist, add to pairs dict
            if key in pairDict:
                pass
            elif varkey in pairDict:
                pass
            else:
                pairDict[key] = val
            # Adds weights to node dicts for each word in the pair
            if x in nodeDict:
                nodeDict[x] += z
            else:
                nodeDict[x] = z
            if y in nodeDict:
                nodeDict[y] += z
            else:
                nodeDict[y] = z
    return graphing(pairDict, nodeDict, word)

list_in = [['friend', 'country', 3, 'P'],
['look', 'country', 4, 'P'],
['person', 'country', 2, 'P'],
['make', 'country', 2, 'P'],
['mimisamat8', 'look', 2, 'T'],
['heoolll', 'look', 2, 'T'],
['look', 'look', 1, 'T'],
['judge', 'person', 1, 'T'],
['kind', 'person', 1, 'T'],
['looks', 'make', 1, 'T'],
['thing', 'make', 1, 'T'],
['personality', 'make', 1, 'T'],
['pasta', 'make', 1, 'T'],
['italy', 'make', 1, 'T']]

print(parse(list_in, 'country'))