#!/usr/bin/env python3
"""
USAF-1951 SVG generator (200 mm wide, element grid 6 columns x groups -2..6).
Outputs:
 - usaf1951_200mm.svg
 - usaf1951_mapping.csv
Notes:
 - SVG units are millimeters (mm). Print/export with 600 dpi for high-frequency fidelity.
"""
import math
from xml.sax.saxutils import escape

# Layout parameters (mm)
WIDTH_MM = 200.0
MARGIN_MM = 10.0
COLS = 6
GROUPS = list(range(-2, 7))  # -2 .. 6 inclusive -> 9 rows
ROWS = len(GROUPS)
ELEM_SIZE_MM = (WIDTH_MM - 2 * MARGIN_MM) / COLS  # square elements
HEIGHT_MM = ROWS * ELEM_SIZE_MM + 2 * MARGIN_MM

FONT_FAMILY = "Arial, Helvetica, sans-serif"
LABEL_FONT_MM = 2.8
SMALL_FONT_MM = 2.2

def lpmm_for(group, element):
    # element in 1..6
    return 2 ** (group + (element - 1) / 6.0)

def fmt(f):
    return f"{f:.6f}"

svg_parts = []
svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH_MM}mm" height="{HEIGHT_MM}mm" viewBox="0 0 {WIDTH_MM} {HEIGHT_MM}" version="1.1">')
svg_parts.append(f'<rect x="0" y="0" width="{WIDTH_MM}" height="{HEIGHT_MM}" fill="white"/>')
# Title
svg_parts.append(f'<text x="{WIDTH_MM/2}" y="{MARGIN_MM/2 + 3}" font-family="{FONT_FAMILY}" font-size="{LABEL_FONT_MM}" text-anchor="middle">USAF 1951 Resolution Test Target — {WIDTH_MM:.0f} mm width</text>')

mapping_lines = ["Group,Element,lp_per_mm,box_x_mm,box_y_mm,box_size_mm"]

for row_idx, G in enumerate(GROUPS):
    y = MARGIN_MM + row_idx * ELEM_SIZE_MM
    for e in range(1, COLS + 1):
        x = MARGIN_MM + (e - 1) * ELEM_SIZE_MM
        lpmm = lpmm_for(G, e)
        half_w = ELEM_SIZE_MM / 2.0

        # compute half-cycle (single stripe width)
        half_cycle_mm = 1.0 / (2.0 * lpmm)  # mm
        # compute number of stripes needed to fill half area
        n_stripes_x = int(math.ceil(half_w / half_cycle_mm))
        n_stripes_y = int(math.ceil(ELEM_SIZE_MM / half_cycle_mm))

        # element group border
        svg_parts.append(f'<g id="G{G}_E{e}" transform="translate({fmt(x)},{fmt(y)})">')
        svg_parts.append(f'<rect x="0" y="0" width="{fmt(ELEM_SIZE_MM)}" height="{fmt(ELEM_SIZE_MM)}" fill="none" stroke="black" stroke-width="0.2"/>')

        # left half: vertical stripes (fill by drawing black stripes; background white)
        for i in range(n_stripes_x):
            sx = i * half_cycle_mm
            sw = half_cycle_mm
            if sx >= half_w:
                break
            # alternate: start with black at leftmost (i=0)
            if i % 2 == 0:
                # ensure stripe doesn't overflow beyond half_w
                sw_eff = min(sw, half_w - sx)
                svg_parts.append(f'<rect x="{fmt(sx)}" y="0" width="{fmt(sw_eff)}" height="{fmt(ELEM_SIZE_MM)}" fill="black"/>')

        # right half: horizontal stripes
        rx0 = half_w
        for j in range(n_stripes_y):
            sy = j * half_cycle_mm
            sh = half_cycle_mm
            if sy >= ELEM_SIZE_MM:
                break
            if j % 2 == 0:
                sh_eff = min(sh, ELEM_SIZE_MM - sy)
                svg_parts.append(f'<rect x="{fmt(rx0)}" y="{fmt(sy)}" width="{fmt(half_w)}" height="{fmt(sh_eff)}" fill="black"/>')

        # add small label: "Gx Ey" and lp/mm below
        label_x = 1.0
        label_y = ELEM_SIZE_MM - 2.8
        svg_parts.append(f'<text x="{fmt(label_x)}" y="{fmt(label_y)}" font-family="{FONT_FAMILY}" font-size="{SMALL_FONT_MM}" fill="black">G{G} E{e}</text>')
        svg_parts.append(f'<text x="{fmt(label_x)}" y="{fmt(label_y + 2.0)}" font-family="{FONT_FAMILY}" font-size="{SMALL_FONT_MM}" fill="black">{fmt(lpmm)} lp/mm</text>')
        svg_parts.append('</g>')

        mapping_lines.append(f"{G},{e},{fmt(lpmm)},{fmt(x)},{fmt(y)},{fmt(ELEM_SIZE_MM)}")

# scale bar (10 mm) bottom-left
scale_x = MARGIN_MM
scale_y = HEIGHT_MM - MARGIN_MM/1.5
svg_parts.append(f'<rect x="{fmt(scale_x)}" y="{fmt(scale_y - 1.5)}" width="10" height="1.0" fill="black"/>')
svg_parts.append(f'<text x="{fmt(scale_x + 12)}" y="{fmt(scale_y - 0.4)}" font-family="{FONT_FAMILY}" font-size="{SMALL_FONT_MM}">10 mm</text>')

svg_parts.append('</svg>')

svg_content = "\n".join(svg_parts)

# write svg
with open("usaf1951_200mm.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
print("Wrote usaf1951_200mm.svg")

# write mapping csv
with open("usaf1951_mapping.csv", "w", encoding="utf-8") as f:
    f.write("\n".join(mapping_lines))
print("Wrote usaf1951_mapping.csv")

# end
