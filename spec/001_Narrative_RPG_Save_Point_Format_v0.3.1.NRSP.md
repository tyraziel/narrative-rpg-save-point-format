# Narrative_RPG_Save_Point_Format_v0.3.1.NRSP.md

**Narrative RPG Save Point Format – Specification v0.3.1**

The Narrative RPG Save Point Format (NRSP) defines a deterministic representation of a narrative state that can be reloaded to continue a story.

NRSP files are organized into named sections using Markdown headers. Section headers define the semantic meaning of the content that follows.

Subheadings within sections are optional unless otherwise specified.

This file format reflects the full modular vision of NRSP v0.3.1. Everything can be in one file, or split as needed.

---

## 💾 Header Metadata in YAML

Each `.NRSP.md` Save Point begins with a YAML frontmatter block that defines its identity and position within a narrative timeline.

| Field         | Required | Description |
|---------------|----------|-------------|
| Title         | ✅        | Human-readable name of the Save Point |
| PreviousSavePoint | ❌   | Optional filename of the immediately preceding Save Point |
| NextSavePoint     | ❌   | Optional filename of the subsequent Save Point |
| AlternateNext     | ❌   | Optional list of filenames representing alternate or forked next Save Points |
| TimelineType  | ❌        | Optional One of: `Mainline`, `Branch`, or `WhatIf` (defaults to `Mainline`) |
| ArcID         | ❌        | Optional identifier for the Save Point within a campaign or story |
| TimelineNote  | ❌        | Optional note describing timeline context or significance |
| SLD           | ❌        | Optional filename of an associated Session Log Document |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown
---
Title: The Conflict at the Broken Bridge
PreviousSavePoint: ArrivalAtGreyford.NRSP.md
NextSavePoint: CrossingTheRavine.NRSP.md
AlternateNext:
  - RetreatToTown.NRSP.md
  - NegotiateWithBandits.NRSP.md
TimelineType: Mainline
ArcID: GB-02
TimelineNote: First major player choice affecting regional control
SLD: Session_2025-03-14.SLD.md
---
```

### Minimal Example

```markdown
---
Title: The Conflict at the Broken Bridge
---
```

---

## 🗓 Narrative Context

The Narrative Context captures the distilled story state at this Save Point.

This section summarizes what matters going forward, such as major outcomes, unresolved threads, emotional shifts, and narrative consequences. It is intentionally concise and does not attempt to record everything that occurred during play.

Detailed moment-to-moment events, dialogue, and rolls SHOULD be captured in the associated Session Log Document (if present).

The structure of this section is intentionally flexible. Authors MAY use headings, bullet points, or prose as appropriate for their story.

### Example

```markdown
## Narrative Context

### Summary
The party confronted bandits controlling the Broken Bridge. After a tense standoff, negotiations failed and violence erupted. Control of the crossing is now uncertain, and word of the conflict is spreading to nearby settlements.

### Notable Moments
- The bridge captain was defeated but not killed
- One party member spared a fleeing bandit
- The bridge structure was damaged during the fight
```

### Minimal Example

```markdown
## Narrative Context

The party reached the Broken Bridge and learned it is controlled by hostile forces.
```

---

## 🧑‍🎤 Character Snapshots

Captures the state of characters at this Save Point.

This section MAY include player characters, companions, recurring NPCs, or other entities.

### Character Subsection

Character Snapshots MAY serve as the complete representation of a character if the author chooses not to maintain separate Character Sheet files.

Each Character defined in this section MUST start with a subsection in the form:
`### Character: [Name]`

This requirement does not apply when Characters are listed exclusively under a
`### Character Sheets` subsection.

If a Character Sheet is linked within an individual character’s subsection, it MUST be labeled in the form:
`Character Sheet: [Name].CS.md`

The structure of this section is intentionally flexible. Authors MAY include as much or as little detail as is necessary to convey character state.

This section MAY include tabular data to represent character stats, inventory, or other structured information.

### Character Sheets Subsection

Alternatively, Character Sheets MAY be listed collectively under a `### Character Sheets` subsection.

### NPC Sheet concept (no new section required)

Some characters MAY have an associated NPC Sheet (.NPC.md) containing extended or restricted details (e.g., secrets, hidden motives, future plot hooks, GM-only context).

NPC Sheets SHOULD NOT duplicate publicly observable details already present in the Character Sheet, except where repetition improves retrieval or reduces ambiguity.

NPC Sheet files (.NPC.md) MAY be linked from a character’s subsection.

If present, the link MUST be labeled in the form:
NPC Sheet: [Name].NPC.md

A character MAY link to both a Character Sheet and an NPC Sheet. In that case:

.CS.md is the shared/public-facing representation of the character.

.NPC.md is the extended/GM-orchestrator representation.

Alternatively, NPC Character Sheets MAY be listed collectively under a `### Character Sheets` subsection.

### Example

```markdown
## Character Snapshots

### Character: Elara
- Role: Reluctant leader
- Level: 3
- Current State: Wounded but resolute
- Notable Traits: Cautious, principled
- Inventory:
  - Broken signet ring
  - Healing draught (1 remaining)
  - The Black Thorn
- Key Relationships:
  - Tomas (trusted ally)
  - Captain Vorn (strained truce)

#### Core Stats
- WITS: 16
- LUCK: 14
- RESOLVE: 17
- EMPATHY: 11
- HP: 15 / 20

### Character Sheets
- Captain_Vorn.CS.md
- Tomas.CS.md
```

### Minimal Example

```markdown
## Character Snapshots

### Character: Elara
Injured during the bridge skirmish, but committed to seeing the party through.
```

### Linking Example

```markdown
## Character Snapshots

### Character: Elara
- Role: Reluctant leader
- Current State: Wounded but resolute
- Key Relationships:
  - Tomas (trusted ally)
  - Captain Vorn (strained truce)

Character Sheet: Elara_Post_Bridge.CS.md
```

### Only Character Sheets Example
```markdown
## Character Snapshots

### Character Sheets
- Elara_Post_Bridge.CS.md
- Captain_Vorn.CS.md
- Tomas.CS.md
```

### NPC Character Sheet Example

```markdown
## Character Snapshots

### Character: Captain Vorn
- Current State: Cooperative, but calculating
- Visible Disposition: Cold professionalism

Character Sheet: Captain_Vorn.CS.md
NPC Sheet: Captain_Vorn.NPC.md
```

### Only Character Sheets and NPCs Example
```markdown
## Character Snapshots

### Character Sheets
- Elara_Post_Bridge.CS.md
- Captain_Vorn.CS.md
- Captain_Vorn.NPC.md
- Tomas.CS.md
```

---

## 🧑‍🤝‍🧑 Party State

The Party State provides a consolidated, situational view of the active group at this Save Point.

Party State is OPTIONAL and MAY be omitted if the Character Snapshots sufficiently describe the current group state.

This section summarizes which characters are currently active, or otherwise unavailable, and captures group-level or comparative information relevant to the immediate narrative or gameplay context.

Party State is intentionally ephemeral and may change frequently between Save Points. It does not replace Character Snapshots or Character Sheets.

This section MAY include tabular data to represent comparative or group-scoped information such as party composition, readiness, formation, temporary conditions, or system-specific stats.

### Example

```markdown
## Party State

Elara and Tomas are traveling together under strain.

| Name   | Status   | Role in Party       | Condition              | Key Notes                                   |
|--------|----------|---------------------|------------------------|---------------------------------------------|
| Elara  | Active   | Reluctant Leader    | Wounded but resolute   | Carrying The Black Thorn; morale holding    |
| Tomas  | Active   | Trusted Ally        | Uninjured              | Defers to Elara’s judgment                  |
| Vorn   | Adjacent | Uneasy Associate    | Physically fit         | Truce in effect; trust remains fragile      |
```

### Minimal Example

```markdown
## Party State

Elara and Tomas are traveling together under strain. Captain Vorn remains nearby under a fragile truce.
```

---

## 🗺️ Location Snapshots

Captures the state of locations at this Save Point.

This section MAY include towns, cities, hubs, regions, planes, galaxies, worlds, or other locations.

### Location Subsection

Location Snapshots MAY serve as the complete representation of a location if the author chooses not to maintain separate Location files.

Each Location defined in this section MUST start with a subsection in the form:
`### Location: [Name]`

This requirement does not apply when Locations are listed exclusively under a
`### Location Sheets` subsection.

If a Location Sheet is linked within an individual location’s subsection, it MUST be labeled in the form:
`Location Sheet: [Name].L.md`

The structure of this section is intentionally flexible. Authors MAY include as much or as little detail as is necessary to convey location information and state.

This section MAY include tabular data to represent shops, taverns, governmental hierarchy, or other structured information.

### Location Sheets Subsection

Alternatively, Location Sheets MAY be listed collectively under a `### Location Sheets` subsection.


## 🔗 Linked Files

Linked Files is an OPTIONAL section and MAY serve as an additional section with a tabular format containing additional files not referenced elsewhere in the NSRP.

### Example

```markdown

## Linked Files

| File        | Notes                        |
|-------------|------------------------------|
| TBD         | TBD                          |
```

---


