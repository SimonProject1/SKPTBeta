#!/usr/bin/env python3
"""Erzeugt die alternative transparente PNG-Navigationsserie für SK PCT Tools 2.6.0.3-Beta.

Gestaltungsprinzip:
- Das Hauptmotiv beschreibt die Funktion: Taschenrechner, Buch oder WWW-Weltkugel.
- Genau ein in die PNG-Pixel gerendertes Textfeld beschreibt die Kategorie.
- Der konkrete Zielname bleibt ausschließlich der Titel unter dem Icon.
- Herstellerziele bleiben reine weiße Kurzmarken mit einem integrierten PCT-Feld.
- Außenrahmen und Favoritenstern werden unverändert zentral von der Oberfläche gerendert.

Die Motive werden dreifach überabgetastet und anschließend hochwertig auf 512 x 512 px
reduziert. Dadurch bleiben Konturen und Beschriftungen auch in kleinen Kacheln sauber.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 512
SCALE = 3
CANVAS = SIZE * SCALE
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "navigation-icons"
OUT.mkdir(parents=True, exist_ok=True)

BLACK = "#000000"
DARK = "#02080D"
DEEP = "#071A29"
NAVY = "#12384D"
STEEL = "#F7FBFF"
STEEL_2 = "#A9C2CF"
STEEL_3 = "#5F8FA4"
CYAN = "#00E6F1"
LIGHT_CYAN = "#77EFF8"
BLUE = "#008CFF"
GREEN = "#78FF32"
GREEN_DARK = "#18A865"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_CONDENSED = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"


def sc(value: float) -> int:
    return round(value * SCALE)


def box(values):
    return tuple(sc(v) for v in values)


def points(values):
    return [(sc(x), sc(y)) for x, y in values]


def rgba(color: str, alpha: int = 255):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def font(size: int, condensed: bool = False):
    return ImageFont.truetype(FONT_CONDENSED if condensed else FONT_BOLD, sc(size))


def fit_font(text: str, max_width: int, start: int, minimum: int = 16, condensed: bool = True):
    for size in range(start, minimum - 1, -1):
        candidate = font(size, condensed)
        if candidate.getbbox(text)[2] <= sc(max_width):
            return candidate
    return font(minimum, condensed)


def canvas():
    return Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))


def linear_gradient(top: str, bottom: str, horizontal_shift: float = 0.22):
    """Schneller vertikaler Verlauf; Licht-/Schattenkanten liefern die 3D-Richtung."""
    image = Image.new("RGBA", (CANVAS, CANVAS))
    draw = ImageDraw.Draw(image)
    ta, tb = rgba(top), rgba(bottom)
    den = max(1, CANVAS - 1)
    for y in range(CANVAS):
        t = y / den
        color = tuple(round(ta[k] * (1 - t) + tb[k] * t) for k in range(4))
        draw.line((0, y, CANVAS, y), fill=color)
    return image


def composite_gradient(im: Image.Image, mask: Image.Image, top: str, bottom: str, horizontal_shift: float = 0.22):
    fill = linear_gradient(top, bottom, horizontal_shift)
    im.alpha_composite(Image.composite(fill, Image.new("RGBA", im.size), mask))


def rounded_mask(rect, radius: int):
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box(rect), radius=sc(radius), fill=255)
    return mask


def polygon_mask(poly):
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).polygon(points(poly), fill=255)
    return mask


def shadow(im: Image.Image, mask: Image.Image, offset=(10, 14), blur=9, opacity=185):
    shifted = Image.new("L", mask.size, 0)
    shifted.paste(mask, (sc(offset[0]), sc(offset[1])))
    shifted = shifted.filter(ImageFilter.GaussianBlur(sc(blur)))
    layer = Image.new("RGBA", im.size, rgba(BLACK, opacity))
    layer.putalpha(shifted.point(lambda p: p * opacity // 255))
    im.alpha_composite(layer)


def glow(im: Image.Image, mask: Image.Image, color=CYAN, blur=10, opacity=105):
    blurred = mask.filter(ImageFilter.GaussianBlur(sc(blur)))
    layer = Image.new("RGBA", im.size, rgba(color, opacity))
    layer.putalpha(blurred.point(lambda p: p * opacity // 255))
    im.alpha_composite(layer)


def rounded_gradient(im: Image.Image, rect, radius: int, top: str, bottom: str, outline=BLACK, width=14, inner=False):
    mask = rounded_mask(rect, radius)
    composite_gradient(im, mask, top, bottom)
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(box(rect), radius=sc(radius), outline=rgba(outline), width=sc(width))
    if inner:
        inset = width + 4
        x0, y0, x1, y1 = rect
        draw.rounded_rectangle(box((x0 + inset, y0 + inset, x1 - inset, y1 - inset)), radius=sc(max(3, radius - inset)), outline=rgba(LIGHT_CYAN, 145), width=sc(4))


def line(draw: ImageDraw.ImageDraw, coords, fill, width, joint="curve"):
    draw.line(box(coords), fill=rgba(fill) if isinstance(fill, str) else fill, width=sc(width), joint=joint)


def center_text(draw: ImageDraw.ImageDraw, xy, text, fnt, fill=STEEL, stroke_width=0, stroke_fill=BLACK):
    draw.text((sc(xy[0]), sc(xy[1])), text, font=fnt, fill=rgba(fill) if isinstance(fill, str) else fill,
              stroke_width=sc(stroke_width), stroke_fill=rgba(stroke_fill), anchor="mm")


def category_badge(im: Image.Image, label: str, y=382):
    """Rendert genau ein integriertes Kategoriefeld."""
    widths = {"PCT": 164, "WISSEN": 270, "EXTERN": 270, "RECHNER": 322, "MATERIAL": 314}
    w = widths.get(label, 300)
    x0 = (SIZE - w) / 2
    rect = (x0, y, x0 + w, y + 78)
    mask = rounded_mask(rect, 22)
    shadow(im, mask, offset=(8, 11), blur=7, opacity=190)
    # Dunkle 3D-Unterkante und eigentliche Signalplatte.
    rounded_gradient(im, (x0 + 7, y + 9, x0 + w + 7, y + 87), 22, "#06131D", "#000000", width=13)
    rounded_gradient(im, rect, 22, BLUE, CYAN, width=14, inner=True)
    draw = ImageDraw.Draw(im)
    line(draw, (x0 + 28, y + 17, x0 + w - 28, y + 17), (255, 255, 255, 165), 6)
    fnt = fit_font(label, w - 38, 43 if len(label) <= 6 else 40, 27, condensed=True)
    center_text(draw, (SIZE / 2, y + 42), label, fnt, fill=STEEL, stroke_width=5, stroke_fill=DEEP)


def calculator(category="RECHNER"):
    im = canvas()
    draw = ImageDraw.Draw(im)
    body = (108, 42, 392, 346)
    body_mask = rounded_mask(body, 48)
    shadow(im, body_mask, offset=(15, 18), blur=12, opacity=205)
    # Sichtbare Gehäusetiefe rechts/unten.
    rounded_gradient(im, (121, 56, 407, 362), 48, NAVY, DARK, width=19)
    rounded_gradient(im, body, 48, "#D9F6FC", "#347996", width=21, inner=True)
    # Linke obere Lichtkante und rechte Gehäusekante.
    line(draw, (144, 67, 275, 67), (255, 255, 255, 205), 10)
    line(draw, (374, 93, 374, 294), (4, 27, 40, 185), 8)

    screen = (137, 82, 363, 164)
    screen_mask = rounded_mask(screen, 19)
    glow(im, screen_mask, CYAN, blur=9, opacity=80)
    rounded_gradient(im, screen, 19, NAVY, DARK, width=14, inner=True)
    center_text(draw, (250, 123), "12.34", font(44, condensed=True), fill=GREEN, stroke_width=3, stroke_fill=DEEP)
    # Displayreflex und kleine Status-LEDs.
    line(draw, (157, 99, 263, 99), (255, 255, 255, 115), 5)
    draw.ellipse(box((326, 100, 341, 115)), fill=rgba(GREEN), outline=rgba(BLACK), width=sc(4))

    key_specs = [
        (154, 212, "7", LIGHT_CYAN), (250, 212, "8", STEEL_2), (346, 212, "9", CYAN),
        (154, 266, "4", STEEL), (250, 266, "5", GREEN), (346, 266, "6", BLUE),
        (154, 320, "1", STEEL_2), (250, 320, "2", LIGHT_CYAN), (346, 320, "+", GREEN),
    ]
    for cx, cy, label, color in key_specs:
        key = (cx - 33, cy - 20, cx + 33, cy + 20)
        key_mask = rounded_mask(key, 12)
        shadow(im, key_mask, offset=(4, 5), blur=2, opacity=150)
        rounded_gradient(im, key, 12, color, STEEL_3 if color in {STEEL, STEEL_2} else NAVY, width=8)
        center_text(draw, (cx, cy + 1), label, font(20), fill=DARK, stroke_width=1, stroke_fill=STEEL)
    category_badge(im, category)
    return im


def book(category="WISSEN"):
    im = canvas()
    draw = ImageDraw.Draw(im)
    left = [(66, 91), (145, 66), (246, 105), (246, 357), (145, 329), (66, 353)]
    right = [(446, 91), (367, 66), (266, 105), (266, 357), (367, 329), (446, 353)]
    full = polygon_mask(left + right[::-1])
    shadow(im, full, offset=(12, 17), blur=11, opacity=200)

    # Dunkle Seiten-/Deckeltiefe hinter den Seiten.
    left_back = [(75, 105), (148, 82), (251, 120), (251, 373), (147, 346), (75, 369)]
    right_back = [(437, 105), (364, 82), (261, 120), (261, 373), (365, 346), (437, 369)]
    draw.polygon(points(left_back), fill=rgba("#063447"), outline=rgba(BLACK))
    draw.line(points(left_back + [left_back[0]]), fill=rgba(BLACK), width=sc(18), joint="curve")
    draw.polygon(points(right_back), fill=rgba("#123B27"), outline=rgba(BLACK))
    draw.line(points(right_back + [right_back[0]]), fill=rgba(BLACK), width=sc(18), joint="curve")

    composite_gradient(im, polygon_mask(left), LIGHT_CYAN, BLUE, 0.08)
    composite_gradient(im, polygon_mask(right), GREEN, GREEN_DARK, 0.08)
    draw.line(points(left + [left[0]]), fill=rgba(BLACK), width=sc(20), joint="curve")
    draw.line(points(right + [right[0]]), fill=rgba(BLACK), width=sc(20), joint="curve")
    # Glänzende Seitenflächen und klare Seitenlinien.
    line(draw, (92, 110, 151, 92, 218, 118), (255, 255, 255, 190), 9)
    line(draw, (420, 110, 361, 92, 294, 118), (255, 255, 255, 175), 9)
    for y, x2 in ((174, 211), (222, 218), (270, 204)):
        line(draw, (101, y, x2, y + 25), DEEP, 12)
        line(draw, (411, y, 512 - x2, y + 25), DEEP, 12)
        line(draw, (104, y - 7, x2 - 5, y + 15), (255, 255, 255, 90), 3)
        line(draw, (408, y - 7, 517 - x2, y + 15), (255, 255, 255, 80), 3)
    # Plastischer Buchrücken.
    line(draw, (256, 102, 256, 360), BLACK, 23)
    line(draw, (250, 112, 250, 339), (255, 255, 255, 110), 5)
    category_badge(im, category)
    return im


def globe(category="EXTERN"):
    im = canvas()
    draw = ImageDraw.Draw(im)
    sphere = (76, 54, 392, 370)
    mask = rounded_mask(sphere, 158)
    shadow(im, mask, offset=(13, 18), blur=12, opacity=205)
    glow(im, mask, CYAN, blur=12, opacity=80)
    rounded_gradient(im, (88, 67, 404, 383), 158, LIGHT_CYAN, BLUE, width=19)
    # Zweite Kontur sorgt für plastische Tiefe.
    draw.ellipse(box((101, 80, 391, 370)), outline=rgba(LIGHT_CYAN, 120), width=sc(5))
    draw.ellipse(box((164, 67, 328, 383)), outline=rgba(BLACK), width=sc(14))
    draw.arc(box((99, 113, 393, 281)), start=5, end=175, fill=rgba(BLACK), width=sc(13))
    draw.arc(box((99, 171, 393, 339)), start=185, end=355, fill=rgba(BLACK), width=sc(13))
    line(draw, (246, 77, 246, 372), BLACK, 13)
    # Kugelglanz links oben.
    draw.arc(box((112, 91, 316, 292)), start=193, end=286, fill=(255, 255, 255, 185), width=sc(10))
    center_text(draw, (246, 229), "WWW", font(47, condensed=True), fill=STEEL, stroke_width=7, stroke_fill=DEEP)

    # Klarer, freigestellter Auswärtspfeil mit 3D-Schatten.
    arrow = [(337, 112), (422, 38), (377, 38), (377, 14), (475, 14), (475, 112), (451, 112), (451, 67), (365, 141)]
    arrow_mask = polygon_mask(arrow)
    shadow(im, arrow_mask, offset=(8, 10), blur=6, opacity=210)
    draw.polygon(points(arrow), fill=rgba(GREEN))
    draw.line(points(arrow + [arrow[0]]), fill=rgba(BLACK), width=sc(18), joint="curve")
    line(draw, (395, 33, 455, 33), (255, 255, 255, 175), 6)
    category_badge(im, category)
    return im


def manufacturer(mark: str, category="PCT"):
    im = canvas()
    draw = ImageDraw.Draw(im)
    lines = mark.split("\n")
    # Ausschließlich Kurzmarke/Name, bewusst ohne Geräte- oder Motivgrafik.
    if len(lines) == 1:
        fnt = fit_font(lines[0], 424, 104, 46, condensed=True)
        center_text(draw, (269, 237), lines[0], fnt, fill=BLACK, stroke_width=15, stroke_fill=BLACK)
        center_text(draw, (260, 226), lines[0], fnt, fill=STEEL, stroke_width=9, stroke_fill=BLACK)
        center_text(draw, (256, 220), lines[0], fnt, fill=STEEL, stroke_width=2, stroke_fill=LIGHT_CYAN)
    else:
        key = max(lines, key=len)
        fnt = fit_font(key, 410, 82, 42, condensed=True)
        for index, text in enumerate(lines):
            y = 181 + index * 91
            center_text(draw, (267, y + 12), text, fnt, fill=BLACK, stroke_width=14, stroke_fill=BLACK)
            center_text(draw, (258, y + 2), text, fnt, fill=STEEL, stroke_width=8, stroke_fill=BLACK)
            center_text(draw, (254, y - 4), text, fnt, fill=STEEL, stroke_width=2, stroke_fill=LIGHT_CYAN)
    category_badge(im, category, y=365)
    return im


def home_icon():
    im = canvas()
    draw = ImageDraw.Draw(im)
    roof = [(67, 233), (256, 61), (445, 233), (400, 285), (256, 157), (112, 285)]
    mask = polygon_mask(roof)
    shadow(im, mask, offset=(14, 18), blur=10, opacity=210)
    draw.polygon(points([(82, 247), (256, 88), (430, 247), (401, 279), (256, 151), (111, 279)]), fill=rgba(BLUE))
    draw.polygon(points(roof), fill=rgba(CYAN))
    draw.line(points(roof + [roof[0]]), fill=rgba(BLACK), width=sc(27), joint="curve")
    body = (127, 232, 385, 442)
    body_mask = rounded_mask(body, 34)
    shadow(im, body_mask, offset=(11, 15), blur=8, opacity=190)
    rounded_gradient(im, body, 34, STEEL, STEEL_2, width=24, inner=True)
    rounded_gradient(im, (218, 315, 294, 442), 13, BLUE, NAVY, width=18)
    line(draw, (98, 217, 256, 75), (255, 255, 255, 180), 8)
    return im


def back_icon():
    im = canvas()
    draw = ImageDraw.Draw(im)
    arrow = [(230, 57), (39, 256), (230, 455), (302, 383), (220, 300), (467, 300), (467, 212), (220, 212), (302, 129)]
    mask = polygon_mask(arrow)
    shadow(im, mask, offset=(13, 16), blur=10, opacity=210)
    draw.polygon(points([(248, 77), (66, 256), (248, 435), (286, 397), (178, 287), (450, 287), (450, 225), (178, 225), (286, 115)]), fill=rgba(BLUE))
    draw.polygon(points(arrow), fill=rgba(CYAN))
    draw.line(points(arrow + [arrow[0]]), fill=rgba(BLACK), width=sc(27), joint="curve")
    line(draw, (91, 238, 225, 99), (255, 255, 255, 180), 9)
    return im


def finalize(image: Image.Image):
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def save(name: str, image: Image.Image):
    finalize(image).save(OUT / name, format="PNG", optimize=True)


def main():
    calculator_files = [
        "app-analogsignal.png", "app-pf-rechner.png", "app-pt-rechner.png",
        "app-einheitenrechner.png", "app-spannungsfall.png", "app-siemens-rohwert.png",
    ]
    master_calculator = calculator("RECHNER")
    for name in calculator_files:
        save(name, master_calculator)
    save("app-einheitendatenbank.png", book("WISSEN"))
    save("app-werkstoffdatenbank.png", book("MATERIAL"))
    save("app-wissensdatenbank.png", book("WISSEN"))
    save("app-eh-viewer.png", globe("EXTERN"))
    save("manufacturer-air-torque.png", manufacturer("AIR\nTORQUE"))
    save("manufacturer-endress-hauser.png", manufacturer("E+H"))
    save("manufacturer-siemens.png", manufacturer("SIEMENS"))
    save("manufacturer-vacon.png", manufacturer("VACON"))
    save("manufacturer-sonstiges.png", manufacturer("ALLG."))
    save("nav-home.png", home_icon())
    save("nav-back.png", back_icon())
    print(f"{len(list(OUT.glob('*.png')))} alternative transparente PNG-Icons erzeugt: {OUT}")


if __name__ == "__main__":
    main()
