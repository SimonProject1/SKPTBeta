#!/usr/bin/env python3
"""Gezielte Browserprüfung für den sicheren Korrekturblock V2.6.5.5-Beta."""
from __future__ import annotations

import asyncio
import glob
import os
from pathlib import Path
from playwright.async_api import async_playwright

BASE = os.environ.get("SK_BASE_URL", "http://127.0.0.1:8080/").rstrip("/") + "/"
SHOT_DIR = Path(os.environ.get("SK_SCREENSHOT_DIR", "/home/oai/share/qa_v2655"))
PROFILES = {
    "320": (320, 800),
    "390": (390, 844),
    "smartphone": (412, 915),
    "tablet": (820, 1180),
    "desktop": (1440, 1000),
}


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


async def style(page, selector: str) -> dict:
    return await page.locator(selector).evaluate(
        """el => { const s=getComputedStyle(el), r=el.getBoundingClientRect(); return {
        display:s.display, fontSize:parseFloat(s.fontSize), hyphens:s.hyphens,
        webkitHyphens:s.webkitHyphens, wordBreak:s.wordBreak, overflowWrap:s.overflowWrap,
        textOverflow:s.textOverflow, whiteSpace:s.whiteSpace, width:r.width, height:r.height,
        left:r.left, right:r.right, top:r.top, bottom:r.bottom,
        scrollWidth:el.scrollWidth, clientWidth:el.clientWidth,
        scrollHeight:el.scrollHeight, clientHeight:el.clientHeight
    }}"""
    )


async def no_page_overflow(page, name: str) -> None:
    data = await page.evaluate("() => ({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth})")
    ensure(data["sw"] <= data["cw"] + 1, f"{name}: horizontaler Seitenüberlauf {data}")


async def run_profile(browser, name: str, width: int, height: int) -> int:
    context = await browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, has_touch=width <= 820)
    page = await context.new_page()
    checks = 0

    await page.goto(BASE, wait_until="networkidle")
    await no_page_overflow(page, f"Home {name}"); checks += 1
    titles = page.locator(".sk-home-app-title")
    ensure(await titles.count() == 10, f"Home {name}: nicht 10 App-Titel"); checks += 1
    for index in range(await titles.count()):
        title = titles.nth(index)
        data = await title.evaluate("el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return {hyphens:s.hyphens,ow:s.overflowWrap,sw:el.scrollWidth,cw:el.clientWidth,right:r.right,parentRight:el.parentElement.getBoundingClientRect().right}}")
        ensure(data["hyphens"] == "none", f"Home {name}: automatische Trennung aktiv: {index} {data}")
        ensure(data["sw"] <= data["cw"] + 1 and data["right"] <= data["parentRight"] + 1, f"Home {name}: App-Titel läuft über: {index} {data}")
        checks += 1
    if width <= 430:
        columns = await page.locator("#pctHomeGrid").evaluate("el=>getComputedStyle(el).gridTemplateColumns.split(' ').length")
        ensure(columns == 3, f"Home {name}: mobiles Dreispaltenraster verloren ({columns})"); checks += 1
    version_fonts = await page.locator(".pct-release-module-copy").evaluate("el=>[...el.children].map(n=>parseFloat(getComputedStyle(n).fontSize))")
    ensure(min(version_fonts) >= 9.95, f"Home {name}: Versionsmodul unter 10 px: {version_fonts}"); checks += 1
    footer_font = await page.locator(".pct-home-footer").evaluate("el=>parseFloat(getComputedStyle(el).fontSize)")
    ensure(footer_font >= 9.95, f"Home {name}: Footertext unter 10 px: {footer_font}"); checks += 1
    await page.screenshot(path=str(SHOT_DIR / f"home_{name}.png"), full_page=False)

    await page.goto(BASE + "analogsignal/", wait_until="networkidle")
    await no_page_overflow(page, f"Analogsignal {name}"); checks += 1
    direction = await style(page, ".analog-direction-card")
    select = await style(page, "#dir")
    ensure(direction["textOverflow"] != "ellipsis" or width > 430, f"Analogsignal {name}: Feldkarte wird ellipsiert")
    if width <= 430:
        grid = await style(page, ".analog-signal-fields")
        ensure(direction["width"] >= grid["width"] - 2, f"Analogsignal {name}: Richtung nicht volle Feldbreite: {direction} / {grid}")
        ensure(select["textOverflow"] == "clip", f"Analogsignal {name}: Select nicht vollständig: {select}")
    ensure(await page.locator("#dir option").all_text_contents() == ["Skalierungswert → Signal", "Signal → Skalierungswert"], f"Analogsignal {name}: Richtungswerte verändert")
    helper = await page.locator(".analog-signal-help p").evaluate("el=>parseFloat(getComputedStyle(el).fontSize)")
    ensure(helper >= 12.95, f"Analogsignal {name}: Hilfstext unter 13 px: {helper}"); checks += 3
    await page.screenshot(path=str(SHOT_DIR / f"analog_{name}.png"), full_page=False)

    await page.goto(BASE + "spannungsfall-rechner/", wait_until="networkidle")
    await no_page_overflow(page, f"Spannungsfall {name}"); checks += 1
    system_card = await style(page, ".voltage-system-card")
    system_select = await style(page, "#system")
    if width <= 430:
        grid = await style(page, ".calc-field-grid")
        ensure(system_card["width"] >= grid["width"] - 2, f"Spannungsfall {name}: Stromart nicht volle Feldbreite")
        ensure(system_select["textOverflow"] == "clip", f"Spannungsfall {name}: Stromart ellipsiert")
    ensure(await page.locator("#system option").all_text_contents() == ["Drehstrom, symmetrisch", "Wechselstrom, einphasig"], f"Spannungsfall {name}: Stromarten verändert")
    checks += 2
    await page.screenshot(path=str(SHOT_DIR / f"voltage_{name}.png"), full_page=False)

    await page.goto(BASE + "wissensdatenbank/", wait_until="networkidle")
    await no_page_overflow(page, f"Wissens-Hub {name}"); checks += 1
    eh = page.locator('.knowledge-hub-card[data-manufacturer-slug="endress-hauser"] h2')
    eh_style = await style(page, '.knowledge-hub-card[data-manufacturer-slug="endress-hauser"] h2')
    ensure(await eh.locator("wbr").count() == 1 and eh_style["hyphens"] == "none", f"Wissens-Hub {name}: Endress+Hauser nicht kontrolliert getrennt")
    checks += 1
    await page.screenshot(path=str(SHOT_DIR / f"knowledge_{name}.png"), full_page=False)

    await page.goto(BASE + "werkstoffdatenbank/", wait_until="networkidle")
    breadcrumb = await style(page, ".knowledge-breadcrumb")
    ensure((breadcrumb["display"] == "none") == (width <= 760), f"Werkstoff {name}: Breadcrumb-Mobilregel falsch: {breadcrumb}")
    await no_page_overflow(page, f"Werkstoff {name}"); checks += 2

    await page.goto(BASE + "wissensdatenbank/endress-hauser-promass-einbaulage/", wait_until="networkidle")
    db_chip = page.locator('.kb-breadcrumb a[href="../"]')
    ensure(await db_chip.count() == 1, f"Wissensbeitrag {name}: Wissensdatenbank-Chip fehlt")
    if width <= 760:
        ensure((await style(page, '.kb-breadcrumb a[href="../"]'))["display"] != "none", f"Wissensbeitrag {name}: Wissensdatenbank-Chip mobil verborgen")
    ensure(await page.locator(".kb-hero h1 wbr").count() == 1, f"Wissensbeitrag {name}: Einbausituation ohne kontrollierten Umbruch")
    await no_page_overflow(page, f"Wissensbeitrag {name}"); checks += 3

    await page.goto(BASE + "einheitendatenbank/", wait_until="networkidle")
    empty = await style(page, "#unitFavoritesEmpty")
    ensure(empty["height"] <= 80 and empty["display"] == "grid", f"Einheitendatenbank {name}: Leerzustand nicht kompakt: {empty}")
    ensure(await page.locator("#unitFavoritesEmpty .sk-star-svg").count() == 1, f"Einheitendatenbank {name}: Stern fehlt")
    checks += 2

    await page.goto(BASE, wait_until="networkidle")
    await page.locator(".sk-favorites-trigger").click()
    favorite_empty = await style(page, ".sk-favorites-empty")
    ensure(favorite_empty["height"] <= 90 and favorite_empty["display"] == "grid", f"Favoritenübersicht {name}: Leerzustand nicht kompakt: {favorite_empty}")
    ensure(await page.locator(".sk-favorites-empty>b").inner_text() == "0", f"Favoritenübersicht {name}: Anzahl 0 fehlt")
    checks += 2
    await page.screenshot(path=str(SHOT_DIR / f"favorites_{name}.png"), full_page=False)

    await context.close()
    return checks


async def main() -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        candidates = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'), reverse=True)
        executable = os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or (candidates[0] if candidates else pw.chromium.executable_path)
        browser = await pw.chromium.launch(headless=True, executable_path=executable, args=['--no-sandbox'])
        total = 0
        for name, (width, height) in PROFILES.items():
            total += await run_profile(browser, name, width, height)
        await browser.close()
    print(f"PASS · {total} gezielte V2.6.5.5-Browserprüfungen · 5 Profile")


if __name__ == "__main__":
    asyncio.run(main())
