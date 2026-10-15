#!/usr/bin/env python3
"""Generate the controlled V2.6.1.4-Beta PNG navigation icon series.

The V2.6.1.2 green-left / blue-upper-right background master is preserved
pixel-for-pixel. Only the white foreground motifs are rebuilt on one shared
symbol grid. Favorite stars remain interactive CSS/HTML controls and are never
baked into the PNG files.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = 512
SCALE = 4
CANVAS = SIZE * SCALE
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "navigation-icons"
PREFIX = "v2-6-1-4-"
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_CONDENSED = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"

# Binding foreground grid in final 512 px coordinates.
SYMBOL_CENTER = (256, 246)
SYMBOL_BOX = (112, 106, 400, 386)  # 288 × 280 px, star-independent.
SYMBOL_MAX_WIDTH = SYMBOL_BOX[2] - SYMBOL_BOX[0]
SYMBOL_MAX_HEIGHT = SYMBOL_BOX[3] - SYMBOL_BOX[1]
MOTIF_CONTOUR = 16                # Identical visible outer comic contour.
DETAIL_CONTOUR = 10               # Closed internal white surfaces.
_FRAME_MASTER: Image.Image | None = None


def sc(value: float) -> int:
    return round(value * SCALE)


def box(values):
    return tuple(sc(v) for v in values)


def points(values):
    return [(sc(x), sc(y)) for x, y in values]


def canvas() -> Image.Image:
    return Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))


def font(size: int, condensed: bool = False):
    return ImageFont.truetype(FONT_CONDENSED if condensed else FONT_BOLD, sc(size))


def fit_font(text: str, max_width: int, start: int, minimum: int = 18):
    for size in range(start, minimum - 1, -1):
        candidate = font(size, condensed=True)
        if candidate.getbbox(text, stroke_width=sc(MOTIF_CONTOUR))[2] <= sc(max_width):
            return candidate
    return font(minimum, condensed=True)


def area_gradient() -> Image.Image:
    """V2.6.1.2 background master — do not change."""
    w = h = sc(410)
    image = Image.new("RGBA", (w, h))
    pixels = image.load()
    stops = (
        (0.00, (47, 158, 96)),
        (0.46, (22, 137, 143)),
        (1.00, (25, 99, 177)),
    )
    for y in range(h):
        yn = y / max(1, h - 1)
        for x in range(w):
            xn = x / max(1, w - 1)
            t = max(0.0, min(1.0, 0.76 * xn + 0.24 * (1.0 - yn)))
            for index in range(len(stops) - 1):
                p0, c0 = stops[index]
                p1, c1 = stops[index + 1]
                if p0 <= t <= p1:
                    f = (t - p0) / (p1 - p0)
                    rgb = tuple(round(c0[i] + (c1[i] - c0[i]) * f) for i in range(3))
                    break
            lift = round(9 * (1.0 - yn) - 7 * yn)
            pixels[x, y] = tuple(max(0, min(255, v + lift)) for v in rgb) + (255,)
    return image


def frame() -> Image.Image:
    """Pixel-identical V2.6.1.2 tile body, contour, depth, and gradient."""
    global _FRAME_MASTER
    if _FRAME_MASTER is not None:
        return _FRAME_MASTER.copy()
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(box((30, 32, 486, 488)), radius=sc(112), fill=(0, 0, 0, 150))
    draw.rounded_rectangle(box((16, 12, 470, 466)), radius=sc(112), fill=BLACK)

    inner_rect = box((38, 34, 448, 444))
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).rounded_rectangle(inner_rect, radius=sc(82), fill=255)
    gradient = area_gradient().resize(
        (inner_rect[2] - inner_rect[0], inner_rect[3] - inner_rect[1]),
        Image.Resampling.BICUBIC,
    )
    layer = canvas()
    layer.paste(gradient, (inner_rect[0], inner_rect[1]))
    image.alpha_composite(Image.composite(layer, canvas(), mask))

    sheen = canvas()
    sd = ImageDraw.Draw(sheen)
    sd.ellipse(box((14, -130, 390, 244)), fill=(255, 255, 255, 20))
    sd.ellipse(box((120, 294, 520, 610)), fill=(0, 0, 0, 22))
    sheen.putalpha(Image.composite(sheen.getchannel("A"), Image.new("L", (CANVAS, CANVAS), 0), mask))
    image.alpha_composite(sheen)
    _FRAME_MASTER = image.copy()
    return image


def closed_round_rect(draw: ImageDraw.ImageDraw, rect, radius: int, contour: int = MOTIF_CONTOUR):
    """Closed white surface with one centered, rounded black contour."""
    draw.rounded_rectangle(box(rect), radius=sc(radius), fill=WHITE, outline=BLACK, width=sc(contour))


def closed_polygon(draw: ImageDraw.ImageDraw, vertices, contour: int = MOTIF_CONTOUR):
    """Closed white polygon with rounded line joins and one black contour."""
    pts = points(vertices)
    draw.polygon(pts, fill=WHITE)
    draw.line(pts + [pts[0]], fill=BLACK, width=sc(contour), joint="curve")


def calculator() -> Image.Image:
    """Symmetric calculator: one display, six equal buttons, no tiny details."""
    image = frame()
    draw = ImageDraw.Draw(image)
    closed_round_rect(draw, (138, 106, 374, 386), 38)
    closed_round_rect(draw, (174, 146, 338, 204), 12, DETAIL_CONTOUR)
    for cy in (258, 326):
        for cx in (188, 256, 324):
            closed_round_rect(draw, (cx - 19, cy - 18, cx + 19, cy + 18), 9, DETAIL_CONTOUR)
    return image


def book() -> Image.Image:
    """Two closed, mirror-symmetric white pages with a clear center fold."""
    image = frame()
    draw = ImageDraw.Draw(image)
    left = [(120, 144), (180, 120), (248, 148), (248, 370), (182, 344), (120, 370)]
    right = [(392, 144), (332, 120), (264, 148), (264, 370), (330, 344), (392, 370)]
    closed_polygon(draw, left)
    closed_polygon(draw, right)
    # Single rounded center fold, same visual contour family, no double outline.
    draw.line(points([(256, 146), (256, 368)]), fill=BLACK, width=sc(MOTIF_CONTOUR), joint="curve")
    draw.ellipse(box((248, 138, 264, 154)), fill=BLACK)
    draw.ellipse(box((248, 360, 264, 376)), fill=BLACK)
    return image


def globe() -> Image.Image:
    """Symmetric globe with few grid lines and a legible closed WWW band."""
    image = frame()
    draw = ImageDraw.Draw(image)
    sphere = (118, 108, 394, 384)
    draw.ellipse(box(sphere), fill=WHITE, outline=BLACK, width=sc(MOTIF_CONTOUR))
    # Two meridian arcs and two latitude arcs are enough at small sizes.
    draw.ellipse(box((196, 108, 316, 384)), outline=BLACK, width=sc(DETAIL_CONTOUR))
    draw.ellipse(box((118, 170, 394, 322)), outline=BLACK, width=sc(DETAIL_CONTOUR))
    # The white band closes the grid cleanly and keeps WWW readable at 64–80 px.
    closed_round_rect(draw, (126, 216, 386, 276), 14, DETAIL_CONTOUR)
    draw.text(
        (sc(256), sc(246)), "WWW", font=font(39, condensed=True), fill=BLACK,
        anchor="mm",
    )
    return image


def manufacturer(mark: str) -> Image.Image:
    """One standardized closed white nameplate; black text is an inner detail."""
    image = frame()
    draw = ImageDraw.Draw(image)
    closed_round_rect(draw, (112, 174, 400, 318), 32)
    lines = mark.split("\n")
    if len(lines) == 1:
        fnt = fit_font(lines[0], 244, 86, 36)
        draw.text(
            (sc(SYMBOL_CENTER[0]), sc(SYMBOL_CENTER[1])), lines[0], font=fnt,
            fill=BLACK, anchor="mm",
        )
    else:
        fnt = fit_font(max(lines, key=len), 244, 49, 36)
        for y, text in zip((220, 272), lines):
            draw.text(
                (sc(SYMBOL_CENTER[0]), sc(y)), text, font=fnt,
                fill=BLACK, anchor="mm",
            )
    return image


def home_icon() -> Image.Image:
    """Closed, symmetric home pictogram on the shared 288 × 280 grid."""
    image = frame()
    draw = ImageDraw.Draw(image)
    house = [
        (112, 236), (256, 106), (400, 236), (374, 264),
        (354, 246), (354, 386), (158, 386), (158, 246), (138, 264),
    ]
    closed_polygon(draw, house)
    closed_round_rect(draw, (226, 298, 286, 386), 10, DETAIL_CONTOUR)
    return image


def back_icon() -> Image.Image:
    """Closed white back arrow with a single rounded black contour."""
    image = frame()
    draw = ImageDraw.Draw(image)
    arrow = [
        (228, 106), (112, 246), (228, 386), (270, 344),
        (232, 304), (400, 304), (400, 188), (232, 188), (270, 148),
    ]
    closed_polygon(draw, arrow)
    return image


def finalize(image: Image.Image) -> Image.Image:
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def save(name: str, image: Image.Image):
    finalize(image).save(OUT / f"{PREFIX}{name}.png", format="PNG", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*"):
        if old.is_file():
            old.unlink()

    # Pixelidentische App-Motive werden einmal als gemeinsamer Master ausgeliefert.
    # Die semantische Zuordnung bleibt im HTML, Manifest und Suchindex erhalten.
    save("app-calculator", calculator())
    save("app-database", book())
    save("app-eh-viewer", globe())
    save("manufacturer-air-torque", manufacturer("AIR\nTORQUE"))
    save("manufacturer-endress-hauser", manufacturer("E+H"))
    save("manufacturer-siemens", manufacturer("SIEMENS"))
    save("manufacturer-sonstiges", manufacturer("ALLG."))
    save("manufacturer-vacon", manufacturer("VACON"))
    save("nav-back", back_icon())
    save("nav-home", home_icon())
    print(
        f"Generated {len(list(OUT.glob('*.png')))} controlled icons in {OUT} · "
        f"grid={SYMBOL_BOX} · center={SYMBOL_CENTER} · contour={MOTIF_CONTOUR}px"
    )


if __name__ == "__main__":
    main()
