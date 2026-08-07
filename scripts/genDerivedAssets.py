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
TUTORIAL_DIR = os.path.join(ASSETS, "tutorial")

THUMB_WIDTH = 800


def is_stale(source, target, force):
    """True when the target needs (re)building."""
    if force or not os.path.exists(target):
        return True
    return os.path.getmtime(source) > os.path.getmtime(target)


def human(num_bytes):
    return f"{num_bytes / 1024:.0f} KB"


def build_company_thumbs(quality, force):
    os.makedirs(THUMB_DIR, exist_ok=True)
    sources = sorted(f for f in os.listdir(COMPANIES_DIR) if f.endswith(".webp"))

    built = skipped = 0
    src_bytes = out_bytes = 0

    for name in sources:
        source = os.path.join(COMPANIES_DIR, name)
        target = os.path.join(THUMB_DIR, name)
        src_bytes += os.path.getsize(source)

        if not is_stale(source, target, force):
            out_bytes += os.path.getsize(target)
            skipped += 1
            continue

        with Image.open(source) as im:
            im = im.convert("RGB")
            height = max(1, round(im.height * THUMB_WIDTH / im.width))
            im = im.resize((THUMB_WIDTH, height), Image.LANCZOS)
            im.save(target, "WEBP", quality=quality, method=6)

        out_bytes += os.path.getsize(target)
        built += 1

    print(
        f"companies: {built} built, {skipped} up to date "
        f"({len(sources)} total) — {human(src_bytes)} full-size "
        f"-> {human(out_bytes)} thumbs"
    )
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="rebuild every variant")
    parser.add_argument("--quality", type=int, default=80, help="WebP quality (default 80)")
    args = parser.parse_args()

    build_company_thumbs(args.quality, args.force)
    build_tutorial_webp(args.quality, args.force)


if __name__ == "__main__":
    main()
