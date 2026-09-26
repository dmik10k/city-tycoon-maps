#!/usr/bin/env python3
"""Slice one ChatGPT avatar-frame sheet into individual frames.

    python3 scripts/sliceFrames.py --sheet <image> --group free \
        --ids free-mint,free-navy,...        (reading order: left->right, top->bottom)

Writes
    assets/frames/masters/<group>.png    the sheet as supplied (RGBA)
    assets/frames/<id>.webp              512x512, alpha
    assets/frames/small/<id>.webp        160x160, alpha (header avatar is ~67 CSS px)

Every frame is normalized on its HOLE, not its bounding box: the transparent disc in the
middle is re-centered and scaled to HOLE_FRACTION of the canvas, so any frame lines up over
the avatar identically however far its ornaments reach.

Background: real alpha is used as-is. A sheet without alpha must be flat #FF00FF and is
chroma-keyed globally (a corner flood-fill would never reach a ring's enclosed hole).

Requires Pillow + numpy.
"""
import argparse
import os
from collections import deque

import numpy as np
from PIL import Image

HOLE_FRACTION = 0.34
SIZE = 512
SMALL = 160
ALPHA_ON = 24
SOLID = 128
GLOW = 24
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'frames')


def grow(seed, allowed):
    """Geodesic dilation: every allowed pixel 4-connected to the seed."""
    region = seed & allowed
    while True:
        g = region.copy()
        g[1:] |= region[:-1]; g[:-1] |= region[1:]
        g[:, 1:] |= region[:, :-1]; g[:, :-1] |= region[:, 1:]
        g &= allowed
        if (g == region).all():
            return region
        region = g


SEAL = 6


def dilate(mask, r):
    out = mask.copy()
    for _ in range(r):
        g = out.copy()
        g[1:] |= out[:-1]; g[:-1] |= out[1:]; g[:, 1:] |= out[:, :-1]; g[:, :-1] |= out[:, 1:]
        out = g
    return out


def key_checkerboard(a):
    """ChatGPT often PAINTS the transparency checkerboard. Its squares are bright neutral greys,
    so remove bright-neutral pixels reachable from the image border, then the same inside each
    frame's hole — never globally, or cream-white icons inside the art would vanish."""
    rgb = a[..., :3].astype(float)
    lo = rgb.min(-1)
    neutral = (lo >= 205) & (rgb.max(-1) - lo <= 18)
    border = np.zeros_like(neutral)
    border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = True
    bg = grow(border, neutral)
    # "Outside" = light pixels reachable from the border or a hole without crossing the frame's
    # dark outline. That is the painted background PLUS any glow painted onto it; the art
    # itself (white feathers, cream icons) sits inside a dark outline and is never reached.
    # A glare can break the outline (the diamond's top edge has none), so first seal gaps by
    # thickening the outline SEAL px, flood, then give the flood back those SEAL px up to the
    # real edge: a gap can then leak SEAL px deep at most, never into a whole gem or ring.
    light = lo >= 150
    sealed = light & ~dilate(~light, SEAL)
    outside = grow(border, sealed)
    for x0, y0, x1, y1 in components(~bg):
        seed = np.zeros_like(neutral)
        seed[(y0 + y1) // 2, (x0 + x1) // 2] = True
        box = np.zeros_like(neutral); box[y0:y1, x0:x1] = True
        outside |= grow(seed, sealed & box)
    outside = dilate(outside, SEAL + 2) & light
    # Out there, opacity comes from how far a pixel is from the pale checkerboard: a plain
    # square -> 0, a glow -> partly transparent. Box-blur it so the squares don't show through.
    alpha = np.clip((236 - lo) * 255 / 90, 0, 255)
    k = 5
    pad = np.pad(alpha, k, mode='edge')
    cs = pad.cumsum(0).cumsum(1)
    cs = np.pad(cs, ((1, 0), (1, 0)))
    n = 2 * k + 1
    blurred = (cs[n:, n:] - cs[:-n, n:] - cs[n:, :-n] + cs[:-n, :-n]) / (n * n)
    alpha = np.where(outside, np.minimum(alpha, blurred), 255)
    # un-mix the pale background from the colour so a glow keeps its own hue
    af = np.maximum(alpha, 1)[..., None] / 255
    fg = np.clip((rgb - (1 - af) * 245) / af, 0, 255)
    a[..., :3] = np.where(outside[..., None], fg, rgb).astype(np.uint8)
    a[..., 3] = alpha.astype(np.uint8)
    return a


def to_rgba(path):
    im = Image.open(path).convert('RGBA')
    a = np.array(im)
    if a[..., 3].min() == 255:
        rgb = a[..., :3].astype(int)
        if np.abs(rgb[2, 2] - [255, 0, 255]).max() < 40:  # flat magenta: key it out globally
            dist = np.sqrt(((rgb - [255, 0, 255]) ** 2).sum(-1))
            a[..., 3] = np.clip((dist - 40) * 255 / 60, 0, 255).astype(np.uint8)
        else:
            a = key_checkerboard(a)
    return a


def components(mask, step=4):
    """Connected components on a downsampled mask -> full-res bounding boxes."""
    h, w = mask.shape
    small = mask[: h // step * step, : w // step * step].reshape(h // step, step, w // step, step).any((1, 3))
    seen = np.zeros_like(small)
    boxes = []
    for y0, x0 in zip(*np.nonzero(small)):
        if seen[y0, x0]:
            continue
        q = deque([(y0, x0)]); seen[y0, x0] = True
        ys, xs = [y0], [x0]
        while q:
            y, x = q.popleft()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < small.shape[0] and 0 <= nx < small.shape[1] and small[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx)); ys.append(ny); xs.append(nx)
        if len(ys) < 50:  # speck
            continue
        boxes.append((min(xs) * step, min(ys) * step, (max(xs) + 1) * step, (max(ys) + 1) * step))
    return boxes


def reading_order(boxes):
    boxes = sorted(boxes, key=lambda b: (b[1] + b[3]) / 2)
    rows, row = [], [boxes[0]]
    for b in boxes[1:]:
        prev = row[-1]
        if (b[1] + b[3]) / 2 - (prev[1] + prev[3]) / 2 > (prev[3] - prev[1]) / 2:
            rows.append(row); row = [b]
        else:
            row.append(b)
    rows.append(row)
    return [b for r in rows for b in sorted(r, key=lambda b: b[0])]


def hole_of(mask, box):
    """Flood the transparent region containing the box center -> (cx, cy, diameter)."""
    x0, y0, x1, y1 = box
    sub = ~mask[y0:y1, x0:x1]
    cy, cx = (y1 - y0) // 2, (x1 - x0) // 2
    if not sub[cy, cx]:
        raise SystemExit(f'frame at {box}: center is not transparent (no hole?)')
    seen = np.zeros_like(sub)
    q = deque([(cy, cx)]); seen[cy, cx] = True
    n = sy = sx = 0
    while q:
        y, x = q.popleft(); n += 1; sy += y; sx += x
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < sub.shape[0] and 0 <= nx < sub.shape[1] and sub[ny, nx] and not seen[ny, nx]:
                if ny in (0, sub.shape[0] - 1) or nx in (0, sub.shape[1] - 1):
                    raise SystemExit(f'frame at {box}: hole leaks to the outside (ring not closed)')
                seen[ny, nx] = True; q.append((ny, nx))
    return x0 + sx / n, y0 + sy / n, 2 * np.sqrt(n / np.pi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sheet', required=True)
    ap.add_argument('--group', required=True)
    ap.add_argument('--ids', required=True)
    args = ap.parse_args()
    ids = [s.strip() for s in args.ids.split(',') if s.strip()]

    rgba = to_rgba(args.sheet)
    mask = rgba[..., 3] > SOLID  # solid art only: soft glows must not bridge two frames
    boxes = reading_order(components(mask))
    if len(boxes) != len(ids):
        raise SystemExit(f'found {len(boxes)} frames, expected {len(ids)}')

    for d in ('masters', 'small', ''):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    Image.fromarray(rgba).save(os.path.join(ROOT, 'masters', f'{args.group}.png'))
    sheet = Image.fromarray(rgba)

    for fid, box in zip(ids, boxes):
        cx, cy, d = hole_of(mask, box)
        side = d / HOLE_FRACTION
        crop = (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)
        x0, y0, x1, y1 = box
        clipped = x0 < crop[0] or y0 < crop[1] or x1 > crop[2] or y1 > crop[3]
        out = sheet.transform((SIZE, SIZE), Image.EXTENT, crop, Image.BICUBIC)
        # the neighbouring frames can fall inside a large crop: keep only this frame's pixels
        keep = Image.new('L', sheet.size, 0)
        keep.paste(255, (x0 - GLOW, y0 - GLOW, x1 + GLOW, y1 + GLOW))  # room for the glow
        for other in boxes:  # ...but never a neighbour's crown tip or sparkle
            if other != box:
                keep.paste(0, other)
        out.putalpha(Image.composite(out.getchannel('A'),
                                     Image.new('L', (SIZE, SIZE), 0),
                                     keep.transform((SIZE, SIZE), Image.EXTENT, crop, Image.NEAREST)))
        out.save(os.path.join(ROOT, f'{fid}.webp'), 'WEBP', quality=90, method=6)
        out.resize((SMALL, SMALL), Image.LANCZOS).save(os.path.join(ROOT, 'small', f'{fid}.webp'), 'WEBP', quality=90, method=6)
        print(f'{fid:22s} hole {d:6.1f}px  scale {SIZE / side:.3f}' + ('  WARNING: clipped at canvas edge' if clipped else ''))


if __name__ == '__main__':
    main()
