# SOP Builder skill — installation

## What this folder is

The source files for the **SOP Builder** skill: `SKILL.md` (the prompt Claude reads) and `example_builder.py` (a syntax reference).

I couldn't write directly into your Cowork user-skills folder from this session — that path is locked. So they're staged here. Run `install.ps1` to copy them to the right place.

## Install

```powershell
cd "C:\Users\Deploy\Desktop\SOP Factory\sop-builder-skill"
.\install.ps1
```

The script tries these locations in order and uses the first one that exists:

1. `%USERPROFILE%\.claude\skills\` (most common)
2. `%APPDATA%\Claude\skills\`
3. `%USERPROFILE%\Documents\Claude\skills\`

If none of those work, the script prints manual instructions.

After install, **restart Cowork** (or start a new conversation) to pick up the skill.

## Verify it loaded

In a new Cowork conversation, ask: "what skills do you have available?" The list should include `sop-builder`.

Or just say "build the SOP" — if the skill is loaded, Claude will invoke it.

## Uninstall

Delete the `sop-builder` folder from whichever location `install.ps1` used.

## What the skill does

Drives the SOP Factory workflow end-to-end:

1. Confirms the SOP Factory path with you
2. Reads the VRSI formatting rules
3. Runs `prep_active.py` to number images + write the manifest
4. Reads each numbered image to understand its content
5. Asks you for title, version, author, filename
6. Generates a tailored builder script using `sop_lib.SOPBuilder`
7. Validates the docx
8. Renders pages and spot-checks
9. Hands you a `computer://` link

Trigger words: *"build the SOP"*, *"create an SOP"*, *"draft an SOP"*, *"use the SOP factory"*, *"turn this transcript into an SOP"*.
