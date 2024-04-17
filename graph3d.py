import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation
import random
from mpl_toolkits.mplot3d import Axes3D

# Make sure to use an interactive backend like TkAgg, Qt5Agg, etc.
# import matplotlib
# matplotlib.use('TkAgg')

# Create the dodecahedral graph
G = nx.dodecahedral_graph()

# Position nodes using 3D spectral layout
pos = nx.spectral_layout(G, dim=3)
nodes = np.array([pos[v] for v in sorted(G)])
edges = np.array([(pos[u], pos[v]) for u, v in G.edges()])

# Setup the 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_axis_off()  # Hide the grid and axis

node = [0]  # Start with node 0 for the random walk

# Frame update function for the animation
def _frame_update(index):
    ax.clear()  # Clear previous frame
    ax.set_axis_off()  # Ensure axis is off after clearing

    # Scatter plot for nodes and plot for edges
    ax.scatter(*nodes.T, alpha=0.2, s=100, color="blue")
    for vizedge in edges:
        ax.plot(*vizedge.T, color="gray")
    
    # Random walk logic
    neighbors = list(G.neighbors(node[0]))
    if index % 5 == 0:  # Change the node at every 5th frame
        node[0] = random.choice(neighbors)
    node_pos = nodes[node[0]]
    
    # Highlight the current node in the random walk
    ax.scatter(*node_pos, alpha=1, marker="s", color="red", s=100)
    
    # Rotate the view for a dynamic effect
    ax.view_init(elev=30, azim=index * 0.5)
    
    return fig,

# Create the animation
ani = animation.FuncAnimation(fig, _frame_update, frames=range(100), interval=50, blit=False)

plt.show()  # Display the plot
