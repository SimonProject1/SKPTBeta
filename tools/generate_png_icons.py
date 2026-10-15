#!/usr/bin/env python3
"""Generate the controlled V2.6.1.1-Beta navigation icon series.

The PNG files contain only transparent pixels plus simple white/neutral symbols
with a black cartoon outline. The common blue-cyan-green tech frame and every
favorite state are rendered centrally by CSS, never embedded in a PNG.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = 512
SCALE = 4
CANVAS = SIZE * SCALE
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "navigation-icons"
PREFIX = "v2-6-1-1-"
WHITE = (255, 255, 255, 255)
SOFT = (222, 222, 222, 255)
BLACK = (0, 0, 0, 255)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_CONDENSED = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"


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
        if candidate.getbbox(text)[2] <= sc(max_width):
            return candidate
    return font(minimum, condensed=True)


def outlined_line(draw: ImageDraw.ImageDraw, coords, white_width: int, black_width: int | None = None):
    black_width = black_width or white_width + 20
    draw.line(points(coords), fill=BLACK, width=sc(black_width), joint="curve")
    draw.line(points(coords), fill=WHITE, width=sc(white_width), joint="curve")


def outlined_round_rect(draw: ImageDraw.ImageDraw, rect, radius: int, white_width: int, black_width: int | None = None):
    black_width = black_width or white_width + 20
    draw.rounded_rectangle(box(rect), radius=sc(radius), outline=BLACK, width=sc(black_width))
    draw.rounded_rectangle(box(rect), radius=sc(radius), outline=WHITE, width=sc(white_width))


def calculator() -> Image.Image:
    """Simple white calculator: display, six keys and a readable plus/minus."""
    image = canvas()
    draw = ImageDraw.Draw(image)
    outlined_round_rect(draw, (102, 46, 410, 466), 52, 24, 46)
    outlined_round_rect(draw, (142, 94, 370, 186), 18, 18, 36)
    # A single quiet display mark; no numbers or micro labels.
    outlined_line(draw, [(176, 140), (336, 140)], 16, 32)
    centers = [(164, 264), (256, 264), (348, 264), (164, 368), (256, 368), (348, 368)]
    for cx, cy in centers:
        draw.rounded_rectangle(box((cx - 28, cy - 24, cx + 28, cy + 24)), radius=sc(11), fill=BLACK)
        draw.rounded_rectangle(box((cx - 17, cy - 14, cx + 17, cy + 14)), radius=sc(7), fill=SOFT)
    return image


def book() -> Image.Image:
    """Simple white open book / reference-work symbol."""
    image = canvas()
    draw = ImageDraw.Draw(image)
    left = [(62, 112), (156, 78), (244, 118), (244, 432), (157, 397), (62, 430), (62, 112)]
    right = [(450, 112), (356, 78), (268, 118), (268, 432), (355, 397), (450, 430), (450, 112)]
    outlined_line(draw, left, 27, 51)
    outlined_line(draw, right, 27, 51)
    outlined_line(draw, [(256, 116), (256, 433)], 24, 48)
    # One broad page cue per side, deliberately without writing or tiny lines.
    outlined_line(draw, [(112, 158), (182, 134)], 15, 31)
    outlined_line(draw, [(400, 158), (330, 134)], 15, 31)
    return image


def globe() -> Image.Image:
    """Simple white WWW globe."""
    image = canvas()
    draw = ImageDraw.Draw(image)
    sphere = box((58, 58, 454, 454))
    draw.ellipse(sphere, outline=BLACK, width=sc(46))
    draw.ellipse(sphere, outline=WHITE, width=sc(24))
    for rect in ((154, 68, 358, 444), (86, 150, 426, 362)):
        draw.ellipse(box(rect), outline=BLACK, width=sc(34))
        draw.ellipse(box(rect), outline=WHITE, width=sc(16))
    outlined_line(draw, [(256, 70), (256, 442)], 16, 34)
    outlined_line(draw, [(72, 256), (440, 256)], 16, 34)
    draw.text((sc(256), sc(258)), "WWW", font=font(38, condensed=True), fill=WHITE,
              stroke_width=sc(7), stroke_fill=BLACK, anchor="mm")
    return image


def manufacturer(mark: str) -> Image.Image:
    """Large quiet white manufacturer mark without category plaques."""
    image = canvas()
    draw = ImageDraw.Draw(image)
    lines = mark.split("\n")
    start_y = 256 if len(lines) == 1 else 205
    step = 102
    fnt = fit_font(max(lines, key=len), 405, 105 if len(lines) == 1 else 83, 38)
    for index, text in enumerate(lines):
        draw.text((sc(256), sc(start_y + index * step)), text, font=fnt, fill=WHITE,
                  stroke_width=sc(11), stroke_fill=BLACK, anchor="mm")
    return image


def home_icon() -> Image.Image:
    image = canvas()
    draw = ImageDraw.Draw(image)
    roof = [(58, 244), (256, 62), (454, 244), (405, 293), (256, 158), (107, 293)]
    body = (135, 239, 377, 452)
    draw.polygon(points(roof), fill=BLACK)
    inset_roof = [(91, 242), (256, 91), (421, 242), (398, 265), (256, 137), (114, 265)]
    draw.polygon(points(inset_roof), fill=WHITE)
    draw.rounded_rectangle(box(body), radius=sc(31), fill=BLACK)
    draw.rounded_rectangle(box((158, 261, 354, 430)), radius=sc(22), fill=WHITE)
    draw.rounded_rectangle(box((224, 324, 288, 452)), radius=sc(12), fill=BLACK)
    return image


def back_icon() -> Image.Image:
    image = canvas()
    draw = ImageDraw.Draw(image)
    arrow = [(224, 56), (34, 256), (224, 456), (307, 374), (237, 304), (474, 304), (474, 208), (237, 208), (307, 138)]
    draw.polygon(points(arrow), fill=BLACK)
    inner = [(225, 96), (75, 256), (225, 416), (270, 372), (185, 286), (442, 286), (442, 226), (185, 226), (270, 140)]
    draw.polygon(points(inner), fill=WHITE)
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

    calculator_names = (
        "app-analogsignal", "app-pf-rechner", "app-pt-rechner",
        "app-einheitenrechner", "app-spannungsfall", "app-siemens-rohwert",
    )
    calculator_master = calculator()
    for name in calculator_names:
        save(name, calculator_master)

    book_master = book()
    for name in ("app-einheitendatenbank", "app-werkstoffdatenbank", "app-wissensdatenbank"):
        save(name, book_master)

    save("app-eh-viewer", globe())
    save("manufacturer-air-torque", manufacturer("AIR\nTORQUE"))
    save("manufacturer-endress-hauser", manufacturer("E+H"))
    save("manufacturer-siemens", manufacturer("SIEMENS"))
    save("manufacturer-sonstiges", manufacturer("ALLG."))
    save("manufacturer-vacon", manufacturer("VACON"))
    save("nav-back", back_icon())
    save("nav-home", home_icon())
    print(f"Generated {len(list(OUT.glob('*.png')))} controlled icons in {OUT}")


if __name__ == "__main__":
    main()
