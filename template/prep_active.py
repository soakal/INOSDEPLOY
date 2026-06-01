#!/usr/bin/env python3
"""
prep_active.py — SOP Factory Pre-Processor
==========================================
Runs before drafting the SOP. Extracts/numbers images and writes a manifest.

What it does:
  1. Scans active/ for PDF and .docx files (recursively)
  2. Extracts embedded images (skips tiny icons/junk < MIN_SIZE_KB)
  3. Auto-numbers all source images 01_xxx.png, 02_xxx.jpg, ...
  4. Optionally reads PROMPT.txt Section 4A for [WEB] gap descriptions and
     downloads matching screenshots from the web (DuckDuckGo image search).
  5. Writes image_manifest.txt describing each numbered image.

Usage:
  python prep_active.py                         # auto-locate active/ as sibling
  python prep_active.py --active C:/path        # explicit path
  python prep_active.py --dry-run               # preview only, no writes
  python prep_active.py --no-loose-images       # skip subfolder screenshots
  python prep_active.py --no-bg-remove          # keep solid backgrounds (default)

Requirements:
  pip install pymupdf python-docx Pillow requests
"""

import argparse
import io
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

MIN_SIZE_KB           = 10        # skip images smaller than this
MAX_WEB_IMGS          = 1         # web images per [WEB] gap entry
WEB_SEARCH_PAUSE      = 1.5       # seconds between web requests
SUPPORTED_IMG         = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}

EXIF_ROTATE_DEFAULT   = True
BG_REMOVE_DEFAULT     = False     # OFF by default — degrades screenshot quality
BG_THRESHOLD_DEFAULT  = 245
RECURSIVE_DEFAULT     = True
LOOSE_IMAGES_DEFAULT  = True
MAX_LOOSE_IMAGES_DEFAULT = 200
JPEG_QUALITY_DEFAULT  = 95

# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg, indent=0):
    prefix = "  " * indent
    text = f"{prefix}{msg}"
    try:
        print(text)
    except UnicodeEncodeError:
        enc = getattr(sys.stdout, "encoding", "utf-8") or "utf-8"
        print(text.encode(enc, errors="replace").decode(enc, errors="replace"))


def slugify(text, maxlen=40):
    """Turn arbitrary text into a safe filename fragment (lowercase, underscores)."""
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "_", text).strip("_")
    return text[:maxlen] or "image"


def _best_caption_from_source(src: Path) -> str:
    """Short, human caption seed for the manifest."""
    stem = (src.stem or "image").strip()
    stem = re.sub(r"\s+", " ", stem)
    return stem[:120] if stem else "image"


def image_too_small(data: bytes) -> bool:
    return len(data) < MIN_SIZE_KB * 1024


def is_numbered_image(path: Path) -> bool:
    return (
        path.is_file()
        and path.suffix.lower() in SUPPORTED_IMG
        and re.match(r"^\d+_", path.name) is not None
    )


def next_index(existing) -> int:
    """Return the next available 1-based image index."""
    used = set()
    for p in existing:
        m = re.match(r"^(\d+)_", p.name)
        if m:
            used.add(int(m.group(1)))
    n = 1
    while n in used:
        n += 1
    return n


def collect_loose_images(active_dir: Path):
    """Loose screenshots/photos under subfolders (excluding numbered top-level)."""
    candidates = []
    for p in active_dir.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in SUPPORTED_IMG:
            continue
        if p.parent == active_dir and is_numbered_image(p):
            continue
        if p.name.lower() == "image_manifest.txt":
            continue
        candidates.append(p)
    return sorted(candidates)


def _near_white_to_alpha(img_rgba, threshold: int):
    """Make near-white pixels transparent. Used only when --bg-remove is on."""
    from PIL import Image, ImageChops
    threshold = max(0, min(255, int(threshold)))
    if threshold <= 0:
        return img_rgba
    rgb = img_rgba.convert("RGB")
    white = Image.new("RGB", rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, white).convert("L")
    tol = 255 - threshold
    alpha = diff.point(lambda p: 0 if p <= tol else 255)
    out = img_rgba.copy()
    out.putalpha(alpha)
    return out


def postprocess_image_bytes(data, src_path=None, *, exif_rotate, bg_remove,
                            bg_threshold, jpeg_quality=JPEG_QUALITY_DEFAULT):
    """Apply EXIF rotation and optional background removal. Returns (bytes, ext)."""
    from PIL import Image, ImageOps
    img = Image.open(io.BytesIO(data))
    src_ext = (src_path.suffix.lower() if src_path else "").lstrip(".")

    if exif_rotate:
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

    if bg_remove:
        img = img.convert("RGBA")
        img = _near_white_to_alpha(img, bg_threshold)
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=False)
        return buf.getvalue(), "png"

    # Screenshots → PNG losslessly
    if src_ext in ("png", "bmp", "gif", "webp") or img.mode in ("RGBA", "LA", "P"):
        out_img = img if img.mode in ("RGBA", "LA") else img.convert("RGB")
        buf = io.BytesIO()
        out_img.save(buf, format="PNG", optimize=False)
        return buf.getvalue(), "png"

    # Photos → high-quality JPEG
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=jpeg_quality,
                            subsampling=0, optimize=True)
    return buf.getvalue(), "jpg"


# ── Image extraction from PDFs ────────────────────────────────────────────────

def extract_from_pdf(pdf_path, out_dir, existing, *, exif_rotate, bg_remove, bg_threshold):
    import fitz  # PyMuPDF
    saved = []
    doc = fitz.open(str(pdf_path))
    stem = slugify(pdf_path.stem)
    for page_num in range(len(doc)):
        page = doc[page_num]
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                base_img = doc.extract_image(xref)
            except Exception:
                continue
            data = base_img["image"]
            if image_too_small(data):
                continue
            try:
                out_data, out_ext = postprocess_image_bytes(
                    data, None, exif_rotate=exif_rotate,
                    bg_remove=bg_remove, bg_threshold=bg_threshold)
            except Exception:
                continue
            idx = next_index(existing + saved)
            fname = f"{idx:02d}_{stem}_p{page_num+1}.{out_ext}"
            dest = out_dir / fname
            dest.write_bytes(out_data)
            saved.append(dest)
            existing.append(dest)
            log(f"✓ PDF image → {fname}", indent=1)
    doc.close()
    return saved


# ── Image extraction from Word docs ──────────────────────────────────────────

def extract_from_docx(docx_path, out_dir, existing, *, exif_rotate, bg_remove, bg_threshold):
    import zipfile
    saved = []
    stem = slugify(docx_path.stem)
    with zipfile.ZipFile(str(docx_path), "r") as z:
        media = sorted(n for n in z.namelist() if n.startswith("word/media/"))
        for media_name in media:
            ext = Path(media_name).suffix.lower()
            if ext not in SUPPORTED_IMG:
                continue
            data = z.read(media_name)
            if image_too_small(data):
                continue
            try:
                out_data, out_ext = postprocess_image_bytes(
                    data, None, exif_rotate=exif_rotate,
                    bg_remove=bg_remove, bg_threshold=bg_threshold)
            except Exception:
                continue
            idx = next_index(existing + saved)
            label = slugify(Path(media_name).stem or stem)
            fname = f"{idx:02d}_{label}.{out_ext}"
            dest = out_dir / fname
            dest.write_bytes(out_data)
            saved.append(dest)
            existing.append(dest)
            log(f"✓ DOCX image → {fname}", indent=1)
    return saved


# ── Parse PROMPT.txt Section 4A web gaps ──────────────────────────────────────

def parse_web_gaps(prompt_path: Path):
    """Extract [WEB] entries from PROMPT.txt Section 4 / 4A."""
    if not prompt_path.exists():
        return []
    text = prompt_path.read_text(encoding="utf-8", errors="replace")
    gaps, in_s4 = [], False
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^\[4A?\]", stripped):
            in_s4 = True; continue
        if re.match(r"^\[\d\]|^\[PRE-RUN\]", stripped) and in_s4:
            in_s4 = False
        if in_s4 and stripped.upper().startswith("[WEB]"):
            desc = stripped[5:].strip()
            if desc.lower().startswith("example:") or not desc:
                continue
            gaps.append({"description": desc, "query": desc})
    return gaps


# ── Web image download (best-effort, optional) ────────────────────────────────

def _ddg_image_urls(query, max_results=3):
    encoded = urllib.parse.quote(query)
    url = f"https://duckduckgo.com/?q={encoded}&iax=images&ia=images"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        msg = str(e)
        if "403" in msg or "Forbidden" in msg or "Tunnel" in msg:
            log("⚠ Web search blocked (proxy/firewall) — skipping web images", indent=2)
        else:
            log(f"⚠ DDG search failed: {e}", indent=2)
        return []
    matches = re.findall(r'"image":"(https?://[^"]+)"', html) or \
              re.findall(r'data-src="(https?://[^"]+\.(?:jpg|png|jpeg)[^"]*)"', html)
    seen, clean = set(), []
    for m in matches:
        if m not in seen:
            seen.add(m); clean.append(m)
        if len(clean) >= max_results:
            break
    return clean


def download_web_image(query, dest_path, *, exif_rotate, bg_remove, bg_threshold):
    urls = _ddg_image_urls(query, max_results=5)
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://duckduckgo.com/"}
    for img_url in urls:
        try:
            req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
            if image_too_small(data):
                continue
            from PIL import Image
            img = Image.open(io.BytesIO(data))
            if img.size[0] < 200 or img.size[1] < 100:
                continue
            out_data, _ = postprocess_image_bytes(
                data, exif_rotate=exif_rotate,
                bg_remove=bg_remove, bg_threshold=bg_threshold)
            dest_path.write_bytes(out_data)
            return True
        except Exception as e:
            log(f"⚠ Could not fetch {img_url[:60]}...: {e}", indent=3)
            time.sleep(0.3)
    return False


# ── Manifest writer ───────────────────────────────────────────────────────────

def write_manifest(out_dir: Path, all_images, web_map):
    manifest = out_dir / "image_manifest.txt"
    lines = [
        "IMAGE MANIFEST — generated by prep_active.py",
        "Read this file to understand what each image shows.",
        "Images are listed in numeric order (01_, 02_, ...).",
        "=" * 60, "",
    ]
    for img in sorted(all_images, key=lambda p: p.name):
        desc = web_map.get(img.name, "[image]")
        lines.append(img.name)
        lines.append(f"  → {desc}")
        lines.append("")
    manifest.write_text("\n".join(lines), encoding="utf-8")
    log(f"✓ Manifest written → {manifest.name}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    global MIN_SIZE_KB
    parser = argparse.ArgumentParser(description="SOP Factory pre-processor")
    parser.add_argument("--active", help="Path to active/ folder (auto-detected if omitted)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--min-kb", type=int, default=MIN_SIZE_KB,
                        help=f"Skip images smaller than N KB (default {MIN_SIZE_KB})")
    parser.add_argument("--bg-remove", dest="bg_remove", action="store_true",
                        help="Remove near-white background (default: off)")
    parser.add_argument("--no-bg-remove", dest="bg_remove", action="store_false")
    parser.set_defaults(bg_remove=BG_REMOVE_DEFAULT)
    parser.add_argument("--bg-threshold", type=int, default=BG_THRESHOLD_DEFAULT,
                        help=f"0..255 (default {BG_THRESHOLD_DEFAULT})")
    parser.add_argument("--exif-rotate", dest="exif_rotate", action="store_true")
    parser.add_argument("--no-exif-rotate", dest="exif_rotate", action="store_false")
    parser.set_defaults(exif_rotate=EXIF_ROTATE_DEFAULT)
    parser.add_argument("--recursive", dest="recursive", action="store_true")
    parser.add_argument("--no-recursive", dest="recursive", action="store_false")
    parser.set_defaults(recursive=RECURSIVE_DEFAULT)
    parser.add_argument("--loose-images", dest="loose_images", action="store_true")
    parser.add_argument("--no-loose-images", dest="loose_images", action="store_false")
    parser.set_defaults(loose_images=LOOSE_IMAGES_DEFAULT)
    parser.add_argument("--max-loose-images", type=int, default=MAX_LOOSE_IMAGES_DEFAULT)
    args = parser.parse_args()
    MIN_SIZE_KB = args.min_kb

    # Locate folders
    if args.active:
        active_dir = Path(args.active).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        active_dir = script_dir.parent / "active"
        if not active_dir.exists():
            active_dir = script_dir.parent / "_active"

    template_dir = active_dir.parent / "template"
    if not template_dir.exists():
        template_dir = active_dir.parent / "_template"
    prompt_path = template_dir / "PROMPT.txt"

    if not active_dir.exists():
        log(f"ERROR: active/ not found at {active_dir}")
        sys.exit(1)

    log("=" * 60)
    log("SOP Factory Pre-Processor")
    log("=" * 60)
    log(f"active/   : {active_dir}")
    log(f"PROMPT.txt: {prompt_path}")
    log("")

    if args.dry_run:
        log("DRY RUN — no files will be written")
        log("")

    existing_images = [p for p in active_dir.iterdir() if is_numbered_image(p)]
    log(f"Existing numbered images: {len(existing_images)}")

    all_images = list(existing_images)
    web_map = {}

    # PDFs
    pdfs = sorted(active_dir.rglob("*.pdf")) if args.recursive else sorted(active_dir.glob("*.pdf"))
    if pdfs:
        log(f"\nExtracting from {len(pdfs)} PDF(s):")
        for pdf in pdfs:
            try: rel = pdf.relative_to(active_dir)
            except Exception: rel = pdf
            log(f"  {rel}")
            if not args.dry_run:
                new = extract_from_pdf(pdf, active_dir, all_images,
                    exif_rotate=args.exif_rotate, bg_remove=args.bg_remove,
                    bg_threshold=args.bg_threshold)
                log(f"→ {len(new)} image(s) extracted", indent=2)
    else:
        log("No PDFs found in active/")

    # DOCX
    docxs = sorted(active_dir.rglob("*.docx")) if args.recursive else sorted(active_dir.glob("*.docx"))
    if docxs:
        log(f"\nExtracting from {len(docxs)} DOCX file(s):")
        for d in docxs:
            try: rel = d.relative_to(active_dir)
            except Exception: rel = d
            log(f"  {rel}")
            if not args.dry_run:
                new = extract_from_docx(d, active_dir, all_images,
                    exif_rotate=args.exif_rotate, bg_remove=args.bg_remove,
                    bg_threshold=args.bg_threshold)
                log(f"→ {len(new)} image(s) extracted", indent=2)
    else:
        log("No DOCX files found in active/")

    # Loose screenshots/photos in subfolders
    if args.loose_images:
        loose = collect_loose_images(active_dir)
        if loose:
            log(f"\nLoose screenshots/photos under active/: {len(loose)}")
            if len(loose) > args.max_loose_images:
                log(f"  WARNING: {len(loose)} exceeds --max-loose-images ({args.max_loose_images})")
                loose = loose[: args.max_loose_images]
            for src in loose:
                try: rel = src.relative_to(active_dir)
                except Exception: rel = src
                if args.dry_run:
                    idx = next_index(all_images)
                    fname = f"{idx:02d}_{slugify(src.stem, maxlen=32)}.png"
                    log(f"  [{idx:02d}] would process {rel} -> {fname}")
                    all_images.append(active_dir / fname)
                    continue
                try:
                    data = src.read_bytes()
                except Exception:
                    continue
                if image_too_small(data):
                    continue
                try:
                    out_data, out_ext = postprocess_image_bytes(
                        data, src,
                        exif_rotate=args.exif_rotate, bg_remove=args.bg_remove,
                        bg_threshold=args.bg_threshold,
                        jpeg_quality=JPEG_QUALITY_DEFAULT)
                except Exception:
                    continue
                idx = next_index(all_images)
                slug = slugify(src.stem, maxlen=32)
                fname = f"{idx:02d}_{slug}.{out_ext}"
                dest = active_dir / fname
                if dest.exists():
                    fname = f"{idx:02d}_{slug}_{int(time.time())}.{out_ext}"
                    dest = active_dir / fname
                dest.write_bytes(out_data)
                all_images.append(dest)
                web_map[fname] = _best_caption_from_source(src)
                log(f"✓ Loose image → {fname}", indent=1)
        else:
            log("\nNo loose screenshots/photos found under active/")

    # Web gaps
    gaps = parse_web_gaps(prompt_path)
    if gaps:
        log(f"\nWeb image gaps in PROMPT.txt Section 4A: {len(gaps)}")
        for gap in gaps:
            desc, query = gap["description"], gap["query"]
            idx = next_index(all_images)
            slug = slugify(desc)
            fname = f"{idx:02d}_web_{slug}.png"
            dest = active_dir / fname
            log(f"  [{idx:02d}] {desc}")
            log(f"Searching: \"{query}\"", indent=2)
            if args.dry_run:
                log(f"→ would save as {fname}", indent=2)
            else:
                ok = download_web_image(query, dest,
                    exif_rotate=args.exif_rotate, bg_remove=args.bg_remove,
                    bg_threshold=args.bg_threshold)
                if ok:
                    log(f"✓ saved → {fname}", indent=2)
                    all_images.append(dest)
                    web_map[fname] = desc
                else:
                    log("✗ no usable image found — placeholder left in SOP", indent=2)
                time.sleep(WEB_SEARCH_PAUSE)
    else:
        log("\nNo [WEB] gap entries found in PROMPT.txt Section 4A")

    # Final manifest
    final = sorted(
        [p for p in active_dir.iterdir()
         if p.suffix.lower() in SUPPORTED_IMG and re.match(r"^\d+_", p.name)],
        key=lambda p: p.name)

    log(f"\n{'='*60}")
    log(f"Images ready in active/: {len(final)}")
    for img in final:
        desc = web_map.get(img.name, "")
        suffix = f"  ← {desc}" if desc else ""
        log(f"  {img.name}{suffix}")

    if not args.dry_run and final:
        write_manifest(active_dir, final, web_map)

    log("\n✓ Done. Next: invoke the SOP Builder skill (or draft the SOP manually).")
    log("=" * 60)


if __name__ == "__main__":
    main()
