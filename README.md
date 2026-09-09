# Finding No-No-Namosh II: The Lost Star

A browser adventure game — sequel to *Finding No-No-Namosh*. Single-file,
no build tools, no server, runs directly in any modern browser (desktop +
mobile/iPhone).

## ⚠️ What this build actually is

This is a **real, playable first chapter**, not a design doc and not a
static demo screen. Everything in it runs: movement, dialogue with
portraits, an interactive apartment intro, a town and valley to explore,
swimming, a water-level dungeon puzzle, a boss fight, inventory, save/load
(3 slots, localStorage), a full English/Swedish language toggle, original
procedural chiptune music/SFX (Web Audio API, no external files, no
copyrighted assets), and desktop + touch controls.

It is **not** the full 15-region, multi-boss, fully-voiced epic described
in the original brief — that is a genuinely large, multi-month scope (original
music per region, hand-animated sprite sheets, ~15 maps, 5+ bosses, full
postgame, full bilingual script for all of it). Building all of that as one
finished, tested deliverable isn't realistic in a single pass, so rather than
hand you an unfinished shell or a document describing what *would* be built,
this delivers one complete, working slice of the real game, built on the
architecture the full game would use — so every following session adds real,
playable regions on top of a foundation that already works end to end.

### What's playable right now
- **Apartment intro**: pet/interact with objects, meet the kittens, discover
  one is missing, the storm scene, the door opens on wet paw prints.
- **Rosewood** (town hub) and **Greenhaven Valley** (overworld, NPCs with
  clues, a pond).
- **Crystalwater Grotto**: a real water-level dungeon puzzle (pull the
  floodgate lever to raise/lower water and reach new areas), ending in a
  boss fight against the **Grotto Guardian** (dodge its telegraphed attack,
  strike back with E).
- Swimming (walk into water, it visibly behaves like water).
- Inventory system, item pickups, quest-state–aware NPCs.
- Save/Continue across 3 slots, autosave every 45s during play.
- Full English ⇄ Swedish toggle (title screen + Options), including all
  dialogue and objectives in this chapter.
- Desktop controls (WASD/Arrows, E interact, B ability, I inventory) and
  a touch D-pad + buttons for mobile/iPhone.

### Art
`assets/` contains the source PNGs and `gen_art.py`, the generator that
produced them, for future editing. **`index.html` itself has the art
embedded as base64** — it no longer depends on `assets/` being present at
runtime. That fixes a real bug from an earlier build: opening the
standalone `index.html` without its `assets` folder alongside it caused
the sprite images to fail to load silently, which crashed the render loop
and produced a black screen. Embedding the art removes that failure mode
entirely — the file is now truly standalone, verified by an actual
headless-browser run (not just inspection).

Every sprite is a pixel grid authored in `gen_art.py`, auto-outlined (the
standard pixel-art silhouette technique) and upscaled with nearest-neighbor
so it stays crisp. Aya has a 4-direction, 4-frame walk cycle; Namosh has a
matching 4-direction walk cycle; the tileset covers grass (2 texture
variants), animated water, path, wall, wood floor, sand, animated crystal
water, grotto floor, fence, rug, dark stone, and a door tile. Run
`python3 gen_art.py` (needs Pillow) to regenerate or extend them, then
re-embed the output as base64 into `index.html` — it's the fastest way to
add more sprites (NPCs, Abdullah, Dr. Meow Skuttan, Mr. Fox) using the same
pipeline.
This is genuinely better than solid-color placeholders, but it is
code-authored pixel art, not the work of a trained pixel artist — if you
want Pokémon/Nintendo-tier art, swapping in artist-made sprite sheets of
the same dimensions (and re-embedding as base64, or switching the loader
back to file paths) will work with no other code changes.

### What's next (not yet built)
The Great River, Azure Coast, boat sailing, Emerald Canopy climbing, Echo
Mountain, Hollow Mountain mine carts, Temple of the Winds, Ashfall Valley,
Mount Qamar, the Star Chamber, the playable-Namosh finale, postgame and the
Moon Vault. The engine (scene system, dialogue, inventory, save system,
localization, procedural audio) is already built to support all of these —
each region is now a matter of building its map, NPCs, and story beats on
top of it.

## Running it
Just open `index.html` in a browser, or deploy the whole folder to GitHub
Pages (Settings → Pages → deploy from this branch/folder). No build step,
no npm install, no server required.

## Controls
| Action | Desktop | Mobile |
|---|---|---|
| Move | WASD / Arrow keys | On-screen D-pad |
| Interact / Attack | E | Round "E" button |
| Ability | B | Round "B" button |
| Inventory | I | Satchel icon (top-right) |
| Advance dialogue | Space / click box | Tap dialogue box |

## Tech notes
- Pure HTML5 Canvas 2D, vanilla JS, no frameworks or external dependencies.
- All art is drawn procedurally (pixel rectangles) directly in code — no
  copyrighted or ripped assets of any kind.
- All music/SFX are generated at runtime via the Web Audio API — original
  chiptune-style melodies, no copyrighted audio.
- Save data lives in `localStorage` under `nonamosh2_slot_1/2/3`.
