#!/usr/bin/env python3
"""Generate only the simplified visible header logo for SK PCT Tools V2.6.3.9-Beta.

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

    # A narrow black contour surrounds a calm, light cyan-steel center. This keeps
    # the gear crisp at 44/52 px while replacing the former heavy dark inner disc.
    draw.ellipse(nav.box((160, 160, 352, 352)), fill=nav.BLACK)
    draw.ellipse(nav.box((175, 175, 337, 337)), fill=(209, 231, 235, 255))
    draw.arc(nav.box((177, 177, 335, 335)), 200, 322, fill=nav.CYAN, width=nav.sc(6))

    # Dark PCT lettering on the light center remains readable at the real header size.
    nav.text_center(draw, (256, 257), "PCT", 76, fill=nav.BLACK, stroke=1, stroke_fill=nav.WHITE)
    return nav.finalize(image)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    build().save(OUT, format="PNG", optimize=True)
    print(f"Generated {OUT.relative_to(ROOT)} only")


if __name__ == "__main__":
    main()
