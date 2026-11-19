#!/usr/bin/env python3
"""Build the French file that matches the Toolkit's own english.xml.

The Toolkit gives its own handle to every text typed in its editors and
stores them in Localization/English/english.xml. This script reads a copy of
that file, finds each English text in the dialogue scripts, and writes
french.xml with the same handles and the French text.

Usage:
  1. Copy the Toolkit's english.xml to Toolkit/english.xml in this repository.
  2. Run: python3 tools/build_french.py
  3. Copy Toolkit/french.xml to the project's Localization/French folder.

Texts the scripts do not know (for example a default text kept from a
duplicated item) are looked up in tools/extra_translations.json. Anything
still unmatched is reported and left in English.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_loca as B  # noqa: E402

ROOT = B.ROOT


def norm(text):
    text = unescape(text)
    text = re.sub(r"</?i>|\*", "", text)
    text = re.sub(r"<br\s*/?>|\\n", " ", text)
    text = text.replace("’", "'")
    return re.sub(r"\s+", " ", text).strip().lower()


def known_texts():
    """Map normalised English text -> list of (label, French text), in order."""
    out = {}
    for path in sorted((ROOT / "Dialogs").glob("GR_*.md")):
        for line_id, _speaker, en, fr in B.parse(path):
            en_v, fr_v = B.expand(en), B.expand(fr)
            if en_v or fr_v:
                versions = list(zip(B.VARIANTS, en_v or [en] * 3, fr_v or [fr] * 3))
            else:
                versions = [("all", en, fr)]
            for variant, en_text, fr_text in versions:
                label = f"{path.stem} {line_id}" + ("" if variant == "all" else f" {variant}")
                out.setdefault(norm(en_text), []).append((label, fr_text.strip()))
    return out


def main():
    src = ROOT / "Toolkit" / "english.xml"
    if not src.exists():
        sys.exit("Copy the Toolkit's english.xml to Toolkit/english.xml first.")
    known = known_texts()
    extras = {norm(k): v for k, v in json.loads((ROOT / "tools" / "extra_translations.json").read_text(encoding="utf-8")).items()}
    used = {}
    lines, report, missing = [], [], []
    for node in ET.parse(src).getroot():
        handle, version, en = node.get("contentuid"), node.get("version", "1"), node.text or ""
        key = norm(en)
        if key in known:
            options = known[key]
            index = used.get(key, 0)
            used[key] = index + 1
            label, fr = options[min(index, len(options) - 1)]
            fr = B.ITALIC.sub(r"<i>\1</i>", fr)
            if len(options) > 1:
                label += f" (text used by {len(options)} lines, matched in order)"
        elif key in extras:
            label, fr = "extra_translations.json", extras[key]
        else:
            label, fr = "NOT FOUND, left in English", unescape(en)
            missing.append(en)
        lines.append(f'<content contentuid="{handle}" version="{version}">{escape(fr)}</content>')
        report.append(f"{handle}  {label}")
    out = ROOT / "Toolkit" / "french.xml"
    header = '<contentList xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
    out.write_text(header + "\n".join(lines) + "\n</contentList>\n", encoding="utf-8")
    print("\n".join(report))
    print(f"\n{len(lines)} texts written to {out.relative_to(ROOT)}, {len(missing)} not found")
    for text in missing:
        print("  not found:", text[:80])


if __name__ == "__main__":
    main()
