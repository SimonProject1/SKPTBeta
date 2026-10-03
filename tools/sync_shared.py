#!/usr/bin/env python3
"""Synchronisiert statische gemeinsame Seitenelemente aus /shared in alle HTML-Seiten."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKERS = {
    "header": re.compile(r"<!-- sk:header:start -->[\s\S]*?<!-- sk:header:end -->"),
    "footer": re.compile(r"<!-- sk:footer:start -->[\s\S]*?<!-- sk:footer:end -->"),
    "controls": re.compile(r"<!-- sk:controls:start -->[\s\S]*?<!-- sk:controls:end -->"),
}


def render(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", escape(str(value), quote=True))
    unresolved = re.findall(r"{{([A-Z_]+)}}", template)
    if unresolved:
        raise ValueError(f"Nicht aufgelöste Template-Platzhalter: {unresolved}")
    return template.strip()


def sync() -> list[str]:
    config = json.loads((ROOT / "release-config.json").read_text(encoding="utf-8"))
    pages = json.loads((ROOT / "shared/pages.json").read_text(encoding="utf-8"))
    header_template = (ROOT / "shared/header.html").read_text(encoding="utf-8")
    footer_template = (ROOT / "shared/footer.html").read_text(encoding="utf-8")
    controls = (ROOT / "shared/controls.html").read_text(encoding="utf-8").strip()
    changed: list[str] = []

    actual_pages = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("index.html")}
    if actual_pages != set(pages):
        raise ValueError(
            "shared/pages.json stimmt nicht mit den HTML-Seiten überein: "
            f"fehlend={sorted(actual_pages-set(pages))}, zusätzlich={sorted(set(pages)-actual_pages)}"
        )

    for relative, meta in pages.items():
        page = ROOT / relative
        text = page.read_text(encoding="utf-8")
        depth = len(Path(relative).parent.parts) if Path(relative).parent != Path(".") else 0
        values = {
            "PRODUCT": config["productName"],
            "VERSION": config["version"],
            "ROOT": "../" * depth if depth else "",
            "SUBTITLE": meta["subtitle"],
            "HOME_HREF": meta["homeHref"],
            "HOME_LABEL": meta["homeLabel"],
            "HOME_ARIA": meta["homeAria"],
        }
        replacements = {
            "header": f"<!-- sk:header:start -->{render(header_template, values)}<!-- sk:header:end -->",
            "footer": f"<!-- sk:footer:start -->{render(footer_template, values)}<!-- sk:footer:end -->",
            "controls": f"<!-- sk:controls:start -->{controls}<!-- sk:controls:end -->",
        }
        updated = text
        for key, pattern in MARKERS.items():
            if len(pattern.findall(updated)) != 1:
                raise ValueError(f"{relative}: Markerblock {key!r} fehlt oder ist nicht eindeutig")
            updated = pattern.sub(lambda _match, value=replacements[key]: value, updated)
        if updated != text:
            page.write_text(updated, encoding="utf-8")
            changed.append(relative)
    return changed


if __name__ == "__main__":
    files = sync()
    print(f"OK: gemeinsame Seitenelemente auf {len(files)} geänderten Seiten synchronisiert.")
