#SLD


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
