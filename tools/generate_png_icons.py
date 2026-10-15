#!/usr/bin/env python3
"""Generate the controlled V2.6.1.2-Beta PNG navigation icon series.

Each 512 × 512 RGBA file is a complete icon tile: transparent outer canvas,
subtle mechanical depth, a strong black rounded comic contour, a soft area
background that starts green at the left and transitions to blue toward the
upper right, and exactly one simple white symbol with a visible black outline.
Favorite stars remain interactive CSS/HTML controls and are never baked in.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SIZE = 512
SCALE = 4
CANVAS = SIZE * SCALE
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "navigation-icons"
PREFIX = "v2-6-1-2-"
WHITE = (255, 255, 255, 255)
SOFT = (238, 244, 247, 255)
BLACK = (0, 0, 0, 255)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_CONDENSED = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
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
        if candidate.getbbox(text)[2] <= sc(max_width):
            return candidate
    return font(minimum, condensed=True)


def area_gradient() -> Image.Image:
    """Muted green-left to blue-upper-right gradient without neon clipping."""
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
            # The left edge remains green; the strongest blue is upper right.
            t = max(0.0, min(1.0, 0.76 * xn + 0.24 * (1.0 - yn)))
            for index in range(len(stops) - 1):
                p0, c0 = stops[index]
                p1, c1 = stops[index + 1]
                if p0 <= t <= p1:
                    f = (t - p0) / (p1 - p0)
                    rgb = tuple(round(c0[i] + (c1[i] - c0[i]) * f) for i in range(3))
                    break
            # Gentle depth: slightly lighter above, slightly quieter below.
            lift = round(9 * (1.0 - yn) - 7 * yn)
            pixels[x, y] = tuple(max(0, min(255, v + lift)) for v in rgb) + (255,)
    return image


def frame() -> Image.Image:
    """Complete icon body with outer comic contour and soft depth."""
    global _FRAME_MASTER
    if _FRAME_MASTER is not None:
        return _FRAME_MASTER.copy()
    image = canvas()
    draw = ImageDraw.Draw(image)
    # Mechanical shadow remains inside the transparent 512 px master.
    draw.rounded_rectangle(box((30, 32, 486, 488)), radius=sc(112), fill=(0, 0, 0, 150))
    draw.rounded_rectangle(box((16, 12, 470, 466)), radius=sc(112), fill=BLACK)

    inner_rect = box((38, 34, 448, 444))
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).rounded_rectangle(inner_rect, radius=sc(82), fill=255)
    gradient = area_gradient().resize((inner_rect[2] - inner_rect[0], inner_rect[3] - inner_rect[1]), Image.Resampling.BICUBIC)
    layer = canvas()
    layer.paste(gradient, (inner_rect[0], inner_rect[1]))
    image.alpha_composite(Image.composite(layer, canvas(), mask))

    # Broad translucent highlight; it is not a second frame or short accent line.
    sheen = canvas()
    sd = ImageDraw.Draw(sheen)
    sd.ellipse(box((14, -130, 390, 244)), fill=(255, 255, 255, 20))
    sd.ellipse(box((120, 294, 520, 610)), fill=(0, 0, 0, 22))
    sheen.putalpha(Image.composite(sheen.getchannel("A"), Image.new("L", (CANVAS, CANVAS), 0), mask))
    image.alpha_composite(sheen)
    _FRAME_MASTER = image.copy()
    return image


def outlined_line(draw: ImageDraw.ImageDraw, coords, white_width: int, black_width: int | None = None):
    black_width = black_width or white_width + 20
    draw.line(points(coords), fill=BLACK, width=sc(black_width), joint="curve")
    draw.line(points(coords), fill=WHITE, width=sc(white_width), joint="curve")


def outlined_round_rect(draw: ImageDraw.ImageDraw, rect, radius: int, white_width: int, black_width: int | None = None):
    black_width = black_width or white_width + 20
    draw.rounded_rectangle(box(rect), radius=sc(radius), outline=BLACK, width=sc(black_width))
    draw.rounded_rectangle(box(rect), radius=sc(radius), outline=WHITE, width=sc(white_width))


def calculator() -> Image.Image:
    image = frame()
    draw = ImageDraw.Draw(image)
    outlined_round_rect(draw, (126, 90, 386, 394), 44, 22, 46)
    outlined_round_rect(draw, (157, 124, 355, 188), 15, 14, 32)
    outlined_line(draw, [(182, 156), (330, 156)], 12, 28)
    centers = [(176, 245), (256, 245), (336, 245), (176, 326), (256, 326), (336, 326)]
    for cx, cy in centers:
        draw.rounded_rectangle(box((cx - 25, cy - 22, cx + 25, cy + 22)), radius=sc(10), fill=BLACK)
        draw.rounded_rectangle(box((cx - 14, cy - 12, cx + 14, cy + 12)), radius=sc(6), fill=SOFT)
    return image


def book() -> Image.Image:
    image = frame()
    draw = ImageDraw.Draw(image)
    left = [(92, 142), (166, 110), (244, 145), (244, 390), (169, 362), (92, 390), (92, 142)]
    right = [(420, 142), (346, 110), (268, 145), (268, 390), (343, 362), (420, 390), (420, 142)]
    outlined_line(draw, left, 24, 50)
    outlined_line(draw, right, 24, 50)
    outlined_line(draw, [(256, 142), (256, 391)], 21, 45)
    return image


def globe() -> Image.Image:
    image = frame()
    draw = ImageDraw.Draw(image)
    sphere = box((108, 108, 404, 404))
    draw.ellipse(sphere, outline=BLACK, width=sc(44))
    draw.ellipse(sphere, outline=WHITE, width=sc(22))
    for rect in ((178, 116, 334, 396), (126, 184, 386, 328)):
        draw.ellipse(box(rect), outline=BLACK, width=sc(30))
        draw.ellipse(box(rect), outline=WHITE, width=sc(14))
    outlined_line(draw, [(256, 119), (256, 393)], 14, 30)
    outlined_line(draw, [(119, 256), (393, 256)], 14, 30)
    return image


def manufacturer(mark: str) -> Image.Image:
    image = frame()
    draw = ImageDraw.Draw(image)
    lines = mark.split("\n")
    start_y = 256 if len(lines) == 1 else 214
    step = 84
    fnt = fit_font(max(lines, key=len), 320, 88 if len(lines) == 1 else 69, 34)
    for index, text in enumerate(lines):
        draw.text((sc(256), sc(start_y + index * step)), text, font=fnt, fill=WHITE,
                  stroke_width=sc(10), stroke_fill=BLACK, anchor="mm")
    return image


def home_icon() -> Image.Image:
    image = frame()
    draw = ImageDraw.Draw(image)
    roof = [(120, 258), (256, 126), (392, 258), (354, 296), (256, 202), (158, 296)]
    draw.polygon(points(roof), fill=BLACK)
    inner_roof = [(148, 255), (256, 151), (364, 255), (349, 270), (256, 183), (163, 270)]
    draw.polygon(points(inner_roof), fill=WHITE)
    draw.rounded_rectangle(box((169, 252, 343, 390)), radius=sc(25), fill=BLACK)
    draw.rounded_rectangle(box((190, 273, 322, 371)), radius=sc(17), fill=WHITE)
    draw.rounded_rectangle(box((231, 318, 281, 390)), radius=sc(9), fill=BLACK)
    return image


def back_icon() -> Image.Image:
    image = frame()
    draw = ImageDraw.Draw(image)
    arrow = [(229, 115), (91, 256), (229, 397), (305, 322), (267, 284), (411, 284), (411, 228), (267, 228), (305, 190)]
    draw.polygon(points(arrow), fill=BLACK)
    inner = [(230, 151), (126, 256), (230, 361), (268, 323), (220, 273), (382, 273), (382, 239), (220, 239), (268, 189)]
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
