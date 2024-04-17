import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

# Create the dodecahedral graph
G = nx.dodecahedral_graph()

# Position nodes using 3D spectral layout
pos = nx.spectral_layout(G, dim=3)
nodes = np.array([pos[v] for v in sorted(G)])
edges = np.array([(pos[u], pos[v]) for u, v in G.edges()])

# Set up the figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize function for the animation
def init():
    # Plot the nodes
    ax.scatter(*nodes.T, s=100, color='blue', alpha=0.6)
    # Plot the edges
    for edge in edges:
        ax.plot(*zip(*edge), color='gray')
    # Set the initial view
    ax.view_init(elev=20, azim=30)
    # Hide the axes
    ax.set_axis_off()
    return fig,

# Update function for the animation
def update(num):
    # Rotate the view
    ax.view_init(elev=20, azim=num)
    return fig,

# Create the animation
ani = animation.FuncAnimation(fig, update, init_func=init, frames=range(0, 360, 2), interval=50, blit=False)

# Display the plot
plt.show()
