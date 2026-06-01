---
name: sop-builder
description: Build a VRSI-format Standard Operating Procedure (SOP) docx from raw source material — voice transcripts, screenshots, photos, scripts, notes — sitting in an "SOP Factory" folder. Trigger when the user asks to build an SOP, draft an SOP, create an SOP, write a new SOP, generate an SOP, turn a transcript into an SOP, or "use the SOP factory". Also trigger on any reference to "SOP Factory", "VRSI SOP", "PROMPT.txt SOP", or commands like "build the SOP", "make me an SOP". The skill drives the full workflow: locates the SOP Factory folder, runs prep_active.py to number images and write a manifest, gathers SOP-specific metadata (title, revision, author, filename) from the user, and uses sop_lib.SOPBuilder to generate a properly formatted .docx with VRSI header/footer, title page, TOC, sections, inline screenshots with captions, and revision history table. Do NOT trigger for generic Word document requests, status updates, or non-VRSI procedure documents.
---

# SOP Builder

A Standard Operating Procedure (SOP) builder for the VRSI format used at Variation Reduction Solutions, Inc. Produces a polished `.docx` from raw source material in a fixed three-folder layout.

## When to use this skill

Trigger on any of:

- "Build the SOP", "create an SOP", "draft an SOP", "make me an SOP", "write a new SOP"
- "Use the SOP factory", "build using the template folder"
- "Turn this transcript into an SOP"
- A user pointing at a folder containing `template/PROMPT.txt`, `active/`, and `output/`

Do **not** trigger for plain Word documents, reports, or memos that have no VRSI procedure shape.

## The folder layout (SOP Factory)

```
<SOP Factory root>/
├─ template/
│   ├─ PROMPT.txt                       # editable per-run prompt
│   ├─ RUN_PREP_ACTIVE.md               # how to run prep_active.py
│   ├─ SOP_TEMPLATE.md                  # VRSI formatting rules
│   ├─ SOP_TEMPLATE_WITH_PHOTOS.docx    # skeleton (header/footer/logo)
│   ├─ SOP_TEMPLATE_WITH_PHOTOS.pdf     # rendered reference
│   ├─ prep_active.py                   # image numbering / manifest
│   ├─ sop_lib.py                       # SOPBuilder helper class
│   └─ promptbuild.py                   # optional reference-pack helper
├─ active/                              # raw source content for current SOP
└─ output/                              # final .docx files
```

Default path: `C:\Users\Deploy\Desktop\SOP Factory`. Confirm with the user (AskUserQuestion) — they may have moved it.

## Workflow — drive these steps in order

### 1. Confirm the SOP Factory location
AskUserQuestion. Default to the path above; allow override. Verify subfolders exist.

### 2. Read the template ground rules (silent)
Read `template/SOP_TEMPLATE.md` and `template/PROMPT.txt`.

### 3. Run prep_active.py
```powershell
cd "<SOP Factory root>\template"
python prep_active.py
```
If packages missing: `python -m pip install pymupdf python-docx Pillow requests`

After it runs, list `active/` for `01_*.png`, `02_*.jpg`... and Read `image_manifest.txt`.

### 4. Read all source files in active/
- `.md`, `.txt` → extract procedure steps
- `.ps1`, `.bat` → extract commands
- Each numbered image → Read it. Filename guesses are unreliable.

### 5. Gather SOP metadata via AskUserQuestion
1. Document title (suggest 2–3 variants from source)
2. Revision + date (default v1.0 — today)
3. Author initials (default BK)
4. Output filename
5. Document number (optional)

### 6. Generate a tailored builder script
Write a Python script that imports `sop_lib.SOPBuilder`. Never hand-roll docx XML.

```python
import sys
sys.path.insert(0, r"<SOP Factory root>\template")
from sop_lib import SOPBuilder

sop = SOPBuilder(
    template_docx=r"<SOP Factory root>\template\SOP_TEMPLATE_WITH_PHOTOS.docx",
    output_docx=r"<SOP Factory root>\output\<filename>.docx",
    active_dir=r"<SOP Factory root>\active",
    revision="1.0",
    date="MM/DD/YYYY",
)

sop.title_page("LINE 1", "AND", "LINE 2",
               subtitle="<station type> — VRSI procedure",
               doc_no="SOP-XXX-001",
               author="BK (Brian Kalsic)")

sop.toc(["1.  Overview", "2.  <Main>", "      A)  <Sub>", "3.  Revision History"])

sop.heading1("1.   Overview")
sop.paragraph("This document covers ...")

sop.heading1("2.   <Main>")
sop.heading2("A)   <Sub>")
sop.bullet("Plain step")
sop.bullet_rich([("Click ", False), ("Backup", True)])
sop.bullet("System-specific step", system_only="Ford Only")
sop.image("01_xxx.png", caption="What this shows")
sop.bullet("Sub-step", sub=True)

sop.heading1("3.   Revision History")
sop.revision_history([("MM/DD/YYYY", "1.0", "First Draft", "BK")])

print(sop.save())
```

### 7. Validate
Run the docx validator on the output. Fix the builder script if it fails.

### 8. Spot-check
Convert to PDF, render pages as JPEG, Read them. Check title page, header (no `[X.X]` left), bullets, image captions, revision history table.

### 9. Hand off
Give the user a `computer://` link to the final docx. No long postamble.

## VRSI cheat sheet (sop_lib.SOPBuilder methods)

| Need | Call |
|---|---|
| Title page | `sop.title_page(line1, "AND", line2, subtitle=..., doc_no=..., author=...)` |
| TOC | `sop.toc([...lines...])` |
| Section heading (bold) | `sop.heading1("1.   Overview")` |
| Subsection (bold italic) | `sop.heading2("A)   ...")` |
| Plain bullet (•) | `sop.bullet("text")` |
| Sub-bullet (○) | `sop.bullet("text", sub=True)` |
| Bold UI in bullet | `sop.bullet_rich([("Click ", False), ("OK", True)])` |
| System flag (red) | `sop.bullet("text", system_only="Ford Only")` |
| Image + caption | `sop.image("01_xxx.png", caption="...")` |
| Image placeholder | `sop.placeholder("Description")` |
| Scenario table | `sop.scenario_table([(scenario, value), ...])` |
| Revision history | `sop.revision_history([(date, ver, comments, author), ...])` |
| Save | `sop.save()` |

## Common pitfalls

- **Don't trust filename slugs.** Read each image before placing it.
- **Don't skip prep_active.py.** Numbered names + manifest are required by `sop.image()`.
- **Don't hand-roll the title page.** Use `sop.title_page()`.
- **Don't insert tables for layout.** Empty tables render as visible boxes. Only use `scenario_table` for real 2-col data.
- **Don't enable bg_remove for screenshots.** It degrades quality.
- **Don't dump all images at the end.** Insert each at its step.
