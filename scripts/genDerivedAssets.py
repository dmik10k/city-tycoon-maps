#!/usr/bin/env python3
"""Generate the derived (small) image variants the game actually displays.

Two families, both idempotent — a variant is only rebuilt when it is missing or
older than its source, so re-running this is cheap.

1. Company card thumbnails
   assets/buildings/companies/<id>.webp   (1774x887, ~210 KB)
     -> assets/buildings/companies/thumb/<id>.webp   (800x400, ~35 KB)

   The card tile in the game renders at roughly 360 CSS px wide, so 800 px
   covers a 2x display. The full-size original is still shipped and is fetched
   only when the player clicks a card open into the lightbox.

     -> assets/buildings/companies/mini/<id>.webp    (240x120, ~5 KB)

   The "Find a business" album shows every company at once as a ~90 CSS px card.
   A decoded 800x400 thumb is ~1.3 MB of memory, so 193 of them (~250 MB) would
   blow a phone's whole budget; the mini is ~115 KB decoded (~22 MB for all).

2b. Building-side textures, small
   assets/buildings/walls/<category>.webp  (1254x1254, the map's facade tiles)
     -> assets/buildings/walls/small/<category>.webp  (512x512)

   The album tiles a category's facade behind its page at ~150 CSS px a tile.
   A 1254px texture decodes to ~6 MB for that; 512px is ~1 MB and still sharp.

2. Tutorial guide portraits
   assets/tutorial/guide-<pose>.png  (RGBA PNG, 107-152 KB)
     -> assets/tutorial/guide-<pose>.webp

   These are NOT resized: they are already small (~270x420) and the CSS renders
   them up to 340 px tall, so there is no spare resolution to give away. The win
   here is purely the format - RGBA PNG is a poor fit for soft-shaded artwork.

Usage:
    python3 scripts/genDerivedAssets.py [--force] [--quality N]

Requires Pillow (no cwebp/sips-webp on the build machine).
"""

import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python3 -m pip install Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

COMPANIES_DIR = os.path.join(ASSETS, "buildings", "companies")
THUMB_DIR = os.path.join(COMPANIES_DIR, "thumb")
MINI_DIR = os.path.join(COMPANIES_DIR, "mini")
WALLS_DIR = os.path.join(ASSETS, "buildings", "walls")
WALLS_SMALL_DIR = os.path.join(WALLS_DIR, "small")
TUTORIAL_DIR = os.path.join(ASSETS, "tutorial")
STREET_ACTIONS_DIR = os.path.join(ASSETS, "street", "actions")
STREET_MASTERS_DIR = os.path.join(STREET_ACTIONS_DIR, "masters")
STREET_SMALL_DIR = os.path.join(STREET_ACTIONS_DIR, "small")

THUMB_WIDTH = 800
MINI_WIDTH = 240


def is_stale(source, target, force):
    """True when the target needs (re)building."""
    if force or not os.path.exists(target):
        return True
    return os.path.getmtime(source) > os.path.getmtime(target)


def human(num_bytes):
    return f"{num_bytes / 1024:.0f} KB"


def build_company_thumbs(quality, force, out_dir=THUMB_DIR, width=THUMB_WIDTH, label="thumbs"):
    os.makedirs(out_dir, exist_ok=True)
    sources = sorted(f for f in os.listdir(COMPANIES_DIR) if f.endswith(".webp"))

    built = skipped = 0
    src_bytes = out_bytes = 0

    for name in sources:
        source = os.path.join(COMPANIES_DIR, name)
        target = os.path.join(out_dir, name)
        src_bytes += os.path.getsize(source)

        if not is_stale(source, target, force):
            out_bytes += os.path.getsize(target)
            skipped += 1
            continue

        with Image.open(source) as im:
            im = im.convert("RGB")
            height = max(1, round(im.height * width / im.width))
            im = im.resize((width, height), Image.LANCZOS)
            im.save(target, "WEBP", quality=quality, method=6)

        out_bytes += os.path.getsize(target)
        built += 1

    print(
        f"companies: {built} built, {skipped} up to date "
        f"({len(sources)} total) — {human(src_bytes)} full-size "
        f"-> {human(out_bytes)} {label}"
    )
    return len(sources)


def build_wall_smalls(quality, force, size=512):
    os.makedirs(WALLS_SMALL_DIR, exist_ok=True)
    sources = sorted(f for f in os.listdir(WALLS_DIR) if f.endswith(".webp"))
    built = skipped = 0
    for name in sources:
        source = os.path.join(WALLS_DIR, name)
        target = os.path.join(WALLS_SMALL_DIR, name)
        if not is_stale(source, target, force):
            skipped += 1
            continue
        with Image.open(source) as im:
            im = im.convert("RGB").resize((size, size), Image.LANCZOS)
            im.save(target, "WEBP", quality=quality, method=6)
        built += 1
    print(f"walls:     {built} built, {skipped} up to date ({len(sources)} total) -> small/{size}px")
    return len(sources)


def build_tutorial_webp(quality, force):
    sources = sorted(f for f in os.listdir(TUTORIAL_DIR) if f.endswith(".png"))

    built = skipped = 0
    src_bytes = out_bytes = 0

    for name in sources:
        source = os.path.join(TUTORIAL_DIR, name)
        target = os.path.join(TUTORIAL_DIR, name[: -len(".png")] + ".webp")
        src_bytes += os.path.getsize(source)

        if not is_stale(source, target, force):
            out_bytes += os.path.getsize(target)
            skipped += 1
            continue

        with Image.open(source) as im:
            # Keep alpha — these are cut-out character portraits over the game UI.
            im = im.convert("RGBA")
            im.save(target, "WEBP", quality=quality, method=6)

        out_bytes += os.path.getsize(target)
        built += 1

    print(
        f"tutorial:  {built} built, {skipped} up to date "
        f"({len(sources)} total) — {human(src_bytes)} PNG "
        f"-> {human(out_bytes)} WebP"
    )
    return len(sources)


def cut_out_flat_background(im, thresh=70):
    """Flat background -> alpha, flood-filled from the four corners (the creature-art method).

    Tolerance 70, not the creature pipeline's 24: generators add a soft coloured glow round the
    object, and 24 left it as a light halo. Only the region CONNECTED to a corner is cleared, so white highlights inside the object
    survive; the art prompts ask for a dark outline so the fill cannot leak inward."""
    from PIL import ImageDraw
    im = im.convert("RGBA")
    w, h = im.size
    for corner in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if im.getpixel(corner)[3] != 0:
            ImageDraw.floodfill(im, corner, (0, 0, 0, 0), thresh=thresh)
    return im


def square_padded(im, pad=0.06):
    """Trim to the object, then pad back to a square so every icon sits at the same scale."""
    box = im.getbbox()
    if box:
        im = im.crop(box)
    side = round(max(im.size) * (1 + 2 * pad))
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
    return canvas


def build_street_actions(quality, force):
    """3. The Street's action art (tiles, confirm sheet, Record chips).

    assets/street/actions/masters/<id>.png   (as generated, flat white or transparent)
      -> assets/street/actions/<id>.webp        256x256, transparent (tiles and sheets)
      -> assets/street/actions/small/<id>.webp   64x64, transparent (chips and rows)
    """
    if not os.path.isdir(STREET_MASTERS_DIR):
        print("street:    no masters yet")
        return 0
    os.makedirs(STREET_SMALL_DIR, exist_ok=True)
    sources = sorted(f for f in os.listdir(STREET_MASTERS_DIR) if f.endswith(".png"))
    built = skipped = 0
    for name in sources:
        source = os.path.join(STREET_MASTERS_DIR, name)
        stem = name[: -len(".png")]
        big = os.path.join(STREET_ACTIONS_DIR, stem + ".webp")
        small = os.path.join(STREET_SMALL_DIR, stem + ".webp")
        if not is_stale(source, big, force) and not is_stale(source, small, force):
            skipped += 1
            continue
        with Image.open(source) as im:
            art = square_padded(cut_out_flat_background(im))
            art.resize((256, 256), Image.LANCZOS).save(big, "WEBP", quality=max(quality, 88), method=6)
            art.resize((64, 64), Image.LANCZOS).save(small, "WEBP", quality=max(quality, 88), method=6)
        built += 1
    print(f"street:    {built} built, {skipped} up to date ({len(sources)} total)")
    return len(sources)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="rebuild every variant")
    parser.add_argument("--quality", type=int, default=80, help="WebP quality (default 80)")
    args = parser.parse_args()

    build_company_thumbs(args.quality, args.force)
    build_company_thumbs(min(args.quality, 75), args.force, MINI_DIR, MINI_WIDTH, "minis")
    build_wall_smalls(args.quality, args.force)
    build_tutorial_webp(args.quality, args.force)
    build_street_actions(args.quality, args.force)


if __name__ == "__main__":
    main()
