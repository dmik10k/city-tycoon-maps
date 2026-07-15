# City Tycoon content CDN

Public maps and static image assets for Mint Street. GitHub is the source and
jsDelivr serves the files from:

`https://cdn.jsdelivr.net/gh/dmik10k/city-tycoon-maps@main/`

## Layout

- `registry.json` and `maps/` — downloadable game maps
- `assets/avatars/` — built-in player avatars
- `assets/buildings/companies/` — company-card artwork
- `assets/buildings/walls/` — daytime facade textures
- `assets/buildings/walls_lit/` — night facade variants
- `assets/tutorial/` — tutorial guide portraits
- `assets/branding/` — logo, favicons, social icon, and editor showcase

Run `npm test` before pushing. The test checks all expected image families and
validates PNG, ICO, and WebP file signatures.
