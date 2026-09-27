"""Digitally add flowering plants to the two front mulch beds in images/exterior.jpg.

Writes images/exterior-flowers.jpg and leaves the original photo untouched.
Usage: python3 add_flowers.py   (requires pillow, numpy, scipy)
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'images', 'exterior.jpg')
OUT = os.path.join(HERE, 'images', 'exterior-flowers.jpg')

SS = 3  # supersampling factor for anti-aliased plant rendering
rng = random.Random(2336)

# Mulch outlines traced from the photo (full-resolution pixel coordinates).
LEFT_BED = [(75, 1583), (170, 1537), (250, 1512), (400, 1503), (600, 1508), (782, 1515),
            (782, 1590), (700, 1598), (600, 1612), (530, 1622), (460, 1625), (350, 1620),
            (260, 1600), (200, 1588)]
RIGHT_BED = [(1045, 1502), (1100, 1495), (1400, 1490), (1560, 1500), (1650, 1535), (1735, 1580),
             (1600, 1582), (1420, 1585), (1415, 1612), (1200, 1605), (1045, 1595)]

# Front (stone-wall) edges of each bed, used to place the border row
LEFT_FRONT = [(95, 1580), (200, 1588), (260, 1600), (350, 1620), (460, 1625), (530, 1622),
              (600, 1612), (700, 1598), (775, 1590)]
RIGHT_FRONT = [(1050, 1595), (1200, 1605), (1415, 1610), (1420, 1578), (1600, 1576), (1720, 1576)]

# Flower colours: (petal base RGB, centre RGB)
PINK = ((228, 62, 128), (250, 214, 90))
RED = ((212, 38, 52), (245, 200, 70))
WHITE = ((246, 244, 238), (238, 196, 60))
PURPLE = ((138, 78, 190), (245, 222, 120))
YELLOW = ((250, 200, 40), (190, 110, 20))


def polygon_mask(shape, poly):
    m = Image.new('L', (shape[1], shape[0]), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return np.asarray(m) > 0


def poisson_points(mask, spacing, tries=4000):
    ys, xs = np.nonzero(mask)
    pts = []
    for _ in range(tries):
        i = rng.randrange(len(xs))
        x, y = int(xs[i]), int(ys[i])
        if all((x - px) ** 2 + (y - py) ** 2 >= spacing ** 2 for px, py in pts):
            pts.append((x, y))
    return pts


def shade(rgb, f):
    return tuple(max(0, min(255, int(c * f))) for c in rgb)


def tint(rgb, t):
    return tuple(int(c + (255 - c) * t) for c in rgb)


def blob(cx, base, R, bumps):
    """Irregular mound outline as a polygon."""
    pts = []
    for i in range(41):
        t = math.pi * i / 40
        k = 1 + sum(a * math.sin(f * t + ph) for a, f, ph in bumps)
        pts.append((cx + math.cos(t) * R * 1.05 * k, base - math.sin(t) * R * 1.05 * k))
    pts.append((cx - R * 1.05, base + R * 0.12))
    pts.append((cx + R * 1.05, base + R * 0.12))
    return pts


def render_plant(radius, colours):
    """Return an RGBA patch (at 1x) of a flowering mound and its anchor offset."""
    R = radius * SS
    W, H = int(R * 2.8), int(R * 2.8)
    cx, base = W / 2, H * 0.8
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bumps = [(rng.uniform(0.04, 0.1), f, rng.uniform(0, 6.3)) for f in (3, 5, 7)]

    # Soft contact shadow on the mulch
    sh = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sh).ellipse((cx - R * 1.15, base - R * 0.22, cx + R * 1.15, base + R * 0.28), fill=170)
    sh = sh.filter(ImageFilter.GaussianBlur(R * 0.18))
    img.paste((6, 7, 5, 255), (0, 0), sh)

    # Dark foliage body (the shadowed gaps between leaves)
    d.polygon(blob(cx, base, R * 0.95, bumps), fill=(34, 58, 24, 255))

    def in_mound(rr_min=0.0, rr_max=1.0):
        t = rng.uniform(0.05, math.pi - 0.05)
        rr = math.sqrt(rng.uniform(rr_min ** 2, rr_max ** 2))
        k = 1 + sum(a * math.sin(f * t + ph) for a, f, ph in bumps)
        return cx + math.cos(t) * R * 1.0 * rr * k, base - math.sin(t) * R * 1.0 * rr * k

    def leaves(n, size=1.0):
        for _ in range(n):
            lx, ly = in_mound(0.1, 1.02)
            light = 0.55 + 0.4 * (base - ly) / R + 0.12 * (lx - cx) / R
            g = shade((rng.randint(44, 76), rng.randint(84, 118), rng.randint(28, 48)), light)
            L, w = R * rng.uniform(0.16, 0.27) * size, R * rng.uniform(0.07, 0.12) * size
            ang = rng.uniform(0, math.pi)
            leaf = [(lx + math.cos(ang) * L * a - math.sin(ang) * w * b, ly + math.sin(ang) * L * a + math.cos(ang) * w * b)
                    for a, b in ((-1, 0), (0, 1), (1, 0), (0, -1))]
            d.polygon(leaf, fill=g + (255,))

    def blossoms(n):
        pts = sorted((in_mound(0.25, 0.98) for _ in range(n)), key=lambda p: p[1])
        for bx, by in pts:
            petal, centre = rng.choice(colours)
            petal = tuple(max(0, min(255, c + rng.randint(-14, 14))) for c in petal)
            r = R * rng.uniform(0.13, 0.19)
            light = 0.7 + 0.35 * (base - by) / R + 0.1 * (bx - cx) / R
            rot = rng.uniform(0, 2 * math.pi)
            # petal shadow first, so overlapping blossoms read as separate flowers
            d.ellipse((bx - r * 1.02, by - r * 0.7, bx + r * 1.02, by + r * 0.86), fill=shade(petal, 0.45 * light) + (200,))
            for k in range(5):
                a = rot + k * 2 * math.pi / 5
                px, py = bx + math.cos(a) * r * 0.46, by + math.sin(a) * r * 0.34
                pr = r * 0.5
                f = light * (1.05 if math.sin(a) < 0 else 0.86)
                col = shade(petal, min(f, 1.0) if petal[0] > 235 and petal[2] > 225 else f)
                d.ellipse((px - pr, py - pr * 0.8, px + pr, py + pr * 0.8), fill=col + (255,))
            cr = r * 0.15
            d.ellipse((bx - cr, by - cr * 0.8, bx + cr, by + cr * 0.8), fill=shade(centre, light) + (255,))

    n_leaf = int(60 + radius * 3)
    n_bloom = int(12 + radius * 1.0)
    leaves(n_leaf)
    blossoms(int(n_bloom * 0.6))
    leaves(int(n_leaf * 0.25), 0.8)   # some leaves in front of blossoms for depth
    blossoms(int(n_bloom * 0.4))

    img = img.resize((W // SS, H // SS), Image.LANCZOS)
    return img, (int(cx / SS), int(base / SS))


def main():
    photo = Image.open(SRC).convert('RGB')
    arr = np.asarray(photo).astype(np.float32)
    h, w = arr.shape[:2]

    # Keep plants off the existing shrubs (green foliage); the tan stone wall and white rocks don't count.
    r, g, b = (ndimage.gaussian_filter(arr[..., i], 3) for i in range(3))
    green = (g > r - 8) & (g > b + 25) & (g > 60)
    shrubs = ndimage.binary_dilation(ndimage.binary_opening(green, iterations=2), iterations=12)

    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    plants = []
    # Colour drifts across each bed (left to right), with a white border row along the stone wall
    drifts = {
        'left': [(0, [PURPLE]), (260, [PINK]), (420, [RED]), (560, [PINK]), (680, [YELLOW, RED])],
        'right': [(0, [PINK]), (1130, [RED]), (1300, [PURPLE]), (1440, [PINK]), (1600, [RED])],
    }
    for name, poly, front_line in (('left', LEFT_BED, LEFT_FRONT), ('right', RIGHT_BED, RIGHT_FRONT)):
        bed = polygon_mask((h, w), poly)
        inner = ndimage.binary_erosion(bed, iterations=14) & ~shrubs
        edge = Image.new('L', (w, h), 0)
        ImageDraw.Draw(edge).line(front_line, fill=255, width=3)
        dist = ndimage.distance_transform_edt(np.asarray(edge) == 0)
        border = inner & (dist > 16) & (dist < 28)
        body = inner & (dist >= 44)
        for (x, y) in poisson_points(border, 32):
            plants.append((y, x, [WHITE]))
        for (x, y) in poisson_points(body, 36):
            cols = [c for x0, c in drifts[name] if x >= x0][-1]
            plants.append((y, x, cols))

    plants.sort(key=lambda p: p[0])  # draw far (top) to near (bottom)
    for y, x, colours in plants:
        depth = (y - 1490) / 135.0
        radius = (19 + 6 * depth) * rng.uniform(0.88, 1.12)
        patch, (ax, ay) = render_plant(radius, colours)
        layer.alpha_composite(patch, (int(x - ax), int(y - ay)))

    # Match the photo's softness and grain, then composite
    layer = layer.filter(ImageFilter.GaussianBlur(0.45))
    la = np.asarray(layer).astype(np.float32)
    alpha = la[..., 3:4] / 255.0
    noise = np.random.default_rng(7).normal(0, 5, la[..., :3].shape)
    rgb = np.clip(la[..., :3] + noise, 0, 255)
    out = arr * (1 - alpha) + rgb * alpha
    Image.fromarray(out.astype(np.uint8)).save(OUT, quality=92, subsampling=0)
    print(f'{len(plants)} plants -> {OUT}')


if __name__ == '__main__':
    main()
