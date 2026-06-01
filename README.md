# INOS SOP Factory

Generates professional VRSI-formatted Standard Operating Procedure documents (`.docx`) from raw source material — transcripts, screenshots, and photos.

## Current SOPs

| Document | Version | Description |
|---|---|---|
| `INOS_DEPLOY-001` | v1.2 | INOS Laptop Deployment & Domain Join |

## Prerequisites

- Python 3.9+
- Dependencies: `pip install python-docx Pillow pymupdf requests`
- Source material (screenshots, transcripts) in `active/`
- Large binaries (SmartDeploy ISO, Ventoy zip) stored separately — see IT for location

## Quick Start

```powershell
# 1. Pre-process images (number them, strip backgrounds, auto-rotate)
python template/prep_active.py

# 2. Build the SOP
python build_inos_sop.py

# 3. Output lands in output/
```

## Repo Layout

```
active/          ← source files (transcripts, screenshots) — not tracked in git
output/          ← generated .docx files — not tracked in git
template/
  sop_lib.py         ← SOPBuilder class
  prep_active.py     ← image pre-processor
  SOP_TEMPLATE.md    ← VRSI style rules
  SOP_TEMPLATE_WITH_PHOTOS.docx  ← document skeleton
build_inos_sop.py    ← INOS_DEPLOY-001 builder script
BUILD_LOG.md         ← build history and change notes
CLAUDE.md            ← AI assistant instructions
```

## Large Files (Not in This Repo)

The following are too large for git and are stored separately:

- `Inos_Deploy_Offline_Window11_25H2_SmartDeploy.iso` — 3 copies: VRSI file server (primary), external hard drive, OneDrive
- `ventoy-1.1.12-windows.zip` — Ventoy installer, available at ventoy.net
- `active/` photos and screenshots — local disk / OneDrive

## Private Repository

This repository is private. Contains VRSI internal deployment procedures. Do not make public.
