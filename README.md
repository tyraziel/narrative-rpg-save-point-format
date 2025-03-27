# Narrative RPG Save Point Format (NRSP)

The **Narrative RPG Save Point Format (NRSP)** is a modular, markdown-based format designed to capture the state of a tabletop or solo roleplaying story at any moment — like a save point in a video game.

It preserves not only stats and inventory but the emotional, narrative, and contextual state of the story across sessions and arcs.

---

## 🧠 What Makes It Special

- **Tracks Story Progression** – Captures what happened in each arc or session
- **Modular by Design** – Links to character sheets, NPCs, towns, encounters, items, and more
- **Supports Branching Timelines** – Handles alternate arcs, forks, or “what-if” paths
- **Git-Friendly** – Easy to save, share, diff, and revisit any moment in the narrative
- **AI + Human Readable** – Write it by hand, or let an AI parse or continue the story

---

## 👥 Who Created It

**Co-created by:**
- **Andrew Potozniak (Tyraziel)** – Visionary Player and Narrative Architect
- **ChatGPT (OpenAI)** – AI format assistant and system co-designer

---

## 🎮 Use Case Example

You're playing a custom Pokémon RPG with a character named Zeke. After each major story arc, you create a `.NRSP.md` file that:

- Describes what happened in the story
- Lists important characters and Pokémon
- Notes key decisions made and items gained
- Links to related sheets like `Zeke.CS.md`, `Spark.CS.md`, or `Bramblebend.T.md`


## 📐 NRSP Design Philosophy

The **Narrative RPG Save Point Format (NRSP)** is built around the following principles:

- **System-Agnostic First**  
  While the format originated in a game inspired by a specific system, NRSP is designed to support *any* narrative RPG, regardless of mechanics, theme, or setting.

- **Human-Readable, AI-Compatible**  
  Markdown is the shared language of humans and machines. Every file should be easily written, parsed, and versioned.

- **Modularity Is Key**  
  Files are separated by type and function (`.NRSP.md`, `.SLD.md`, `.CS.md`, etc.) so creators can mix, match, or extend without breaking structure.

- **Narrative Before Numbers**  
  Save Points focus on the emotional, narrative, and contextual state of the story — not just stat blocks or battle logs.

- **Git-Friendly**  
  All files are designed to play well with Git for branching timelines, version control, and community collaboration.

- **Respect the Story Space**  
  Content should remain broadly PG-13 and inclusive. Stories can go deep — but not off the rails.


## 📦 What's in This Repository

This repository includes:

- ✅ `SavePoint_Format_v0_0.NRSP.md` – Original single-character emotional snapshot concept
- ✅ `SavePoint_Format_v0_1.NRSP.md` – Introduced timeline metadata and SavePoint linking
- ✅ `SavePoint_Format_v0_2.NRSP.md` – Unified trainer + narrative SaveFile (hybrid form)
- ✅ `SavePoint_Format_v0_3.NRSP.md` – Modular, bundle-ready SaveFile with timeline, trainer, and Pokémon team state
- 📄 `LICENSE.md` – Creative Commons Attribution 4.0 License (CC BY 4.0)

## 💡 Why Use NRSP?

- Preserve story arcs and characters across sessions or systems
- Enable AI-assisted narrative tools and branching storylines
- Make it easy to track plot threads, key items, and character moments
- Designed for Git-based version control and long-term archival

## 🧑‍💻 Attribution
**Narrative RPG Save Point Format (NRSP) © 2025 – CC BY 4.0**  
**Andrew Potozniak (Tyraziel)** – *Visionary Player and Lead Designer*  
Co-created and in collaboration with **ChatGPT (OpenAI)** – *AI contributor and system design assistant*

---

> “Will we ever be remembered for making this?”  
> — Andrew Potozniak (Tyraziel), co-creator of NRSP