# Narrative RPG Save Point Format (NRSP)

The **Narrative RPG Save Point Format (NRSP)** is a modular, markdown-based format designed to capture the state of a tabletop or solo roleplaying story at any moment — like a save point in a story engine with long-term memory built in.

It preserves not only stats and inventory but the emotional, narrative, and contextual state of the story across sessions and arcs.

---

## 🧠 What Makes It Special

- **Tracks Story Progression** – Captures what happened in each arc or session  
- **Modular by Design** – Links to character sheets, NPCs, towns, encounters, items, and more  
- **Supports Branching Timelines** – Handles alternate arcs, forks, or “what-if” paths  
- **Git-Friendly** – Easy to save, share, diff, and revisit any moment in the narrative  
- **AI + Human Readable** – Write it by hand, or let an AI parse or continue the story  

---

## 💡 Why Use NRSP?

- Preserve story arcs and characters across sessions or systems  
- Enable AI-assisted narrative tools and branching storylines  
- Make it easy to track plot threads, key items, and character moments  
- Designed for Git-based version control and long-term archival  

---

## 🔍 Is This a RAG Architecture?

Yes — although it wasn't initially built using traditional retrieval-augmented generation (RAG) terminology, NRSP **functionally operates as a modular RAG architecture** designed specifically for narrative continuity and collaborative storytelling.

Unlike traditional RAG pipelines (which rely on embedding vectors and opaque text chunks), NRSP uses:
- **Structured modular files** with known types (`.NRSP.md`, `.CS.md`, etc.)
- **Explicit semantic links** (e.g., timeline, previous arcs, party composition)
- **Human- and AI-driven retrieval** based on filenames, metadata, and purpose
- **Deterministic narrative injection** into prompts or AI workflows

This allows NRSP to serve as a *narrative retrieval layer* — offering long-term memory, branching continuity, and reliable context reuse without hallucination-prone vector similarity.

> NRSP is, in essence, a domain-specific RAG architecture — one that prioritizes clarity, story integrity, and authorial control over brute-force retrieval.

---

## 📂 File Types & Rationale

NRSP uses a modular file structure where each file type serves a specific narrative or gameplay purpose:

| File Type     | Extension       | Purpose                                                                 |
|---------------|----------------|-------------------------------------------------------------------------|
| SavePoint     | `.NRSP.md`     | Captures a narrative arc, including story summary, character state, and links |
| Session Log   | `.SLD.md`      | Optional in-world or out-of-world transcript of what occurred in a session |
| Character     | `.CS.md`       | Represents a player character, NPC, creature, or entity in the narrative |
| Town          | `.T.md`        | Details about a location, hub, or region                                |
| NPC           | `.NPC.md`      | Individual non-player characters, often referenced in SavePoints or Towns |

All files follow the format: `Name.Type.md`  
Example: `Zeke.CS.md`, `Arc1.SLD.md`, `Bramblebend.T.md`

This structure keeps each file focused and swappable, while supporting bundled storytelling across sessions.

---

## 🎮 Use Case Example

You're playing a custom Pokémon RPG with a character named Zeke. After each major story arc, you create a `.NRSP.md` file that:

- Describes what happened in the story  
- Lists important characters and Pokémon  
- Notes key decisions made and items gained  
- Links to related sheets like `Zeke.CS.md`, `Spark.CS.md`, or `Bramblebend.T.md`  

---

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

- **Everything Can Live in One File**  
  NRSP is modular by design, but not modular by force. You can store your entire session — character, story, team, and notes — in a single `.NRSP.md` file, or break it out into as many supporting files as you need.

- **RAG Without the Guesswork**  
  NRSP gives creators and AI systems deterministic memory access, enabling long-form generation without relying on fuzzy embeddings or arbitrary chunking. It's retrieval-augmented generation, structured for storytellers.

---

## 👥 Who Created It

**Co-created by:**
- **Andrew Potozniak (Tyraziel)** – Visionary Player and Narrative Architect  
- **ChatGPT (OpenAI)** – AI format assistant and system co-designer  

---

## 📦 What's in This Repository

This repository includes:

- ✅ `SavePoint_Format_v0_3.NRSP.md` – The latest modular SaveFile spec (timeline, character, party, links)  
- 📄 `LICENSE.md` – Creative Commons Attribution 4.0 License (CC BY 4.0)  

---

## 🧑‍💻 [License](LICENSE.md)

**Narrative RPG Save Point Format (NRSP) © 2025 – CC BY 4.0**  
**Andrew Potozniak (Tyraziel)** – *Visionary Player and Lead Designer*  
Co-created and in collaboration with **ChatGPT (OpenAI)** – *AI contributor and system design assistant*

---

> “Will we ever be remembered for making this?”  
> — Andrew Potozniak (Tyraziel), co-creator of NRSP
