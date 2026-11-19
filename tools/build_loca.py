#!/usr/bin/env python3
"""Build the localization files from the dialogue scripts.

Reads every Dialogs/GR_*.md file and writes:
  Localization/English/GortashRomance.loca.xml
  Localization/French/GortashRomance.loca.xml
  Localization/handles.md   (line id -> handle, to copy into the Toolkit)
  docs/voice_lines.md       (every spoken line per character, for voice actors)
  Toolkit/texts_to_paste.md (every English text, ready to paste into the Toolkit)

Handles are derived from the file name, the line id and the variant, so they
stay the same when the text is edited. Renaming a line id changes its handle.

Usage: python3 tools/build_loca.py
"""
import re
import sys
import uuid
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
NAMESPACE = uuid.UUID("6f0c1c5e-7c0a-4a55-9f0e-0b9a3d2e4c11")
VARIANTS = ("M", "F", "NB")

NODE = re.compile(r"^\*\*(\w+) - (.+?)\*\*(.*)$")
LANG = re.compile(r"^- (EN|FR): (.*)$")
GROUP = re.compile(r"\[([^\[\]]+? / [^\[\]]+? / [^\[\]]+?)\]")
ITALIC = re.compile(r"\*(.+?)\*")


def handle(scene, line_id, variant):
    u = uuid.uuid5(NAMESPACE, f"{scene}:{line_id}:{variant}")
    return "h" + str(u).replace("-", "g")


def expand(text):
    """Return the three versions of a line, or None if it has no variants."""
    if not GROUP.search(text):
        return None
    out = []
    for i in range(3):
        out.append(GROUP.sub(lambda m: m.group(1).split(" / ")[i], text))
    return out


def clean(text):
    return escape(ITALIC.sub(r"<i>\1</i>", text.strip()))


def parse(path):
    """Yield (line_id, speaker, en, fr) for every line of a script."""
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    cols = None
    while i < len(lines):
        line = lines[i]
        m = NODE.match(line)
        if m:
            texts = {}
            for nxt in lines[i + 1:i + 3]:
                lm = LANG.match(nxt)
                if lm:
                    texts[lm.group(1)] = lm.group(2)
            if set(texts) != {"EN", "FR"}:
                sys.exit(f"{path.name}: line {m.group(1)} needs an EN and a FR text")
            yield m.group(1), m.group(2), texts["EN"], texts["FR"]
            cols = None
        elif line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if "Id" in cells and "EN" in cells and "FR" in cells:
                cols = cells
            elif cols and not set(line) <= set("|- "):
                if len(cells) != len(cols):
                    sys.exit(f"{path.name}: bad table row: {line}")
                row = dict(zip(cols, cells))
                yield row["Id"], "Player", row["EN"], row["FR"]
        else:
            cols = None
        i += 1


def main():
    en_out, fr_out, table = [], [], []
    voices = {}
    paste = []
    for path in sorted((ROOT / "Dialogs").glob("GR_*.md")):
        scene = path.stem
        seen = set()
        table.append(f"\n## {scene}\n\n| Id | Speaker | Variant | Handle | English text |\n|---|---|---|---|---|")
        paste.append(f"\n## {scene}\n")
        for line_id, speaker, en, fr in parse(path):
            if line_id in seen:
                sys.exit(f"{path.name}: line id {line_id} is used twice")
            seen.add(line_id)
            en_v, fr_v = expand(en), expand(fr)
            if en_v or fr_v:
                versions = list(zip(VARIANTS, en_v or [en] * 3, fr_v or [fr] * 3))
            else:
                versions = [("all", en, fr)]
            if speaker not in ("Player", "Narrator") and not speaker.startswith("Item"):
                for variant, en_text, fr_text in versions:
                    label = line_id if variant == "all" else f"{line_id} ({variant})"
                    voices.setdefault(speaker, []).append(f"| {scene} | {label} | {en_text} | {fr_text} |")
            if en_v:
                for variant, en_text, _ in versions:
                    paste.append(f"**{line_id} ({variant})** - {speaker}\n\n```\n{ITALIC.sub(r'<i>\\1</i>', en_text.strip())}\n```\n")
            else:
                note = " - three identical nodes, one per identity" if fr_v else ""
                paste.append(f"**{line_id}** - {speaker}{note}\n\n```\n{ITALIC.sub(r'<i>\\1</i>', en.strip())}\n```\n")
            for variant, en_text, fr_text in versions:
                h = handle(scene, line_id, variant)
                # No XML comments: the Toolkit crashed on files that had them.
                en_out.append(f'  <content contentuid="{h}" version="1">{clean(en_text)}</content>')
                fr_out.append(f'  <content contentuid="{h}" version="1">{clean(fr_text)}</content>')
                preview = en_text if len(en_text) <= 60 else en_text[:57] + "..."
                table.append(f"| {line_id} | {speaker} | {variant} | `{h}` | {preview.replace('|', '/')} |")

    for lang, body in (("English", en_out), ("French", fr_out)):
        out = ROOT / "Localization" / lang / "GortashRomance.loca.xml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text('<?xml version="1.0" encoding="utf-8"?>\n<contentList>\n' + "\n".join(body) + "\n</contentList>\n", encoding="utf-8")

    header = ("# Localization handles\n\nGenerated by `tools/build_loca.py`. Do not edit by hand.\n\n"
              "Variant `all`: one text for everyone. Variants `M`, `F`, `NB`: three texts on the same node, "
              "one per player identity (masculine, feminine, non-binary).\n")
    (ROOT / "Localization" / "handles.md").write_text(header + "\n".join(table) + "\n", encoding="utf-8")
    doc = ["# Voice lines", "", "Generated by `tools/build_loca.py`. Do not edit by hand.", "",
           "Every spoken line, grouped by character, for anyone who wants to record them. Player and narrator lines are not listed."]
    for speaker in sorted(voices, key=lambda k: -len(voices[k])):
        doc += ["", f"## {speaker} ({len(voices[speaker])} lines)", "", "| Scene | Line | English | French |", "|---|---|---|---|"]
        doc += voices[speaker]
    (ROOT / "docs" / "voice_lines.md").write_text("\n".join(doc) + "\n", encoding="utf-8")
    sheet = ["# English texts to paste into the Toolkit", "", "Generated by `tools/build_loca.py`. Do not edit by hand.", "",
             "The Toolkit gives its own handle to each text typed in its editors, so every English text is pasted there by hand.",
             "The French file is then built from the Toolkit's `english.xml` with `tools/build_french.py`."]
    (ROOT / "Toolkit").mkdir(exist_ok=True)
    (ROOT / "Toolkit" / "texts_to_paste.md").write_text("\n".join(sheet + paste), encoding="utf-8")
    print(f"{len(en_out)} strings written per language")


if __name__ == "__main__":
    main()
