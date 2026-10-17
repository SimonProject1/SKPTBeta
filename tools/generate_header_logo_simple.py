#!/usr/bin/env python3
"""Generate only the simplified visible header logo for SK PCT Tools V2.6.3.8-Beta.

This standalone generator deliberately writes only assets/header-logo-simple.png.
It must never overwrite the approved PWA, favicon, Apple touch, maskable or
installed-app logo family.
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from PIL import ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "header-logo-simple.png"
NAV_SOURCE = Path(__file__).with_name("generate_png_icons.py")
spec = importlib.util.spec_from_file_location("sk_pct_icon_system", NAV_SOURCE)
nav = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(nav)


def gear_points(cx: float, cy: float, root_radius: float = 108, tooth_radius: float = 146, teeth: int = 10):
    """Return a deliberately low-detail, calm ten-tooth gear."""
    points = []
    for index in range(teeth * 4):
        angle = -math.pi / 2 + index * 2 * math.pi / (teeth * 4)
        radius = tooth_radius if index % 4 in (1, 2) else root_radius
        points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    return points


def build():
    # Exact body/material family used by Search, Favorites and the release module.
    image = nav.navigation_frame()
    draw = ImageDraw.Draw(image)

    # One large, quiet PCT gear: no circuit rails, nodes, fasteners or extra frame.
    gear = nav.points(gear_points(256, 256))
    draw.polygon(gear, fill=(222, 232, 239, 255))
    draw.line(gear + [gear[0]], fill=nav.BLACK, width=nav.sc(17), joint="curve")

    # Strong central disc and one restrained cyan light edge preserve PCT identity.
    draw.ellipse(nav.box((151, 151, 361, 361)), fill=nav.BLACK)
    draw.ellipse(nav.box((171, 171, 341, 341)), fill=(5, 23, 36, 255))
    draw.arc(nav.box((171, 171, 341, 341)), 202, 322, fill=nav.CYAN, width=nav.sc(7))

    # Large high-contrast lettering remains readable at the real 44/52 px header size.
    nav.text_center(draw, (256, 257), "PCT", 74, fill=nav.WHITE, stroke=4, stroke_fill=nav.BLACK)
    return nav.finalize(image)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    build().save(OUT, format="PNG", optimize=True)
    print(f"Generated {OUT.relative_to(ROOT)} only")


if __name__ == "__main__":
    main()
