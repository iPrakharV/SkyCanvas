import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# The graph to visualize
G = nx.cycle_graph(20)

# 3D spring layout
pos = nx.spring_layout(G, dim=3, seed=779)
# Extract node and edge positions from the layout
node_xyz = np.array([pos[v] for v in sorted(G)])
edge_xyz = np.array([(pos[u], pos[v]) for u, v in G.edges()])

# Create the 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Plot the nodes - in shades of pink with edge colors in white for contrast
ax.scatter(*node_xyz.T, s=100, c="hotpink", edgecolor="w")

# Plot the edges in a lighter shade of pink
for vizedge in edge_xyz:
    ax.plot(*vizedge.T, color="lightpink")

# Add node labels with a fabulous pink hue
for i, xyz in enumerate(node_xyz):
    ax.text(*xyz, f'{i}', color='deeppink', fontsize=10, ha='center', va='center')

# Format axes to show the tick labels
ax.grid(True)
ax.set_xlabel("X-axis", fontsize=12)
ax.set_ylabel("Y-axis", fontsize=12)
ax.set_zlabel("Z-axis", fontsize=12)

plt.show()
