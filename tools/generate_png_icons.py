#!/usr/bin/env python3
"""Erzeugt die transparenten PNG-Navigationsicons für SK PCT Tools 2.6.0.1-Beta."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = 512
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "navigation-icons"
OUT.mkdir(parents=True, exist_ok=True)

BLACK = "#000000"
DARK = "#02080D"
DEEP = "#071A29"
STEEL = "#F7FBFF"
STEEL_2 = "#A9C2CF"
CYAN = "#00E6F1"
LIGHT_CYAN = "#77EFF8"
BLUE = "#008CFF"
GREEN = "#78FF32"
GREEN_DARK = "#18A865"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_CONDENSED = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"


def font(size: int, condensed: bool = False):
    return ImageFont.truetype(FONT_CONDENSED if condensed else FONT_BOLD, size)


def vertical_gradient(top: str, bottom: str) -> Image.Image:
    a = Image.new("RGBA", (SIZE, SIZE))
    ta = tuple(int(top[i:i+2], 16) for i in (1, 3, 5))
    tb = tuple(int(bottom[i:i+2], 16) for i in (1, 3, 5))
    px = a.load()
    for y in range(SIZE):
        t = y / (SIZE - 1)
        c = tuple(round(ta[k] * (1 - t) + tb[k] * t) for k in range(3)) + (255,)
        for x in range(SIZE):
            px[x, y] = c
    return a


def rounded_gradient(im: Image.Image, box, radius, top, bottom, outline=BLACK, width=16):
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
    im.alpha_composite(Image.composite(vertical_gradient(top, bottom), Image.new("RGBA", (SIZE, SIZE)), mask))
    ImageDraw.Draw(im).rounded_rectangle(box, radius=radius, outline=outline, width=width)


def fit_font(text: str, max_width: int, start: int, minimum: int = 18, condensed=False):
    for size in range(start, minimum - 1, -2):
        f = font(size, condensed)
        if f.getbbox(text)[2] <= max_width:
            return f
    return font(minimum, condensed)


def center_text(draw, xy, text, fnt, fill=STEEL, stroke_width=0, stroke_fill=BLACK, anchor="mm"):
    draw.text(xy, text, font=fnt, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill, anchor=anchor)


def badge(im: Image.Image, label: str, y=382, wide=False):
    draw = ImageDraw.Draw(im)
    width = 242 if wide or len(label) > 3 else 160
    x0 = (SIZE - width) // 2
    box = (x0, y, x0 + width, y + 70)
    rounded_gradient(im, box, 18, BLUE, CYAN, width=12)
    f = fit_font(label, width - 28, 50 if len(label) <= 3 else 42, 28, condensed=True)
    center_text(draw, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2 + 1), label, f, fill=DARK)


def calculator(area="PCT"):
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    rounded_gradient(im, (62, 30, 450, 474), 70, "#BDE8F4", "#347996", width=20)
    # linke obere Glanzkante
    draw.line((112, 63, 287, 63), fill=(255, 255, 255, 175), width=13)
    rounded_gradient(im, (104, 91, 408, 199), 24, "#12384D", DARK, width=16)
    center_text(draw, (256, 145), "123.4", font(60), fill=GREEN, stroke_width=5)
    colors = [LIGHT_CYAN, STEEL_2, CYAN, STEEL, GREEN, BLUE]
    centers = [(138, 258), (256, 258), (374, 258), (138, 342), (256, 342), (374, 342)]
    labels = ["7", "8", "9", "4", "5", "+"]
    for (cx, cy), color, label in zip(centers, colors, labels):
        draw.rounded_rectangle((cx-42, cy-30, cx+42, cy+30), radius=17, fill=color, outline=BLACK, width=13)
        center_text(draw, (cx, cy+1), label, font(29), fill=DARK)
    badge(im, area, y=389, wide=len(area) > 3)
    return im


def book(area="PCT"):
    im = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    left = [(54, 92), (135, 72), (243, 112), (243, 405), (132, 367), (54, 389)]
    right = [(458, 92), (377, 72), (269, 112), (269, 405), (380, 367), (458, 389)]
    draw.polygon(left, fill=CYAN)
    draw.line(left + [left[0]], fill=BLACK, width=20, joint="curve")
    draw.polygon(right, fill=GREEN)
    draw.line(right + [right[0]], fill=BLACK, width=20, joint="curve")
    # Lichtflächen und Seitenlinien
    draw.line((82, 113, 137, 99, 220, 127), fill=(255,255,255,190), width=12, joint="curve")
    draw.line((430, 113, 375, 99, 292, 127), fill=(255,255,255,180), width=12, joint="curve")
    for y, end in ((186, 203), (243, 215), (300, 198)):
        draw.line((99, y, end, y+24), fill=DEEP, width=14)
        draw.line((413, y, 512-end, y+24), fill=DEEP, width=14)
    draw.line((256, 107, 256, 408), fill=BLACK, width=22)
    badge(im, area, y=385, wide=len(area) > 3)
    return im


def globe(area="PCT"):
    im = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    # Weltkugel
    rounded_gradient(im, (66, 68, 414, 416), 174, LIGHT_CYAN, BLUE, width=20)
    draw.ellipse((144, 68, 336, 416), outline=BLACK, width=15)
    draw.line((240, 77, 240, 407), fill=BLACK, width=14)
    draw.arc((77, 122, 403, 309), start=5, end=175, fill=BLACK, width=14)
    draw.arc((77, 178, 403, 365), start=185, end=355, fill=BLACK, width=14)
    center_text(draw, (240, 244), "WWW", font(58, condensed=True), fill=STEEL, stroke_width=9)
    # Auswärtspfeil
    draw.line((344, 116, 452, 25), fill=BLACK, width=45)
    draw.line((344, 116, 452, 25), fill=GREEN, width=25)
    draw.line((390, 25, 452, 25, 452, 87), fill=BLACK, width=45, joint="curve")
    draw.line((390, 25, 452, 25, 452, 87), fill=GREEN, width=25, joint="curve")
    badge(im, area, y=393)
    return im


def manufacturer(mark: str, area="PCT", two_lines=False):
    im = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    lines = mark.split("\n") if two_lines or "\n" in mark else [mark]
    if len(lines) == 1:
        f = fit_font(lines[0], 432, 106, 48, condensed=True)
        center_text(draw, (256, 226), lines[0], f, fill=STEEL, stroke_width=13)
    else:
        f = fit_font(max(lines, key=len), 420, 84, 44, condensed=True)
        center_text(draw, (256, 177), lines[0], f, fill=STEEL, stroke_width=12)
        center_text(draw, (256, 267), lines[1], f, fill=STEEL, stroke_width=12)
    badge(im, area, y=365)
    return im


def home_icon():
    im = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    roof = [(70, 241), (256, 72), (442, 241), (395, 292), (256, 169), (117, 292)]
    draw.polygon(roof, fill=CYAN)
    draw.line(roof+[roof[0]], fill=BLACK, width=28, joint="curve")
    draw.rounded_rectangle((126, 238, 386, 449), radius=34, fill=STEEL, outline=BLACK, width=26)
    draw.rounded_rectangle((218, 319, 294, 449), radius=14, fill=BLUE, outline=BLACK, width=20)
    return im


def back_icon():
    im = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    pts = [(238, 70), (51, 256), (238, 442), (298, 382), (213, 299), (456, 299), (456, 213), (213, 213), (298, 130)]
    draw.polygon(pts, fill=CYAN)
    draw.line(pts+[pts[0]], fill=BLACK, width=26, joint="curve")
    draw.line((101, 232, 228, 104), fill=(255,255,255,180), width=13)
    return im


def save(name: str, image: Image.Image):
    image.save(OUT / name, format="PNG", optimize=True)


def main():
    calculator_files = [
        "app-analogsignal.png", "app-pf-rechner.png", "app-pt-rechner.png",
        "app-einheitenrechner.png", "app-spannungsfall.png", "app-siemens-rohwert.png",
    ]
    for name in calculator_files:
        save(name, calculator("PCT"))
    save("app-einheitendatenbank.png", book("PCT"))
    save("app-werkstoffdatenbank.png", book("PIPING"))
    save("app-wissensdatenbank.png", book("PCT"))
    save("app-eh-viewer.png", globe("PCT"))
    save("manufacturer-air-torque.png", manufacturer("AIR\nTORQUE", two_lines=True))
    save("manufacturer-endress-hauser.png", manufacturer("E+H"))
    save("manufacturer-siemens.png", manufacturer("SIEMENS"))
    save("manufacturer-vacon.png", manufacturer("VACON"))
    save("manufacturer-sonstiges.png", manufacturer("ALLG."))
    save("nav-home.png", home_icon())
    save("nav-back.png", back_icon())
    print(f"{len(list(OUT.glob('*.png')))} transparente PNG-Icons erzeugt: {OUT}")


if __name__ == "__main__":
    main()
