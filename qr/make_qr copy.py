# pip install qrcode[pil]
import qrcode

DATA = "https://example.com"
OUT  = "qr_circle_sticker.svg"

BG = "#37abc8"   # sticker/background
FG = "#37abc8"   # QR code color (reference uses blue modules on white)
QR_BG = "#ffffff"
FULL_MATRIX = True  # True = show outer modules clipped by circle
DIAMETER_MM = 40 # typical conference sticker size

# High error correction helps when cropping to a circle
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=1,
    border=4,  # quiet zone (keep this)
)
qr.add_data(DATA)
qr.make(fit=True)

m = qr.get_matrix()  # list[list[bool]]
n = len(m)           # modules per side

# Finder pattern corners (account for quiet zone)
quiet = qr.border
content = n - quiet * 2
finders = [
    (quiet, quiet),
    (quiet + content - 7, quiet),
    (quiet, quiet + content - 7),
]

def in_finder(x, y):
    for fx, fy in finders:
        if fx <= x < fx + 7 and fy <= y < fy + 7:
            return True
    return False

# Layout: either full matrix clipped to circle, or square QR centered in circle.
if FULL_MATRIX:
    pad = 0
else:
    pad = n * 0.09  # dynamic padding around the QR square inside the circle
view = n + pad * 2
qr_x = pad
qr_y = pad

# SVG header
svg = []
svg.append(f'''<?xml version="1.0" encoding="UTF-8"?>''')
svg.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg" width="{DIAMETER_MM}mm" height="{DIAMETER_MM}mm" viewBox="0 0 {view} {view}">'''
)

# Circular clip + circular background
svg.append("<defs>")
svg.append(f'''  <clipPath id="clipCircle"><circle cx="{view/2}" cy="{view/2}" r="{view/2}"/></clipPath>''')
svg.append("</defs>")
circle_fill = QR_BG if FULL_MATRIX else BG
circle_stroke = f' stroke="{BG}"' if FULL_MATRIX else ""
svg.append(f'''<circle cx="{view/2}" cy="{view/2}" r="{view/2}" fill="{circle_fill}"{circle_stroke}/>''')

# Draw QR square + modules (clipped to circle)
svg.append(f'''<g clip-path="url(#clipCircle)">''')
if not FULL_MATRIX:
    svg.append(f'''  <rect x="{qr_x}" y="{qr_y}" width="{n}" height="{n}" fill="{QR_BG}"/>''')
for y in range(n):
    for x in range(n):
        if m[y][x] and not in_finder(x, y):
            svg.append(f'''  <rect x="{qr_x + x}" y="{qr_y + y}" width="1" height="1" fill="{FG}"/>''')

# Rounded finder “eyes” (outer blue, middle white, inner blue)
def finder(fx, fy):
    ox = qr_x + fx
    oy = qr_y + fy
    svg.append(f'''  <rect x="{ox}" y="{oy}" width="7" height="7" rx="1.6" ry="1.6" fill="{FG}"/>''')
    svg.append(f'''  <rect x="{ox+1}" y="{oy+1}" width="5" height="5" rx="1.2" ry="1.2" fill="{QR_BG}"/>''')
    svg.append(f'''  <rect x="{ox+2}" y="{oy+2}" width="3" height="3" rx="0.9" ry="0.9" fill="{FG}"/>''')

for fx, fy in finders:
    finder(fx, fy)

svg.append("</g>")
svg.append("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print(f"Wrote {OUT}")
