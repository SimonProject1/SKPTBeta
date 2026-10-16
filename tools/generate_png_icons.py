#!/usr/bin/env python3
"""Generate the complete SK PCT Tools V2.6.3.2-Beta icon system.

Design goal: retain the approved application/knowledge icon family while giving
the four header/navigation controls a deliberately calmer body: one compact
cyan/blue/green surface, no second black tile, no decorative circuit rails and
large white symbols with one clean black contour.
"""
from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = 512
SCALE = 4
CANVAS = SIZE * SCALE
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "navigation-icons"
PREFIX = "v2-6-3-2-"
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
DARK = (3, 15, 24, 255)
CYAN = (0, 224, 255, 255)
GREEN = (100, 255, 38, 255)
BLUE = (30, 135, 224, 255)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_CONDENSED = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
MOTIF_CONTOUR = 15
DETAIL_CONTOUR = 9
SYMBOL_BOX = (102, 98, 410, 392)
SYMBOL_CENTER = (256, 246)
_FRAME_MASTER: Image.Image | None = None


def sc(value: float) -> int:
    return round(value * SCALE)


def box(values):
    return tuple(sc(v) for v in values)


def points(values):
    return [(sc(x), sc(y)) for x, y in values]


def font(size: int, condensed: bool = False):
    return ImageFont.truetype(FONT_CONDENSED if condensed else FONT_BOLD, sc(size))


def fit_font(text: str, max_width: int, start: int, minimum: int = 20):
    for size in range(start, minimum - 1, -1):
        candidate = font(size, condensed=True)
        if candidate.getbbox(text, stroke_width=sc(2))[2] <= sc(max_width):
            return candidate
    return font(minimum, condensed=True)


def canvas() -> Image.Image:
    return Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))


def area_gradient() -> Image.Image:
    w = h = sc(410)
    image = Image.new("RGBA", (w, h))
    pixels = image.load()
    stops = ((0.00, (36, 165, 91)), (0.46, (12, 139, 152)), (1.00, (24, 99, 186)))
    for y in range(h):
        yn = y / max(1, h - 1)
        for x in range(w):
            xn = x / max(1, w - 1)
            t = max(0.0, min(1.0, 0.74 * xn + 0.26 * (1.0 - yn)))
            rgb = stops[-1][1]
            for index in range(len(stops) - 1):
                p0, c0 = stops[index]
                p1, c1 = stops[index + 1]
                if p0 <= t <= p1:
                    f = (t - p0) / (p1 - p0)
                    rgb = tuple(round(c0[i] + (c1[i] - c0[i]) * f) for i in range(3))
                    break
            lift = round(10 * (1.0 - yn) - 8 * yn)
            pixels[x, y] = tuple(max(0, min(255, v + lift)) for v in rgb) + (255,)
    return image


def thick_line(draw: ImageDraw.ImageDraw, pts, color=WHITE, width=10, black_width=None, joint="curve"):
    black_width = black_width or width + 10
    p = points(pts)
    draw.line(p, fill=BLACK, width=sc(black_width), joint=joint)
    draw.line(p, fill=color, width=sc(width), joint=joint)


def node(draw: ImageDraw.ImageDraw, x, y, color, radius=8):
    draw.ellipse(box((x-radius-4, y-radius-4, x+radius+4, y+radius+4)), fill=BLACK)
    draw.ellipse(box((x-radius, y-radius, x+radius, y+radius)), fill=color)
    draw.ellipse(box((x-3, y-3, x+3, y+3)), fill=WHITE)


def frame() -> Image.Image:
    global _FRAME_MASTER
    if _FRAME_MASTER is not None:
        return _FRAME_MASTER.copy()
    image = canvas()
    draw = ImageDraw.Draw(image)
    # Deep offset shadow and the retained rounded industrial body.
    draw.rounded_rectangle(box((30, 32, 486, 488)), radius=sc(112), fill=(0, 0, 0, 150))
    draw.rounded_rectangle(box((16, 12, 470, 466)), radius=sc(112), fill=BLACK)
    inner_rect = box((38, 34, 448, 444))
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).rounded_rectangle(inner_rect, radius=sc(82), fill=255)
    gradient = area_gradient().resize((inner_rect[2]-inner_rect[0], inner_rect[3]-inner_rect[1]), Image.Resampling.BICUBIC)
    layer = canvas(); layer.paste(gradient, (inner_rect[0], inner_rect[1]))
    image.alpha_composite(Image.composite(layer, canvas(), mask))
    # Sheen and depth remain beneath the technical accents.
    sheen = canvas(); sd = ImageDraw.Draw(sheen)
    sd.ellipse(box((14, -130, 390, 244)), fill=(255, 255, 255, 18))
    sd.ellipse(box((120, 294, 520, 610)), fill=(0, 0, 0, 26))
    sheen.putalpha(Image.composite(sheen.getchannel("A"), Image.new("L", (CANVAS, CANVAS), 0), mask))
    image.alpha_composite(sheen)
    draw = ImageDraw.Draw(image)
    # Segmented cyan/green inner rails: technical depth without reducing clarity.
    draw.line(points([(89, 73), (238, 73)]), fill=BLACK, width=sc(12))
    draw.line(points([(89, 73), (238, 73)]), fill=CYAN, width=sc(5))
    draw.line(points([(73, 89), (73, 212)]), fill=BLACK, width=sc(12))
    draw.line(points([(73, 89), (73, 212)]), fill=CYAN, width=sc(5))
    draw.line(points([(274, 415), (414, 415)]), fill=BLACK, width=sc(12))
    draw.line(points([(274, 415), (414, 415)]), fill=GREEN, width=sc(5))
    draw.line(points([(415, 274), (415, 397)]), fill=BLACK, width=sc(12))
    draw.line(points([(415, 274), (415, 397)]), fill=GREEN, width=sc(5))
    for x, y, c in ((89,73,CYAN),(238,73,CYAN),(73,212,CYAN),(274,415,GREEN),(415,274,GREEN),(415,397,GREEN)):
        node(draw, x, y, c, 6)
    # Small industrial fasteners.
    for x, y, c in ((88,388,GREEN),(390,86,CYAN)):
        draw.ellipse(box((x-9,y-9,x+9,y+9)), fill=BLACK)
        draw.ellipse(box((x-5,y-5,x+5,y+5)), fill=c)
    _FRAME_MASTER = image.copy()
    return image


def navigation_frame() -> Image.Image:
    """Clean single-body frame used only by Home/Back/Search/Favorites.

    The outer transparent canvas is the complete touch graphic.  The visible
    body has one slim black contour and no shadow tile, circuit rails, colored
    strokes or dark inner panel.
    """
    image = canvas()
    draw = ImageDraw.Draw(image)
    outer = box((28, 28, 484, 484))
    inner = box((40, 40, 472, 472))
    draw.rounded_rectangle(outer, radius=sc(116), fill=BLACK)
    mask = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(mask).rounded_rectangle(inner, radius=sc(104), fill=255)
    gradient = area_gradient().resize((inner[2]-inner[0], inner[3]-inner[1]), Image.Resampling.BICUBIC)
    layer = canvas()
    layer.paste(gradient, (inner[0], inner[1]))
    image.alpha_composite(Image.composite(layer, canvas(), mask))
    # Restrained depth only; no decorative lines or additional container.
    sheen = canvas()
    sd = ImageDraw.Draw(sheen)
    sd.ellipse(box((44, -92, 430, 252)), fill=(255, 255, 255, 22))
    sheen.putalpha(Image.composite(sheen.getchannel("A"), Image.new("L", (CANVAS, CANVAS), 0), mask))
    image.alpha_composite(sheen)
    return image


def rr(draw, rect, radius=18, fill=WHITE, contour=MOTIF_CONTOUR):
    draw.rounded_rectangle(box(rect), radius=sc(radius), fill=fill, outline=BLACK, width=sc(contour))


def ellipse(draw, rect, fill=WHITE, contour=MOTIF_CONTOUR):
    draw.ellipse(box(rect), fill=fill, outline=BLACK, width=sc(contour))


def polygon(draw, vertices, fill=WHITE, contour=MOTIF_CONTOUR):
    pts = points(vertices)
    draw.polygon(pts, fill=fill)
    draw.line(pts + [pts[0]], fill=BLACK, width=sc(contour), joint="curve")


def text_center(draw, xy, text, size, fill=BLACK, condensed=True, stroke=0, stroke_fill=BLACK):
    draw.text((sc(xy[0]), sc(xy[1])), text, font=font(size, condensed), fill=fill,
              anchor="mm", stroke_width=sc(stroke), stroke_fill=stroke_fill)


def accent_bar(draw, pts, color=CYAN, width=7):
    thick_line(draw, pts, color=color, width=width, black_width=width+7)


def calculator_panel(display="12.34"):
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(132,104,380,388),36)
    rr(d,(160,136,352,210),13,fill=DARK,contour=DETAIL_CONTOUR)
    text_center(d,(256,173),display,38,fill=GREEN)
    for cy in (258,326):
        for i,cx in enumerate((184,256,328)):
            rr(d,(cx-20,cy-18,cx+20,cy+18),8,fill=WHITE,contour=DETAIL_CONTOUR)
            if (cy+i)%2: d.ellipse(box((cx-5,cy-5,cx+5,cy+5)),fill=CYAN)
    accent_bar(d,[(150,116),(220,116)],CYAN,5)
    accent_bar(d,[(292,376),(362,376)],GREEN,5)
    return image


def app_analogsignal():
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(118,116,394,368),34)
    rr(d,(146,144,366,214),12,fill=DARK,contour=DETAIL_CONTOUR)
    text_center(d,(256,178),"4–20 mA",32,fill=GREEN)
    # Process signal path with terminals and an analogue waveform.
    thick_line(d,[(148,286),(180,286),(200,252),(230,326),(262,246),(294,316),(320,278),(364,278)],CYAN,8,15)
    node(d,148,286,GREEN,7); node(d,364,278,GREEN,7)
    text_center(d,(256,342),"SIGNAL",24,fill=BLACK)
    return image


def app_pf():
    image=frame(); d=ImageDraw.Draw(image)
    ellipse(d,(126,104,386,364))
    # Gauge arc and pointer.
    d.arc(box((158,136,354,332)),200,340,fill=BLACK,width=sc(22)); d.arc(box((158,136,354,332)),200,270,fill=CYAN,width=sc(9)); d.arc(box((158,136,354,332)),270,340,fill=GREEN,width=sc(9))
    thick_line(d,[(256,246),(326,196)],BLACK,8,14)
    ellipse(d,(239,229,273,263),fill=WHITE,contour=DETAIL_CONTOUR)
    text_center(d,(256,304),"K / f",38)
    rr(d,(176,340,336,388),12,fill=DARK,contour=DETAIL_CONTOUR); text_center(d,(256,364),"P+F",27,fill=GREEN)
    return image


def app_pt():
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(190,104,286,304),44)
    ellipse(d,(158,258,318,404))
    rr(d,(225,136,251,316),10,fill=WHITE,contour=DETAIL_CONTOUR)
    d.ellipse(box((207,296,269,358)),fill=GREEN,outline=BLACK,width=sc(DETAIL_CONTOUR))
    for y,c in ((154,CYAN),(192,CYAN),(230,GREEN)):
        thick_line(d,[(294,y),(338,y)],c,5,11)
    text_center(d,(342,326),"Pt",35,fill=WHITE,stroke=3)
    return image


def app_unit_converter():
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(116,118,258,214),22); text_center(d,(187,166),"bar",34)
    rr(d,(254,278,396,374),22); text_center(d,(325,326),"kPa",31)
    polygon(d,[(276,122),(392,122),(392,166),(276,166),(304,194),(276,222),(200,144)],fill=WHITE,contour=DETAIL_CONTOUR)
    polygon(d,[(236,370),(120,370),(120,326),(236,326),(208,298),(236,270),(312,348)],fill=WHITE,contour=DETAIL_CONTOUR)
    accent_bar(d,[(288,154),(366,154)],CYAN,5); accent_bar(d,[(146,338),(224,338)],GREEN,5)
    return image


def app_unit_database():
    image=frame(); d=ImageDraw.Draw(image)
    left=[(110,142),(174,118),(248,148),(248,370),(176,344),(110,370)]
    right=[(402,142),(338,118),(264,148),(264,370),(336,344),(402,370)]
    polygon(d,left); polygon(d,right)
    d.line(points([(256,148),(256,368)]),fill=BLACK,width=sc(MOTIF_CONTOUR))
    for y,c in ((190,CYAN),(238,GREEN),(286,CYAN)):
        thick_line(d,[(144,y),(218,y+10)],c,5,10); thick_line(d,[(294,y+10),(368,y)],c,5,10)
    # Database badge at the fold.
    ellipse(d,(218,286,294,320),fill=WHITE,contour=DETAIL_CONTOUR)
    rr(d,(218,302,294,358),10,fill=WHITE,contour=DETAIL_CONTOUR)
    d.arc(box((218,328,294,364)),0,180,fill=BLACK,width=sc(DETAIL_CONTOUR))
    return image


def app_material_database():
    image=frame(); d=ImageDraw.Draw(image)
    for off,c in ((42,GREEN),(21,CYAN),(0,WHITE)):
        polygon(d,[(120,170+off),(318,118+off),(394,170+off),(196,224+off)],fill=WHITE,contour=DETAIL_CONTOUR)
        accent_bar(d,[(160,181+off),(286,147+off)],c if c!=WHITE else CYAN,5)
    # Hex bolt = industrial material reference.
    polygon(d,[(256,258),(308,288),(308,348),(256,378),(204,348),(204,288)],fill=WHITE,contour=DETAIL_CONTOUR)
    ellipse(d,(236,298,276,338),fill=DARK,contour=DETAIL_CONTOUR)
    return image


def app_knowledge_database():
    image=frame(); d=ImageDraw.Draw(image)
    left=[(108,140),(174,116),(246,148),(246,366),(176,340),(108,368)]
    right=[(404,140),(338,116),(266,148),(266,366),(336,340),(404,368)]
    polygon(d,left); polygon(d,right)
    d.line(points([(256,150),(256,364)]),fill=BLACK,width=sc(MOTIF_CONTOUR))
    # Circuit-like knowledge paths.
    for pts_,c in (([(142,188),(190,188),(214,210)],CYAN), ([(370,188),(322,188),(298,210)],GREEN), ([(142,272),(196,272),(220,250)],GREEN), ([(370,272),(316,272),(292,250)],CYAN)):
        thick_line(d,pts_,c,5,10); node(d,*pts_[0],c,5)
    ellipse(d,(218,210,294,286),fill=WHITE,contour=DETAIL_CONTOUR); text_center(d,(256,248),"i",42)
    return image


def app_voltage_drop():
    image=frame(); d=ImageDraw.Draw(image)
    # Cable and terminals behind the bolt.
    thick_line(d,[(112,320),(176,320),(214,350)],CYAN,12,24)
    thick_line(d,[(298,350),(336,320),(400,320)],GREEN,12,24)
    ellipse(d,(90,296,134,340),fill=WHITE,contour=DETAIL_CONTOUR); ellipse(d,(378,296,422,340),fill=WHITE,contour=DETAIL_CONTOUR)
    polygon(d,[(278,96),(164,250),(238,250),(204,396),(350,214),(272,214),(322,96)],fill=WHITE)
    accent_bar(d,[(268,128),(198,230)],CYAN,6); accent_bar(d,[(258,354),(320,270)],GREEN,6)
    return image


def app_siemens_raw():
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(112,112,400,380),30)
    rr(d,(142,140,370,210),12,fill=DARK,contour=DETAIL_CONTOUR); text_center(d,(256,175),"RAW 13824",28,fill=GREEN)
    # PLC rack and terminals.
    for x in (150,218,286,354):
        rr(d,(x-24,238,x+24,334),8,fill=WHITE,contour=DETAIL_CONTOUR)
        d.ellipse(box((x-7,254,x+7,268)),fill=CYAN if x<256 else GREEN,outline=BLACK,width=sc(4))
        thick_line(d,[(x-10,300),(x+10,300)],BLACK,5,7)
    accent_bar(d,[(144,356),(244,356)],CYAN,5); accent_bar(d,[(268,356),(368,356)],GREEN,5)
    return image


def app_eh_viewer():
    image=frame(); d=ImageDraw.Draw(image)
    ellipse(d,(108,112,366,370))
    d.ellipse(box((180,112,294,370)),outline=BLACK,width=sc(DETAIL_CONTOUR))
    d.ellipse(box((108,174,366,310)),outline=BLACK,width=sc(DETAIL_CONTOUR))
    rr(d,(118,222,356,282),14,fill=WHITE,contour=DETAIL_CONTOUR); text_center(d,(237,252),"WWW",34)
    polygon(d,[(318,132),(392,92),(390,128),(424,128),(424,190),(388,190),(388,224),(344,154)],fill=WHITE,contour=DETAIL_CONTOUR)
    accent_bar(d,[(349,143),(397,116)],GREEN,5)
    return image


def knowledge_air_torque():
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(124,176,388,322),48)
    ellipse(d,(174,126,338,290)); text_center(d,(256,208),"90°",37)
    thick_line(d,[(168,344),(118,306),(128,372)],CYAN,11,21)
    thick_line(d,[(344,344),(394,306),(384,372)],GREEN,11,21)
    text_center(d,(256,350),"ACT",28,fill=WHITE,stroke=3)
    return image


def knowledge_promass():
    image=frame(); d=ImageDraw.Draw(image)
    thick_line(d,[(102,286),(180,286)],CYAN,18,32); thick_line(d,[(332,286),(410,286)],GREEN,18,32)
    rr(d,(166,152,346,358),34)
    ellipse(d,(194,174,318,298),fill=WHITE,contour=DETAIL_CONTOUR)
    thick_line(d,[(218,246),(256,212),(294,246)],CYAN,7,14)
    rr(d,(214,318,298,382),14,fill=WHITE,contour=DETAIL_CONTOUR); text_center(d,(256,350),"ṁ",30)
    return image


def knowledge_p320():
    image=frame(); d=ImageDraw.Draw(image)
    ellipse(d,(136,104,376,344)); text_center(d,(256,204),"P320",37)
    thick_line(d,[(256,344),(256,392)],GREEN,12,23)
    polygon(d,[(256,224),(326,248),(314,330),(256,374),(198,330),(186,248)],fill=WHITE,contour=DETAIL_CONTOUR)
    thick_line(d,[(222,296),(248,322),(294,270)],GREEN,9,18)
    return image


def knowledge_sps_raw():
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(112,116,400,374),30)
    for x in (154,214,274,334):
        rr(d,(x-22,148,x+22,326),7,fill=WHITE,contour=DETAIL_CONTOUR)
        for y,c in ((178,CYAN),(216,GREEN),(254,CYAN)):
            d.ellipse(box((x-7,y-7,x+7,y+7)),fill=c,outline=BLACK,width=sc(4))
    rr(d,(142,328,370,388),12,fill=DARK,contour=DETAIL_CONTOUR); text_center(d,(256,358),"0…27648",27,fill=GREEN)
    return image


def knowledge_vacon():
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(136,102,376,390),34)
    rr(d,(166,134,346,216),12,fill=DARK,contour=DETAIL_CONTOUR); text_center(d,(256,175),"50.0 Hz",29,fill=GREEN)
    thick_line(d,[(172,276),(196,250),(220,302),(244,250),(268,302),(292,250),(316,276),(340,276)],CYAN,7,14)
    polygon(d,[(188,342),(218,312),(248,342),(230,342),(230,374),(206,374),(206,342)],fill=WHITE,contour=DETAIL_CONTOUR)
    polygon(d,[(324,312),(294,342),(264,312),(282,312),(282,280),(306,280),(306,312)],fill=WHITE,contour=DETAIL_CONTOUR)
    return image


def manufacturer(mark: str):
    image=frame(); d=ImageDraw.Draw(image)
    rr(d,(102,164,410,326),32)
    # Industrial nameplate fasteners.
    for x in (126,386):
        ellipse(d,(x-10,235-10,x+10,235+10),fill=DARK,contour=5)
    lines=mark.split("\n")
    if len(lines)==1:
        f=fit_font(lines[0],232,75,31)
        d.text((sc(256),sc(232)),lines[0],font=f,fill=BLACK,anchor="mm")
    else:
        f=fit_font(max(lines,key=len),232,47,30)
        for y,t in zip((210,260),lines): d.text((sc(256),sc(y)),t,font=f,fill=BLACK,anchor="mm")
    accent_bar(d,[(144,294),(252,294)],CYAN,5); accent_bar(d,[(260,294),(368,294)],GREEN,5)
    return image


def nav_home():
    image=navigation_frame(); d=ImageDraw.Draw(image)
    polygon(d,[(94,238),(256,92),(418,238),(382,278),(360,258),(360,398),(152,398),(152,258),(130,278)],fill=WHITE,contour=17)
    rr(d,(222,294,290,398),10,fill=WHITE,contour=11)
    return image


def nav_back():
    image=navigation_frame(); d=ImageDraw.Draw(image)
    polygon(d,[(230,90),(82,256),(230,422),(284,368),(244,326),(424,326),(424,186),(244,186),(284,144)],fill=WHITE,contour=17)
    return image


def nav_search():
    """Large white magnifier without the former black inner disc."""
    image=navigation_frame(); d=ImageDraw.Draw(image)
    # Two nested outline strokes leave the center open to the common body.
    d.ellipse(box((92,84,338,330)), outline=BLACK, width=sc(38))
    d.ellipse(box((92,84,338,330)), outline=WHITE, width=sc(21))
    thick_line(d,[(304,296),(414,406)],WHITE,34,58)
    return image


def nav_favorite():
    """Large white star on the clean shared body."""
    image=navigation_frame(); d=ImageDraw.Draw(image)
    star=[]
    cx=256; cy=246
    for index in range(10):
        angle=-math.pi/2+index*math.pi/5
        radius=166 if index%2==0 else 78
        star.append((cx+math.cos(angle)*radius,cy+math.sin(angle)*radius))
    polygon(d,star,fill=WHITE,contour=17)
    return image


def finalize(image: Image.Image) -> Image.Image:
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def save(name: str, image: Image.Image):
    finalize(image).save(OUT / f"{PREFIX}{name}.png", format="PNG", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.iterdir():
        if old.is_file(): old.unlink()
    icons = {
        "app-analogsignal": app_analogsignal,
        "app-pf-rechner": app_pf,
        "app-pt-rechner": app_pt,
        "app-einheitenrechner": app_unit_converter,
        "app-einheitendatenbank": app_unit_database,
        "app-werkstoffdatenbank": app_material_database,
        "app-wissensdatenbank": app_knowledge_database,
        "app-spannungsfall": app_voltage_drop,
        "app-siemens-rohwert": app_siemens_raw,
        "app-eh-viewer": app_eh_viewer,
        "knowledge-air-torque-antrieb-drehrichtung": knowledge_air_torque,
        "knowledge-endress-hauser-promass-einbaulage": knowledge_promass,
        "knowledge-siemens-sitrans-p320-sil-verriegelung": knowledge_p320,
        "knowledge-siemens-sps-rohwert": knowledge_sps_raw,
        "knowledge-vacon-frequenzumrichter-ist-sollwert-abweichung": knowledge_vacon,
        "manufacturer-air-torque": lambda: manufacturer("AIR\nTORQUE"),
        "manufacturer-endress-hauser": lambda: manufacturer("E+H"),
        "manufacturer-siemens": lambda: manufacturer("SIEMENS"),
        "manufacturer-sonstiges": lambda: manufacturer("ALLG."),
        "manufacturer-vacon": lambda: manufacturer("VACON"),
        "nav-back": nav_back,
        "nav-home": nav_home,
        "nav-search": nav_search,
        "nav-favorite": nav_favorite,
    }
    for name, factory in icons.items(): save(name, factory())
    print(f"Generated {len(icons)} V2.6.3.2 icons in {OUT} · grid={SYMBOL_BOX} · contour={MOTIF_CONTOUR}px")


if __name__ == "__main__":
    main()
