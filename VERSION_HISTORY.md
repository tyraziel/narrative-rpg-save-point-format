# NRSP Format – Version History

This document outlines the official version history of the Narrative RPG Save Point Format (NRSP).

---

## License History

**2026-01-26**: Project relicensed from **CC BY 4.0** to **MIT License** to simplify usage, improve compatibility with software projects, and reduce attribution friction while maintaining credit to original creators.

---

## v0.4 – Major overhaul and specification definition (2025-12-17)

Version 0.4 defines the formal specifications of the NRSP and its companion file types, establishing stable, system-agnostic contracts for long-term use.

## v0.3 – Modular SaveFile Format (2025-03-27)

Version 0.3 introduces a fully modular, bundle-ready SavePoint format, designed to store not only narrative state but also timeline metadata, character sheets, team info, and related files. This version supersedes .NRSF.md and defines .NRSP.md as the canonical extension.

- Finalized `.NRSP.md` as the canonical file extension (deprecated `.NRSF.md`)
- Formalized modular file types: `.NRSP.md`, `.SLD.md`, `.CS.md`, `.T.md`, `.NPC.md`
- Unified SavePoint structure with metadata, player character state, party, NPCs, towns, and linked file references
- Added project scaffolding: `README.md`, `LICENSE.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`
- Format originally licensed under Creative Commons CC BY 4.0 (relicensed to MIT in 2026)

## v0.2 – Session Log and Timeline Prototype (2025-03-25)
- Recognized `.NRSF.md` alone was insufficient to reconstruct full narrative context
- Introduced the Session Log Document (`.SLD.md`) to augment SavePoint files
- Added SavePoint timeline linking: `PreviousArc`, `NextArc`, and `AlternateNext`
- Defined timeline types: `Mainline`, `Branch`, and `WhatIf`

## v0.1 – Hybrid Snapshot Format (2025-03-24)
- Combined player character, Pokémon party, and session summary into a unified markdown file
- Introduced optional fatigue system and structured stat blocks
- Used legacy `.NRSF.md` file extension (retroactively renamed to `.NRSP.md`)

## v0.0 – Conceptual Origin (2025-03-23)
- Created the first SavePoint snapshot for a trainer’s narrative state
- No formal file structure or metadata yet
- Established tone, emotional goals, and the foundational concept of “saving the narrative”

---

All versions prior to v1.0 are considered part of the evolving NRSP development process.
