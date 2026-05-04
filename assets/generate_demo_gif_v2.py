#!/usr/bin/env python3
"""
Generate a high-quality demo GIF for OpenDraft.
1280x720, dark terminal theme, smooth animations.
Uses PIL for rendering and ffmpeg for optimized GIF encoding.
"""

import os
import math
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ============================================================
# CONFIGURATION
# ============================================================
W, H = 1280, 720
FPS = 15  # Output frame rate (reduced for file size, still smooth)
TMP_DIR = tempfile.mkdtemp(prefix="opendraft_gif_")
OUT_PATH = os.path.join(os.path.dirname(__file__), "demo.gif")

# Colors
BG = (26, 26, 46)            # #1a1a2e
TERMINAL_BG = (22, 33, 62)   # #16213e
ACCENT_CYAN = (0, 217, 255)  # #00d9ff
ACCENT_PINK = (255, 107, 157)# #ff6b9d
TEXT = (234, 234, 234)       # #eaeaea
SUBTEXT = (136, 146, 176)    # #8892b0
TITLE_BAR_BG = (30, 30, 50)  # Slightly lighter than terminal bg
GRID_COLOR = (40, 40, 70)    # Very faint grid
SHADOW_COLOR = (10, 10, 25)

# Terminal window
TERM_W, TERM_H = 960, 600
TERM_X = (W - TERM_W) // 2
TERM_Y = (H - TERM_H) // 2
RADIUS = 14
TITLE_H = 38

# ============================================================
# FONTS
# ============================================================
def load_font(size):
    """Load the best available monospace font."""
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/System/Library/Fonts/Courier.ttc",
        "/Library/Fonts/JetBrainsMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

FONT_MAIN = load_font(18)
FONT_SMALL = load_font(14)
FONT_LARGE = load_font(22)
FONT_EMOJI = load_font(20)  # Fallback for emoji sizing

def text_size(draw, text, font):
    """Get text bounding box size."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

# ============================================================
# DRAWING HELPERS
# ============================================================
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)

def ease_out_elastic(t):
    c4 = (2 * math.pi) / 3
    if t == 0:
        return 0
    if t == 1:
        return 1
    return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1

def ease_out_quad(t):
    return 1 - (1 - t) * (1 - t)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    r = radius
    # Draw main body
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)
    # Draw four corners
    draw.pieslice([x1, y1, x1 + 2*r, y1 + 2*r], 180, 270, fill=fill)
    draw.pieslice([x2 - 2*r, y1, x2, y1 + 2*r], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2*r, x1 + 2*r, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2*r, y2 - 2*r, x2, y2], 0, 90, fill=fill)
    if outline:
        # Simplified outline
        draw.arc([x1, y1, x1 + 2*r, y1 + 2*r], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*r, y1, x2, y1 + 2*r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2*r, x1 + 2*r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2*r, y2 - 2*r, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + r, y1, x2 - r, y1], fill=outline, width=width)
        draw.line([x1 + r, y2, x2 - r, y2], fill=outline, width=width)
        draw.line([x1, y1 + r, x1, y2 - r], fill=outline, width=width)
        draw.line([x2, y1 + r, x2, y2 - r], fill=outline, width=width)

# ============================================================
# BACKGROUND & TERMINAL
# ============================================================
grid_cache = None

def draw_grid_background(img):
    """Draw faint grid on background."""
    global grid_cache
    if grid_cache is None:
        grid_cache = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(grid_cache)
        step = 40
        for x in range(0, W, step):
            gd.line([(x, 0), (x, H)], fill=GRID_COLOR + (40,), width=1)
        for y in range(0, H, step):
            gd.line([(0, y), (W, y)], fill=GRID_COLOR + (40,), width=1)
    img.paste(grid_cache, (0, 0), grid_cache)

shadow_cache = None

def get_shadow():
    global shadow_cache
    if shadow_cache is None:
        # Create shadow mask
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        # Draw large blurred rounded rect
        sd.rounded_rectangle(
            [TERM_X - 20, TERM_Y - 20, TERM_X + TERM_W + 20, TERM_Y + TERM_H + 20],
            radius=RADIUS + 10, fill=SHADOW_COLOR + (180,)
        )
        shadow_cache = shadow.filter(ImageFilter.GaussianBlur(radius=25))
    return shadow_cache

def draw_terminal_window(draw, img):
    """Draw the terminal window with shadow, title bar, and body."""
    # Shadow
    img.paste(get_shadow(), (0, 0), get_shadow())
    
    # Terminal body
    draw.rounded_rectangle(
        [TERM_X, TERM_Y, TERM_X + TERM_W, TERM_Y + TERM_H],
        radius=RADIUS, fill=TERMINAL_BG
    )
    
    # Title bar
    draw.rounded_rectangle(
        [TERM_X, TERM_Y, TERM_X + TERM_W, TERM_Y + TITLE_H],
        radius=RADIUS, fill=TITLE_BAR_BG
    )
    # Fill the bottom corners of title bar so they don't show rounded
    draw.rectangle([TERM_X, TERM_Y + TITLE_H - RADIUS, TERM_X + TERM_W, TERM_Y + TITLE_H], fill=TITLE_BAR_BG)
    
    # macOS window controls
    btn_y = TERM_Y + TITLE_H // 2
    btn_r = 6
    spacing = 22
    start_x = TERM_X + 20
    # Red
    draw.ellipse([start_x - btn_r, btn_y - btn_r, start_x + btn_r, btn_y + btn_r], fill=(255, 95, 86))
    # Yellow
    draw.ellipse([start_x + spacing - btn_r, btn_y - btn_r, start_x + spacing + btn_r, btn_y + btn_r], fill=(255, 189, 46))
    # Green
    draw.ellipse([start_x + 2*spacing - btn_r, btn_y - btn_r, start_x + 2*spacing + btn_r, btn_y + btn_r], fill=(39, 201, 63))
    
    # Title text
    title = "opendraft — zsh"
    tw, th = text_size(draw, title, FONT_SMALL)
    draw.text((TERM_X + (TERM_W - tw)//2, TERM_Y + (TITLE_H - th)//2), title, fill=SUBTEXT, font=FONT_SMALL)

# ============================================================
# CONTENT DRAWING
# ============================================================
def draw_text_line(draw, x, y, text, color, font=FONT_MAIN):
    """Draw a line of text."""
    draw.text((x, y), text, fill=color, font=font)
    return text_size(draw, text, font)[0]

def draw_progress_bar(draw, x, y, width, height, progress, frame_idx):
    """Draw a smooth gradient progress bar."""
    # Background
    draw.rounded_rectangle([x, y, x + width, y + height], radius=height//2, fill=(40, 50, 80))
    
    if progress <= 0:
        return
    
    fill_w = int(width * progress)
    if fill_w < 2:
        return
    
    # Gradient fill - cyan to slightly lighter cyan
    for i in range(fill_w):
        t = i / width
        # Gradient from #00d9ff to a slightly different cyan
        r = int(lerp(0, 100, t))
        g = int(lerp(217, 230, t))
        b = int(lerp(255, 255, t))
        draw.line([(x + i, y), (x + i, y + height)], fill=(r, g, b))
    
    # Rounded cap on the right
    cap_r = height // 2
    # Simplified: the bar looks fine with just the vertical lines
    # Add a subtle glow on the leading edge
    if fill_w < width:
        glow_x = x + fill_w
        for g in range(4):
            alpha = 120 - g * 30
            glow_color = (0, 217, 255)
            draw.line([(glow_x + g, y - 1), (glow_x + g, y + height + 1)], fill=glow_color, width=1)
    
    # Percentage text
    pct = int(progress * 100)
    pct_text = f"{pct}%"
    tw, th = text_size(draw, pct_text, FONT_SMALL)
    draw.text((x + width + 12, y + (height - th)//2), pct_text, fill=ACCENT_CYAN, font=FONT_SMALL)

def draw_cursor(draw, x, y, visible):
    """Draw a blinking cursor."""
    if visible:
        draw.rectangle([x, y, x + 10, y + 20], fill=TEXT)

def draw_typing_pulse(draw, x, y, intensity):
    """Draw a small pulsing dot near cursor to simulate typing sound visually."""
    if intensity <= 0:
        return
    r = int(3 * intensity)
    if r > 0:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=ACCENT_PINK + (int(200 * intensity),))

def draw_checkmark(draw, x, y, scale, color=ACCENT_CYAN):
    """Draw an animated checkmark."""
    if scale <= 0:
        return
    # Simple checkmark path
    points = [
        (x + 2, y + 8),
        (x + 6, y + 12),
        (x + 14, y + 2),
    ]
    # Scale around center
    cx, cy = x + 8, y + 7
    scaled = []
    for px, py in points:
        sx = cx + (px - cx) * scale
        sy = cy + (py - cy) * scale
        scaled.append((sx, sy))
    
    # Draw thick line
    for i in range(len(scaled) - 1):
        draw.line([scaled[i], scaled[i+1]], fill=color, width=max(1, int(2.5 * scale)))

def draw_phase_line(draw, x, y, icon, label, detail, color, check_scale=1.0, is_active=False):
    """Draw a phase line with optional animated checkmark."""
    # Checkmark box
    check_x = x
    check_y = y + 2
    if check_scale >= 1.0:
        draw_checkmark(draw, check_x, check_y, 1.0, color=ACCENT_CYAN)
    elif check_scale > 0:
        draw_checkmark(draw, check_x, check_y, check_scale, color=ACCENT_CYAN)
    
    # Icon
    icon_x = x + 24
    draw.text((icon_x, y), icon, fill=color, font=FONT_MAIN)
    
    # Label
    label_x = icon_x + 28
    label_w = draw_text_line(draw, label_x, y, label, color)
    
    # Detail (subtext)
    detail_x = label_x + label_w + 8
    draw_text_line(draw, detail_x, y, detail, SUBTEXT)
    
    if is_active:
        # Subtle glow behind active line
        pass  # Optional

# ============================================================
# FRAME RENDERING
# ============================================================
class Animator:
    def __init__(self):
        self.frames = []
        self.frame_idx = 0
    
    def add_frame(self, img):
        path = os.path.join(TMP_DIR, f"frame_{self.frame_idx:05d}.png")
        img.save(path, "PNG")
        self.frames.append(path)
        self.frame_idx += 1
    
    def render(self):
        """Render frames to optimized GIF using ffmpeg."""
        # Use ffmpeg to create optimized palette GIF
        pattern = os.path.join(TMP_DIR, "frame_%05d.png")
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", pattern,
            "-vf",
            "split[s0][s1];[s0]palettegen=max_colors=96[p];[s1][p]paletteuse=dither=bayer",
            "-loop", "0",
            OUT_PATH
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Check size and optimize further if needed
        size = os.path.getsize(OUT_PATH)
        print(f"GIF saved: {OUT_PATH}")
        print(f"Frames: {self.frame_idx}, File size: {size / 1024 / 1024:.2f} MB")
        
        if size > 2 * 1024 * 1024:
            print("File too large, re-encoding with more aggressive optimization...")
            cmd2 = [
                "ffmpeg", "-y",
                "-i", OUT_PATH,
                "-vf",
                "fps=10,scale=1280:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=bayer",
                "-loop", "0",
                OUT_PATH + ".tmp"
            ]
            subprocess.run(cmd2, check=True, capture_output=True)
            os.replace(OUT_PATH + ".tmp", OUT_PATH)
            size = os.path.getsize(OUT_PATH)
            print(f"Re-encoded. File size: {size / 1024 / 1024:.2f} MB")

animator = Animator()

def make_frame(lines, cursor_info=None, progress=None, check_scales=None, typing_pulse=None):
    """Render a single frame."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    
    # Background grid
    draw_grid_background(img)
    
    # Terminal window
    draw_terminal_window(draw, img)
    
    # Content area
    content_x = TERM_X + 24
    content_y = TERM_Y + TITLE_H + 20
    line_height = 28
    
    for i, line_data in enumerate(lines):
        if isinstance(line_data, tuple) and len(line_data) == 2:
            color, text = line_data
            draw.text((content_x, content_y + i * line_height), text, fill=color, font=FONT_MAIN)
        elif isinstance(line_data, dict):
            # Complex line
            x = content_x
            for segment in line_data.get("segments", []):
                seg_color = segment.get("color", TEXT)
                seg_text = segment.get("text", "")
                seg_font = segment.get("font", FONT_MAIN)
                tw, _ = text_size(draw, seg_text, seg_font)
                draw.text((x, content_y + i * line_height), seg_text, fill=seg_color, font=seg_font)
                x += tw
    
    # Cursor
    if cursor_info:
        cx, cy, visible = cursor_info
        draw_cursor(draw, cx, cy, visible)
        if typing_pulse and typing_pulse > 0:
            draw_typing_pulse(draw, cx + 16, cy + 10, typing_pulse)
    
    # Progress bar
    if progress is not None:
        bar_x = content_x
        bar_y = TERM_Y + TERM_H - 60
        bar_w = 500
        bar_h = 10
        draw_progress_bar(draw, bar_x, bar_y, bar_w, bar_h, progress, animator.frame_idx)
    
    # Phase check scales
    if check_scales:
        for idx, scale in enumerate(check_scales):
            if scale > 0:
                check_y = content_y + idx * line_height + 4
                draw_checkmark(draw, content_x - 2, check_y, min(1.0, scale))
    
    animator.add_frame(img)

# ============================================================
# ANIMATION TIMELINE
# ============================================================
cmd_text = 'opendraft "Neural Networks in Healthcare" --type master --lang en'
prompt_text = "~/research $ "

# Precompute text widths for cursor positioning
tmp_img = Image.new("RGB", (1, 1))
tmp_draw = ImageDraw.Draw(tmp_img)
prompt_w, _ = text_size(tmp_draw, prompt_text, FONT_MAIN)

# Helper: get cursor position after typing n chars of command
def cursor_pos(n):
    typed = cmd_text[:n]
    tw, _ = text_size(tmp_draw, typed, FONT_MAIN)
    return TERM_X + 24 + prompt_w + tw, TERM_Y + TITLE_H + 20 + 28

# Helper: typing delays (variable speed)
def typing_delay_for_char(c):
    if c == ' ':
        return 2  # Fast for spaces
    if c in '"-=/':
        return 5  # Slower for special chars
    if c.isupper():
        return 4
    return 3  # Normal

# --- SCENE 1: Empty terminal with blinking cursor (1.5s) ---
for i in range(int(1.5 * FPS)):
    blink = (i % 20) < 10
    lines = [(ACCENT_PINK, prompt_text)]
    cx = TERM_X + 24 + prompt_w
    cy = TERM_Y + TITLE_H + 20 + 28
    make_frame(lines, cursor_info=(cx, cy, blink))

# --- SCENE 2: Typing command (variable speed) ---
total_typed = 0
char_idx = 0
while char_idx < len(cmd_text):
    c = cmd_text[char_idx]
    delay = typing_delay_for_char(c)
    for _ in range(delay):
        blink = (animator.frame_idx % 20) < 10
        lines = [
            (ACCENT_PINK, prompt_text),
            (TEXT, cmd_text[:char_idx]),
        ]
        cx, cy = cursor_pos(char_idx)
        pulse = 0.8 if _ == 0 else max(0, 0.8 - _ * 0.3)
        make_frame(lines, cursor_info=(cx, cy, blink), typing_pulse=pulse)
    char_idx += 1

# Hold typed command briefly
for i in range(int(0.4 * FPS)):
    blink = (animator.frame_idx % 20) < 10
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
    ]
    cx, cy = cursor_pos(len(cmd_text))
    make_frame(lines, cursor_info=(cx, cy, blink))

# --- SCENE 3: Command submitted, cursor moves down, header appears ---
# 0.5s: header fades in
header_text = "▶ OpenDraft v2.1 — 19-agent research pipeline"
for i in range(int(0.6 * FPS)):
    t = i / (0.6 * FPS)
    alpha = ease_out_cubic(t)
    # Blend color
    header_color = lerp_color((22, 33, 62), ACCENT_CYAN, alpha)
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (header_color, header_text),
    ]
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 3
    blink = (animator.frame_idx % 20) < 10
    make_frame(lines, cursor_info=(cx, cy, blink))

# --- PHASE 1: Research ---
phase1_label = "Research Phase"
phase1_detail = "→ 142 papers found"
phase1_icon = "●"

for i in range(int(3.5 * FPS)):
    t = i / (3.5 * FPS)
    progress = ease_out_cubic(t)
    blink = (animator.frame_idx % 20) < 10
    
    # Active phase line with pulsing indicator
    pulse = 0.5 + 0.5 * math.sin(i * 0.3)
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
    ]
    
    # Phase 1 active
    active_color = lerp_color(SUBTEXT, ACCENT_CYAN, pulse)
    lines.append((active_color, f"{phase1_icon}  {phase1_label}    → Finding papers from 500M+ sources..."))
    
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 5
    make_frame(lines, cursor_info=(cx, cy, blink), progress=progress)

# Phase 1 complete - checkmark animation
for i in range(int(0.4 * FPS)):
    t = i / (0.4 * FPS)
    scale = ease_out_elastic(t)
    blink = (animator.frame_idx % 20) < 10
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (SUBTEXT, "🏗️  Structure Phase   → Building thesis outline..."),
    ]
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 6
    make_frame(lines, cursor_info=(cx, cy, blink), check_scales=[0, scale, 0])

# --- PHASE 2: Structure ---
phase2_label = "Structure Phase"
phase2_detail = "→ 8 chapters, 24 sections"
phase2_icon = "●"

for i in range(int(3.0 * FPS)):
    t = i / (3.0 * FPS)
    progress = ease_out_cubic(t)
    blink = (animator.frame_idx % 20) < 10
    pulse = 0.5 + 0.5 * math.sin(i * 0.3)
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
    ]
    
    active_color = lerp_color(SUBTEXT, ACCENT_CYAN, pulse)
    lines.append((active_color, f"{phase2_icon}  {phase2_label}    → Building thesis outline..."))
    
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 6
    make_frame(lines, cursor_info=(cx, cy, blink), progress=progress)

# Phase 2 complete
for i in range(int(0.4 * FPS)):
    t = i / (0.4 * FPS)
    scale = ease_out_elastic(t)
    blink = (animator.frame_idx % 20) < 10
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
        (SUBTEXT, "✍️  Writing Phase     → Drafting sections..."),
    ]
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 7
    make_frame(lines, cursor_info=(cx, cy, blink), check_scales=[0, 0, scale, 0])

# --- PHASE 3: Writing ---
phase3_label = "Writing Phase"
phase3_detail = "→ 18,420 words drafted"
phase3_icon = "●"

for i in range(int(3.0 * FPS)):
    t = i / (3.0 * FPS)
    progress = ease_out_cubic(t)
    blink = (animator.frame_idx % 20) < 10
    pulse = 0.5 + 0.5 * math.sin(i * 0.3)
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
    ]
    
    active_color = lerp_color(SUBTEXT, ACCENT_CYAN, pulse)
    lines.append((active_color, f"{phase3_icon}  {phase3_label}    → Drafting sections..."))
    
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 7
    make_frame(lines, cursor_info=(cx, cy, blink), progress=progress)

# Phase 3 complete
for i in range(int(0.4 * FPS)):
    t = i / (0.4 * FPS)
    scale = ease_out_elastic(t)
    blink = (animator.frame_idx % 20) < 10
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
        (ACCENT_CYAN, f"✓  {phase3_label}    {phase3_detail}"),
        (SUBTEXT, "🔍 Citation Phase    → Verifying sources..."),
    ]
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 8
    make_frame(lines, cursor_info=(cx, cy, blink), check_scales=[0, 0, 0, scale, 0])

# --- PHASE 4: Citations ---
phase4_label = "Citation Phase"
phase4_detail = "→ 38 sources verified (CrossRef, arXiv)"
phase4_icon = "●"

for i in range(int(3.0 * FPS)):
    t = i / (3.0 * FPS)
    progress = ease_out_cubic(t)
    blink = (animator.frame_idx % 20) < 10
    pulse = 0.5 + 0.5 * math.sin(i * 0.3)
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
        (ACCENT_CYAN, f"✓  {phase3_label}    {phase3_detail}"),
    ]
    
    active_color = lerp_color(SUBTEXT, ACCENT_CYAN, pulse)
    lines.append((active_color, f"{phase4_icon}  {phase4_label}    → Verifying sources..."))
    
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 8
    make_frame(lines, cursor_info=(cx, cy, blink), progress=progress)

# Phase 4 complete
for i in range(int(0.4 * FPS)):
    t = i / (0.4 * FPS)
    scale = ease_out_elastic(t)
    blink = (animator.frame_idx % 20) < 10
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
        (ACCENT_CYAN, f"✓  {phase3_label}    {phase3_detail}"),
        (ACCENT_CYAN, f"✓  {phase4_label}    {phase4_detail}"),
        (SUBTEXT, "📄 Export Phase      → Generating PDF..."),
    ]
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 9
    make_frame(lines, cursor_info=(cx, cy, blink), check_scales=[0, 0, 0, 0, scale, 0])

# --- PHASE 5: Export ---
phase5_label = "Export Phase"
phase5_detail = "→ thesis.pdf saved"
phase5_icon = "●"

for i in range(int(3.0 * FPS)):
    t = i / (3.0 * FPS)
    progress = ease_out_cubic(t)
    blink = (animator.frame_idx % 20) < 10
    pulse = 0.5 + 0.5 * math.sin(i * 0.3)
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
        (ACCENT_CYAN, f"✓  {phase3_label}    {phase3_detail}"),
        (ACCENT_CYAN, f"✓  {phase4_label}    {phase4_detail}"),
    ]
    
    active_color = lerp_color(SUBTEXT, ACCENT_CYAN, pulse)
    lines.append((active_color, f"{phase5_icon}  {phase5_label}    → Generating PDF..."))
    
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 9
    make_frame(lines, cursor_info=(cx, cy, blink), progress=progress)

# Phase 5 complete
for i in range(int(0.4 * FPS)):
    t = i / (0.4 * FPS)
    scale = ease_out_elastic(t)
    blink = (animator.frame_idx % 20) < 10
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
        (ACCENT_CYAN, f"✓  {phase3_label}    {phase3_detail}"),
        (ACCENT_CYAN, f"✓  {phase4_label}    {phase4_detail}"),
        (ACCENT_CYAN, f"✓  {phase5_label}    {phase5_detail}"),
    ]
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 10
    make_frame(lines, cursor_info=(cx, cy, blink), check_scales=[0, 0, 0, 0, 0, scale])

# --- FINAL STATS ---
# Fade in stats
for i in range(int(0.5 * FPS)):
    t = i / (0.5 * FPS)
    alpha = ease_out_cubic(t)
    stats_color = lerp_color(TERMINAL_BG, ACCENT_PINK, alpha)
    
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
        (ACCENT_CYAN, f"✓  {phase3_label}    {phase3_detail}"),
        (ACCENT_CYAN, f"✓  {phase4_label}    {phase4_detail}"),
        (ACCENT_CYAN, f"✓  {phase5_label}    {phase5_detail}"),
        (SUBTEXT, ""),
    ]
    
    time_color = lerp_color(TERMINAL_BG, ACCENT_PINK, alpha)
    cost_color = lerp_color(TERMINAL_BG, ACCENT_PINK, alpha)
    lines.append((time_color, "⏱️  12m 34s"))
    lines.append((cost_color, "💰  ~$0.35 (Gemini Flash)"))
    
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 12
    blink = (animator.frame_idx % 20) < 10
    make_frame(lines, cursor_info=(cx, cy, blink))

# Hold final state
for i in range(int(2.5 * FPS)):
    blink = (animator.frame_idx % 20) < 10
    lines = [
        (ACCENT_PINK, prompt_text),
        (TEXT, cmd_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, header_text),
        (SUBTEXT, ""),
        (ACCENT_CYAN, f"✓  {phase1_label}    {phase1_detail}"),
        (ACCENT_CYAN, f"✓  {phase2_label}    {phase2_detail}"),
        (ACCENT_CYAN, f"✓  {phase3_label}    {phase3_detail}"),
        (ACCENT_CYAN, f"✓  {phase4_label}    {phase4_detail}"),
        (ACCENT_CYAN, f"✓  {phase5_label}    {phase5_detail}"),
        (SUBTEXT, ""),
        (ACCENT_PINK, "◷  12m 34s"),
        (ACCENT_PINK, "$  ~$0.35 (Gemini Flash)"),
    ]
    cx = TERM_X + 24
    cy = TERM_Y + TITLE_H + 20 + 28 * 12
    make_frame(lines, cursor_info=(cx, cy, blink))

# ============================================================
# RENDER
# ============================================================
if __name__ == "__main__":
    print(f"Rendering {animator.frame_idx} frames to {TMP_DIR}...")
    animator.render()
    
    # Verify
    from PIL import Image as PILImage
    gif = PILImage.open(OUT_PATH)
    print(f"\nFinal GIF verification:")
    print(f"  Path: {OUT_PATH}")
    print(f"  Size: {os.path.getsize(OUT_PATH) / 1024 / 1024:.2f} MB")
    print(f"  Dimensions: {gif.size[0]}x{gif.size[1]}")
    print(f"  Frames: {getattr(gif, 'n_frames', 1)}")
    print(f"  Format: {gif.format}")
    
    # Cleanup temp
    import shutil
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    print(f"\nCleaned up temp directory.")
