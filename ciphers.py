import tkinter as tk
import math

class Tier1AllDigitsPreview:
    def __init__(self, root):
        self.root = root
        self.root.title("Tier 1: Raw Non-Overlapping 4-Segment Digits (0–9) — Desktop Clock Style")
        self.root.configure(bg='#111111')
        self.root.resizable(False, False)

        self.cijfer_matrix = {
            '0': ('S1',),
            '1': ('S4',),
            '2': ('S1', 'S3'),
            '3': ('S1', 'S3', 'S4'),
            '4': ('S2', 'S4'),
            '5': ('S1', 'S2', 'S3'),
            '6': ('S1', 'S2'),
            '7': ('S3', 'S4'),
            '8': ('S1', 'S2', 'S3', 'S4'),
            '9': ('S2', 'S3', 'S4')
        }

        tk.Label(
            root,
            text="TIER 1 — PURE 4-SEGMENT CONNECTED CLOCK STYLE (DIGITS 0–9)",
            font=("Helvetica", 12, "bold"),
            fg="#ff4d4d",
            bg="#111111",
            pady=14
        ).pack()

        grid_frame = tk.Frame(root, bg='#111111', padx=20, pady=4)
        grid_frame.pack()

        for idx in range(10):
            cijfer = str(idx)
            segs = self.cijfer_matrix[cijfer]

            card = tk.Frame(grid_frame, bg='#161616', padx=8, pady=8, relief='solid', bd=1)
            card.grid(row=idx // 5, column=idx % 5, padx=8, pady=8)

            canvas = tk.Canvas(card, width=140, height=215, bg='#111111', highlightthickness=0)
            canvas.pack()

            self.teken_cijfer(canvas, 14, cijfer)

            info = f"Digit {cijfer}\n{' + '.join(segs)}"
            tk.Label(
                card,
                text=info,
                font=("Helvetica", 9, "bold"),
                fg="#cccccc",
                bg="#161616",
                pady=4
            ).pack()

        tk.Label(
            root,
            text="Red = Active Driven Strokes (S1–S4) with Calligraphic Hairline Connectors   |   Dark Gray = Inactive Segments",
            font=("Helvetica", 9),
            fg="#777777",
            bg="#111111",
            pady=12
        ).pack()

    def transformeer_punt(self, x, y, cy=150, schuinte=0.20, schaal=0.72, ox=0, oy=-20):
        nieuw_x = x + schuinte * (cy - y)
        return ox + nieuw_x * schaal, oy + y * schaal

    def teken_schuine_lijn(self, canvas, x1, y1, x2, y2, kleur, dikte):
        tx1, ty1 = self.transformeer_punt(x1, y1)
        tx2, ty2 = self.transformeer_punt(x2, y2)
        canvas.create_line(tx1, ty1, tx2, ty2, fill=kleur, width=dikte * 0.72, capstyle='round')

    def teken_schuine_boog(self, canvas, cx, cy, r_x, r_y, start_graden, extent_graden, kleur, dikte):
        punten = []
        stappen = 30
        for i in range(stappen + 1):
            hoek_rad = math.radians(start_graden + (extent_graden * i / stappen))
            px = cx + r_x * math.cos(hoek_rad)
            py = cy - r_y * math.sin(hoek_rad)
            punten.append(self.transformeer_punt(px, py))
        for i in range(len(punten) - 1):
            canvas.create_line(punten[i], punten[i+1], fill=kleur, width=dikte * 0.72, capstyle='round', joinstyle='round')

    def teken_schuine_line_direct(self, canvas, exact_x1, exact_y1, x2, y2, kleur, dikte):
        tx1, ty1 = self.transformeer_punt(exact_x1, exact_y1, cy=150)
        tx2, ty2 = self.transformeer_punt(x2, y2)
        canvas.create_line(tx1, ty1, tx2, ty2, fill=kleur, width=dikte * 0.72, capstyle='round')

    def teken_segment(self, canvas, x_offset, segment_naam, actief):
        w, h = 100, 200
        cy = 150
        kleur = '#ff1e1e' if actief else '#222222'
        dikte = 14 if actief else 1.2
        dikte_verbinding = 1.0 if actief else 1.2

        if segment_naam == 'S1':
            cx_boog = x_offset + 34 + (w - 25) / 2
            cy_boog = cy + (h / 2) / 2
            r_x = (w - 10) / 2
            r_y = (h / 2) / 2
            self.teken_schuine_boog(canvas, cx_boog, cy_boog, r_x, r_y, 194, 126, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + 28, cy + 88 - 0.6 * h/4, x_offset + w - 68, cy + 78 - 0.3 * h/2, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + 58, cy + 30 - 0.6 * h/4, x_offset + w - 40, cy + 30 - 0.3 * h/2, kleur, dikte)
            boog_start_x = cx_boog + r_x * math.cos(math.radians(194))
            boog_start_y = cy_boog - r_y * math.sin(math.radians(194))
            self.teken_schuine_line_direct(canvas, boog_start_x, boog_start_y, x_offset + 28, cy + 88 - 0.6 * h/4, kleur, dikte_verbinding)
            self.teken_schuine_lijn(canvas, x_offset + w - 68, cy + 78 - 0.3 * h/2, x_offset + 58, cy + 30 - 0.6 * h/4, kleur, dikte_verbinding)

        elif segment_naam == 'S2':
            cx_boog = x_offset + 25 + (w - 25) / 2
            cy_boog = (cy + 20 - h/2) + ((cy + 20) - (cy + 20 - h/2)) / 2
            r_x = (w - 25) / 2
            r_y = ((cy + 20) - (cy + 20 - h/2)) / 2
            self.teken_schuine_boog(canvas, cx_boog, cy_boog, r_x, r_y, 135, 70, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + 40, cy + 28 - 0.6 * h/4, x_offset + w - 52, cy + 28 - 0.3 * h/2, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + w + 8, cy - h/2 + 150, x_offset + w + 4, cy + h/2 - 65, kleur, dikte)
            boog_onder_x = cx_boog + r_x * math.cos(math.radians(205))
            boog_onder_y = cy_boog - r_y * math.sin(math.radians(205))
            self.teken_schuine_line_direct(canvas, boog_onder_x, boog_onder_y, x_offset + 40, cy + 28 - 0.6 * h/4, kleur, dikte_verbinding)
            boog_boven_x = cx_boog + r_x * math.cos(math.radians(135))
            boog_boven_y = cy_boog - r_y * math.sin(math.radians(135))
            self.teken_schuine_line_direct(canvas, boog_boven_x, boog_boven_y, x_offset + w + 8, cy - h/2 + 150, kleur, dikte_verbinding)

        elif segment_naam == 'S3':
            self.teken_schuine_lijn(canvas, x_offset + 48, cy + 10 - h/2, x_offset + w - 5, cy + 10 - h/2, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + 40, cy - 60 - 0.6 * h/4, x_offset + w - 65, cy - 55 - 0.3 * h/2, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + 90, cy - 18 - 0.6 * h/4, x_offset + w - 4, cy - 30 - 0.3 * h/2, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + 40, cy - 60 - 0.6 * h/4, x_offset + 48, cy + 10 - h/2, kleur, dikte_verbinding)
            self.teken_schuine_lijn(canvas, x_offset + w - 5, cy + 10 - h/2, x_offset + 90, cy - 18 - 0.6 * h/4, kleur, dikte_verbinding)

        elif segment_naam == 'S4':
            self.teken_schuine_lijn(canvas, x_offset + w - 3, cy - h/2 + 120, x_offset + w, cy + h/2 - 75, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + w + 2, cy - h/2 + 28, x_offset + w, cy + h/2 - 180, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + w + 1, cy - h/2 + 62, x_offset + w, cy + h/2 - 140, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + w + 8, cy - h/2 + 158, x_offset + 8 + w, cy + h/2 - 26, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + 70, cy + 10 - 0.6 * h/4, x_offset + w - 22, cy - 1 - 0.3 * h/2, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + w - 10, cy + 10 - 0.6 * h/4, x_offset + w - 10, cy + 11 - 0.3 * h/2, kleur, dikte)
            self.teken_schuine_lijn(canvas, x_offset + w + 2, cy - h/2 + 28, x_offset + w + 1, cy - h/2 + 62, kleur, dikte_verbinding)
            self.teken_schuine_lijn(canvas, x_offset + w, cy + h/2 - 140, x_offset + w - 22, cy - 1 - 0.3 * h/2, kleur, dikte_verbinding)
            self.teken_schuine_lijn(canvas, x_offset + 70, cy + 10 - 0.6 * h/4, x_offset + w - 10, cy + 10 - 0.6 * h/4, kleur, dikte_verbinding)
            self.teken_schuine_lijn(canvas, x_offset + w - 10, cy + 11 - 0.3 * h/2, x_offset + w - 3, cy - h/2 + 120, kleur, dikte_verbinding)
            self.teken_schuine_lijn(canvas, x_offset + w + 18, cy - h/2 + 158, x_offset + w + 10, cy - h/2 + 158, kleur, dikte_verbinding)
            self.teken_schuine_lijn(canvas, x_offset + w + 8, cy + h/2 - 75, x_offset + w + 18, cy - h/2 + 158, kleur, dikte_verbinding)
            self.teken_schuine_lijn(canvas, x_offset + w, cy + h/2 - 75, x_offset + w + 8, cy + h/2 - 75, kleur, dikte_verbinding)

    def teken_cijfer(self, canvas, x_offset, cijfer):
        actieve_segmenten = self.cijfer_matrix.get(cijfer, ())
        for seg in ('S1', 'S2', 'S3', 'S4'):
            self.teken_segment(canvas, x_offset, seg, seg in actieve_segmenten)

if __name__ == "__main__":
    root = tk.Tk()
    app = Tier1AllDigitsPreview(root)
    root.mainloop()