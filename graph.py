import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation

# Create the dodecahedral graph
G = nx.dodecahedral_graph()

# Position nodes using 3D spectral layout
pos = nx.spectral_layout(G, dim=3)
nodes = np.array([pos[v] for v in G])
edges = np.array([(pos[u], pos[v]) for u, v in G.edges()])

# Initialize plot for rotating 3D graph
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.set_axis_off()

def init():
    # Plot nodes
    ax.scatter(*nodes.T, alpha=0.2, s=100, color='blue')
    # Plot edges
    for vizedge in edges:
        ax.plot(*vizedge.T, color='gray')
    return fig,

def update(frame):
    # Rotate the view
    ax.view_init(30, frame)
    return fig,

# Create the animation for rotating 3D graph
ani = animation.FuncAnimation(fig, update, init_func=init, frames=np.arange(0, 360, 2), interval=50)

# Random walk on rotating 3D graph
# Initialize the node for random walk
node = [0]

def update_random_walk(frame):
    ax.clear()
    ax.set_axis_off()
    ax.scatter(*nodes.T, alpha=0.2, s=100, color="blue")
    for vizedge in edges:
        ax.plot(*vizedge.T, color="gray")
    
    # Random walk logic
    neighbors = list(G.neighbors(node[0]))
    if frame % 5 == 0:
        node[0] = np.random.choice(neighbors)
    
    node_pos = nodes[node[0]]
    ax.scatter(*node_pos, color="red", s=200, marker='o')
    ax.view_init(30, frame)
    return fig,

# Create the animation for random walk on rotating 3D graph
ani2 = animation.FuncAnimation(fig, update_random_walk, frames=np.arange(0, 360, 2), interval=50)

plt.show()
