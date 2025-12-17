# Narrative_RPG_Character_Sheet_Format_v0.4.0.CS.md

**Narrative RPG Character Sheet – Specification v0.4.0**

The Character Sheet (CS) of the Narrative RPG Save Point Format (NRSP) is the detailed identity and narrative state of a player character, companion, recurring non-player character (NPC) or a non-player entity with ongoing narrative significance.

Character Sheets MAY evolve over time and multiple `.CS.md` files MAY exist for the same character to represent changes in state, role, or narrative phase.

CS files are organized into named sections using Markdown headers.  Section headers define the semantic meaning of the content that follows.  A CS MAY contain any number of named sections but MUST contain at least one named section to be valid.  A CS MAY describe the character in prose, bullet points, tables, or mixed formats.

Each Character Sheet MAY reference multiple Save Points.

When present, referenced Save Points indicate narrative states for which this Character Sheet is valid.

Subheadings within sections are optional unless otherwise specified.

The CS sections and subsections defined here are suggestions and MAY be extended by the author.

This file format reflects the modularity of NRSP v0.4.0 splitting out the Character Sheet.

---

## 💾 Header Metadata in YAML

Each `.CS.md` Character Sheet MUST begin with a YAML frontmatter block that defines the character’s identity, lineage and the Save Points that it is a part of.

| Field | Required | Description |
|------|----------|-------------|
| Name | ✅ | Canonical name of the character |
| Type | ❌ | Optional one of: `PC`, `Companion`, `NPC`, `Entity` (defaults to `PC`) |
| IntroducedIn | ❌ | Optional filename of the Save Point or Module where the character first appears |
| CurrentAsOf | ❌ | Optional list of filenames of Save Points for which this Character Sheet is valid |
| Supersedes | ❌ | Optional filename of a prior Character Sheet this file replaces |
| SupersededBy | ❌ | Optional filename of a later Character Sheet that replaces this one |
| Status | ❌ | Optional narrative status (e.g., `Active`, `Missing`, `Deceased`, `Retired`) |
| Tags | ❌ | Optional list of semantic tags for categorization or retrieval |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown
---
Name: Elara Vance
Type: PC
IntroducedIn: Arrival_At_FortTier.NRSP.md
CurrentAsOf: The_Day_The_Gears_Fell_Silent.NRSP.md
Status: Active
Tags:
  - Leader
  - Strategist
---
