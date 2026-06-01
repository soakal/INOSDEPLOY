# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

An **SOP Factory** for producing professional VRSI-formatted Standard Operating Procedure documents (`.docx`) from raw source material (transcripts, screenshots, photos, notes). The output follows VRSI house style as defined in `template/SOP_TEMPLATE.md`.

## Generating a New SOP

The full workflow:

1. **Place source files** — transcripts (`.md`), screenshots, photos into `active/`
2. **Pre-process images** — run from the repo root:
   ```powershell
   python template/prep_active.py
   ```
   This numbers images (`01_*.png`, `02_*.jpg`, …), strips near-white backgrounds, auto-rotates via EXIF, and writes `active/image_manifest.txt`.
   Optional flags: `--dry-run`, `--no-bg-remove`, `--no-exif-rotate`, `--no-recursive`, `--no-loose-images`

3. **Write and run a builder script** — import `SOPBuilder` from `template/sop_lib.py`, call its methods to assemble the document, then call `.save()`. See `sop-builder-skill/example_builder.py` for a working template.

4. **Output lands in** `output/` as a `.docx` file.

## SOPBuilder API (`template/sop_lib.py`)

```python
from template.sop_lib import SOPBuilder

b = SOPBuilder("template/SOP_TEMPLATE_WITH_PHOTOS.docx")
b.title_page(line1, connector, line2, subtitle, doc_no, author)
b.toc(["1. Section", "2. Section"])
b.heading1("Section Name")
b.heading2("Subsection")
b.paragraph("Body text")
b.bullet("• Top-level bullet")
b.bullet("○ Sub-bullet", level=2)
b.bullet_rich([("plain text "), ("Bold UI Name", True), (" more text")])
b.image("01_screenshot.png", caption="Caption text", width_in=6.0)
b.callout("WARNING", "Text for a red warning box")
b.callout("INFO", "Text for a blue info box")   # also: IMPORTANT, TIP, NOTE
b.scenario_table([("Label", "Value"), ...])
b.revision_history([("2026-05-29", "1.0", "Initial release", "Author")])
b.save("output/MY_SOP_v1.0.docx")
```

## VRSI Formatting Rules (from `template/SOP_TEMPLATE.md`)

- **Images**: must be pre-numbered (`01_name.png`, `02_name.png`, …) before insertion
- **Bullets**: `•` for top-level, `○` for sub-items
- **UI element names** (buttons, fields, tabs): bold
- **System-specific flags**: red italic (e.g., *Ford Only*)
- **Commands/paths**: code formatting
- **Document structure**: title page → TOC → body sections → revision history table

## Repo Layout

```
active/              ← drop source files here (transcripts, screenshots, photos)
output/              ← generated .docx files land here
INOS Needed Files/   ← large binaries (ISO, zip) — excluded from git
template/
  sop_lib.py         ← SOPBuilder class (core builder API)
  prep_active.py     ← image pre-processor (run before building)
  SOP_TEMPLATE.md    ← VRSI style rules (read before generating content)
  PROMPT.txt         ← editable per-run prompt template
  SOP_TEMPLATE_WITH_PHOTOS.docx  ← skeleton with VRSI header/footer/logo
sop-builder-skill/
  SKILL.md           ← Claude skill definition
  example_builder.py ← reference builder script showing full API usage
  install.ps1        ← installs skill into Cowork
build_inos_sop.py    ← INOS_DEPLOY-001 builder (current, v1.3)
BUILD_LOG.md         ← full build history and change notes
```

## Python Dependencies

```
python-docx
Pillow
pymupdf
requests
```

Install: `pip install python-docx Pillow pymupdf requests`

## Claude Skill

The `sop-builder` skill is triggered by phrases like "build the SOP", "create an SOP", or "use the SOP factory". Install it:

```powershell
cd "sop-builder-skill"
.\install.ps1
```

When the skill fires, it: reads VRSI rules → runs `prep_active.py` → reads all source files → collects metadata → generates and executes a builder script → validates the output `.docx`.
