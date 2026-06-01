"""
build_inos_sop_draft.py
=======================
Builds the VRSI-formatted "iNOS Laptop Deployment AND Domain Join" SOP
(INOS_DEPLOY-001 v1.0) using the SOPBuilder helper in sop_lib.py.

Source material:
  - Transcript: iNOS-Laptop-Deployment-Domain-Join-SOP transcript.md
  - Ventoy USB build steps: VENTOY-001_v1.0.docx (full procedure)
  - VRSI rules: SOP_TEMPLATE.md
  - Confirmed image slot mappings (parallel vision analysis)

Image slots with confirmed mappings are inserted with b.image(...).
Slots that are proprietary iNOS screens or unavailable as a faithful public
screenshot are inserted with b.placeholder(...).
"""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "template"))
from sop_lib import SOPBuilder

b = SOPBuilder(
    template_docx=str(BASE / "template" / "SOP_TEMPLATE_WITH_PHOTOS.docx"),
    output_docx=str(BASE / "output" / "INOS_DEPLOY-001_v1.0.docx"),
    active_dir=str(BASE / "active"),
    revision="1.0",
    date="05/29/2026",
)

# ===========================================================================
# TITLE PAGE
# ===========================================================================
b.title_page(
    line1="iNOS Laptop Deployment",
    connector="AND",
    line2="Domain Join",
    subtitle="Remote deployment of iNOS Windows 25H2 image with VPN and domain join",
    doc_no="INOS_DEPLOY-001",
    author="BK",
)

# ===========================================================================
# TABLE OF CONTENTS
# ===========================================================================
b.toc([
    "1.   Overview",
    "2.   Prerequisites",
    "3.   Phase 1 — Build the Ventoy USB",
    "       A)  Download and Extract Ventoy",
    "       B)  Install Ventoy to USB Drive",
    "       C)  Load the iNOS ISO onto the Ventoy USB",
    "4.   Phase 2 — Boot to SmartDeploy",
    "5.   Phase 3 — Image Deployment (Automated)",
    "       A)  Background Tasks",
    "       B)  Completion Signal",
    "6.   Phase 4 — Connect to VPN",
    "7.   Phase 5 — Domain Join",
    "8.   Phase 6 — First Domain Login",
    "9.   Quick Reference Checklist",
    "10.  Known Issues / Notes",
    "11.  Appendix — One-Time Boot Menu",
    "12.  Revision History",
])

# ===========================================================================
# 1. OVERVIEW
# ===========================================================================
b.heading1("1.   Overview")
b.paragraph(
    "This document describes how to remotely deploy the iNOS Windows 25H2 image "
    "to a laptop, connect to the corporate VPN, and join the machine to the "
    "domain. It is written for IT technicians performing field or remote "
    "deployments and assumes per-device credentials have been provided "
    "separately."
)
b.paragraph(
    "Estimated end-to-end time is roughly 45 minutes, the bulk of which is the "
    "automated SmartDeploy imaging step (about 25-30 minutes). Following this "
    "procedure consistently ensures reliable, repeatable deployments across all "
    "supported hardware."
)

# ===========================================================================
# 2. PREREQUISITES
# ===========================================================================
b.heading1("2.   Prerequisites")
b.bullet_rich([
    ("Ventoy USB drive", True),
    (" — minimum 64 GB. Build it using Phase 1 below.", False),
])
b.bullet_rich([
    ("Image file: ", False),
    ("iNOS Windows 25H2.iso", True),
    (".", False),
])
b.bullet_rich([
    ("Target laptop", True),
    (" with Secure Boot disabled in BIOS.", False),
])
b.bullet("Per-device credentials (provided separately):")
b.bullet_rich([("PC name — format ", False), ("iNOS-LAPT-####", True)], sub=True)
b.bullet("Domain username / password", sub=True)
b.bullet("VPN username / password", sub=True)
b.bullet("Duo MFA enrollment", sub=True)
b.bullet("Windows 10 or Windows 11 PC with internet access (to build the Ventoy USB).")
b.bullet_rich([
    ("Ventoy installation package (", False),
    ("ventoy-1.1.10-windows.zip", True),
    (").", False),
])
b.paragraph(
    "WARNING: PC names must be unique across the fleet. A duplicate name will "
    "break the domain join. Never reuse a number."
)

b.page_break()

# ===========================================================================
# 3. PHASE 1 — BUILD THE VENTOY USB
# ===========================================================================
b.heading1("3.   Phase 1 — Build the Ventoy USB")
b.paragraph(
    "Ventoy is an open-source multi-boot USB tool that boots ISO, WIM, IMG, "
    "VHD(x), and EFI files directly without reformatting the drive for each "
    "image. Combined with the SmartDeploy offline media, this enables fully "
    "self-contained Windows 11 imaging with no network access required."
)
b.paragraph(
    "WARNING: Installing Ventoy will FORMAT the USB drive and erase ALL existing "
    "data. Back up any important files on the USB drive before proceeding."
)

# ---- A) Download and Extract Ventoy ----
b.heading2("A)   Download and Extract Ventoy")
b.bullet_rich([
    ("Navigate to the official Ventoy GitHub releases page: ", False),
    ("https://github.com/ventoy/Ventoy/releases", True),
])
b.bullet_rich([
    ("Download ", False),
    ("ventoy-1.1.10-windows.zip", True),
    (" (approximately 16 MB).", False),
])
b.bullet_rich([
    ("Right-click the downloaded ZIP file and select ", False),
    ("Extract All...", True),
    (" or use 7-Zip.", False),
])
b.bullet("Extract to a convenient location (e.g., the Downloads folder).")
b.bullet_rich([
    ("Open the extracted folder. The path should be: ", False),
    ("Downloads > ventoy-1.1.10-windows > ventoy-1.1.10", True),
    (".", False),
])
b.bullet("Verify the extracted folder contains the expected files and folders:")
b.bullet_rich([("Ventoy2Disk.exe", True), (" — main installer GUI (use this to install Ventoy to USB)", False)], sub=True)
b.bullet_rich([("VentoyPlugson.exe", True), (" — plugin configuration tool for advanced settings", False)], sub=True)
b.bullet_rich([("VentoyVlnk.exe", True), (" — utility for creating Ventoy Vlnk shortcut files", False)], sub=True)
b.bullet_rich([("FOR_X64_ARM.txt", True), (" — instructions for 64-bit / ARM alternative executables", False)], sub=True)
b.bullet_rich([("plugin\\", True), (", ", False), ("ventoy\\", True), (", ", False), ("altexe\\", True), (", and ", False), ("boot\\", True), (" folders", False)], sub=True)

# ---- B) Install Ventoy to USB Drive ----
b.heading2("B)   Install Ventoy to USB Drive")
b.paragraph(
    "WARNING: Double-check the selected device. Selecting the wrong drive will "
    "result in permanent data loss. By default, Ventoy only lists USB drives to "
    "help prevent accidental selection of internal disks."
)
b.bullet("Insert the target USB flash drive into the PC.")
b.bullet("Ensure no important data remains on the drive, as it will be formatted.")
b.bullet_rich([
    ("Double-click ", False),
    ("Ventoy2Disk.exe", True),
    (" from the extracted ", False),
    ("ventoy-1.1.10", True),
    (" folder.", False),
])
b.bullet_rich([
    ("If prompted by User Account Control (UAC), click ", False),
    ("Yes", True),
    (" to allow.", False),
])
b.bullet_rich([
    ("In the ", False),
    ("Device", True),
    (" dropdown at the top of the Ventoy2Disk window, select your USB flash drive.", False),
])
b.bullet("Verify the drive letter and capacity match your intended USB drive.")
b.bullet_rich([
    ("Click the ", False),
    ("Option", True),
    (" menu and select ", False),
    ("Partition Style", True),
    (" — choose ", False),
    ("MBR", True),
    (" (default) or ", False),
    ("GPT", True),
    (". MBR is recommended for broadest compatibility.", False),
])
b.bullet_rich([
    ("If Secure Boot support is needed, enable it under ", False),
    ("Option > Secure Boot Support", True),
    (".", False),
])
b.bullet_rich([
    ("Click the ", False),
    ("Install", True),
    (" button at the bottom of the window.", False),
])
b.bullet_rich([
    ("Click ", False),
    ("OK", True),
    (" on the first confirmation dialog warning that all data on the USB drive will be destroyed.", False),
])
b.bullet_rich([("Click ", False), ("OK", True), (" again on the second confirmation dialog to proceed.", False)])
b.bullet("Wait for the installation to complete. The progress bar will fill and a success message will appear.")
b.bullet_rich([("Click ", False), ("OK", True), (" to dismiss the success dialog.", False)])
b.bullet_rich([
    ("Verify the Ventoy2Disk GUI shows the installed version under ", False),
    ("Ventoy In Device", True),
    (" (e.g., 1.1.10).", False),
])
b.bullet_rich([
    ("Open File Explorer and verify the USB drive is labeled ", False),
    ("Ventoy", True),
    (" and formatted as exFAT. A second small hidden partition (", False),
    ("VTOYEFI", True),
    (") is normal.", False),
])

# ---- C) Load the iNOS ISO onto the Ventoy USB ----
b.heading2("C)   Load the iNOS ISO onto the Ventoy USB")
b.paragraph(
    "NOTE: The Ventoy USB drive contains two partitions. The Ventoy (data) "
    "partition is where ISO files go; the VTOYEFI (boot) partition holds the "
    "boot loader and should be left alone. The iNOS offline ISO can be large, "
    "so ensure the drive has at least 64 GB capacity."
)
b.bullet_rich([
    ("Locate ", False),
    ("iNOS Windows 25H2.iso", True),
    (" (the SmartDeploy offline deployment media) on the PC.", False),
])
b.bullet_rich([
    ("Open the Ventoy USB drive in File Explorer (the drive labeled ", False),
    ("Ventoy", True),
    (").", False),
])
b.bullet_rich([
    ("Copy and paste (or drag and drop) ", False),
    ("iNOS Windows 25H2.iso", True),
    (" into the root of the Ventoy (data) partition. Do NOT extract the ISO — Ventoy boots it directly.", False),
])
b.bullet_rich([
    ("Confirm ", False),
    ("iNOS Windows 25H2.iso", True),
    (" is present on the Ventoy drive, then safely eject the USB when done.", False),
])
b.placeholder("The iNOS ISO placed in the root of the Ventoy (data) partition, with the EFI partition left untouched")

b.page_break()

# ===========================================================================
# 4. PHASE 2 — BOOT TO SMARTDEPLOY
# ===========================================================================
b.heading1("4.   Phase 2 — Boot to SmartDeploy")
b.bullet("Insert the Ventoy USB into the target laptop. Use a USB port directly on the chassis; avoid hubs.")
b.bullet_rich([
    ("Enter BIOS and confirm ", False),
    ("Secure Boot = Off", True),
    (".", False),
])
b.image("43_media_1.jpg", caption="Confirm Secure Boot is set to Disabled before saving and exiting BIOS.")
b.bullet_rich([
    ("Power on and open the one-time boot menu (usually ", False),
    ("F11", True),
    (" or ", False),
    ("F12", True),
    (" — varies by model; see the Appendix).", False),
])
b.image("29_img_3097.jpg", caption="Select the USB flash drive from the one-time boot menu.")
b.bullet_rich([("Select the ", False), ("USB flash drive", True), (".", False)])
b.bullet_rich([
    ("When the Ventoy menu loads, select the ", False),
    ("iNOS Windows 25H2 ISO", True),
    (" and choose ", False),
    ("Boot in normal mode", True),
    (".", False),
])
b.image("31_img_3099.jpg", caption="From the Ventoy menu, select the iNOS Windows 25H2 ISO.")
b.bullet_rich([
    ("SmartDeploy launches into its WinPE environment (looks like a Windows boot screen). Allow 1-3 minutes for SmartPE to load.", False),
])
b.image("08_snipaste_2026_05_28_15_59_08.png", caption="SmartDeploy launches into its WinPE environment.")
b.paragraph(
    "WARNING: 30-second cancel window — point of no return. Once SmartDeploy "
    "starts, you have about 30 seconds to cancel. After that, the internal "
    "drive is wiped and imaging begins. This is irreversible."
)
b.image("09_snipaste_2026_05_28_15_59_31.png", caption="The 30-second cancel window before the disk is wiped. After this, deployment is irreversible.")

b.page_break()

# ===========================================================================
# 5. PHASE 3 — IMAGE DEPLOYMENT (AUTOMATED)
# ===========================================================================
b.heading1("5.   Phase 3 — Image Deployment (Automated)")
b.paragraph(
    "SmartDeploy wipes the disk and lays down the image. Expect about 25-30 "
    "minutes until the Windows desktop appears. The PC then auto-logs into a "
    "local user."
)
b.image("11_snipaste_2026_05_28_16_00_32.png", caption="SmartDeploy deploys the iNOS image. Total runtime is roughly 25-30 minutes.")

# ---- A) Background Tasks ----
b.heading2("A)   Background Tasks")
b.paragraph("Post-deploy scripts keep running for several minutes after the desktop appears:")
b.bullet("Application installs (FortiClient VPN, Casbury/Cosbury, others)")
b.bullet("Application updates")
b.bullet("Configuration scripts")
b.paragraph("Desktop icons populate as each script completes.")

# ---- B) Completion Signal ----
b.heading2("B)   Completion Signal")
b.bullet_rich([
    ("Deployment is complete when ", False),
    ("Domain Join.K", True),
    (" appears on the desktop. FortiClient should also be visible.", False),
])
b.image("18_snipaste_2026_05_28_16_31_25.png", caption="Deployment is complete once the Domain Join.K icon appears on the desktop. FortiClient should also be visible.")
b.paragraph(
    "TIP: Most desktop icons are just completion markers / log files and can be "
    "deleted. Keep FortiClient on the desktop for easy access."
)

b.page_break()

# ===========================================================================
# 6. PHASE 4 — CONNECT TO VPN
# ===========================================================================
b.heading1("6.   Phase 4 — Connect to VPN")
b.bullet_rich([("Open ", False), ("FortiClient VPN", True), (".", False)])
b.bullet_rich([("Click ", False), ("Connect", True), (" on the iNOS profile.", False)])
b.image("01_screenshot.png", caption="Open FortiClient and click Connect on the iNOS VPN profile.")
b.bullet("Authenticate with the provided VPN credentials.")
b.bullet_rich([("Approve the ", False), ("Duo", True), (" push.", False)])
b.placeholder("The Duo push prompt on a phone — tap Approve to complete VPN authentication")
b.paragraph(
    "WARNING: VPN required before domain join. The VPN must be connected before "
    "running the domain join script. The script fails without it."
)
b.bullet_rich([
    ("Confirm FortiClient shows a ", False),
    ("connected", True),
    (" state (green indicator) before continuing.", False),
])
b.placeholder("FortiClient showing a connected state (green indicator) on the iNOS VPN profile")

b.page_break()

# ===========================================================================
# 7. PHASE 5 — DOMAIN JOIN
# ===========================================================================
b.heading1("7.   Phase 5 — Domain Join")
b.bullet_rich([
    ("Right-click ", False),
    ("Domain Join.K", True),
    (" on the desktop and choose ", False),
    ("Run as administrator", True),
    (".", False),
])
b.paragraph(
    "IMPORTANT: Do not double-click. Double-clicking will not work. It must be "
    "right-click → Run as administrator."
)
b.image("21_snipaste_2026_05_28_17_02_58.png", caption="Right-click the Domain Join.K icon and choose Run as administrator. Double-clicking will not work.")
b.bullet("When prompted for the PC name, enter the device's assigned name:")
b.bullet_rich([("Format: ", False), ("iNOS-LAPT-####", True)], sub=True)
b.bullet("The number must be unique — never reuse one.", sub=True)
b.image("23_snipaste_2026_05_29_07_51_07.png", caption="Enter the assigned PC name in the format iNOS-LAPT-####. The number must be unique.")
b.bullet_rich([
    ("The script joins the machine to ", False),
    ("BSI.local", True),
    (" (or the domain shown on screen).", False),
])
b.image("24_snipaste_2026_05_29_07_51_58.png", caption="The script confirms the machine has joined BSI.local.")
b.bullet_rich([("When prompted, ", False), ("reboot", True), (".", False)])
b.image("25_snipaste_2026_05_29_07_52_45.png", caption="Accept the reboot prompt to complete the domain join.")

b.page_break()

# ===========================================================================
# 8. PHASE 6 — FIRST DOMAIN LOGIN
# ===========================================================================
b.heading1("8.   Phase 6 — First Domain Login")
b.paragraph("After reboot, one of two things happens:")
b.scenario_table(
    [
        ("Auto-logs into local BSI user", "Sign out, then choose Other user"),
        ("Lands on the login screen", "Click Other user"),
    ],
    headers=("Scenario", "Action"),
)
b.paragraph("Then:")
b.bullet_rich([
    ("On the ", False),
    ("Other user", True),
    (" screen, find the ", False),
    ("FortiClient login option", True),
    (" (bottom-right of the credential fields).", False),
])
b.image("42_img_3111.jpg", caption="At the Other user screen, click the FortiClient icon (bottom-right) to connect VPN before signing in.")
b.bullet("Click it — this connects the VPN before Windows authentication.")
b.bullet_rich([
    ("Enter your ", False),
    ("domain credentials", True),
    (". The same username/password is used twice: once for the VPN, once for the Windows login.", False),
])
b.image("27_img_3095.jpg", caption="Enter your domain credentials for the VPN portion of the login.")
b.bullet_rich([("Approve the ", False), ("Duo", True), (" prompt.", False)])
b.placeholder("The Duo prompt at the logon screen — approve to complete the VPN-at-logon step")
b.bullet("You are now signed in.")
b.paragraph(
    "INFO: Going forward, until the device is physically on the corporate "
    "network, every login requires the VPN-at-logon flow. Once on the domain "
    "network, normal login works without the VPN step. Subsequent VPN connects "
    "only prompt for the Duo push — not full credentials."
)

b.page_break()

# ===========================================================================
# 9. QUICK REFERENCE CHECKLIST
# ===========================================================================
b.heading1("9.   Quick Reference Checklist")
b.bullet("Ventoy USB built (>= 64 GB) with iNOS ISO at root")
b.bullet("Secure Boot disabled in BIOS")
b.bullet("Booted from USB → SmartDeploy launched")
b.bullet("Allowed the 30-sec wipe countdown")
b.bullet_rich([("Waited for ", False), ("Domain Join.K", True), (" icon on desktop", False)])
b.bullet("FortiClient VPN connected + Duo approved")
b.bullet_rich([("Right-clicked ", False), ("Domain Join.K", True), (" → Run as administrator", False)])
b.bullet_rich([("Entered unique PC name (", False), ("iNOS-LAPT-####", True), (")", False)])
b.bullet("Rebooted after domain join")
b.bullet_rich([("Logged in via ", False), ("Other user", True), (" + FortiClient at logon screen", False)])
b.bullet("Duo approved → domain login successful")

# ===========================================================================
# 10. KNOWN ISSUES / NOTES
# ===========================================================================
b.heading1("10.  Known Issues / Notes")
b.bullet_rich([
    ("Auto-login to local BSI user after reboot", True),
    (" — under investigation. Workaround: sign out, use Other user.", False),
])
b.bullet_rich([
    ("Duplicate PC names", True),
    (" cause domain join failure — always confirm the assigned number.", False),
])
b.bullet_rich([
    ("Boot key", True),
    (" (", False),
    ("F11", True),
    (" / ", False),
    ("F12", True),
    (" / etc.) varies by laptop model — TBD per hardware spec.", False),
])

# ===========================================================================
# 11. APPENDIX — ONE-TIME BOOT MENU
# ===========================================================================
b.heading1("11.  Appendix — One-Time Boot Menu")
b.bullet("Power off the laptop completely.")
b.bullet_rich([
    ("Power on, then tap ", False),
    ("F12", True),
    (" repeatedly at the Dell logo.", False),
])
b.bullet("The One Time Boot Menu appears.")
b.paragraph("What you will see:")
b.bullet_rich([
    ("UEFI BOOT", True),
    (" — Windows Boot Manager, UEFI USB devices, UEFI network/PXE", False),
])
b.bullet_rich([
    ("OTHER OPTIONS", True),
    (" — BIOS Setup, Diagnostics, BIOS Flash Update, SupportAssist OS Recovery", False),
])
b.paragraph(
    "This overrides boot order for that single boot only — your normal boot "
    "order stays unchanged."
)

b.page_break()

# ===========================================================================
# 12. REVISION HISTORY
# ===========================================================================
b.heading1("12.  Revision History")
b.revision_history([("05/29/2026", "1.0", "Initial release", "BK")])

out = b.save()
print(f"Saved: {out}")
