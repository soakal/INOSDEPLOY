# Running `prep_active.py` (SOP Factory Pre-Processor)

This script prepares images in your `active\` folder **before** you draft the SOP (any tool).

## What it does

- Finds source files in `active\`:
  - Extracts embedded images from `*.pdf` and `*.docx` (recursively, including subfolders)
  - Optionally downloads web reference screenshots for any `[WEB] ...` entries in `PROMPT.txt`
- Cleans up extracted/downloaded images:
  - **Auto-rotates** images using EXIF orientation (helps phone photos appear upright)
  - **Removes near-white background** and saves as **transparent PNG** (best for UI screenshots)
- Writes outputs to the **top level** of `active\`:
  - Numbered images: `01_...png`, `02_...png`, ...
  - `image_manifest.txt` describing what each numbered image is

## Prerequisites (Windows)

- Install Python 3 (already installed if `python --version` works)
- Install required packages once:

```powershell
python -m pip install pymupdf python-docx Pillow requests
```

## How to run (PowerShell)

1) Put your source PDFs/DOCX (and any notes/scripts) anywhere under:

- `...\SOP Factory\active\`

2) Open PowerShell and run:

```powershell
cd "C:\Users\Deploy\Desktop\SOP Factory\template"
python .\prep_active.py
```

3) When it finishes:
- Check `...\SOP Factory\active\` for numbered images (`01_...png`, `02_...png`, ...)
- Read `image_manifest.txt` for image descriptions
- Then draft the SOP using your preferred tool (Cowork is optional)

## Dry run (no changes)

Use this to preview what it will do without writing any files:

```powershell
cd "C:\Users\Deploy\Desktop\SOP Factory\template"
python .\prep_active.py --dry-run
```

## Useful options

- **Point at a specific active folder** (if needed):

```powershell
python .\prep_active.py --active "C:\Users\Deploy\Desktop\SOP Factory\active"
```

- **Disable background removal** (keeps solid backgrounds):

```powershell
python .\prep_active.py --no-bg-remove
```

- **Tune background removal** (0–255; higher = remove only “more white” pixels):

```powershell
python .\prep_active.py --bg-threshold 250
```

- **Disable EXIF auto-rotate**:

```powershell
python .\prep_active.py --no-exif-rotate
```

- **Disable recursive scanning** (only scan top-level `active\` for PDFs/DOCX):

```powershell
python .\prep_active.py --no-recursive
```

## Notes / expected behavior

- The script numbers images it **extracts from PDFs/DOCX**, **downloads from `[WEB]` gaps**, and (by default) **processes loose screenshots/photos found in subfolders** under `active\`.
- If you want to skip loose subfolder screenshots/photos for a run, use:

```powershell
python .\prep_active.py --no-loose-images
```
