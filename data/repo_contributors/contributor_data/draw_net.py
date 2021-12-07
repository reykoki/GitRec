import csv
import networkx as nx
import matplotlib.pyplot as plt
import os
import glob

repo_colors = ['mediumspringgreen', 'coral', 'deeppink', 'salmon', 'greenyellow', 'aquamarine', 'gold', 'magenta', 'orange', 'plum', 'palegreen']
node_colors = ['darkblue', 'darkolivegreen', 'teal', 'indigo', 'brown', 'maroon', 'purple', 'darkslategrey', 'forestgreen', 'darkgoldenrod', 'saddlebrown']

for filepath in glob.iglob('*csv'):
    filename = os.path.basename(filepath)
    repo_name = filename.split('_')[0]
    print(repo_name)

    nodelist = [repo_name]
    sizes = [300]
    nodecolor = [repo_colors.pop()]
    contr_color = node_colors.pop()

    G = nx.Graph()
    with open(filename, 'r') as f:
        next(f)
        for line in f:
            line = line.rstrip()

            entry = line.split(',')
            node_name = entry[1]
            length = 1/int(entry[-1])

            G.add_nodes_from([repo_name, node_name])
            G.add_edge(repo_name, node_name, length = length)
            nodelist.append(node_name)
            sizes.append(50)
            nodecolor.append(contr_color)

    fig, ax = plt.subplots(figsize=(8,8))
    ax.axis("off")
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color = nodecolor, nodelist=nodelist, node_size = sizes)
    plt.title(repo_name, fontsize=14)
    #plt.show()
    plt.savefig('results/' + repo_name + '.png')

