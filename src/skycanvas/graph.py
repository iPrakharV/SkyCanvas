from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from random import Random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


PositionMap = dict[int, np.ndarray]


@dataclass(frozen=True)
class GraphScene:
    graph: nx.Graph
    positions: PositionMap

    @property
    def node_array(self) -> np.ndarray:
        return np.array([self.positions[node] for node in sorted(self.graph.nodes)])


def build_cycle_scene(node_count: int = 20, seed: int = 779) -> GraphScene:
    if node_count < 3:
        raise ValueError("node_count must be at least 3")

    graph = nx.cycle_graph(node_count)
    positions = nx.spring_layout(graph, dim=3, seed=seed)
    return GraphScene(graph=graph, positions=positions)


def build_dodecahedral_scene(seed: int = 779) -> GraphScene:
    graph = nx.dodecahedral_graph()
    positions = nx.spring_layout(graph, dim=3, seed=seed)
    return GraphScene(graph=graph, positions=positions)


def random_walk_path(
    graph: nx.Graph,
    *,
    start: int = 0,
    steps: int = 25,
    seed: int | None = 779,
) -> list[int]:
    if start not in graph:
        raise ValueError(f"start node {start} is not in the graph")
    if steps < 0:
        raise ValueError("steps must be non-negative")

    rng = Random(seed)
    current = start
    path = [current]

    for _ in range(steps):
        neighbors = sorted(graph.neighbors(current))
        if not neighbors:
            path.append(current)
            continue
        current = rng.choice(neighbors)
        path.append(current)

    return path


def render_scene(
    scene: GraphScene,
    *,
    output_path: str | Path | None = None,
    highlight_node: int | None = None,
    show_labels: bool = False,
    title: str | None = None,
    elevation: float = 24,
    azimuth: float = 38,
    show: bool = False,
) -> tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=(8, 6), facecolor="#f7f7f2")
    ax = fig.add_subplot(111, projection="3d", facecolor="#f7f7f2")
    ax.view_init(elev=elevation, azim=azimuth)
    ax.set_axis_off()

    node_xyz = scene.node_array
    ax.scatter(*node_xyz.T, s=140, color="#1d4ed8", alpha=0.28)

    for start, end in scene.graph.edges:
        edge_xyz = np.array((scene.positions[start], scene.positions[end]))
        ax.plot(*edge_xyz.T, color="#334155", alpha=0.42, linewidth=1.5)

    if highlight_node is not None:
        if highlight_node not in scene.graph:
            raise ValueError(f"highlight node {highlight_node} is not in the graph")
        node_position = scene.positions[highlight_node]
        ax.scatter(*node_position, s=220, color="#dc2626", marker="s", alpha=0.95)

    if show_labels:
        for node in sorted(scene.graph.nodes):
            ax.text(*scene.positions[node], str(node), color="#0f172a", fontsize=8)

    if title:
        ax.set_title(title, color="#0f172a", fontsize=16, pad=14)

    fig.tight_layout()

    if output_path is not None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=180, bbox_inches="tight")

    if show:
        plt.show()

    return fig, ax
