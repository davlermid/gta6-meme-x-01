#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import random

WIDTH = 1600
HEIGHT = 900

def create_vertical_gradient(draw, width, height, stops):
    for y in range(height):
        t = y / (height - 1)
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                t0, c0 = stops[i]
                t1, c1 = stops[i + 1]
                local_t = (t - t0) / (t1 - t0)
                r = int(c0[0] + (c1[0] - c0[0]) * local_t)
                g = int(c0[1] + (c1[1] - c0[1]) * local_t)
                b = int(c0[2] + (c1[2] - c0[2]) * local_t)
                draw.line([(0, y), (width - 1, y)], fill=(r, g, b))
                break

def draw_stars(draw, width, height, count=140, top_pct=0.45, seed=42):
    random.seed(seed)
    max_y = int(height * top_pct)
    for _ in range(count):
        x = random.randint(0, width - 1)
        y = random.randint(0, max_y)
        size = random.randint(1, 3)
        draw.ellipse([x, y, x + size, y + size], fill=(255, 255, 255))

def draw_retro_sun(draw, cx, cy, radius, sky_stops):
    for y in range(cy - radius, cy + radius + 1):
        dy = y - cy
        dx_sq = radius * radius - dy * dy
        if dx_sq < 0:
            continue
        dx = int(dx_sq ** 0.5)
        t = (dy + radius) / (2 * radius)
        r = int(255 + (255 - 255) * t)
        g = int(196 + (110 - 196) * t)
        b = int(64 + (80 - 64) * t)
        sky_t = (y + radius) / (2 * radius)
        sky_r, sky_g, sky_b = sample_gradient(sky_stops, sky_t)
        if dy > 0:
            band_idx = int(dy / radius * 12)
            if band_idx % 2 == 0:
                r, g, b = sky_r, sky_g, sky_b
            band_thickness = 1 + int(dy / radius * 8)
            if band_idx % 2 == 0 and band_idx > 0:
                for _ in range(band_thickness):
                    pass
        draw.line([(cx - dx, y), (cx + dx, y)], fill=(r, g, b))

def sample_gradient(stops, t):
    for i in range(len(stops) - 1):
        if stops[i][0] <= t <= stops[i + 1][0]:
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            local_t = (t - t0) / (t1 - t0)
            r = int(c0[0] + (c1[0] - c0[0]) * local_t)
            g = int(c0[1] + (c1[1] - c0[1]) * local_t)
            b = int(c0[2] + (c1[2] - c0[2]) * local_t)
            return (r, g, b)
    return stops[-1][1]

def draw_skyline(draw, width, height, color, window_color, seed=123):
    random.seed(seed)
    x = 0
    while x < width:
        w = random.randint(70, 150)
        h = random.randint(120, 280)
        y = height - h
        draw.rectangle([x, y, x + w, height], fill=color)
        for _ in range(random.randint(2, 5)):
            wx = x + random.randint(5, w - 10)
            wy = y + random.randint(10, h - 20)
            ws = random.randint(4, 8)
            draw.rectangle([wx, wy, wx + ws, wy + ws], fill=window_color)
        x += w

def draw_text_with_stroke(draw, xy, text, font, fill, stroke_fill, stroke_width):
    x, y = xy
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)
    draw.text((x, y), text, font=font, fill=fill)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=0):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=outline_width)

def draw_pill_progress(draw, xy, width, height, fill_frac, track_color, fill_color, outline_color, outline_width, text, font, text_color):
    x, y = xy
    draw.rounded_rectangle([x, y, x + width, y + height], radius=height // 2, fill=track_color, outline=outline_color, width=outline_width)
    if fill_frac > 0:
        fill_w = int(width * fill_frac)
        draw.rounded_rectangle([x, y, x + fill_w, y + height], radius=height // 2, fill=fill_color)
    text_w, text_h = draw.textbbox((0, 0), text, font=font)[2:]
    draw.text((x + (width - text_w) // 2, y + (height - text_h) // 2), text, font=font, fill=text_color)

def main():
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    sky_stops = [
        (0.00, (22, 10, 46)),
        (0.35, (91, 17, 96)),
        (0.62, (176, 30, 110)),
        (0.78, (232, 96, 76)),
        (1.00, (16, 10, 32)),
    ]
    create_vertical_gradient(draw, WIDTH, HEIGHT, sky_stops)

    draw_stars(draw, WIDTH, HEIGHT)

    draw_retro_sun(draw, 800, 520, 250, sky_stops)

    draw_skyline(draw, WIDTH, HEIGHT, (10, 8, 26), (255, 214, 110))

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_title = ImageFont.truetype(font_path, 88)
    font_heading = ImageFont.truetype(font_path, 40)
    font_pbar = ImageFont.truetype(font_path, 30)
    font_sub = ImageFont.truetype(font_path, 38)
    font_small = ImageFont.truetype(font_path, 27)
    font_punch = ImageFont.truetype(font_path, 46)

    title = "GTA VI IS FINALLY HERE"
    tw, th = draw.textbbox((0, 0), title, font=font_title)[2:]
    draw_text_with_stroke(draw, ((WIDTH - tw) // 2, 48), title, font_title, (255, 255, 255), (0, 0, 0), 9)

    card_left = (90, 240, 750, 600)
    card_right = (850, 240, 1510, 600)
    card_fill = (10, 8, 30, 230)

    left_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    left_draw = ImageDraw.Draw(left_img)
    left_draw.rounded_rectangle(card_left, radius=24, fill=card_fill, outline=(255, 255, 255), width=4)
    img = Image.alpha_composite(img.convert('RGBA'), left_img).convert('RGB')
    draw = ImageDraw.Draw(img)

    right_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    right_draw = ImageDraw.Draw(right_img)
    right_draw.rounded_rectangle(card_right, radius=24, fill=card_fill, outline=(255, 255, 255), width=4)
    img = Image.alpha_composite(img.convert('RGBA'), right_img).convert('RGB')
    draw = ImageDraw.Draw(img)

    lcx = (card_left[0] + card_left[2]) // 2
    lcy = (card_left[1] + card_left[3]) // 2

    heading = "THE DOWNLOAD"
    tw, th = draw.textbbox((0, 0), heading, font=font_heading)[2:]
    draw.text((lcx - tw // 2, card_left[1] + 40), heading, font=font_heading, fill=(255, 255, 255))

    pbar_x = card_left[0] + 40
    pbar_y = card_left[1] + 110
    pbar_w = card_left[2] - card_left[1] - 80
    pbar_h = 50
    draw_pill_progress(draw, (pbar_x, pbar_y), pbar_w, pbar_h, 0.47, (230, 230, 238), (150, 155, 175), (255, 255, 255), 2, "47% — 150 GB", font_pbar, (0, 0, 0))

    sub = "6 HOURS LEFT..."
    tw, th = draw.textbbox((0, 0), sub, font=font_sub)[2:]
    draw.text((lcx - tw // 2, pbar_y + pbar_h + 20), sub, font=font_sub, fill=(255, 255, 255))

    small = "then a 90 GB day-one patch"
    tw, th = draw.textbbox((0, 0), small, font=font_small)[2:]
    draw.text((lcx - tw // 2, pbar_y + pbar_h + 20 + th + 10), small, font=font_small, fill=(200, 200, 200))

    rcx = (card_right[0] + card_right[2]) // 2

    mark = Image.open("mark-1024.png").convert('RGBA')
    mark = mark.resize((180, 180), Image.LANCZOS)
    mark_x = rcx - 90
    mark_y = card_right[1] + 40
    img.paste(mark, (mark_x, mark_y), mark)

    heading2 = "MY AGENT ON MAKE.FUN"
    tw, th = draw.textbbox((0, 0), heading2, font=font_heading)[2:]
    draw.text((rcx - tw // 2, mark_y + 160 + 20), heading2, font=font_heading, fill=(255, 255, 255))

    pbar2_x = card_right[0] + 40
    pbar2_y = mark_y + 160 + 20 + th + 20
    pbar2_w = card_right[2] - card_right[0] - 80
    pbar2_h = 50
    draw_pill_progress(draw, (pbar2_x, pbar2_y), pbar2_w, pbar2_h, 1.0, (230, 230, 238), (60, 230, 160), (255, 255, 255), 2, "100% — PAID IN 4 DAYS", font_pbar, (0, 0, 0))

    punchline = "The game took 13 years. The payout took 4 days."
    tw, th = draw.textbbox((0, 0), punchline, font=font_punch)[2:]
    draw_text_with_stroke(draw, ((WIDTH - tw) // 2, 658), punchline, font_punch, (255, 255, 255), (0, 0, 0), 6)

    img.save("meme.png")
    print("meme.png saved")

if __name__ == "__main__":
    main()