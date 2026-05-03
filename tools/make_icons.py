"""Generate two .ico files for TkRadio desktop shortcuts.

Headless icon: deep blue, crescent moon = "runs quietly in the background".
Head icon:     amber/orange, magnifier = "debug / browser visible".

Both share the same radio silhouette so the pair reads as one app, two modes.
Drawn at 4x then downscaled for clean anti-aliased edges.
"""
from PIL import Image, ImageDraw
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "Images" / "icons"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SIZES = [16, 32, 48, 64, 128, 256]
SS = 4  # supersampling factor


def vertical_gradient(size, top, bottom):
    """Build a vertical gradient image."""
    w, h = size
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def draw_radio(draw, cx, cy, w, h, body_color, grill_color, dial_color, accent):
    """Draw a stylised radio centered at (cx, cy)."""
    # Body
    left, top = cx - w // 2, cy - h // 2
    right, bottom = cx + w // 2, cy + h // 2
    draw.rounded_rectangle((left, top, right, bottom), radius=h // 6, fill=body_color)

    # Inner panel (slight inset, darker)
    inset = h // 14
    panel = (left + inset, top + inset, right - inset, bottom - inset)
    inner = tuple(max(0, c - 22) for c in body_color)
    draw.rounded_rectangle(panel, radius=h // 8, fill=inner)

    # Speaker grill (left half)
    grill_cx = left + w // 4 + inset
    grill_cy = cy
    grill_r = h // 3
    draw.ellipse(
        (grill_cx - grill_r, grill_cy - grill_r, grill_cx + grill_r, grill_cy + grill_r),
        fill=grill_color,
    )
    # Concentric grill rings
    for k in range(1, 4):
        r = grill_r - k * (grill_r // 4)
        ring = tuple(max(0, c - 35 * (4 - k) // 4) for c in grill_color)
        draw.ellipse(
            (grill_cx - r, grill_cy - r, grill_cx + r, grill_cy + r),
            outline=ring,
            width=max(2, h // 60),
        )
    # Center dot
    cd = grill_r // 5
    draw.ellipse(
        (grill_cx - cd, grill_cy - cd, grill_cx + cd, grill_cy + cd),
        fill=accent,
    )

    # Tuner display (right half)
    tuner_left = grill_cx + grill_r + inset // 2
    tuner_w = right - inset - tuner_left
    tuner_h = h // 3
    tuner_top = cy - tuner_h // 2 - inset
    draw.rounded_rectangle(
        (tuner_left, tuner_top, tuner_left + tuner_w, tuner_top + tuner_h),
        radius=tuner_h // 5,
        fill=dial_color,
    )
    # Tuner needle
    needle_x = tuner_left + int(tuner_w * 0.62)
    draw.line(
        (needle_x, tuner_top + 4, needle_x, tuner_top + tuner_h - 4),
        fill=accent,
        width=max(3, h // 50),
    )
    # Tuner ticks
    for i in range(1, 8):
        tx = tuner_left + int(tuner_w * i / 8)
        draw.line(
            (tx, tuner_top + tuner_h - 6, tx, tuner_top + tuner_h - 2),
            fill=tuple(max(0, c - 50) for c in dial_color),
            width=max(1, h // 90),
        )

    # Two knobs below tuner
    knob_y = tuner_top + tuner_h + inset // 2 + h // 30
    knob_r = h // 18
    for i, kx in enumerate([tuner_left + tuner_w // 4, tuner_left + 3 * tuner_w // 4]):
        draw.ellipse(
            (kx - knob_r, knob_y - knob_r, kx + knob_r, knob_y + knob_r),
            fill=tuple(max(0, c - 40) for c in body_color),
            outline=accent,
            width=max(2, h // 80),
        )

    # Antenna (extends up-right from top-right corner)
    ant_base = (right - inset * 2, top + inset)
    ant_tip = (right + w // 5, top - h // 3)
    draw.line(
        (ant_base[0], ant_base[1], ant_tip[0], ant_tip[1]),
        fill=tuple(max(0, c - 40) for c in body_color),
        width=max(4, h // 40),
    )
    # Antenna tip ball
    tr = max(4, h // 35)
    draw.ellipse(
        (ant_tip[0] - tr, ant_tip[1] - tr, ant_tip[0] + tr, ant_tip[1] + tr),
        fill=accent,
    )


def draw_sound_waves(draw, cx, cy, base_r, color, count=3):
    """Draw concentric arcs to suggest sound emission."""
    for i in range(count):
        r = base_r + i * (base_r // 2)
        bbox = (cx - r, cy - r, cx + r, cy + r)
        # Alpha-modulated outline
        a = max(60, 220 - i * 60)
        draw.arc(bbox, start=300, end=60, fill=color + (a,), width=max(3, base_r // 8))


def make_headless_icon(size_px):
    s = size_px * SS
    bg = vertical_gradient((s, s), (32, 64, 128), (12, 28, 64)).convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # Soft outer rounded mask (so corners are smooth when used as .ico)
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), radius=s // 8, fill=255)
    bg.putalpha(mask)

    draw = ImageDraw.Draw(bg)

    # Subtle sound waves behind the radio (cool cyan)
    overlay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    draw_sound_waves(od, s // 2 - s // 14, s // 2, s // 5, (140, 220, 255), count=3)
    bg = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(bg)

    # Radio
    draw_radio(
        draw,
        cx=s // 2,
        cy=s // 2 + s // 30,
        w=int(s * 0.70),
        h=int(s * 0.46),
        body_color=(210, 215, 225),
        grill_color=(60, 70, 90),
        dial_color=(180, 230, 200),
        accent=(255, 200, 80),
    )

    # Crescent moon badge (top-right) — "runs quietly"
    badge_r = s // 9
    bx, by = s - badge_r - s // 16, badge_r + s // 16
    # Disc
    draw.ellipse(
        (bx - badge_r, by - badge_r, bx + badge_r, by + badge_r),
        fill=(255, 235, 160),
    )
    # Bite out a smaller offset disc to make crescent
    bite_r = int(badge_r * 0.85)
    ox, oy = bx + badge_r // 3, by - badge_r // 6
    draw.ellipse(
        (ox - bite_r, oy - bite_r, ox + bite_r, oy + bite_r),
        fill=(12, 28, 64, 255),  # match darker bottom of gradient — visually "cuts" the moon
    )

    return bg.resize((size_px, size_px), Image.LANCZOS)


def make_head_icon(size_px):
    s = size_px * SS
    bg = vertical_gradient((s, s), (240, 150, 40), (180, 60, 20)).convert("RGBA")

    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, s - 1, s - 1), radius=s // 8, fill=255)
    bg.putalpha(mask)

    draw = ImageDraw.Draw(bg)

    # Sound waves
    overlay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    draw_sound_waves(od, s // 2 - s // 14, s // 2, s // 5, (255, 240, 200), count=3)
    bg = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(bg)

    # Radio (warmer body to harmonise with amber bg)
    draw_radio(
        draw,
        cx=s // 2,
        cy=s // 2 + s // 30,
        w=int(s * 0.70),
        h=int(s * 0.46),
        body_color=(60, 35, 25),
        grill_color=(20, 14, 10),
        dial_color=(255, 220, 120),
        accent=(255, 250, 230),
    )

    # Magnifier badge (top-right) — "debug / visible"
    badge_r = s // 9
    bx, by = s - badge_r - s // 16, badge_r + s // 16
    # Lens disc
    draw.ellipse(
        (bx - badge_r, by - badge_r, bx + badge_r, by + badge_r),
        fill=(255, 245, 220),
        outline=(60, 30, 15),
        width=max(3, s // 110),
    )
    # Inner lens highlight
    inner_r = int(badge_r * 0.55)
    draw.ellipse(
        (bx - inner_r - badge_r // 6, by - inner_r - badge_r // 6,
         bx + inner_r - badge_r // 6, by + inner_r - badge_r // 6),
        outline=(255, 255, 255, 200),
        width=max(2, s // 160),
    )
    # Handle
    hx1, hy1 = bx + int(badge_r * 0.65), by + int(badge_r * 0.65)
    hx2, hy2 = hx1 + badge_r, hy1 + badge_r
    draw.line((hx1, hy1, hx2, hy2), fill=(60, 30, 15), width=max(6, s // 60))
    # Handle cap
    cr = max(4, s // 90)
    draw.ellipse((hx2 - cr, hy2 - cr, hx2 + cr, hy2 + cr), fill=(60, 30, 15))

    return bg.resize((size_px, size_px), Image.LANCZOS)


def build_ico(maker, out_path: Path):
    """Render one image per size, then save as multi-resolution .ico."""
    images = [maker(sz) for sz in SIZES]
    # PIL's save with .ico writes embedded sizes from the `sizes` argument.
    images[-1].save(
        out_path,
        format="ICO",
        sizes=[(sz, sz) for sz in SIZES],
        append_images=images[:-1],
    )
    print(f"wrote {out_path}")


if __name__ == "__main__":
    build_ico(make_headless_icon, OUT_DIR / "tkradio_headless.ico")
    build_ico(make_head_icon, OUT_DIR / "tkradio_head.ico")
    # Also save 256-px PNG previews so the user can see them outside Explorer
    make_headless_icon(256).save(OUT_DIR / "tkradio_headless.png")
    make_head_icon(256).save(OUT_DIR / "tkradio_head.png")
    print("done")
