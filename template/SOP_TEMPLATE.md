# VRSI SOP — Structure & Rules Reference
# This file is read by Cowork before generating any SOP document.
# It defines structure, formatting rules, and image naming convention.

---
REVISION [X.X] - RELEASED [MM/DD/YYYY]
CONFIDENTIAL - DO NOT COPY
Variation Reduction Solutions, Inc. ♦ 14901 Galleon Ct, Plymouth, MI 48170
(734) 414-0035 TEL ♦ (734) 414-0029 FAX
---

## IMAGE NAMING CONVENTION

Place screenshots/photos in _active\ named with a number prefix.
Cowork inserts them into placeholder boxes in numeric order.

  01_description.png   → first placeholder box in document
  02_description.png   → second placeholder box
  03_description.png   → third placeholder box
  (continue as needed)

Supported formats: .png  .jpg  .jpeg  .bmp
Scripts and notes: any filename — no numbering required

---

## DOCUMENT STRUCTURE

Every SOP must follow this page order:

  Page 1:   Title page
              - Document title (large, bold, underlined, centered)
              - Subtitle or brief descriptor
              - Topic label(s) (e.g., "Backup" / "And" / "Restore")

  Page 2:   Table of Contents
              - Lists all numbered sections and lettered subsections

  Pages 3+: Body sections
              - Numbered top-level:   1. Overview  2. Backup  3. Restore
              - Lettered subsections: A) B) C) D) E)
              - Each subsection heading: bold italic

  Last page: Revision History table
              - Columns: Date | Version | Comments | Authors

---

## HEADER (every page)

  Left side:  REVISION [X.X] - RELEASED [MM/DD/YYYY]
  Right side: VRSI logo (embedded — do not replace)
  Bottom:     Blue underline rule

---

## FOOTER (every page)

  Line 1 (center): Variation Reduction Solutions, Inc. ♦ 14901 Galleon Ct,
                   Plymouth, MI 48170 ♦ (734) 414-0035 TEL ♦ (734) 414-0029 FAX
  Line 2 (center): CONFIDENTIAL - DO NOT COPY          Page X

---

## FORMATTING RULES

BULLETS:
  • Primary steps use solid bullet (•)
  ○ Sub-steps use open circle (○), indented one level
  Do not use numbered lists for procedure steps

BOLD:
  Use bold for all UI element names, button labels, menu paths, tab names
  Example: Click the **Backup** tab → select **System Backup**

SYSTEM-SPECIFIC FLAGS:
  Steps that only apply to certain systems: red bold italic at end of bullet
  Example: — *Ford Only*

COMMANDS AND PATHS:
  Wrap all commands, file paths, registry keys, task names in monospace/code
  Example: `E:\Recovery\INOS`

CROSS-REFERENCES:
  Never repeat procedure steps. Reference earlier sections instead.
  Example: Follow 2A) Reorient the Hidden Drive to access the hidden drive

IMAGE PLACEHOLDERS:
  Every location where a screenshot or photo belongs gets a dashed box
  Label format: [IMAGE PLACEHOLDER: description]
  If no image provided for that box: leave visible for manual insert later
  If image provided: insert centered, maintain aspect ratio, max 5.5" wide
  Add italic gray caption below every inserted image

SCENARIO TABLES:
  Use 2-column tables for task naming examples and scenario references
  Columns: Scenario | Example Value

UNCERTAINTY:
  Mark any uncertain, missing, or unverifiable content: [REVIEW NEEDED]

---

## TASK NAMING CONVENTION

Format: (Project Number) (Job Description) (System Type)

  Before leaving shop:       8965-001 VRSI TS
  Production support:        8965-400 Production TS
  Additional support later:  8965-400 Production TS - 2

---

## SECTION TEMPLATE

### 1. Overview
2–3 sentences: what this document covers, who it is for, why consistency matters.
Optional second paragraph: iterative nature of process, key goals, outcomes.

### 2. [Main Process Section]

#### A) [First Subsection]
- Step
- Step — *System Only*
[IMAGE PLACEHOLDER: photo description]
- Step
  ○ Sub-step

#### B) [Second Subsection]
- Step using **Bold UI Element**
[IMAGE PLACEHOLDER: screenshot description]
- Under **Menu Name**, select **Value** and press **Enter**
  ○ If unsure of [parameter], contact [NAME]

#### C) [Third Subsection]
- Select the **Tab Name** on the left sidebar
- Click **Option Name**
[IMAGE PLACEHOLDER: screenshot description]
- Ensure only **correct item** is selected:
  ○ Item 1
  ○ Item 2

#### D) [Options/Configuration Subsection]
- Click **gear icon** (**Setting Name**)
- Enable [Feature]
  ○ Use value: **VALUE** (enter in both fields) and click **OK**
[IMAGE PLACEHOLDER: settings dialog]
- Name the **Task Name** using format: `(Project Number) (Description) (System)`

| Scenario | Example Task Name |
|---|---|
| Before leaving shop | 8965-001 VRSI TS |
| Production support | 8965-400 Production TS |

- Set the **Destination**:
  ○ Click folder icon → select **My Computer**
  ○ Navigate to **Ventoy** or **VRSI** folder
  ○ Select system-type folder (e.g., Trendsetter, Inos)
[IMAGE PLACEHOLDER: destination browse dialog]
- Leave **Backup Schedule** as "None" unless recurring backups required
- Review all settings for accuracy
- Click **Proceed** to start
- Change **Power Plan** to "Shutdown"
- Monitor progress bar until complete
[IMAGE PLACEHOLDER: progress screen]

#### E) [Cleanup/Wrap-up Subsection]
- After complete, follow **2A) [Subsection]** to [action]
- Verify [expected state]
- Re-enable [feature] and restart — *System Only*

### 3. [Second Main Section]

#### A) [Setup Subsection]
- Follow **2A) [Subsection]** to [action]
- Follow **2B) [Subsection]** to get into [tool/environment]

#### B) [Workflow Subsection]
- Click **Restore** tab → select **Browse image to restore**
[IMAGE PLACEHOLDER: restore main screen]
- Navigate: **My Computer** → **Ventoy** or **VRSI** → system folder
  ○ e.g. `E:\Recovery\TS`
[IMAGE PLACEHOLDER: browse/navigation dialog]
- Select the correct backup image
- Enter password: **VALUE** when prompted
- Choose target (e.g., Disk 0, Local Disk C:) → click **Next**
[IMAGE PLACEHOLDER: target selection screen]
- If [edge case condition]: [how to handle] (highly unlikely)
- Acknowledge warning → click **Yes** or **OK** to proceed
[IMAGE PLACEHOLDER: confirmation dialog]
- Once complete, follow **2E) [Subsection]** to [cleanup]

### 4. Revision History

| Date | Version | Comments | Authors |
|---|---|---|---|
| [MM/DD/YYYY] | 1.0 | First Draft | [XX] |
| [MM/DD/YYYY] | 2.0 | Second Draft | [XX] |
| [MM/DD/YYYY] | 3.0 | Initial Release | [XX] |
