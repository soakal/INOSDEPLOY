# INOS_DEPLOY-001 — SOP Build Log

Record of how the **INOS Laptop Deployment AND Domain Join** SOP (`INOS_DEPLOY-001 v1.2`) was produced.

- **Output:** `output/INOS_DEPLOY-001_v1.2.docx`
- **Builder script:** `build_inos_sop.py` (re-run any time to regenerate)
- **Author:** BK · **Revision:** 1.2 · **Date:** 05/29/2026
- **Status:** Production-ready

## v1.2 changes (05/29/2026)
- **BIOS / boot-menu entry inlined into Phase 2** — the procedure now tells the tech exactly how to get in (Dell: full shutdown → tap **F2** at the logo for **BIOS Setup** to confirm Secure Boot Off → **Save & Exit** → tap **F12** for the **One-Time Boot Menu**), with non-Dell key hints as sub-bullets. No Appendix lookup required. Appendix retained as supplementary reference.
- **Real Duo screenshot** — replaced the generic stock `web_duo_push.png` (an "ACME Corp" placeholder) with the actual VRSI prompt `active/Duo.JPEG` ("Are you logging in to Fortinet FortiGate SSL VPN?" — VariationReductionSolutions / Detroit, MI) in **both** Phase 4 and Phase 6. Inserted at `width_in=2.8` so the portrait phone shot fits the page; captions rewritten to match the real prompt.
- **Credential-caching clarified** — Phase 6 INFO callout rewritten: the VPN-at-logon flow is needed only for the **first** domain login; afterward domain credentials are cached, so the user signs in normally **without** the VPN. The laptop has no day-to-day VRSI network access; reconnect VPN only if IT asks. (The old "every login requires the VPN-at-logon flow" wording was wrong and is removed.)
- **VPN-client / test-IP issue:** owner asked to leave this alone for now (not sure a doc change is needed) — no edit made.

## v1.1 changes (05/29/2026)
- **Product name standardized to `INOS`** (all caps) throughout the document — title, body, captions, ISO name, and PC-name format (`INOS-LAPT-###`). Per owner request.
- **Ventoy screenshots made English-only:**
  - `48_ventoy_installer_format.png` — German confirmation buttons **Ja/Nein → Yes/No** (in-place font overlay).
  - `web_ventoy_partitions.png` — was a **Turkish** File Explorer + Ventoy2Disk window showing the wrong version (1.0.90/1.0.88). Cropped to just the File Explorer partition tiles (dropping the contradictory Turkish window), overlaid English sizes, and normalized the data-partition label to **Ventoy (D:)** to match the doc.

---

## Source material (`active/`)
- `iNOS-Laptop-Deployment-Domain-Join-SOP transcript.md` — the procedure (6 phases + checklist + appendix)
- `VENTOY-001_v1.0.docx` — full Ventoy USB build procedure (folded into Phase 1)
- 26 screenshots + 18 photos → numbered `01_*`–`44_*` by `template/prep_active.py`
- Web-sourced fills: `45`–`51` (Ventoy installer/boot), `web_duo_push.png`, `web_forticlient_connected.png`, `web_ventoy_partitions.png`

---

## Process

1. **Pre-process images** — `python template/prep_active.py` numbered all images and wrote `active/image_manifest.txt`.
2. **Initial build (multi-agent, Opus)** — parallel vision agents mapped images to transcript steps; a Ventoy docx extraction agent pulled the full USB-build procedure into Phase 1; draft → VRSI review → finalize → execute.
3. **Ventoy enrichment** — added official Ventoy2Disk installer screenshots (device select, format warning, success, post-install) to Phase 1 §B; moved `44_media.jpg` (Dell One-Time Boot Settings) into Phase 2.
4. **Production-readiness pass (8-agent Opus workflow)** — parallel audits (technical / image-caption / VRSI formatting / editorial) + placeholder web-fill → synthesize → apply → verify. 31 findings (2 critical, 5 major) resolved.
5. **Owner confirmations applied** — see below.
6. **Version-matched screenshots** — relabeled the Ventoy installer screenshots `47` and `50` from 1.1.09 → **1.1.12** (red version text only; GUI is identical across versions).

---

## Key fixes applied
- Added a `callout(kind, text)` helper to `template/sop_lib.py` — WARNING (red) / IMPORTANT/TIP (orange) / NOTE/INFO (blue) render as colored boxes instead of plain text.
- Phase 6 image/caption swap (`27_img_3095.jpg` ↔ `42_img_3111.jpg`) so FortiClient-at-logon vs. Other-user screens are captioned correctly.
- Domain-join captions corrected to in-progress vs. success/reboot screens.
- "Windows 11" → "iNOS Windows 25H2" contradiction fixed; VPN profile named **VRSI-Corp**.
- 4 placeholders filled with verified web images (Ventoy partitions, Duo push ×2, FortiClient connected).
- Terminology normalized: **DOMAIN JOIN** (not "Domain Join.K"), **VRSI / VRSI.local** (not BSI).

## Owner-confirmed decisions
- **PC name format:** `iNOS-LAPT-###` (3 digits).
- **Ventoy version:** **1.1.12** (text + zip name + screenshots all match).
- **No named background-app installs** beyond FortiClient VPN.

---

## Remaining gaps (optional, need physical access — not blockers)
- Ventoy installer screenshots are **edited 1.1.09 captures** relabeled to 1.1.12 (illustrative, not real 1.1.12 captures). Replace with true captures from an actual 1.1.12 build if exact fidelity is wanted.
- `web_forticlient_connected.png` and `web_ventoy_partitions.png` are generic, non-VRSI web images — swap for real environment captures anytime. (Duo is now a real VRSI capture as of v1.2; `web_duo_push.png` is no longer used.)
- Known Issues notes boot key "TBD per hardware spec."

---

## Regenerate
```powershell
cd "C:\Users\briank\Desktop\Inos deployment sop"
python build_inos_sop.py
```
