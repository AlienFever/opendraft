#!/usr/bin/env python3
"""Generate a demo GIF for OpenDraft README."""

from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as iio
import os

# Terminal dimensions
W, H = 900, 520
# Colors (dark terminal theme)
BG = (30, 30, 30)
FG = (220, 220, 220)
GREEN = (80, 250, 123)
YELLOW = (241, 250, 140)
CYAN = (139, 233, 253)
PURPLE = (189, 147, 249)
GRAY = (100, 100, 100)
PROMPT = (255, 121, 198)

# Try to get a monospace font
font_paths = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Courier.dfont",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/Library/Fonts/Andale Mono.ttf",
]
font = None
for fp in font_paths:
    try:
        font = ImageFont.truetype(fp, 16)
        break
    except:
        continue
if font is None:
    font = ImageFont.load_default()

def make_frame(lines, cursor_pos=None, progress=None):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Title bar
    draw.rectangle([0, 0, W, 32], fill=(50, 50, 50))
    draw.text((12, 8), "opendraft — bash", fill=FG, font=font)
    # Window controls
    draw.ellipse([W-60, 12, W-48, 24], fill=(255, 95, 86))
    draw.ellipse([W-40, 12, W-28, 24], fill=(255, 189, 46))
    draw.ellipse([W-20, 12, W-8, 24], fill=(39, 201, 63))

    y = 48
    for i, (color, text) in enumerate(lines):
        draw.text((16, y), text, fill=color, font=font)
        y += 22

    if progress is not None:
        bar_w = 400
        bar_h = 8
        bar_x = 16
        bar_y = H - 40
        draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=4, fill=(60, 60, 60))
        fill_w = int(bar_w * progress)
        if fill_w > 0:
            draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], radius=4, fill=GREEN)
        pct = int(progress * 100)
        draw.text((bar_x + bar_w + 12, bar_y - 4), f"{pct}%", fill=GREEN, font=font)

    if cursor_pos:
        cx, cy = cursor_pos
        draw.rectangle([cx, cy, cx + 8, cy + 18], fill=FG)
    return img

# Build animation frames
frames = []

# Scene 1: typing command
cmd = "opendraft \"Neural Networks in Healthcare\" --type master --lang en"
for i in range(1, len(cmd) + 1):
    lines = [
        (PROMPT, "~/research $ "),
        (FG, cmd[:i]),
    ]
    cx = 16 + font.getlength("~/research $ " + cmd[:i])
    frames.append(make_frame(lines, cursor_pos=(cx, 70)))

# Scene 2: command submitted, starting
for _ in range(8):
    lines = [
        (PROMPT, "~/research $ "),
        (FG, cmd),
        (GRAY, ""),
        (CYAN, "🚀 OpenDraft v2.1 — 19-agent research pipeline"),
        (GRAY, ""),
        (YELLOW, "📚 Research Phase    → Finding papers from 500M+ sources..."),
    ]
    frames.append(make_frame(lines))

# Scene 3: research progress
for i in range(0, 101, 2):
    lines = [
        (PROMPT, "~/research $ "),
        (FG, cmd),
        (GRAY, ""),
        (CYAN, "🚀 OpenDraft v2.1 — 19-agent research pipeline"),
        (GRAY, ""),
        (GREEN, "✅ Research Phase    → 142 papers found"),
        (YELLOW, "🏗️  Structure Phase   → Building thesis outline..."),
    ]
    frames.append(make_frame(lines, progress=i/100))

# Scene 4: writing
for i in range(0, 101, 3):
    lines = [
        (PROMPT, "~/research $ "),
        (FG, cmd),
        (GRAY, ""),
        (CYAN, "🚀 OpenDraft v2.1 — 19-agent research pipeline"),
        (GRAY, ""),
        (GREEN, "✅ Research Phase    → 142 papers found"),
        (GREEN, "✅ Structure Phase   → 8 chapters, 24 sections"),
        (YELLOW, "✍️  Writing Phase     → Drafting sections..."),
    ]
    frames.append(make_frame(lines, progress=i/100))

# Scene 5: citations
for i in range(0, 101, 4):
    lines = [
        (PROMPT, "~/research $ "),
        (FG, cmd),
        (GRAY, ""),
        (CYAN, "🚀 OpenDraft v2.1 — 19-agent research pipeline"),
        (GRAY, ""),
        (GREEN, "✅ Research Phase    → 142 papers found"),
        (GREEN, "✅ Structure Phase   → 8 chapters, 24 sections"),
        (GREEN, "✅ Writing Phase     → 18,420 words drafted"),
        (YELLOW, "🔍 Citation Phase    → Verifying sources..."),
    ]
    frames.append(make_frame(lines, progress=i/100))

# Scene 6: export
for i in range(0, 101, 5):
    lines = [
        (PROMPT, "~/research $ "),
        (FG, cmd),
        (GRAY, ""),
        (CYAN, "🚀 OpenDraft v2.1 — 19-agent research pipeline"),
        (GRAY, ""),
        (GREEN, "✅ Research Phase    → 142 papers found"),
        (GREEN, "✅ Structure Phase   → 8 chapters, 24 sections"),
        (GREEN, "✅ Writing Phase     → 18,420 words drafted"),
        (GREEN, "✅ Citation Phase    → 38 sources verified (CrossRef, arXiv)"),
        (YELLOW, "📄 Export Phase      → Generating PDF..."),
    ]
    frames.append(make_frame(lines, progress=i/100))

# Scene 7: done
for _ in range(20):
    lines = [
        (PROMPT, "~/research $ "),
        (FG, cmd),
        (GRAY, ""),
        (CYAN, "🚀 OpenDraft v2.1 — 19-agent research pipeline"),
        (GRAY, ""),
        (GREEN, "✅ Research Phase    → 142 papers found"),
        (GREEN, "✅ Structure Phase   → 8 chapters, 24 sections"),
        (GREEN, "✅ Writing Phase     → 18,420 words drafted"),
        (GREEN, "✅ Citation Phase    → 38 sources verified (CrossRef, arXiv)"),
        (GREEN, "✅ Export Phase      → thesis.pdf saved"),
        (GRAY, ""),
        (PURPLE, "⏱️  Total time: 12m 34s"),
        (PURPLE, "💰  Cost: ~$0.35 (Gemini Flash)"),
    ]
    frames.append(make_frame(lines))

# Save GIF
out_path = os.path.join(os.path.dirname(__file__), "demo.gif")
iio.imwrite(out_path, frames, duration=60, loop=0)
print(f"GIF saved: {out_path} ({len(frames)} frames)")
