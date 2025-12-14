# Narrative_RPG_Save_Point_Format_v0.3.1.NRSP.md

**Narrative RPG Save Point Format – Specification v0.3.1**

The Narrative RPG Save Point Format (NRSP) defines a deterministic representation of a narrative state that can be reloaded to continue a story.

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

## 🧑‍🎤 Player Character Snapshots

A concise summary of the PCs' state(s) at this SavePoint.

```markdown
### Trainer: Zeke
- Role: Wildcard Wrestler
- Trait Focus: Grit / Chaos
- Notable Personality: Impulsive, showy, loyal to team
- Inventory:
  - Emberheart (intact)
  - Poké Balls ×3
  - Custom sunglasses (from Suds)
- Key Bonds:
  - Spark (Ride-or-die)
  - Blaze (Trusted protector)
  - Suds (Snack-stick MVP)

#### Core Stats
- Grit: 4
- Resolve: 2
- Empathy: 2
- Smarts: 1
- Command: 3
- HP (optional): 5
```

---

## Party State

Use a table to summarize active and benched party members, including traits and key moves.

```markdown
| Name     | Role             | Trait       | Signature Move         | G | R | E | S | HP | Bond Level | Notes                       |
|----------|------------------|-------------|-------------------------|---|---|---|---|----|-------------|-----------------------------|
| Spark    | Ride-or-die      | Echo Bond   | Electro Dash           | 4 | 2 | 2 | 3 | 2  | Core + Echo | Spark Cutter originator     |
| Blaze    | Protector        | Blaze Bomb  | White Flame Blaze Bomb | 3 | 3 | 2 | 4 | 2  | Core        | Arsonist and volleyballer   |
| Suds     | Comic Relief     | Fastball    | Stick Slam Combo       | 3 | 2 | 5 | 2 | 5  | Core        | Noodle champ                |
```

Stat columns (Grit, Resolve, etc.) can be customized to your system.

---



## 🔗 Linked Files

SavePoints link to modular companion files using a standardized structure.

| File Type   | Suggested File Name          |
|-------------|------------------------------|
| Session Log | EmberwoodMystery.SLD.md      |
| Trainer     | Zeke.CS.md                   |
| Pokémon     | Spark.CS.md, Blaze.CS.md     |
| Town Sheet  | Bramblebend.T.md             |
| NPCs        | Reina.NPC.md, Milo.NPC.md    |

---

This file format reflects the full modular vision of NRSP v0.3.1. Everything can be in one file, or split as needed.

## Session Log Document (SLD)

An SLD (.SLD.md) is the detailed, chronological record of what happened during play.

Think of the SLD as the: transcript, play notes, rolls, dialogue, decisions, moment-to-moment events.

### How the SLD relates to the NRSP:
- SLD = "What Happened"
- NRSP = "What matters going forward"

The NRSP might refer to an SLD, but is not a replacement for the SLD.

Typical relationship:

You play a session → notes/transcript go into an SLD
At a natural break (arc end, major decision) → you create an NRSP SavePoint
The SavePoint links to the SLD for full detail, but only carries distilled state

Why this separation matters:

Keeps SavePoints concise and reloadable
Prevents token bloat
Preserves full history without forcing it into context

Mirrors code:
SLD = commit history, NRSP = tagged release
