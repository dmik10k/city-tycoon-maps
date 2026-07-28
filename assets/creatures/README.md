# Kids-view creature portraits (CDN)

This directory is published through jsDelivr. Keep one **square WebP** image per
`<archetype>_<state>.webp` here.

These render as the big-face creature portrait in the game's Kids-view Businesses
tab, replacing the hand-drawn SVG face for archetypes that have art here.

## How it works

- `archetypeForTier(tier)` (`server_logic`/`src/react` — five R&D-tier archetypes:
  tortoise, rabbit, fox, wolf, dragon) picks the archetype; the company's
  status/age picks the state.
- An archetype with no images here still renders using the original SVG-drawn
  face — this directory is additive, not a hard requirement.
- Run `npm test` from this repository before publishing so missing or invalid
  files are caught before the game requests them.
- Push the changed file to `main`; jsDelivr serves it from this repository.

## Format

- Format: **.webp** (lowercase `.webp` extension).
- Square, big-face portrait — **512×512** (2x from a 256 base, matches the
  `avatars/` convention). Rendered at whatever size the creature portrait column
  is (currently up to ~150px), scaled down client-side.
- Transparent or plain background; centered, front-facing, symmetrical pose —
  no accessories that could be mistaken for a UI element (see prompts used to
  generate the current set).

## States (5 per archetype)

- `happy` — status `healthy`
- `sad` — status `warning`
- `critical` — status `critical`
- `dead` — status `bankrupt`
- `elderly` — overrides happy/sad/critical (not dead) whenever the company is
  past its value-optimal reinvent age (`obsolescence.reinventOptimal ||
  reinventAdvised`) — "time to sell", independent of today's P&L.

## Required filenames (1 archetype so far — tortoise)

### tortoise (R&D tier 0 — Dividend/immortal companies)

- `tortoise_happy.webp`
- `tortoise_sad.webp`
- `tortoise_critical.webp`
- `tortoise_dead.webp`
- `tortoise_elderly.webp`

Not yet provided (still rendered via the SVG-drawn face): `rabbit`, `fox`,
`wolf`, `dragon`.
