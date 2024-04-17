import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import networkx as nx
import numpy as np

class GraphPlot3D:
    def __init__(self, graph, positions):
        self.graph = graph
        self.positions = positions
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.node_xyz = np.array([self.positions[v] for v in sorted(self.graph)])

    def plot_nodes(self, node_color='hotpink', node_size=100, edge_color='w'):
        self.ax.scatter(*self.node_xyz.T, s=node_size, c=node_color, edgecolor=edge_color)

    def plot_edges(self, line_color='lightpink'):
        edge_xyz = np.array([(self.positions[u], self.positions[v]) for u, v in self.graph.edges()])
        for vizedge in edge_xyz:
            self.ax.plot(*vizedge.T, color=line_color)

    def add_labels(self, font_color='deeppink', font_size=10):
        for i, xyz in enumerate(self.node_xyz):
            self.ax.text(*xyz, f'{i}', color=font_color, fontsize=font_size, ha='center', va='center')

    def add_image_at_origin(self, image_path, zoom=0.1, layer=0):
        img = plt.imread(image_path)
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (0, 0, layer), frameon=False, boxcoords="data", pad=0, xycoords='data')
        self.ax.add_artist(ab)

    def format_axes(self):
        self.ax.grid(True)
        self.ax.set_xlabel("X-axis", fontsize=12)
        self.ax.set_ylabel("Y-axis", fontsize=12)
        self.ax.set_zlabel("Z-axis", fontsize=12)
        self.ax.set_axis_off()  # Optional: turn off the axis

    def show(self):
        plt.show()

# Create a cycle graph
G = nx.cycle_graph(20)
# Generate a 3D spring layout
pos = nx.spring_layout(G, dim=3, seed=779)

# Create an instance of the GraphPlot3D class
graph_plot = GraphPlot3D(G, pos)

# Plot nodes, edges, and add labels
graph_plot.plot_nodes()
graph_plot.plot_edges()
graph_plot.add_labels()

# Load an image and place it at the origin
graph_plot.add_image_at_origin('/assets/images/hooman.png.png', zoom=0.05, layer=-0.1)  # Adjust 'path_to_your_image.png' and other parameters as needed

# Format the axes and show the plot
graph_plot.format_axes()
graph_plot.show()
