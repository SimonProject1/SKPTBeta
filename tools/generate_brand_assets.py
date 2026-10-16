#!/usr/bin/env python3
"""Generate the SK PCT Tools V2.6.3.0-Beta brand and PWA logo family.

The mark deliberately reuses the exact industrial frame language of the approved
navigation icons while keeping the PCT / Tool's by S.K. identity. The redundant
small SK nameplate above the gear is intentionally absent because the ownership
line is already present below. Standard icons retain transparent outer corners;
maskable/iOS variants use an opaque, full-bleed background and keep the complete
brand mark in the central safe zone.
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAV_SOURCE = Path(__file__).with_name("generate_png_icons.py")
spec = importlib.util.spec_from_file_location("sk_pct_icon_system", NAV_SOURCE)
nav = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(nav)

SIZE = nav.SIZE
SCALE = nav.SCALE
CANVAS = nav.CANVAS


def gear_points(cx: float, cy: float, root_radius: float = 123, tooth_radius: float = 151, teeth: int = 12):
    result = []
    for index in range(teeth * 4):
        angle = -math.pi / 2 + index * 2 * math.pi / (teeth * 4)
        radius = tooth_radius if index % 4 in (1, 2) else root_radius
        result.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    return result


def add_brand_mark(image: Image.Image) -> Image.Image:
    """Draw only the protected central brand mark; all geometry stays mask-safe."""
    draw = ImageDraw.Draw(image)
    # The gear is deliberately larger after removing the redundant upper SK block.
    gear = nav.points(gear_points(256, 220))
    draw.polygon(gear, fill=(207, 220, 230, 255))
    draw.line(gear + [gear[0]], fill=nav.BLACK, width=nav.sc(15), joint="curve")

    # Industrial dark core and two function-colored signal arcs.
    draw.ellipse(nav.box((151, 115, 361, 325)), fill=nav.BLACK)
    draw.ellipse(nav.box((168, 132, 344, 308)), fill=(5, 23, 36, 255), outline=(32, 65, 84, 255), width=nav.sc(9))
    draw.arc(nav.box((165, 129, 347, 311)), 188, 302, fill=nav.CYAN, width=nav.sc(9))
    draw.arc(nav.box((165, 129, 347, 311)), 8, 122, fill=nav.GREEN, width=nav.sc(9))

    # Dominant product identity remains readable down to favicon size.
    nav.text_center(draw, (256, 221), "PCT", 92, fill=nav.WHITE, stroke=4, stroke_fill=nav.BLACK)

    # The ownership field grows with the main mark and remains inside the safe zone.
    nav.rr(draw, (116, 342, 396, 412), 18, fill=nav.WHITE, contour=12)
    nav.text_center(draw, (256, 374), "TOOL'S BY S.K.", 29, fill=nav.BLACK)
    nav.accent_bar(draw, [(140, 399), (248, 399)], nav.CYAN, 5)
    nav.accent_bar(draw, [(264, 399), (372, 399)], nav.GREEN, 5)
    return image


def standard_master() -> Image.Image:
    return nav.finalize(add_brand_mark(nav.frame()))


def maskable_master() -> Image.Image:
    # Full-bleed, opaque base: crop-safe for circle, squircle and rounded-square masks.
    background = nav.area_gradient().resize((CANVAS, CANVAS), Image.Resampling.BICUBIC)
    image = Image.new("RGBA", (CANVAS, CANVAS), nav.DARK)
    image.alpha_composite(background)
    depth = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    depth_draw = ImageDraw.Draw(depth)
    depth_draw.ellipse(nav.box((-70, -150, 390, 250)), fill=(255, 255, 255, 16))
    depth_draw.ellipse(nav.box((116, 292, 570, 620)), fill=(0, 0, 0, 30))
    image = Image.alpha_composite(image, depth)
    draw = ImageDraw.Draw(image)
    # Decorative rails may be masked; the full central mark remains inside the safe circle.
    for pts, color in (
        ([(28, 48), (188, 48)], nav.CYAN),
        ([(48, 28), (48, 188)], nav.CYAN),
        ([(324, 464), (484, 464)], nav.GREEN),
        ([(464, 324), (464, 484)], nav.GREEN),
    ):
        nav.thick_line(draw, pts, color=color, width=5, black_width=12)
    for x, y, color in ((48, 48, nav.CYAN), (188, 48, nav.CYAN), (48, 188, nav.CYAN), (324, 464, nav.GREEN), (464, 324, nav.GREEN), (464, 464, nav.GREEN)):
        nav.node(draw, x, y, color, 6)
    image = add_brand_mark(image)
    result = nav.finalize(image).convert("RGBA")
    # Maskable and iOS assets must be fully opaque; translucent decorative layers
    # affect RGB shading only and may never punch holes into the full-bleed base.
    result.putalpha(255)
    return result


def save_resized(source: Image.Image, filename: str, size: int) -> None:
    image = source if source.size == (size, size) else source.resize((size, size), Image.Resampling.LANCZOS)
    image.save(ASSETS / filename, format="PNG", optimize=True)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    standard = standard_master()
    maskable = maskable_master()
    save_resized(standard, "logo-sk-pct-tools.png", 512)
    save_resized(standard, "icon-512.png", 512)
    save_resized(standard, "icon-192.png", 192)
    save_resized(standard, "favicon.png", 64)
    save_resized(maskable, "apple-touch-icon.png", 180)
    save_resized(maskable, "icon-maskable-192.png", 192)
    save_resized(maskable, "icon-maskable-512.png", 512)
    print("Generated 7 SK PCT Tools V2.6.3.0-Beta brand/PWA assets")


if __name__ == "__main__":
    main()
