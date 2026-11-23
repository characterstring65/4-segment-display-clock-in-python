import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors

# Kleurenpalet voor passief reflecterend LCD-glas
LCD_BG = colors.HexColor('#d8e3d8')
BEZEL_BG = colors.HexColor('#1c2026')
SEG_AAN = colors.HexColor('#151828')
SEG_GRIJS = colors.HexColor('#7e8984')
SEG_UIT = colors.HexColor('#cad6ca')
LEVER_ACCENT = colors.HexColor('#151828')

CIJFER_MATRIX = {
    '0': ['S1'],
    '1': ['S4'],
    '2': ['S1', 'S3'],
    '3': ['S1', 'S3', 'S4'],
    '4': ['S2', 'S4'],
    '5': ['S1', 'S2', 'S3'],
    '6': ['S1', 'S2'],
    '7': ['S3', 'S4'],
    '8': ['S1', 'S2', 'S3', 'S4'],
    '9': ['S2', 'S3', 'S4']
}


def transformeer_punt(x, y, ox, oy, scale, cy=120.0, schuinte=0.20):
    nieuw_x = x + schuinte * (cy - y)
    # ReportLab heeft y=0 onderaan; spiegel y ten opzichte van top oy
    return ox + nieuw_x * scale, oy - y * scale


def teken_lijn(c, x1, y1, x2, y2, ox, oy, scale, kleur, dikte):
    tx1, ty1 = transformeer_punt(x1, y1, ox, oy, scale)
    tx2, ty2 = transformeer_punt(x2, y2, ox, oy, scale)
    c.setStrokeColor(kleur)
    c.setLineWidth(dikte * scale)
    c.setLineCap(1)  # Round cap
    c.line(tx1, ty1, tx2, ty2)


def teken_boog(c, cx, cy_arc, r_x, r_y, start_graden, extent_graden, ox, oy, scale, kleur, dikte):
    c.setStrokeColor(kleur)
    c.setLineWidth(dikte * scale)
    c.setLineCap(1)
    c.setLineJoin(1)
    p = c.beginPath()
    stappen = 36
    for i in range(stappen + 1):
        hoek_rad = math.radians(start_graden + (extent_graden * i / stappen))
        px = cx + r_x * math.cos(hoek_rad)
        py = cy_arc - r_y * math.sin(hoek_rad)
        tx, ty = transformeer_punt(px, py, ox, oy, scale)
        if i == 0:
            p.moveTo(tx, ty)
        else:
            p.lineTo(tx, ty)
    c.drawPath(p, stroke=1, fill=0)


def teken_digit(c, segs, ox, oy, scale, toon_uit=True, toon_levers=False):
    s1 = 'S1' in segs
    s2 = 'S2' in segs
    s3 = 'S3' in segs
    s4 = 'S4' in segs

    l1_left = toon_levers and (
        (s1 and not s2 and not s3 and not s4) or
        (s1 and s2 and not s3 and not s4) or
        (s1 and s2 and s3 and s4) or
        (s1 and s3 and not s2 and not s4)
    )
    l2_waist = toon_levers and (s1 and s3 and not s2 and not s4)

    w, h = 100.0, 200.0
    cy = 150.0

    # S1
    if s1 or toon_uit:
        k1 = SEG_AAN if s1 else SEG_UIT
        d1 = 16.0 if s1 else 1.2
        teken_boog(c, 34 + (w - 25) / 2, cy + (h / 2) / 2, (w - 10) / 2, (h / 2) / 2, 194, 126, ox, oy, scale, k1, d1)
        teken_lijn(c, 28, cy + 88 - 0.6 * h / 4, w - 68, cy + 78 - 0.3 * h / 2, ox, oy, scale, k1, d1)
        if not toon_levers:
            teken_lijn(c, 58, cy + 30 - 0.6 * h / 4, w - 40, cy + 30 - 0.3 * h / 2, ox, oy, scale, k1, d1)

    # S2
    if s2 or toon_uit:
        k2 = SEG_AAN if s2 else SEG_UIT
        d2 = 16.0 if s2 else 1.2
        teken_boog(
            c,
            25 + (w - 25) / 2,
            (cy + 20 - h / 2) + ((cy + 20) - (cy + 20 - h / 2)) / 2,
            (w - 25) / 2,
            ((cy + 20) - (cy + 20 - h / 2)) / 2,
            135, 70, ox, oy, scale, k2, d2
        )
        teken_lijn(c, 40, cy + 28 - 0.6 * h / 4, w - 62, cy + 28 - 0.3 * h / 2, ox, oy, scale, k2, d2)

    # S3
    if s3 or toon_uit:
        k3 = SEG_AAN if s3 else SEG_UIT
        d3 = 16.0 if s3 else 1.2
        teken_lijn(c, 48, cy + 10 - h / 2, w - 5, cy + 10 - h / 2, ox, oy, scale, k3, d3)
        teken_lijn(c, 40, cy - 60 - 0.6 * h / 4, w - 65, cy - 55 - 0.3 * h / 2, ox, oy, scale, k3, d3)
        teken_lijn(c, 105, cy - 22 - 0.6 * h / 4, w + 5, cy - 30 - 0.3 * h / 2, ox, oy, scale, k3, d3)

    # S4
    if s4 or toon_uit:
        k4 = SEG_AAN if s4 else SEG_UIT
        d4 = 16.0 if s4 else 1.2
        teken_lijn(c, w + 2, cy - h / 2 + 28, w, cy + h / 2 - 180, ox, oy, scale, k4, d4)
        teken_lijn(c, w - 1, cy - h / 2 + 62, w - 9, cy + h / 2 - 136, ox, oy, scale, k4, d4)
        teken_lijn(c, w + 8, cy - h / 2 + 158, 8 + w, cy + h / 2 - 26, ox, oy, scale, k4, d4)
        teken_lijn(c, 70, cy + 10 - 0.6 * h / 4, w - 22, cy - 1 - 0.3 * h / 2, ox, oy, scale, k4, d4)

        k4_acc = SEG_GRIJS if s4 else SEG_UIT
        d4_acc = 16.0 if s4 else 1.2
        teken_lijn(c, w - 10, cy + 10 - 0.6 * h / 4, w - 10, cy + 11 - 0.3 * h / 2, ox, oy, scale, k4_acc, d4_acc)

    # Overlap S2 & S4 (50% dambord-effect)
    if s2 or s4 or toon_uit:
        if s2 and s4:
            k_ov, d_ov = SEG_AAN, 16.0
        elif s2 or s4:
            k_ov, d_ov = SEG_GRIJS, 16.0
        else:
            k_ov, d_ov = SEG_UIT, 1.2
        teken_lijn(c, w + 8, cy - h / 2 + 150, w + 4, cy + h / 2 - 65, ox, oy, scale, k_ov, d_ov)
        teken_lijn(c, w - 1, cy - h / 2 + 120, w + 1, cy + h / 2 - 75, ox, oy, scale, k_ov, d_ov)

    # Overlap S3 & S4
    if s3 or s4 or toon_uit:
        if s3 and s4:
            k_ow, d_ow = SEG_AAN, 16.0
        elif s3 or s4:
            k_ow, d_ow = SEG_GRIJS, 16.0
        else:
            k_ow, d_ow = SEG_UIT, 1.2
        teken_lijn(c, w + 2, cy - h / 2 + 28, w, cy + h / 2 - 180, ox, oy, scale, k_ow, d_ow)

    # Optionele sub-segmenten (+L1 linkerboog & +L2 middenbalkje)
    if toon_levers:
        if l1_left or toon_uit:
            kl1 = LEVER_ACCENT if l1_left else SEG_UIT
            dl1 = 16.0 if l1_left else 1.2
            teken_boog(c, 34 + (w - 25) / 2, cy + (h / 2) / 2, (w - 10) / 2, (h / 2) / 2, 105, 60, ox, oy, scale, kl1, dl1)
        if l2_waist or toon_uit:
            kl2 = LEVER_ACCENT if l2_waist else SEG_UIT
            dl2 = 15.0 if l2_waist else 1.2
            teken_lijn(c, 105, cy - 36, 68, cy, ox, oy, scale, kl2, dl2)


def teken_multidigit_venster(c, x_left, y_top, tekst, digit_height_mm, toon_uit=True, toon_levers=False):
    # Visuele verticale spanne in lokale coördinaten loopt van y=45 tot y=236 (hoogte = 191 eenheden)
    scale = (digit_height_mm * mm) / 191.0
    pad_y = 2.4 * mm  # Gelijke boven- en ondermarge in elk LCD-venster
    pad_x = 3.2 * mm
    char_step = 112.0 * scale
    punct_step = 36.0 * scale

    totale_breedte = pad_x * 2
    for ch in tekst:
        totale_breedte += punct_step if ch in (':', '.') else char_step

    lcd_h = (digit_height_mm * mm) + pad_y * 2
    bezel_pad = 1.6 * mm

    # Donkere behuizingsrand (Bezel)
    c.setFillColor(BEZEL_BG)
    c.roundRect(
        x_left - bezel_pad,
        y_top - lcd_h - bezel_pad,
        totale_breedte + bezel_pad * 2,
        lcd_h + bezel_pad * 2,
        2.0 * mm,
        stroke=0,
        fill=1
    )

    # Groengrijs LCD-glasvlak
    c.setFillColor(LCD_BG)
    c.rect(x_left, y_top - lcd_h, totale_breedte, lcd_h, stroke=0, fill=1)

    # Top-anker zodanig dat de hoogste streek (y=45) exact pad_y onder y_top start
    oy = y_top - pad_y + 45.0 * scale
    cur_x = x_left + pad_x

    for ch in tekst:
        if ch == ':':
            c.setFillColor(SEG_AAN)
            r = 8.5 * scale
            cx_dot = cur_x + punct_step * 0.45
            _, ty1 = transformeer_punt(0, 105.0, 0, oy, scale)
            _, ty2 = transformeer_punt(0, 175.0, 0, oy, scale)
            c.circle(cx_dot, ty1, r, stroke=0, fill=1)
            c.circle(cx_dot, ty2, r, stroke=0, fill=1)
            cur_x += punct_step
        elif ch == '.':
            c.setFillColor(SEG_AAN)
            r = 8.5 * scale
            cx_dot = cur_x + punct_step * 0.35
            _, ty_dot = transformeer_punt(0, 224.0, 0, oy, scale)
            c.circle(cx_dot, ty_dot, r, stroke=0, fill=1)
            cur_x += punct_step
        elif ch in CIJFER_MATRIX:
            ox = cur_x - 12.0 * scale
            teken_digit(c, CIJFER_MATRIX[ch], ox, oy, scale, toon_uit=toon_uit, toon_levers=toon_levers)
            cur_x += char_step

    return x_left + totale_breedte + bezel_pad, y_top - lcd_h - bezel_pad


def bouw_pdf(bestandsnaam="4segment_multidigit_lcd_sheet.pdf"):
    width, height = A4
    c = canvas.Canvas(bestandsnaam, pagesize=A4)
    c.setTitle("4-Segment Multi-Digit LCD 1:1 Print Sheet")

    margin = 16 * mm
    y = height - 18 * mm

    # Titel
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor('#151828'))
    c.drawString(margin, y, "4-Segment Fluid Matrix — 1:1 Multi-Digit LCD Scale Sheet")
    y -= 5.5 * mm
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor('#4a5568'))
    c.drawString(margin, y, "Print at 100% / Actual Size (no scaling) to inspect true physical multi-digit LCD legibility.")

    # 50 mm Kalibratieliniaal rechtsboven
    rx = width - margin - 50 * mm
    ry = height - 21 * mm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.line(rx, ry, rx + 50 * mm, ry)
    for i in range(6):
        tx = rx + i * 10 * mm
        c.line(tx, ry, tx, ry + 2.5 * mm)
        c.setFont("Helvetica", 6.5)
        c.drawCentredString(tx, ry + 3.5 * mm, f"{i*10}")
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(rx + 25 * mm, ry - 3.2 * mm, "CALIBRATION: 50 mm")

    y -= 10 * mm

    # Sectie 1: Doorlopende 0123456789 reeksen
    stroken = [
        ("1. Full 10-Digit Strip — 10 mm Digit Height (Pure 4-Segment Matrix + Off-State Segments)", "0123456789", 10.0, True, False),
        ("2. Full 10-Digit Strip — 8 mm Digit Height (High-Contrast Active Segments Only)", "0123456789", 8.0, False, False),
        ("3. Full 10-Digit Strip — 6 mm Compact Pocket Scale (Pure 4-Segment Matrix)", "0123456789", 6.0, True, False),
        ("4. Full 10-Digit Strip — 10 mm Height with +L1 (60° Left Arc) & +L2 (Digit 2 Waist)", "0123456789", 10.0, True, True),
    ]

    for titel, tekst, d_mm, toon_uit, toon_levers in stroken:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.HexColor('#1e2126'))
        c.drawString(margin, y, titel)
        y -= 2.5 * mm
        _, y_bottom = teken_multidigit_venster(c, margin + 1.6 * mm, y, tekst, d_mm, toon_uit=toon_uit, toon_levers=toon_levers)
        y = y_bottom - 7.5 * mm

    # Sectie 2: Praktijkvoorbeelden op ware grootte
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor('#151828'))
    c.drawString(margin, y, "5. Real-World Multi-Digit Applications (1:1 Physical Scale)")
    y -= 6 * mm

    # Rij A: Tafelklok (14:38:52) en Polshorloge (20:49) op 7.5 mm
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(margin, y, "6-Digit Desk Clock (7.5 mm)")
    c.drawString(margin + 96 * mm, y, "4-Digit Wrist Watch (7.5 mm)")
    y -= 2.5 * mm
    _, yb1 = teken_multidigit_venster(c, margin + 1.6 * mm, y, "14:38:52", 7.5, toon_uit=True, toon_levers=False)
    _, yb2 = teken_multidigit_venster(c, margin + 97.6 * mm, y, "20:49", 7.5, toon_uit=True, toon_levers=False)
    y = min(yb1, yb2) - 7.5 * mm

    # Rij B: SMD Multimeterpen (1.847) en Rekenmachinehorloge (31415926)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(margin, y, "3½-Digit SMD Probe Pen (7.5 mm)")
    c.drawString(margin + 68 * mm, y, "8-Digit Calculator Watch (6.5 mm)")
    y -= 2.5 * mm
    _, yb3 = teken_multidigit_venster(c, margin + 1.6 * mm, y, "1.847", 7.5, toon_uit=True, toon_levers=False)
    _, yb4 = teken_multidigit_venster(c, margin + 69.6 * mm, y, "31415926", 6.5, toon_uit=False, toon_levers=False)
    y = min(yb3, yb4) - 7.5 * mm

    # Rij C: Ultra-compacte 4.5 mm micro-displays
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor('#334155'))
    c.drawString(margin, y, "Micro Ring Watch (4.5 mm)")
    c.drawString(margin + 54 * mm, y, "Micro Sensor Readout (4.5 mm)")
    c.drawString(margin + 114 * mm, y, "Enhanced Sub-Segment Micro (4.5 mm)")
    y -= 2.5 * mm
    _, yb5 = teken_multidigit_venster(c, margin + 1.6 * mm, y, "09:27", 4.5, toon_uit=False, toon_levers=False)
    _, yb6 = teken_multidigit_venster(c, margin + 55.6 * mm, y, "5.603", 4.5, toon_uit=True, toon_levers=False)
    _, yb7 = teken_multidigit_venster(c, margin + 115.6 * mm, y, "7890", 4.5, toon_uit=False, toon_levers=True)

    c.showPage()
    c.save()
    print(f"Succesvol gegenereerd: {bestandsnaam}")


if __name__ == "__main__":
    bouw_pdf()
