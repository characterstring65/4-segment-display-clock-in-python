import tkinter as tk
import math

class ScoreboardLeverPreview:
    def __init__(self, root):
        self.root = root
        self.root.title("Mechanical Club Scoreboard - 4 Lamellae + Left-Arc Lever (L1) & Waist Lever (L2)")
        self.root.configure(bg='#2b2f36')
        self.root.resizable(False, False)

        self.lcd_bg = '#e4ece4'
        self.seg_aan = '#151828'
        self.seg_uit = '#cbd6cb'
        self.lever_kleur = '#d95f02'  # Warm orange showing the passive lever-driven extensions

        self.cijfer_matrix = {
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

        tk.Label(
            root,
            text="MECHANICAL CLUB SCOREBOARD: 4 MAIN LAMELLAE + PASSIVE LINKAGE LEVERS",
            font=("Helvetica", 12, "bold"),
            fg="#f0f4f8",
            bg="#2b2f36",
            pady=12
        ).pack()

        grid_frame = tk.Frame(root, bg='#2b2f36', padx=20, pady=5)
        grid_frame.pack()

        for idx, (cijfer, segs) in enumerate(self.cijfer_matrix.items()):
            card = tk.Frame(grid_frame, bg='#1e2126', padx=8, pady=8, relief='raised', bd=2)
            card.grid(row=idx // 5, column=idx % 5, padx=8, pady=8)

            canvas = tk.Canvas(card, width=140, height=190, bg=self.lcd_bg, highlightthickness=1, highlightbackground="#5a655a")
            canvas.pack()
            self.teken_cijfer(canvas, segs)

            s1, s2, s3, s4 = 'S1' in segs, 'S2' in segs, 'S3' in segs, 'S4' in segs
            l1 = (s1 and not s2 and not s3 and not s4) or (s1 and s2 and not s3 and not s4) or (s1 and s2 and s3 and s4)
            l2 = (s1 and s3 and not s2 and not s4)

            info = f"Digit {cijfer}\n{' + '.join(segs)}"
            if l1:
                info += " +L1(left)"
            if l2:
                info += " +L2"

            tk.Label(
                card,
                text=info,
                font=("Helvetica", 9, "bold"),
                fg="#ffd166" if (l1 or l2) else "#e0e6ed",
                bg="#1e2126",
                pady=4
            ).pack()

        tk.Label(
            root,
            text="Dark = Main Driven Lamellae (S1–S4)   |   Orange = Passive Lever Extensions (+L1 left-side S1 arc for 0, 6, 8; +L2 waist for 2)",
            font=("Helvetica", 9, "bold"),
            fg="#9aa5b4",
            bg="#2b2f36",
            pady=12
        ).pack()

    def transformeer_punt(self, x, y, cy=120, schuinte=0.20, schaal=0.68, ox=24, oy=18):
        nieuw_x = x + schuinte * (cy - y)
        return ox + nieuw_x * schaal, oy + y * schaal

    def teken_schuine_lijn(self, canvas, x1, y1, x2, y2, kleur, dikte):
        tx1, ty1 = self.transformeer_punt(x1, y1)
        tx2, ty2 = self.transformeer_punt(x2, y2)
        canvas.create_line(tx1, ty1, tx2, ty2, fill=kleur, width=dikte * 0.68, capstyle='round')

    def teken_schuine_boog(self, canvas, cx, cy, r_x, r_y, start_graden, extent_graden, kleur, dikte):
        punten = []
        stappen = 30
        for i in range(stappen + 1):
            hoek_rad = math.radians(start_graden + (extent_graden * i / stappen))
            px = cx + r_x * math.cos(hoek_rad)
            py = cy - r_y * math.sin(hoek_rad)
            punten.append(self.transformeer_punt(px, py))
        for i in range(len(punten) - 1):
            canvas.create_line(punten[i], punten[i+1], fill=kleur, width=dikte * 0.68, capstyle='round', joinstyle='round')

    def teken_cijfer(self, canvas, segs):
        s1 = 'S1' in segs
        s2 = 'S2' in segs
        s3 = 'S3' in segs
        s4 = 'S4' in segs

        l1_left_arc = (s1 and not s2 and not s3 and not s4) or (s1 and s2 and not s3 and not s4) or (s1 and s2 and s3 and s4)
        l2_waist = (s1 and s3 and not s2 and not s4)

        w, h = 100, 200
        cy = 150

        # S1
        k1 = self.seg_aan if s1 else self.seg_uit
        d1 = 16 if s1 else 1.2
        self.teken_schuine_boog(canvas, 34 + (w - 25) / 2, cy + (h / 2) / 2, (w - 10) / 2, (h / 2) / 2, 194, 126, k1, d1)
        self.teken_schuine_lijn(canvas, 28, cy + 88 - 0.6 * h/4, w - 68, cy + 78 - 0.3 * h/2, k1, d1)
        self.teken_schuine_lijn(canvas, 58, cy + 30 - 0.6 * h/4, w - 40, cy + 30 - 0.3 * h/2, k1, d1)

        # S2
        k2 = self.seg_aan if s2 else self.seg_uit
        d2 = 16 if s2 else 1.2
        self.teken_schuine_boog(canvas, 25 + (w - 25) / 2, (cy + 20 - h/2) + ((cy + 20) - (cy + 20 - h/2)) / 2, (w - 25) / 2, ((cy + 20) - (cy + 20 - h/2)) / 2, 135, 70, k2, d2)
        self.teken_schuine_lijn(canvas, 40, cy + 28 - 0.6 * h/4, w - 62, cy + 28 - 0.3 * h/2, k2, d2)
        self.teken_schuine_lijn(canvas, w + 8, cy - h/2 + 150, w + 4, cy + h/2 - 65, k2, d2)
        self.teken_schuine_lijn(canvas, w - 1, cy - h/2 + 120, w + 1, cy + h/2 - 75, k2, d2)
        self.teken_schuine_lijn(canvas, w + 8, cy - h/2 + 158, 8 + w, cy + h/2 - 26, k2, d2)

        # S3
        k3 = self.seg_aan if s3 else self.seg_uit
        d3 = 16 if s3 else 1.2
        self.teken_schuine_lijn(canvas, 48, cy + 10 - h/2, w - 5, cy + 10 - h/2, k3, d3)
        self.teken_schuine_lijn(canvas, 40, cy - 60 - 0.6 * h/4, w - 65, cy - 55 - 0.3 * h/2, k3, d3)
        self.teken_schuine_lijn(canvas, 105, cy - 22 - 0.6 * h/4, w + 5, cy - 30 - 0.3 * h/2, k3, d3)
        self.teken_schuine_lijn(canvas, w + 2, cy - h/2 + 28, w, cy + h/2 - 180, k3, d3)

        # S4
        k4 = self.seg_aan if s4 else self.seg_uit
        d4 = 16 if s4 else 1.2
        self.teken_schuine_lijn(canvas, w + 2, cy - h/2 + 28, w, cy + h/2 - 180, k4, d4)
        self.teken_schuine_lijn(canvas, w - 1, cy - h/2 + 62, w - 9, cy + h/2 - 136, k4, d4)
        self.teken_schuine_lijn(canvas, w + 8, cy - h/2 + 158, 8 + w, cy + h/2 - 26, k4, d4)
        self.teken_schuine_lijn(canvas, 70, cy + 10 - 0.6 * h/4, w - 22, cy - 1 - 0.3 * h/2, k4, d4)
        self.teken_schuine_lijn(canvas, w + 8, cy - h/2 + 150, w + 4, cy + h/2 - 65, k4, d4)
        self.teken_schuine_lijn(canvas, w - 1, cy - h/2 + 120, w + 1, cy + h/2 - 75, k4, d4)
        self.teken_schuine_lijn(canvas, 105, cy - 22 - 0.6 * h/4, w + 5, cy - 30 - 0.3 * h/2, k4, d4)

        # L1: Extra stukje cirkel van S1 aan de linkerkant (bij 0, 6 en 8)
        kl1 = self.lever_kleur if l1_left_arc else self.seg_uit
        dl1 = 16 if l1_left_arc else 1.2
        self.teken_schuine_boog(canvas, 34 + (w - 25) / 2, cy + (h / 2) / 2, (w - 10) / 2, (h / 2) / 2, 60, 110, kl1, dl1)

        # L2: Middenbalkje bij 2
        kl2 = self.lever_kleur if l2_waist else self.seg_uit
        dl2 = 15 if l2_waist else 1.2
        self.teken_schuine_lijn(canvas, 95, cy - 26, 36, cy + 36, kl2, dl2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreboardLeverPreview(root)
    root.mainloop()
