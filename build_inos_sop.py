"""
build_inos_sop.py
=================
Builds the VRSI-formatted "INOS Laptop Deployment AND Domain Join" SOP
(INOS_DEPLOY-001 v1.3) using the SOPBuilder helper in sop_lib.py.

Source material:
  - Transcript: iNOS-Laptop-Deployment-Domain-Join-SOP transcript.md
  - Ventoy USB build steps: VENTOY-001_v1.0.docx (full procedure)
  - VRSI rules: SOP_TEMPLATE.md
  - Confirmed image slot mappings (parallel vision analysis)

Image slots with confirmed mappings are inserted with b.image(...).
Slots that are proprietary INOS screens or unavailable as a faithful public
screenshot are inserted with b.placeholder(...).
"""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "template"))
from sop_lib import SOPBuilder

b = SOPBuilder(
    template_docx=str(BASE / "template" / "SOP_TEMPLATE_WITH_PHOTOS.docx"),
    output_docx=str(BASE / "output" / "INOS_DEPLOY-001_v1.3.docx"),
    active_dir=str(BASE / "active"),
    revision="1.3",
    date="06/01/2026",
)

# ===========================================================================
# TITLE PAGE
# ===========================================================================
b.title_page(
    line1="INOS Laptop Deployment",
    connector="AND",
    line2="Domain Join",
    subtitle="Remote deployment of INOS Windows 25H2 image with VPN and domain join",
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
    "       A)   Download and Extract Ventoy",
    "       B)   Install Ventoy to USB Drive",
    "       C)   Load the INOS ISO onto the Ventoy USB",
    "4.   Phase 2 — Boot to SmartDeploy",
    "5.   Phase 3 — Image Deployment (Automated)",
    "       A)   Background Tasks",
    "       B)   Completion Signal",
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
    "This document describes how to remotely deploy the INOS Windows 25H2 image "
    "to a laptop, connect to the corporate VPN, and join the machine to the "
    "domain. It is written for IT technicians performing field or remote "
    "deployments and assumes per-device credentials have been provided "
    "separately."
)
b.paragraph(
    "Estimated end-to-end time is roughly 45 minutes, the bulk of which is the "
    "automated SmartDeploy imaging step (about 25–30 minutes). Following this "
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
    ("INOS Windows 25H2.iso", True),
    (".", False),
])
b.bullet_rich([
    ("Target laptop", True),
    (" with Secure Boot disabled in BIOS.", False),
])
b.bullet("Per-device credentials (provided separately):")
b.bullet_rich([("PC name — format ", False), ("INOS-LAPT-###", True)], sub=True)
b.bullet("Domain username / password", sub=True)
b.bullet("VPN username / password", sub=True)
b.bullet("Duo MFA enrollment", sub=True)
b.bullet("Windows 10 or Windows 11 PC with internet access (to build the Ventoy USB).")
b.bullet_rich([
    ("Ventoy installation package (", False),
    ("ventoy-1.1.12-windows.zip", True),
    (").", False),
])
b.callout(
    "WARNING",
    "PC names must be unique across the fleet. A duplicate name will "
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
    "self-contained INOS Windows 25H2 imaging with no network access required."
)
b.callout(
    "WARNING",
    "Installing Ventoy will FORMAT the USB drive and erase ALL existing "
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
    ("ventoy-1.1.12-windows.zip", True),
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
    ("Downloads > ventoy-1.1.12-windows > ventoy-1.1.12", True),
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
b.callout(
    "WARNING",
    "Double-check the selected device. Selecting the wrong drive will "
    "result in permanent data loss. By default, Ventoy only lists USB drives to "
    "help prevent accidental selection of internal disks."
)
b.bullet("Insert the target USB flash drive into the PC.")
b.bullet("Ensure no important data remains on the drive, as it will be formatted.")
b.bullet_rich([
    ("Double-click ", False),
    ("Ventoy2Disk.exe", True),
    (" (or right-click ", False),
    ("Run as administrator", True),
    (") from the extracted ", False),
    ("ventoy-1.1.12", True),
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
b.image("47_ventoy_installer_device.png", caption="Ventoy2Disk main window. Select the target USB drive from the Device dropdown, then click Install.")
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
b.image("48_ventoy_installer_format.png", caption="Ventoy warns that the device will be formatted and all data lost. Click Yes to continue. A second confirmation may follow — confirm it as well.")
b.bullet("Wait for the installation to complete. The progress bar will fill and a success message will appear.")
b.image("49_ventoy_installer_success.png", caption="Ventoy displays a Congratulations dialog when installation is successful. Click OK to dismiss.")
b.bullet_rich([("Click ", False), ("OK", True), (" to dismiss the success dialog.", False)])
b.bullet_rich([
    ("Verify the Ventoy2Disk GUI shows the installed version under ", False),
    ("Ventoy In Device", True),
    (" (e.g., 1.1.12).", False),
])
b.image("50_ventoy_installer_postinstall.png", caption="After a successful install, the Ventoy In Device version matches Ventoy In Package, and the Update button becomes active.")
b.bullet_rich([
    ("Open File Explorer and verify the USB drive is labeled ", False),
    ("Ventoy", True),
    (" (the data partition is typically exFAT, depending on the format option chosen during install). A second small hidden partition (labeled ", False),
    ("VTOYEFI", True),
    (", sometimes shown as Ventoy EFI) is normal.", False),
])

# ---- C) Load the INOS ISO onto the Ventoy USB ----
b.heading2("C)   Load the INOS ISO onto the Ventoy USB")
b.callout(
    "NOTE",
    "The Ventoy USB drive contains two partitions. The Ventoy (data) "
    "partition is where ISO files go; the VTOYEFI (boot) partition (sometimes "
    "shown as Ventoy EFI) holds the boot loader and should be left alone. The "
    "INOS offline ISO can be large, so ensure the drive has at least 64 GB capacity."
)
b.bullet_rich([
    ("Locate ", False),
    ("INOS Windows 25H2.iso", True),
    (" (the SmartDeploy offline deployment media) on the PC.", False),
])
b.bullet_rich([
    ("Open the Ventoy USB drive in File Explorer (the drive labeled ", False),
    ("Ventoy", True),
    (").", False),
])
b.bullet_rich([
    ("Copy and paste (or drag and drop) ", False),
    ("INOS Windows 25H2.iso", True),
    (" into the root of the Ventoy (data) partition. Do NOT extract the ISO — Ventoy boots it directly.", False),
])
b.bullet_rich([
    ("Confirm ", False),
    ("INOS Windows 25H2.iso", True),
    (" is present on the Ventoy drive, then safely eject the USB when done.", False),
])
b.image("web_ventoy_partitions.png", caption="Windows File Explorer showing the two Ventoy partitions: the large exFAT data partition (where the ISO is copied) and the small ~32 MB VTOYEFI/EFI partition, which is left untouched.")

b.page_break()

# ===========================================================================
# 4. PHASE 2 — BOOT TO SMARTDEPLOY
# ===========================================================================
b.heading1("4.   Phase 2 — Boot to SmartDeploy")
b.bullet("Insert the Ventoy USB into the target laptop. Use a USB port directly on the chassis; avoid hubs.")
b.bullet("Power the laptop off completely (a full shutdown, not sleep or restart).")
b.bullet_rich([
    ("Power it on and immediately tap ", False),
    ("F2", True),
    (" repeatedly at the Dell logo to enter ", False),
    ("BIOS Setup", True),
    (".", False),
])
b.bullet_rich([
    ("Non-Dell hardware uses a different key — usually ", False),
    ("F2", True),
    (", ", False),
    ("Del", True),
    (", ", False),
    ("F10", True),
    (", or ", False),
    ("Esc", True),
    (". Watch the splash screen for the on-screen prompt.", False),
], sub=True)
b.bullet_rich([
    ("In BIOS, confirm ", False),
    ("Secure Boot = Off", True),
    (", then ", False),
    ("Save & Exit", True),
    (".", False),
])
b.image("43_media_1.jpg", caption="The Dell BIOS Setup → Boot Configuration page (Secure Boot settings). Ensure Secure Boot is disabled (here, Enable Microsoft UEFI CA is set to OFF) before saving and exiting.")
b.bullet_rich([
    ("Let the laptop restart, then immediately tap ", False),
    ("F12", True),
    (" repeatedly at the Dell logo to open the ", False),
    ("One-Time Boot Menu", True),
    (".", False),
])
b.bullet_rich([
    ("On non-Dell hardware the one-time boot menu is usually ", False),
    ("F12", True),
    (", ", False),
    ("F11", True),
    (", ", False),
    ("F9", True),
    (", or ", False),
    ("Esc", True),
    (".", False),
], sub=True)
b.image("44_media.jpg", caption="The Dell One-Time Boot Settings menu. Select the USB flash drive entry under UEFI Boot Devices to boot from the Ventoy USB.")
b.bullet_rich([("Select the ", False), ("USB flash drive", True), (" from the UEFI Boot Devices list.", False)])
b.bullet_rich([
    ("When the Ventoy menu loads, select the ", False),
    ("INOS Windows 25H2 ISO", True),
    (" and choose ", False),
    ("Boot in normal mode", True),
    (".", False),
])
b.image("31_img_3099.jpg", caption="From the Ventoy menu, select the INOS Windows 25H2 ISO.")
b.bullet_rich([
    ("SmartDeploy launches into its WinPE environment (looks like a Windows boot screen). Allow 1–3 minutes for the WinPE environment to load.", False),
])
b.image("08_snipaste_2026_05_28_15_59_08.png", caption="SmartDeploy launches into its WinPE environment.")
b.callout(
    "WARNING",
    "30-second cancel window — point of no return. Once SmartDeploy "
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
    "SmartDeploy wipes the disk and lays down the image. Expect about 25–30 "
    "minutes until the Windows desktop appears. The PC then auto-logs into a "
    "local user."
)
b.image("11_snipaste_2026_05_28_16_00_32.png", caption="SmartDeploy deploys the INOS image. Total runtime is roughly 25–30 minutes.")

# ---- A) Background Tasks ----
b.heading2("A)   Background Tasks")
b.paragraph("Post-deploy scripts keep running for several minutes after the desktop appears:")
b.bullet("Application installs (FortiClient VPN and others)")
b.bullet("Application updates")
b.bullet("Configuration scripts")
b.paragraph("Desktop icons populate as each script completes.")

# ---- B) Completion Signal ----
b.heading2("B)   Completion Signal")
b.bullet_rich([
    ("Deployment is complete when ", False),
    ("DOMAIN JOIN", True),
    (" appears on the desktop. FortiClient should also be visible.", False),
])
b.image("19_snipaste_2026_05_28_16_42_52.png", caption="Deployment is complete once the DOMAIN JOIN icon appears on the desktop. FortiClient should also be visible.")
b.callout(
    "TIP",
    "Most desktop icons are just completion markers / log files and can be "
    "deleted. Keep FortiClient on the desktop for easy access."
)

b.page_break()

# ===========================================================================
# 6. PHASE 4 — CONNECT TO VPN
# ===========================================================================
b.heading1("6.   Phase 4 — Connect to VPN")
b.bullet_rich([("Open ", False), ("FortiClient VPN", True), (".", False)])
b.bullet_rich([("Click ", False), ("Connect", True), (" on the VRSI-Corp profile.", False)])
b.image("01_screenshot.png", caption="Open FortiClient and click Connect on the VRSI-Corp VPN profile (the INOS deployment profile).")
b.bullet("Authenticate with the provided VPN credentials.")
b.bullet_rich([("Approve the ", False), ("Duo", True), (" push on your phone.", False)])
b.image("Duo.JPEG", width_in=2.8, caption="The Duo prompt as it appears for VRSI: “Are you logging in to Fortinet FortiGate SSL VPN?” Confirm the details match your sign-in (VariationReductionSolutions, your username, your location and time), then tap the green Approve button.")
b.callout(
    "WARNING",
    "VPN required before domain join. The VPN must be connected before "
    "running the domain join script. The script fails without it."
)
b.bullet_rich([
    ("Confirm FortiClient shows a ", False),
    ("connected", True),
    (" state (green indicator) before continuing.", False),
])
b.image("web_forticlient_connected.png", caption="FortiClient VPN in the 'VPN Connected' state, showing the connection details (VPN name, IP address, duration, bytes sent/received) and the Disconnect button.")

b.page_break()

# ===========================================================================
# 7. PHASE 5 — DOMAIN JOIN
# ===========================================================================
b.heading1("7.   Phase 5 — Domain Join")
b.bullet_rich([
    ("Right-click ", False),
    ("DOMAIN JOIN", True),
    (" on the desktop and choose ", False),
    ("Run as administrator", True),
    (".", False),
])
b.callout(
    "IMPORTANT",
    "Do not double-click. Double-clicking will not work. It must be "
    "right-click → Run as administrator."
)
b.image("21_snipaste_2026_05_28_17_02_58.png", caption="Right-click the DOMAIN JOIN icon and choose Run as administrator. Double-clicking will not work.")
b.bullet("When prompted for the PC name, enter the device's assigned name:")
b.bullet_rich([("Format: ", False), ("INOS-LAPT-###", True)], sub=True)
b.bullet("The number must be unique — never reuse one.", sub=True)
b.image("23_snipaste_2026_05_29_07_51_07.png", caption="Enter the assigned PC name in the format INOS-LAPT-###. The number must be unique.")
b.bullet_rich([
    ("The script joins the machine to ", False),
    ("VRSI.local", True),
    (" (or the domain shown on screen).", False),
])
b.image("24_snipaste_2026_05_29_07_51_58.png", caption="After entering the PC name, the script begins joining the machine to VRSI.local.")
b.bullet_rich([("When prompted, ", False), ("reboot", True), (".", False)])
b.image("25_snipaste_2026_05_29_07_52_45.png", caption="The script reports [OK] Successfully joined vrsi.local. Answer Y at the reboot prompt to complete the domain join.")

b.page_break()

# ===========================================================================
# 8. PHASE 6 — FIRST DOMAIN LOGIN
# ===========================================================================
b.heading1("8.   Phase 6 — First Domain Login")
b.paragraph("After reboot, one of two things happens:")
b.scenario_table(
    [
        ("Auto-logs into local VRSI user", "Sign out, then choose Other user"),
        ("Lands on the login screen", "Click Other user"),
    ],
    headers=("Scenario", "Action"),
)
b.paragraph("Then:")
b.bullet_rich([
    ("On the ", False),
    ("Other user", True),
    (" screen, click ", False),
    ("Sign-in options", True),
    (", then choose the ", False),
    ("FortiClient credential provider", True),
    (" (shield icon).", False),
])
b.image("27_img_3095.jpg", caption="At the login screen, select the FortiClient sign-in option (shield icon) to connect the VPN before signing in. Enter your domain credentials for the VPN portion of the login.")
b.bullet("Select it — this connects the VPN before Windows authentication.")
b.bullet_rich([
    ("Enter your ", False),
    ("domain credentials", True),
    (". The same username/password is used twice: once for the VPN, once for the Windows login.", False),
])
b.image("42_img_3111.jpg", caption="The Other user login screen. If the VPN-at-logon fields are not shown, use the sign-in option to switch to the FortiClient credential provider.")
b.bullet_rich([("Approve the ", False), ("Duo", True), (" prompt on your phone.", False)])
b.image("Duo.JPEG", width_in=2.8, caption="The VRSI Duo prompt — “Are you logging in to Fortinet FortiGate SSL VPN?” Verify the details and tap Approve to complete the VPN-at-logon step.")
b.bullet("You are now signed in.")
b.callout(
    "INFO",
    "First domain login only. The VPN-at-logon flow (FortiClient sign-in "
    "plus the Duo approval) is required only for this first domain sign-in. Once "
    "it succeeds, the domain credentials are cached on the laptop, so the user "
    "logs in normally afterward without connecting to the VPN. The laptop does "
    "not have day-to-day access to the VRSI network — only reconnect the VPN if "
    "IT asks the user to perform a specific task."
)

b.page_break()

# ===========================================================================
# 9. QUICK REFERENCE CHECKLIST
# ===========================================================================
b.heading1("9.   Quick Reference Checklist")
b.bullet("Ventoy USB built (minimum 64 GB) with INOS ISO at root")
b.bullet("Secure Boot disabled in BIOS")
b.bullet("Booted from USB → SmartDeploy launched")
b.bullet("Allowed the 30-second wipe countdown")
b.bullet_rich([("Waited for ", False), ("DOMAIN JOIN", True), (" icon on desktop", False)])
b.bullet("FortiClient VPN connected + Duo approved")
b.bullet_rich([("Right-clicked ", False), ("DOMAIN JOIN", True), (" → Run as administrator", False)])
b.bullet_rich([("Entered unique PC name (", False), ("INOS-LAPT-###", True), (")", False)])
b.bullet("Rebooted after domain join")
b.bullet_rich([("Logged in via ", False), ("Other user", True), (" + FortiClient at logon screen", False)])
b.bullet("Duo approved → domain login successful")

# ===========================================================================
# 10. KNOWN ISSUES / NOTES
# ===========================================================================
b.heading1("10.  Known Issues / Notes")
b.bullet_rich([
    ("Auto-login to local VRSI user after reboot", True),
    (" — under investigation. Workaround: sign out, use Other user.", False),
])
b.bullet_rich([
    ("Duplicate PC names", True),
    (" cause domain join failure — always confirm the assigned number.", False),
])
b.bullet_rich([
    ("Boot / BIOS keys vary by model", True),
    (" — the keys for supported hardware (Dell: ", False),
    ("F2", True),
    (" for BIOS Setup, ", False),
    ("F12", True),
    (" for the boot menu; non-Dell: ", False),
    ("F12", True),
    (" / ", False),
    ("F11", True),
    (" / ", False),
    ("F9", True),
    (" / ", False),
    ("Esc", True),
    (") are documented in Phase 2. Confirm against the on-screen prompt at the brand splash screen.", False),
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
b.image("44_media.jpg", caption="Dell One-Time Boot Settings menu. Select the USB flash drive from the UEFI Boot Devices list to boot from Ventoy.")
b.paragraph("What you will see:")
b.bullet_rich([
    ("UEFI Boot Devices", True),
    (" — Windows Boot Manager, UEFI USB devices, UEFI network/PXE", False),
])
b.bullet_rich([
    ("Pre-Boot Tasks", True),
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
b.revision_history([
    ("05/29/2026", "1.0", "Initial Release", "BK"),
    ("05/29/2026", "1.1", "Standardized product name to INOS throughout; replaced non-English (German/Turkish) Ventoy screenshots with English equivalents", "BK"),
    ("05/29/2026", "1.2", "Inlined BIOS-entry and one-time-boot-menu key steps into Phase 2; replaced the generic Duo screenshot with the real VRSI FortiGate SSL VPN Duo prompt; clarified that domain credentials cache after the first login, so the VPN is not needed for later sign-ins", "BK"),
    ("06/01/2026", "1.3", "Builder script paths made portable (relative to script location); README and LICENSE added; repository published to GitHub (soakal/INOSDEPLOY, private)", "BK"),
])

out = b.save()
print(f"Saved: {out}")
