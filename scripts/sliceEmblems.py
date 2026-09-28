#!/usr/bin/env python3
"""Slice one ChatGPT guild-emblem sheet into individual emblems.

    python3 scripts/sliceEmblems.py --sheet <image> --first 1 [--count 20] [--dry-run]

`--first` is the NUMBER of the sheet's first emblem (sheet N starts at 20N-19): ids are assigned
in reading order (left->right, top->bottom) as e001, e002, ... exactly as the game repo's
server_logic/guild/emblemCatalogue.js lists its subjects. Those ids are database keys: a redraw
reuses an id, never renames one.

Writes
    assets/emblems/masters/sheet-<first>.png   the keyed sheet (RGBA)
    assets/emblems/<id>.webp                   160x160, alpha (the guild page)
    assets/emblems/small/<id>.webp             64x64, alpha (beside a name, the picker)

Background: real alpha is used as-is; flat #FF00FF is chroma-keyed. A PAINTED CHECKERBOARD (what
ChatGPT actually returns) is flood-filled from the sheet's border, never globally, and with NO
seed inside an emblem: unlike a frame, an emblem has no hole, and its centre is the cream charge,
which a centre flood would erase. The shield's navy outline stops the flood.

Requires Pillow + numpy. Shares its helpers with sliceFrames.py.
"""
import argparse
import os

import numpy as np
from PIL import Image

from sliceFrames import grow, dilate, components, reading_order, EDGE, SOLID, SEAL

SIZE = 160
SMALL = 64
MARGIN = 0.04
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'emblems')


def key_border(a):
    """The painted checkerboard, removed from the outside in.

    The background is NEUTRAL GREY: the light and dark squares, and (in a JPEG) the faint darker
    seams ChatGPT paints between cells. A flood that only crosses LIGHT pixels stops at those
    seams, so every cell's checkerboard survived at full opacity (the first run of this script).
    So the flood crosses any neutral grey from the border, and stops only at colour: every
    emblem is ringed by a polished gold rim and a navy outline, both clearly coloured, and its
    cream charge sits inside the enamel where the flood never reaches."""
    rgb = a[..., :3].astype(float)
    lo, hi = rgb.min(-1), rgb.max(-1)
    neutral = (hi - lo <= 24) & (lo >= 110)
    border = np.zeros_like(neutral)
    border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = True
    outside = grow(border, neutral)
    # A one-pixel feather on the cut so the rim is not jagged at 64px.
    alpha = np.where(outside, 0.0, 255.0)
    pad = np.pad(alpha, 1, mode='edge')
    soft = sum(pad[dy:dy + alpha.shape[0], dx:dx + alpha.shape[1]] for dy in range(3) for dx in range(3)) / 9
    a[..., 3] = np.where(outside, np.minimum(soft, 255) * (soft > 128), 255).astype(np.uint8)
    return a


def to_rgba(path):
    a = np.array(Image.open(path).convert('RGBA'))
    if a[..., 3].min() < 255:
        return a
    rgb = a[..., :3].astype(int)
    if np.abs(rgb[2, 2] - [255, 0, 255]).max() < 40:
        dist = np.sqrt(((rgb - [255, 0, 255]) ** 2).sum(-1))
        a[..., 3] = np.clip((dist - 40) * 255 / 60, 0, 255).astype(np.uint8)
        return a
    return key_border(a)


def square(img, size):
    """The emblem fitted into a transparent square, centred, aspect kept, MARGIN all round."""
    inner = int(round(size * (1 - 2 * MARGIN)))
    w, h = img.size
    s = inner / max(w, h)
    fitted = img.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(fitted, ((size - fitted.width) // 2, (size - fitted.height) // 2), fitted)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sheet', required=True)
    ap.add_argument('--first', type=int, required=True, help='number of the first emblem on the sheet')
    ap.add_argument('--count', type=int, default=20)
    ap.add_argument('--dry-run', action='store_true', help='report what would be cut, write nothing')
    args = ap.parse_args()

    rgba = to_rgba(args.sheet)
    mask = rgba[..., 3] > SOLID
    rgba[..., 3] = np.where(dilate(mask, EDGE), rgba[..., 3], 0)
    boxes = components(mask)
    # A painted checkerboard (a JPEG especially) leaves faint seams that survive the key as thin
    # slivers, ~20x50px against ~280x310px emblems. Anything under a quarter of the median
    # emblem's area is one of those, never art.
    areas = sorted((b[2] - b[0]) * (b[3] - b[1]) for b in boxes)
    median = areas[len(areas) // 2] if areas else 0
    boxes = reading_order([b for b in boxes if (b[2] - b[0]) * (b[3] - b[1]) >= median / 4])
    if len(boxes) != args.count:
        raise SystemExit(f'found {len(boxes)} emblems, expected {args.count}')

    ids = [f'e{n:03d}' for n in range(args.first, args.first + args.count)]
    sheet = Image.fromarray(rgba)
    if not args.dry_run:
        for d in ('masters', 'small', ''):
            os.makedirs(os.path.join(ROOT, d), exist_ok=True)
        sheet.save(os.path.join(ROOT, 'masters', f'sheet-{args.first:03d}.png'))

    for eid, (x0, y0, x1, y1) in zip(ids, boxes):
        crop = sheet.crop((max(0, x0 - EDGE), max(0, y0 - EDGE), x1 + EDGE, y1 + EDGE))
        # keep only this emblem's own pixels (a neighbour never sits inside its box, but be sure)
        bbox = crop.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        if bbox:
            crop = crop.crop(bbox)
        print(f'{eid}  {x1 - x0}x{y1 - y0}px at ({x0},{y0})')
        if args.dry_run:
            continue
        square(crop, SIZE).save(os.path.join(ROOT, f'{eid}.webp'), 'WEBP', quality=90, method=6)
        square(crop, SMALL).save(os.path.join(ROOT, 'small', f'{eid}.webp'), 'WEBP', quality=90, method=6)


if __name__ == '__main__':
    main()
