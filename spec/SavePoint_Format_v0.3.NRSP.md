# SavePoint_Format_v0_3.NRSP.md

**Narrative RPG Save Point Format – Specification v0.3**

Version 0.3 introduces a fully modular, bundle-ready SavePoint format, designed to store not only narrative state but also timeline metadata, character sheets, team info, and related files. This version supersedes `.NRSF.md` and defines `.NRSP.md` as the canonical extension.

---

## 💾 Header Metadata (Frontmatter)

Each `.NRSP.md` SavePoint begins with a set of YAML-style key-value pairs:

```markdown
Title: Emberwood Mystery
PreviousArc: null
NextArc: TrialOfMemories.NRSP.md
AlternateNext:
  - EmberFestivalAlt.NRSP.md
TimelineType: Mainline
ArcID: EW01
TimelineNote: First successful trust trial with a Legendary
SLD: EmberwoodMystery.SLD.md
```

### Field Breakdown

| Field         | Required | Description |
|---------------|----------|-------------|
| Title         | ✅        | Human-readable name of the arc or session |
| PreviousArc   | ❌        | Filename of the prior SavePoint |
| NextArc       | ❌        | Filename of the next SavePoint |
| AlternateNext | ❌        | List of alternate or forked SavePoints |
| TimelineType  | ❌        | Mainline (default), Branch, or WhatIf |
| ArcID         | ❌        | Optional unique arc identifier |
| TimelineNote  | ❌        | Freeform note about story context |
| SLD           | ❌        | Session Log Document filename (if used) |

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

## 🗓 Narrative Context

```markdown
### Summary:
Zeke has just won the Ember Cup. Trust with Suicune is established. Zapdos rumors begin.

### Notable Moments:
- Spark Cutter with Emberheart
- Blaze Bomb aerial KO
- Fastball Special → Blaze
- Suicune's test of stillness
```

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

This file format reflects the full modular vision of NRSP v0.3. Everything can be in one file — or split as needed.
