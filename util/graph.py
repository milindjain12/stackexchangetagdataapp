import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    Tag_G = None

    def __init__(self):
        self.Tag_G = nx.Graph()

    def createGraph(self, stack_exchange_tags):
        for tag in stack_exchange_tags:
            prev = []
            for item in tag:
                if item not in self.Tag_G:
                    self.Tag_G.add_node(item)
                if(len(prev) != 0):
                    for node in prev:
                        if(self.Tag_G.has_edge(item, node)):
                            wt = self.Tag_G[item][node]["weight"]
                            self.Tag_G[item][node]["weight"] = wt+1
                        else:
                            self.Tag_G.add_edge(item, node, weight=1)
                prev.append(item)

    def generateEdgeList(self):
        print("Edge List:")
        for ed in nx.generate_edgelist(self.Tag_G):
            print(ed)

    def findNeighborsOfaTag(self, tag):
        try:
            neighbors_list = list(self.Tag_G.neighbors(tag))
            edge_with_weights = []
            for neighbor in neighbors_list:
                wt = self.Tag_G.get_edge_data(tag, neighbor)
                edge_with_weights.append((neighbor, wt["weight"]))
            edge_with_weights = tuple(
                sorted(edge_with_weights, key=lambda x: x[1], reverse=True))
            associated_tags = self.generateAssociatedTags(
                tag, edge_with_weights)
            return associated_tags
        except nx.NetworkXError:
            return []

    def generateAssociatedTags(self, tag, edge_with_weights):
        associatedTags = []
        for edge in edge_with_weights:
            associatedTags.append(edge[0])
        return associatedTags[:5]

    def plotGraph(self):
        # set figure size
        plt.figure(figsize=(50, 50))
        e_list = [(u, v) for (u, v, d) in self.Tag_G.edges(data=True)]

        pos = nx.spring_layout(self.Tag_G)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(self.Tag_G, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(self.Tag_G, pos, edgelist=e_list, width=1)

        # labels
        nx.draw_networkx_labels(
            self.Tag_G, pos, font_size=8, font_family='sans-serif')
        plt.axis('off')
        plt.show()
