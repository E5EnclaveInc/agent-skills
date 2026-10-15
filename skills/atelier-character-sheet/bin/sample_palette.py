#!/usr/bin/env python3
"""Sample dominant colors from a reference image.

Usage: python3 sample_palette.py <image> [n=7]
Prints the top n colors as hex, largest cluster first, near-duplicates merged.
The atelier assigns professional names; this script only measures.
"""
import sys
from PIL import Image


def main():
    path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    im = Image.open(path).convert("RGB").resize((160, 160))
    # Quantize to a small palette, then merge near-duplicates.
    q = im.quantize(colors=24, method=Image.MEDIANCUT)
    pal = q.getpalette()[:24 * 3]
    counts = sorted(q.getcolors(), reverse=True)
    clusters = []  # (count, (r,g,b))
    for cnt, idx in counts:
        r, g, b = pal[idx * 3:idx * 3 + 3]
        placed = False
        for i, (c, (cr, cg, cb)) in enumerate(clusters):
            if abs(r - cr) + abs(g - cg) + abs(b - cb) < 35:
                clusters[i] = (c + cnt, (r, g, b))
                placed = True
                break
        if not placed:
            clusters.append((cnt, (r, g, b)))
    clusters.sort(reverse=True)
    for _, (r, g, b) in clusters[:n]:
        print("#%02x%02x%02x" % (r, g, b))


if __name__ == "__main__":
    main()
