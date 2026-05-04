#!/usr/bin/env python3
"""Generate a 1200x630 OpenGraph social preview image for OpenDraft."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630

# Colors
dark = (15, 15, 25)
accent = (80, 250, 123)
accent2 = (139, 233, 253)
text_light = (240, 240, 240)
text_gray = (160, 160, 170)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 72)
font_sub = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 32)
font_tag = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)

def draw_rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

img = Image.new("RGB", (W, H), dark)
draw = ImageDraw.Draw(img)

# Subtle grid background
for i in range(0, W, 40):
    draw.line([(i, 0), (i, H)], fill=(30, 30, 40), width=1)
for i in range(0, H, 40):
    draw.line([(0, i), (W, i)], fill=(30, 30, 40), width=1)

# Decorative accent bar on left
draw.rectangle([0, 0, 8, H], fill=accent)

# Title
draw.text((60, 120), "OpenDraft", fill=text_light, font=font_title)

# Subtitle
subtitle = "AI Research Draft Generator"
draw.text((60, 220), subtitle, fill=accent2, font=font_sub)

# Description lines
desc_lines = [
    "19 specialized agents · 500M+ academic sources",
    "Verified citations · PDF/DOCX/LaTeX export",
    "100% free & open source (MIT license)",
]
y = 320
for line in desc_lines:
    draw.text((60, y), line, fill=text_gray, font=font_tag)
    y += 40

# CTA badge
badge_text = "Try free at OpenPaper.dev →"
bbox = draw.textbbox((0, 0), badge_text, font=font_tag)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
bx1, by1 = 60, 480
bx2, by2 = bx1 + tw + 40, by1 + th + 24
draw.rounded_rectangle([bx1, by1, bx2, by2], radius=8, fill=accent)
draw.text((bx1 + 20, by1 + 10), badge_text, fill=dark, font=font_tag)

# Right side decorative terminal window
term_x, term_y = 720, 100
term_w, term_h = 420, 430
draw.rounded_rectangle([term_x, term_y, term_x + term_w, term_y + term_h], radius=12, fill=(25, 25, 35), outline=(50, 50, 60), width=2)

# Terminal title bar
draw.rounded_rectangle([term_x, term_y, term_x + term_w, term_y + 36], radius=12, fill=(40, 40, 50))
draw.rectangle([term_x, term_y + 20, term_x + term_w, term_y + 36], fill=(40, 40, 50))
draw.text((term_x + 16, term_y + 8), "opendraft — bash", fill=text_gray, font=font_tag)

# Dots
draw.ellipse([term_x + term_w - 60, term_y + 10, term_x + term_w - 46, term_y + 24], fill=(255, 95, 86))
draw.ellipse([term_x + term_w - 40, term_y + 10, term_x + term_w - 26, term_y + 24], fill=(255, 189, 46))
draw.ellipse([term_x + term_w - 20, term_y + 10, term_x + term_w - 6, term_y + 24], fill=(39, 201, 63))

# Terminal content
term_lines = [
    ("~/research $", (255, 121, 198)),
    ('opendraft "Neural Networks in Healthcare"', text_light),
    ("", text_gray),
    ("🚀 OpenDraft v2.1", accent2),
    ("", text_gray),
    ("✅ Research    → 142 papers found", accent),
    ("✅ Structure   → 8 chapters", accent),
    ("✅ Writing     → 18,420 words", accent),
    ("✅ Citations   → 38 verified", accent),
    ("✅ Export      → thesis.pdf", accent),
    ("", text_gray),
    ("⏱️  12m 34s · 💰 ~$0.35", (189, 147, 249)),
]
ty = term_y + 56
for tline, tcolor in term_lines:
    draw.text((term_x + 20, ty), tline, fill=tcolor, font=font_tag)
    ty += 32

# Save
out = os.path.join(os.path.dirname(__file__), "social-preview.png")
img.save(out, "PNG")
print(f"Saved: {out} ({W}x{H})")
