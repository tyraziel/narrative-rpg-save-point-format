# Narrative_RPG_Location_Sheet_Format_v0.4.0.LS.md

**Narrative RPG Location Sheet – Specification v0.4.0**

The Location Sheet (LS) of the Narrative RPG Save Point Format (NRSP) is the detailed information and narrative state of a location with ongoing narrative significance.

Locations MAY evolve over time and multiple `.LS.md` files MAY exist for the same location to represent changes in state, role, or narrative phase.

LS files are organized into named sections using Markdown headers.  Section headers define the semantic meaning of the content that follows.  A LS MAY contain any number of named sections but MUST contain at least one named section to be valid.  A LS MAY describe the location in prose, bullet points, tables, or mixed formats.

Each Location Sheet MAY reference multiple Save Points.

When present, referenced Save Points indicate narrative states for which this Location Sheet is valid.

Subheadings within sections are optional unless otherwise specified.

The LS sections and subsections defined here are suggestions and MAY be extended by the author.

This file format reflects the modularity of NRSP v0.4.0 splitting out the Location Sheet.

---

## 💾 Header Metadata in YAML

Each `.L.md` Location MUST begin with a YAML frontmatter block that defines the location and the Save Points that it is a part of.

| Field | Required | Description |
|------|----------|-------------|
| Name | ✅ | Canonical name of the location |
| Type | ❌ | Optional one of: `Town`, `Village`, `World`, `Galaxy`, etc (defaults to `Town`) |
| GMSheet | ❌ | Optional filename of the LGM.md containing extended or restricted details |
| System | ❌ | Optional mechanical or narrative system used to interpret location information |
| IntroducedIn | ❌ | Optional filename of the Save Point or Module where the location first appears |
| CurrentAsOf | ❌ | Optional list of filenames of Save Points for which this Location Sheet is valid |
| Supersedes | ❌ | Optional filename of a prior Location Sheet this file replaces |
| SupersededBy | ❌ | Optional filename of a later Location Sheet that replaces this one |
| Status | ❌ | Optional narrative status (e.g., `Active`, `Missing`, `Deceased`, `Retired`) |
| Tags | ❌ | Optional list of semantic tags for categorization or retrieval |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown

```