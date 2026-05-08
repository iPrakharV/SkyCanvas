from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")

from skycanvas import (  # noqa: E402
    build_cycle_scene,
    build_dodecahedral_scene,
    random_walk_path,
    render_scene,
)


def test_cycle_scene_uses_requested_node_count() -> None:
    scene = build_cycle_scene(node_count=8, seed=1)

    assert scene.graph.number_of_nodes() == 8
    assert scene.graph.number_of_edges() == 8
    assert scene.node_array.shape == (8, 3)


def test_dodecahedral_scene_shape() -> None:
    scene = build_dodecahedral_scene()

    assert scene.graph.number_of_nodes() == 20
    assert scene.graph.number_of_edges() == 30
    assert scene.node_array.shape == (20, 3)


def test_random_walk_is_reproducible() -> None:
    scene = build_cycle_scene(node_count=8, seed=1)

    first = random_walk_path(scene.graph, start=0, steps=10, seed=42)
    second = random_walk_path(scene.graph, start=0, steps=10, seed=42)

    assert first == second
    assert len(first) == 11
    assert all(node in scene.graph for node in first)


def test_random_walk_rejects_invalid_start_node() -> None:
    scene = build_cycle_scene(node_count=8, seed=1)

    with pytest.raises(ValueError):
        random_walk_path(scene.graph, start=99)


def test_render_scene_writes_png(tmp_path: Path) -> None:
    scene = build_cycle_scene(node_count=8, seed=1)
    output_path = tmp_path / "scene.png"

    render_scene(scene, output_path=output_path, highlight_node=0)

    assert output_path.exists()
    assert output_path.stat().st_size > 0
