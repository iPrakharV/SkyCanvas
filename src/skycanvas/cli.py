from __future__ import annotations

import argparse
from pathlib import Path

from .graph import (
    build_cycle_scene,
    build_dodecahedral_scene,
    random_walk_path,
    render_scene,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a 3D graph layout for the SkyCanvas prototype."
    )
    parser.add_argument(
        "--graph",
        choices=("cycle", "dodecahedral"),
        default="dodecahedral",
        help="Graph topology to render.",
    )
    parser.add_argument(
        "--nodes",
        type=int,
        default=20,
        help="Node count for the cycle graph.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=779,
        help="Seed used for the cycle layout and random walk.",
    )
    parser.add_argument(
        "--walk-steps",
        type=int,
        default=25,
        help="Random-walk steps before selecting the highlighted node.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/demo.png"),
        help="Path for the rendered PNG.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Open the Matplotlib window after rendering.",
    )
    parser.add_argument(
        "--labels",
        action="store_true",
        help="Show node labels in the rendered image.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.graph == "cycle":
        scene = build_cycle_scene(node_count=args.nodes, seed=args.seed)
        title = f"Cycle graph with {args.nodes} nodes"
    else:
        scene = build_dodecahedral_scene(seed=args.seed)
        title = "Dodecahedral graph layout"

    walk = random_walk_path(scene.graph, steps=args.walk_steps, seed=args.seed)
    render_scene(
        scene,
        output_path=args.output,
        highlight_node=walk[-1],
        show_labels=args.labels,
        title=title,
        show=args.show,
    )
    print(f"Wrote {args.output}")
    return 0
