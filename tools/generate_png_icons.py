#!/usr/bin/env python3
"""Erzeugt die entschlackte transparente PNG-Navigationsserie für 2.6.1.0-Beta.

Verbindliches Prinzip der App-Icon-Komponente:
- ein gemeinsamer Cartoon-Tech-Außenrahmen in CSS,
- genau ein großes, klares Hauptmotiv in der PNG,
- ein kleiner Favoritenstern als unabhängiger Bedienzustand.

Die App-PNGs enthalten keine Kategoriefelder und keine Texte RECHNER, WISSEN,
MATERIAL, EXTERN, PCT oder PIPING. Die Bedeutung des Ziels steht ausschließlich
im sichtbaren HTML-Titel unter dem Icon. Ausnahme: Das kleine WWW ist Bestandteil
des Weltkugelmotivs; Hersteller-Kurzmarken dienen selbst als Hauptmotiv.
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


def fit_font(text: str, max_width: int, start: int, minimum: int = 18):
    for size in range(start, minimum - 1, -1):
        candidate = font(size, condensed=True)
        if candidate.getbbox(text)[2] <= sc(max_width):
            return candidate
    return font(minimum, condensed=True)


def canvas():
    return Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))


def rounded_mask(rect, radius: int):
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box(rect), radius=sc(radius), fill=255)
    return mask


def ellipse_mask(rect):
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).ellipse(box(rect), fill=255)
    return mask


def polygon_mask(poly):
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).polygon(points(poly), fill=255)
    return mask


def vertical_gradient(top: str, bottom: str):
    image = Image.new("RGBA", (CANVAS, CANVAS))
    draw = ImageDraw.Draw(image)
    ta, tb = rgba(top), rgba(bottom)
    den = max(1, CANVAS - 1)
    for y in range(CANVAS):
        t = y / den
        color = tuple(round(ta[k] * (1 - t) + tb[k] * t) for k in range(4))
        draw.line((0, y, CANVAS, y), fill=color)
    return image


def fill_mask(image: Image.Image, mask: Image.Image, top: str, bottom: str):
    image.alpha_composite(Image.composite(vertical_gradient(top, bottom), Image.new("RGBA", image.size), mask))


def shadow(image: Image.Image, mask: Image.Image, offset=(10, 12), blur=5, opacity=150):
    shifted = Image.new("L", mask.size, 0)
    shifted.paste(mask, (sc(offset[0]), sc(offset[1])))
    shifted = shifted.filter(ImageFilter.GaussianBlur(sc(blur)))
    layer = Image.new("RGBA", image.size, rgba(BLACK, opacity))
    layer.putalpha(shifted.point(lambda p: p * opacity // 255))
    image.alpha_composite(layer)


def line(draw: ImageDraw.ImageDraw, coords, fill, width, joint="curve"):
    color = rgba(fill) if isinstance(fill, str) else fill
    draw.line(box(coords), fill=color, width=sc(width), joint=joint)


def center_text(draw: ImageDraw.ImageDraw, xy, text, fnt, fill=STEEL, stroke_width=0, stroke_fill=BLACK):
    draw.text(
        (sc(xy[0]), sc(xy[1])), text, font=fnt,
        fill=rgba(fill) if isinstance(fill, str) else fill,
        stroke_width=sc(stroke_width), stroke_fill=rgba(stroke_fill), anchor="mm"
    )


def rounded_shape(image: Image.Image, rect, radius: int, top: str, bottom: str, width=18):
    mask = rounded_mask(rect, radius)
    fill_mask(image, mask, top, bottom)
    ImageDraw.Draw(image).rounded_rectangle(box(rect), radius=sc(radius), outline=rgba(BLACK), width=sc(width))
    return mask


def calculator():
    """Großer Taschenrechner: Display, sechs Tasten und deutliches ±."""
    image = canvas()
    draw = ImageDraw.Draw(image)
    body = (92, 46, 420, 456)
    body_mask = rounded_mask(body, 54)
    shadow(image, body_mask, offset=(12, 14), blur=5, opacity=155)
    rounded_shape(image, body, 54, "#D7F8FC", "#347996", width=24)

    # Eine einzige dezente Tiefenkante statt doppelter Schatten/Reflexe.
    line(draw, (128, 77, 323, 77), (255, 255, 255, 165), 8)
    line(draw, (394, 105, 394, 398), (3, 24, 37, 170), 7)

    screen = (128, 103, 384, 199)
    rounded_shape(image, screen, 22, NAVY, DARK, width=16)
    center_text(draw, (256, 151), "12.34", font(49, condensed=True), fill=GREEN, stroke_width=2, stroke_fill=DEEP)

    key_specs = [
        (157, 268, "7", LIGHT_CYAN), (256, 268, "8", STEEL_2), (355, 268, "9", CYAN),
        (157, 370, "±", GREEN),       (256, 370, "0", STEEL),   (355, 370, "=", BLUE),
    ]
    for cx, cy, label, color in key_specs:
        rect = (cx - 39, cy - 34, cx + 39, cy + 34)
        rounded_shape(image, rect, 17, color, NAVY, width=10)
        center_text(draw, (cx, cy + 1), label, font(28), fill=DARK, stroke_width=1, stroke_fill=STEEL)
    return image


def book():
    """Aufgeschlagenes Buch mit zwei Farbflächen und schwarzer Mittelfalte."""
    image = canvas()
    draw = ImageDraw.Draw(image)
    left = [(54, 105), (145, 72), (246, 116), (246, 430), (145, 391), (54, 423)]
    right = [(458, 105), (367, 72), (266, 116), (266, 430), (367, 391), (458, 423)]
    full = polygon_mask(left + right[::-1])
    shadow(image, full, offset=(12, 15), blur=5, opacity=155)

    fill_mask(image, polygon_mask(left), LIGHT_CYAN, BLUE)
    fill_mask(image, polygon_mask(right), GREEN, GREEN_DARK)
    draw.line(points(left + [left[0]]), fill=rgba(BLACK), width=sc(22), joint="curve")
    draw.line(points(right + [right[0]]), fill=rgba(BLACK), width=sc(22), joint="curve")

    # Nur eine kurze Lichtkante je Seite, keine Text- oder Seitenlinien.
    line(draw, (84, 124, 146, 102, 210, 127), (255, 255, 255, 175), 8)
    line(draw, (428, 124, 366, 102, 302, 127), (255, 255, 255, 155), 8)
    line(draw, (256, 112, 256, 431), BLACK, 24)
    return image


def globe():
    """Klare Weltkugel mit sparsamen Längen-/Breitengraden und kleinem WWW."""
    image = canvas()
    draw = ImageDraw.Draw(image)
    sphere = (58, 58, 454, 454)
    mask = ellipse_mask(sphere)
    shadow(image, mask, offset=(11, 14), blur=5, opacity=155)
    fill_mask(image, mask, LIGHT_CYAN, BLUE)
    draw.ellipse(box(sphere), outline=rgba(BLACK), width=sc(24))

    # Drei Längengrade und drei Breitengrade reichen für eine klare Kugelwirkung.
    draw.ellipse(box((151, 70, 361, 442)), outline=rgba(BLACK), width=sc(15))
    line(draw, (256, 72, 256, 440), BLACK, 15)
    draw.arc(box((78, 100, 434, 304)), start=7, end=173, fill=rgba(BLACK), width=sc(15))
    line(draw, (71, 256, 441, 256), BLACK, 15)
    draw.arc(box((78, 208, 434, 412)), start=187, end=353, fill=rgba(BLACK), width=sc(15))

    # Ein einziger Lichtbogen, keine Neonwolke oder zweite Außenkontur.
    draw.arc(box((88, 86, 366, 364)), start=198, end=284, fill=(255, 255, 255, 165), width=sc(9))
    center_text(draw, (256, 259), "WWW", font(34, condensed=True), fill=STEEL, stroke_width=5, stroke_fill=DEEP)
    return image


def manufacturer(mark: str):
    """Ruhige Hersteller-Kurzmarke als Hauptmotiv, ohne PCT-Kategoriefeld."""
    image = canvas()
    draw = ImageDraw.Draw(image)
    lines = mark.split("\n")
    if len(lines) == 1:
        fnt = fit_font(lines[0], 410, 100, 42)
        center_text(draw, (256, 242), lines[0], fnt, fill=STEEL, stroke_width=11, stroke_fill=BLACK)
    else:
        key = max(lines, key=len)
        fnt = fit_font(key, 390, 76, 38)
        start_y = 196 if len(lines) == 2 else 160
        for index, text in enumerate(lines):
            center_text(draw, (256, start_y + index * 91), text, fnt, fill=STEEL, stroke_width=10, stroke_fill=BLACK)
    # Kleiner ruhiger Farbakzent, keine Kategorie und kein Leuchteffekt.
    line(draw, (154, 354, 220, 354), BLUE, 14)
    line(draw, (220, 354, 286, 354), CYAN, 14)
    line(draw, (286, 354, 358, 354), GREEN, 14)
    return image


def home_icon():
    image = canvas()
    draw = ImageDraw.Draw(image)
    roof = [(58, 239), (256, 58), (454, 239), (406, 287), (256, 153), (106, 287)]
    shadow(image, polygon_mask(roof), offset=(12, 14), blur=5, opacity=160)
    draw.polygon(points(roof), fill=rgba(CYAN))
    draw.line(points(roof + [roof[0]]), fill=rgba(BLACK), width=sc(26), joint="curve")
    body = (126, 234, 386, 454)
    rounded_shape(image, body, 34, STEEL, STEEL_2, width=24)
    rounded_shape(image, (218, 318, 294, 454), 12, BLUE, NAVY, width=17)
    return image


def back_icon():
    image = canvas()
    draw = ImageDraw.Draw(image)
    arrow = [(229, 54), (35, 256), (229, 458), (306, 381), (224, 300), (476, 300), (476, 212), (224, 212), (306, 131)]
    shadow(image, polygon_mask(arrow), offset=(12, 14), blur=5, opacity=160)
    draw.polygon(points(arrow), fill=rgba(CYAN))
    draw.line(points(arrow + [arrow[0]]), fill=rgba(BLACK), width=sc(26), joint="curve")
    return image


def finalize(image: Image.Image):
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def save(name: str, image: Image.Image):
    finalize(image).save(OUT / name, format="PNG", optimize=True)


def main():
    calculator_files = [
        "app-analogsignal.png", "app-pf-rechner.png", "app-pt-rechner.png",
        "app-einheitenrechner.png", "app-spannungsfall.png", "app-siemens-rohwert.png",
    ]
    master_calculator = calculator()
    for name in calculator_files:
        save(name, master_calculator)
    master_book = book()
    save("app-einheitendatenbank.png", master_book)
    save("app-werkstoffdatenbank.png", master_book)
    save("app-wissensdatenbank.png", master_book)
    save("app-eh-viewer.png", globe())
    save("manufacturer-air-torque.png", manufacturer("AIR\nTORQUE"))
    save("manufacturer-endress-hauser.png", manufacturer("E+H"))
    save("manufacturer-siemens.png", manufacturer("SIEMENS"))
    save("manufacturer-vacon.png", manufacturer("VACON"))
    save("manufacturer-sonstiges.png", manufacturer("ALLG."))
    save("nav-home.png", home_icon())
    save("nav-back.png", back_icon())
    print(f"{len(list(OUT.glob('*.png')))} entschlackte transparente PNG-Icons erzeugt: {OUT}")


if __name__ == "__main__":
    main()
