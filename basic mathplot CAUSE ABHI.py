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

    def add_image_at_origin(self, image_path, zoom=0.1):
        try:
            img = plt.imread(image_path)
            imagebox = OffsetImage(img, zoom=zoom)
            ab = AnnotationBbox(imagebox, (0, 0), frameon=False,
                                xycoords='axes fraction', box_alignment=(0, 0))
            self.ax.add_artist(ab)
        except FileNotFoundError:
            print(f"File not found: {image_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def format_axes(self):
        self.ax.grid(False)  # Set to True if you want the grid
        self.ax.set_xlabel("X-axis", fontsize=12)
        self.ax.set_ylabel("Y-axis", fontsize=12)
        self.ax.set_zlabel("Z-axis", fontsize=12)
        
        # Set tick values for each axis
        x_ticks = np.linspace(min(self.node_xyz[:, 0]), max(self.node_xyz[:, 0]), 5)
        y_ticks = np.linspace(min(self.node_xyz[:, 1]), max(self.node_xyz[:, 1]), 5)
        z_ticks = np.linspace(min(self.node_xyz[:, 2]), max(self.node_xyz[:, 2]), 5)
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)
        self.ax.set_zticks(z_ticks)
        
        # Optionally turn off the axis
        # self.ax.set_xticks([])
        # self.ax.set_yticks([])
        # self.ax.set_zticks([])

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

# Format the axes
graph_plot.format_axes()

# Before showing the plot, add the image at the bottom left corner
graph_plot.add_image_at_origin('hooman.png', zoom=0.02)

# Finally, display the plot
graph_plot.show()
