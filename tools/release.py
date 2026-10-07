#!/usr/bin/env python3
"""Technische Versionierung, PWA-Precache, Prüfsummen und ZIP-Release automatisieren."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "release-config.json"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+\.\d+(?:-Beta(?:\.\d+)?)?$")


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def save_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_version(version: str) -> None:
    if not VERSION_RE.fullmatch(version):
        raise ValueError("Version muss dem Muster X.Y.Z.W oder X.Y.Z.W-Beta[.N] entsprechen.")
    config = load_config()
    previous = config["version"]
    product_name = "SK PLT Tools"
    short_name = "SK PLT Tools"
    app_slug = f"sk-plt-tools-{version.lower()}"
    cache_prefix = "sk-plt-tools-"
    config["version"] = version
    config["productName"] = product_name
    config["shortName"] = short_name
    if "-Beta" not in version:
        config["stableBaseline"] = version
    config["archiveName"] = f"SK-PLT-Tools-V{version}.zip"
    save_json(CONFIG_PATH, config)
    (ROOT / "VERSION").write_text(version + "\n", encoding="utf-8")

    nav_path = ROOT / "assets/navigation-tree.json"
    nav = json.loads(nav_path.read_text(encoding="utf-8"))
    nav["version"] = version
    save_json(nav_path, nav)

    manifest_path = ROOT / "manifest.webmanifest"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["id"] = f"./?app={app_slug}"
    manifest["name"] = product_name
    manifest["short_name"] = short_name
    manifest["start_url"] = f"./?app={app_slug}"
    manifest["version"] = version
    manifest["description"] = f"Praktische Werkzeuge und Wissensdatenbank für die Prozessleittechnik · Version {version}"
    save_json(manifest_path, manifest)

    for relative in ("assets/app.js", "service-worker.js"):
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        text, count = re.subn(r"const RELEASE='[^']+';", f"const RELEASE='{version}';", text)
        if count < 1:
            raise ValueError(f"{relative}: RELEASE-Konstante fehlt")
        if relative == "service-worker.js":
            text, count = re.subn(r"const CACHE_PREFIX='[^']+';", f"const CACHE_PREFIX='{cache_prefix}';", text)
            if count != 1:
                raise ValueError("service-worker.js: CACHE_PREFIX-Konstante fehlt oder ist nicht eindeutig")
        else:
            channel = 'beta' if '-Beta' in version else 'release'
            text = re.sub(r"channel:'[^']+'", f"channel:'{channel}'", text)
            text = re.sub(r"name:'[^']+'", f"name:'{product_name}'", text, count=1)
        path.write_text(text, encoding="utf-8")

    for page in ROOT.rglob("index.html"):
        text = page.read_text(encoding="utf-8")
        text = re.sub(r'data-sk-version="[^"]+"', f'data-sk-version="{version}"', text)
        text = re.sub(r'([?&]v=)[^"&]+', lambda m: m.group(1) + version, text)
        if page == ROOT / "index.html":
            text = re.sub(r'(<span class="badge">Version )[^<]+(</span>)', rf'\g<1>{version}\2', text)
        page.write_text(text, encoding="utf-8")

    # Versionierte Laufzeitquellen, Tests und Dokumentation dürfen keine alte
    # technische Version in Kommentaren, Fetch-URLs oder Metadaten behalten.
    if previous != version:
        for path in ROOT.rglob("*"):
            if not path.is_file() or path == CONFIG_PATH or path.suffix.lower() not in {".js", ".css", ".json", ".html", ".md", ".txt", ".py", ".webmanifest"}:
                continue
            text = path.read_text(encoding="utf-8")
            if previous in text:
                path.write_text(text.replace(previous, version), encoding="utf-8")

        old_handover = ROOT / f"PROJEKTUEBERGABE_V{previous}.txt"
        new_handover = ROOT / f"PROJEKTUEBERGABE_V{version}.txt"
        if old_handover.exists():
            old_handover.rename(new_handover)

    # Tests carry technical assertions and should move with the release automatically.
    for path in (ROOT / "tools").glob("*.*"):
        if path.suffix not in {".py", ".js"} or path.name == Path(__file__).name:
            continue
        text = path.read_text(encoding="utf-8")
        if previous != version:
            text = text.replace(previous, version)
        path.write_text(text, encoding="utf-8")

    from sync_shared import sync
    sync()


def web_runtime_files() -> list[str]:
    """Return deployable local files that must be available offline."""
    excluded_roots = {"tools", "shared", "test-artifacts"}
    excluded_names = {
        "SHA256SUMS.txt", "README.md", "RELEASE-NOTES.txt", "DEPLOYMENT.md",
        "ARCHITEKTUR-CLEAN-DESIGN.md", "TESTBERICHT-UND-ABNAHME.md", "STABLE-BASELINE.txt",
        "VERSION", "release-config.json",
    }
    files: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name in excluded_names:
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] in excluded_roots or path.name.startswith("PROJEKTUEBERGABE_"):
            continue
        if path.name == "service-worker.js":
            continue
        files.append("./" + relative.as_posix())
    return sorted(files)


def update_precache() -> None:
    sw_path = ROOT / "service-worker.js"
    text = sw_path.read_text(encoding="utf-8")
    routes = {"./"}
    for page in ROOT.rglob("index.html"):
        relative = page.relative_to(ROOT).as_posix()
        routes.add("./" + relative)
        parent = page.parent.relative_to(ROOT).as_posix()
        if parent != ".":
            routes.add("./" + parent.rstrip("/") + "/")
    entries = sorted(routes | set(web_runtime_files()), key=lambda value: (value != "./", value))
    block = "// precache:start\n" + ",\n".join(f"  {json.dumps(item)}" for item in entries) + "\n  // precache:end"
    updated, count = re.subn(r"// precache:start[\s\S]*?// precache:end", block, text)
    if count != 1:
        raise ValueError("service-worker.js: Precache-Marker fehlt oder ist nicht eindeutig")
    sw_path.write_text(updated, encoding="utf-8")


def generate_checksums() -> int:
    output = ROOT / "SHA256SUMS.txt"
    files = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path != output and "__pycache__" not in path.parts and path.name != ".DS_Store"
    )
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  ./{path.relative_to(ROOT).as_posix()}" for path in files]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(files)


def enforce_privacy_gate() -> None:
    """Block the known real, filled protocol from every release artifact."""
    forbidden_name = "_".join(("228", "SR4", "K06", "E07.1.pdf"))
    forbidden_hash = "744f24436071c5c9f36d91fc82fa2a6" + "a16f20ec8662bd81f68e3f53321792772"
    violations: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.name == forbidden_name or hashlib.sha256(path.read_bytes()).hexdigest() == forbidden_hash:
            violations.append(path.relative_to(ROOT).as_posix())
    if violations:
        raise ValueError(f"Datenschutz-Gate: reale ausgefüllte Testdatei im Release: {violations}")


def build_zip(output: Path | None = None) -> Path:
    config = load_config()
    output = output or ROOT.parent / config["archiveName"]
    output = output.resolve()
    if output.exists():
        output.unlink()
    root_name = f"SK-PLT-Tools-V{config['version']}"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.name == ".DS_Store":
                continue
            archive.write(path, (Path(root_name) / path.relative_to(ROOT)).as_posix())
    return output


def verify_version() -> None:
    config = load_config()
    version = config["version"]
    checks = {
        "VERSION": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "navigation-tree.json": json.loads((ROOT / "assets/navigation-tree.json").read_text(encoding="utf-8"))["version"],
        "manifest.webmanifest": json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))["version"],
    }
    wrong = {name: value for name, value in checks.items() if value != version}
    if wrong:
        raise ValueError(f"Inkonsistente technische Versionen: {wrong}")
    for page in ROOT.rglob("index.html"):
        if f'data-sk-version="{version}"' not in page.read_text(encoding="utf-8"):
            raise ValueError(f"{page.relative_to(ROOT)}: data-sk-version inkonsistent")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="Neue technische Version setzen")
    parser.add_argument("--zip", action="store_true", help="Vollständiges ZIP-Paket erzeugen")
    parser.add_argument("--checksums", action="store_true", help="SHA256SUMS.txt neu erzeugen")
    parser.add_argument("--all", action="store_true", help="Version synchronisieren, Precache/Prüfsummen/ZIP erzeugen")
    parser.add_argument("--output", type=Path, help="Optionaler ZIP-Zielpfad")
    args = parser.parse_args()
    config = load_config()
    version = args.version or config["version"]
    if args.all or args.version:
        update_version(version)
        update_precache()
    verify_version()
    enforce_privacy_gate()
    count = generate_checksums() if (args.all or args.checksums) else 0
    output = build_zip(args.output) if (args.all or args.zip) else None
    print(f"OK: Version {version} konsistent" + (f", {count} Prüfsummen" if count else "") + (f", ZIP {output}" if output else ""))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        raise SystemExit(1)
