"""
example_builder.py — Reference implementation for the SOP Builder skill.
Shows the call shapes for sop_lib.SOPBuilder. Use as syntax reference only —
each SOP needs its own builder script tailored to its content.
"""

import sys
from pathlib import Path

SOP_FACTORY = Path(r"C:\Users\Deploy\Desktop\SOP Factory")
sys.path.insert(0, str(SOP_FACTORY / "template"))
from sop_lib import SOPBuilder

sop = SOPBuilder(
    template_docx=SOP_FACTORY / "template" / "SOP_TEMPLATE_WITH_PHOTOS.docx",
    output_docx=SOP_FACTORY / "output" / "Example_v1.0.docx",
    active_dir=SOP_FACTORY / "active",
    revision="1.0",
    date="05/03/2026",
)

sop.title_page(
    "GOCATOR SENSOR TEST", "&", "LICENSE ACTIVATION",
    subtitle="Gocator 3210 / inos Station — VRSI Procedure",
    doc_no="SOP-GOCAT-INOS-001",
    author="BK (Brian Kalsic)",
)

sop.toc([
    "1.  Overview",
    "2.  Hardware & Connections",
    "      A)  Sensor Unit",
    "      B)  Cable Identification",
    "3.  Sensor Functionality Test",
    "      A)  Launch Accelerator",
    "      B)  Set Voltage to 24V",
    "      C)  Verify Firmware",
    "      D)  Snapshot Test",
    "      E)  Restore Voltage to 48V",
    "4.  License Assignment in Maestro",
    "5.  Revision History",
])

sop.heading1("1.   Overview")
sop.paragraph("This document covers the procedure for ...")

sop.heading1("2.   Hardware & Connections")
sop.heading2("A)   Sensor Unit")
sop.bullet("Inspect the sensor body for damage")
sop.bullet_rich([("Confirm part number reads ", False), ("3100-8640-090-07", True)])
sop.bullet("Voltage flag", system_only="Test Cabinet Only")
sop.image("18_img_2988.jpg", caption="Cable label", width_in=3.5)

sop.heading2("B)   Cable Identification")
sop.bullet("Locate the white VRSI label")
sop.placeholder("Photo of cable connector seated in port")

sop.page_break()

sop.heading1("3.   Sensor Functionality Test")
sop.heading2("A)   Launch Accelerator")
sop.bullet_rich([("Open ", False), ("Gocator Inos License", True),
                 (" folder, double-click ", False), ("Gocator Accelerator", True)])
sop.image("13_accelerator.png", caption="Accelerator dialog showing Online status",
          width_in=3.2)

# ... continue similarly for other sections

sop.heading1("5.   Revision History")
sop.revision_history([("05/03/2026", "1.0", "First Draft", "BK")])

out = sop.save()
print(f"Saved: {out}")
