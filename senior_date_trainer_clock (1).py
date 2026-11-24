import tkinter as tk
from datetime import datetime, timedelta
import math
import random

class SeniorDateTrainerClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Senior Datum-Trainer Wandklok & 4-Knops Afstandsbediening")
        self.root.configure(bg="#1c1f24")
        self.root.resizable(False, False)

        self.clock_bg = "#121519"
        self.time_on = "#52e396"
        self.time_off = "#1d242a"
        self.date_dark_bg = "#14171b"
        self.date_lit_bg = "#1d2b24"
        self.date_on = "#ffd166"
        self.date_off = "#1b2026"

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

        self.start_segment = {
            '0': 'S1',
            '1': 'S4',
            '2': 'S3',
            '3': 'S1',
            '4': 'S2',
            '5': 'S3',
            '6': 'S1',
            '7': 'S4',
            '8': 'S2',
            '9': 'S3'
        }

        self.score = 0
        self.datum_zichtbaar = False
        self.oefen_modus = False
        self.huidige_datum = datetime.now()
        self.pogingen = 0

        wall_frame = tk.Frame(root, bg="#252930", bd=4, relief="ridge", padx=18, pady=14)
        wall_frame.pack(padx=16, pady=(16, 10), fill="x")

        top_bar = tk.Frame(wall_frame, bg="#252930")
        top_bar.pack(fill="x", pady=(0, 8))

        tk.Label(
            top_bar,
            text="WANDKLOK",
            font=("Helvetica", 11, "bold"),
            fg="#9aa5b4",
            bg="#252930"
        ).pack(side="left")

        self.score_label = tk.Label(
            top_bar,
            text="Punten: 0",
            font=("Helvetica", 12, "bold"),
            fg="#ffd166",
            bg="#252930"
        )
        self.score_label.pack(side="right")

        self.time_canvas = tk.Canvas(
            wall_frame, width=380, height=115, bg=self.clock_bg,
            highlightthickness=2, highlightbackground="#3a404a"
        )
        self.time_canvas.pack(pady=(0, 10))

        self.date_canvas = tk.Canvas(
            wall_frame, width=380, height=95, bg=self.date_dark_bg,
            highlightthickness=2, highlightbackground="#3a404a"
        )
        self.date_canvas.pack()

        self.status_label = tk.Label(
            wall_frame,
            text="Raad het startsegment van het laatste cijfer van de dag!",
            font=("Helvetica", 10, "bold"),
            fg="#e0e6ed",
            bg="#252930",
            pady=8
        )
        self.status_label.pack()

        remote_frame = tk.Frame(root, bg="#2d323b", bd=3, relief="raised", padx=18, pady=14)
        remote_frame.pack(padx=16, pady=(0, 12), fill="x")

        tk.Label(
            remote_frame,
            text="AFSTANDSBEDIENING (1 DRUK OP HET STARTSEGMENT)",
            font=("Helvetica", 10, "bold"),
            fg="#cbd5e1",
            bg="#2d323b"
        ).pack(pady=(0, 10))

        btn_grid = tk.Frame(remote_frame, bg="#2d323b")
        btn_grid.pack()

        knoppen = (
            ("S2", "Cijfers: 4, 8\n(Boog linksboven)", 0, 0),
            ("S3", "Cijfers: 2, 5, 9\n(Bovenbalk)", 0, 1),
            ("S1", "Cijfers: 0, 3, 6\n(Boog linksonder)", 1, 0),
            ("S4", "Cijfers: 1, 7\n(Rechterstam)", 1, 1),
        )

        self.knop_widgets = {}
        for seg, hint, r, c in knoppen:
            btn = tk.Button(
                btn_grid,
                text=f"{seg}\n{hint}",
                font=("Helvetica", 11, "bold"),
                width=18,
                height=3,
                bg="#3b4252",
                fg="#f8fafc",
                activebackground="#52e396",
                activeforeground="#121519",
                relief="raised",
                bd=3,
                cursor="hand2",
                command=lambda s=seg: self.druk_knop(s)
            )
            btn.grid(row=r, column=c, padx=8, pady=6)
            self.knop_widgets[seg] = btn

        ctrl_frame = tk.Frame(root, bg="#1c1f24", pady=6)
        ctrl_frame.pack(padx=16, pady=(0, 14), fill="x")

        self.mode_btn = tk.Button(
            ctrl_frame,
            text="Oefenmodus: Willekeurige dag",
            font=("Helvetica", 9, "bold"),
            bg="#374151",
            fg="#f3f4f6",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.nieuwe_oefendag
        )
        self.mode_btn.pack(side="left")

        self.today_btn = tk.Button(
            ctrl_frame,
            text="Terug naar Vandaag",
            font=("Helvetica", 9, "bold"),
            bg="#374151",
            fg="#f3f4f6",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.zet_vandaag
        )
        self.today_btn.pack(side="right")

        self.update_klok()

    def transformeer_punt(self, x, y, cy, schuinte=0.20, schaal=0.45, ox=0, oy=0):
        nieuw_x = x + schuinte * (cy - y)
        return ox + nieuw_x * schaal, oy + y * schaal

    def teken_lijn(self, canvas, x1, y1, x2, y2, kleur, dikte, cy, schaal, ox, oy):
        tx1, ty1 = self.transformeer_punt(x1, y1, cy, 0.20, schaal, ox, oy)
        tx2, ty2 = self.transformeer_punt(x2, y2, cy, 0.20, schaal, ox, oy)
        canvas.create_line(tx1, ty1, tx2, ty2, fill=kleur, width=dikte * schaal, capstyle="round")

    def teken_boog(self, canvas, cx, cy_arc, rx, ry, start_g, extent_g, kleur, dikte, cy, schaal, ox, oy):
        punten = list()
        stappen = 24
        for i in range(stappen + 1):
            rad = math.radians(start_g + (extent_g * i / stappen))
            px = cx + rx * math.cos(rad)
            py = cy_arc - ry * math.sin(rad)
            punten.append(self.transformeer_punt(px, py, cy, 0.20, schaal, ox, oy))
        for i in range(len(punten) - 1):
            canvas.create_line(punten[i], punten[i+1], fill=kleur, width=dikte * schaal, capstyle="round")

    def teken_4seg_cijfer(self, canvas, teken, aan_kleur, uit_kleur, schaal, ox, oy):
        segs = self.cijfer_matrix.get(teken, ())
        s1, s2, s3, s4 = 'S1' in segs, 'S2' in segs, 'S3' in segs, 'S4' in segs
        w, h, cy = 100, 200, 150

        k1, d1 = (aan_kleur, 16) if s1 else (uit_kleur, 1.5)
        self.teken_boog(canvas, 34 + (w - 25)/2, cy + (h/2)/2, (w - 10)/2, (h/2)/2, 194, 126, k1, d1, cy, schaal, ox, oy)
        self.teken_lijn(canvas, 28, cy + 88 - 0.6*h/4, w - 68, cy + 78 - 0.3*h/2, k1, d1, cy, schaal, ox, oy)
        self.teken_lijn(canvas, 58, cy + 30 - 0.6*h/4, w - 40, cy + 30 - 0.3*h/2, k1, d1, cy, schaal, ox, oy)

        k2, d2 = (aan_kleur, 16) if s2 else (uit_kleur, 1.5)
        self.teken_boog(canvas, 25 + (w - 25)/2, (cy + 20 - h/2) + ((cy + 20) - (cy + 20 - h/2))/2, (w - 25)/2, ((cy + 20) - (cy + 20 - h/2))/2, 135, 70, k2, d2, cy, schaal, ox, oy)
        self.teken_lijn(canvas, 40, cy + 28 - 0.6*h/4, w - 62, cy + 28 - 0.3*h/2, k2, d2, cy, schaal, ox, oy)
        self.teken_lijn(canvas, w + 8, cy - h/2 + 150, w + 4, cy + h/2 - 65, k2, d2, cy, schaal, ox, oy)
        self.teken_lijn(canvas, w - 1, cy - h/2 + 120, w + 1, cy + h/2 - 75, k2, d2, cy, schaal, ox, oy)
        self.teken_lijn(canvas, w + 8, cy - h/2 + 158, 8 + w, cy + h/2 - 26, k2, d2, cy, schaal, ox, oy)

        k3, d3 = (aan_kleur, 16) if s3 else (uit_kleur, 1.5)
        self.teken_lijn(canvas, 48, cy + 10 - h/2, w - 5, cy + 10 - h/2, k3, d3, cy, schaal, ox, oy)
        self.teken_lijn(canvas, 40, cy - 60 - 0.6*h/4, w - 65, cy - 55 - 0.3*h/2, k3, d3, cy, schaal, ox, oy)
        self.teken_lijn(canvas, 105, cy - 22 - 0.6*h/4, w + 5, cy - 30 - 0.3*h/2, k3, d3, cy, schaal, ox, oy)
        self.teken_lijn(canvas, w + 2, cy - h/2 + 28, w, cy + h/2 - 180, k3, d3, cy, schaal, ox, oy)

        k4, d4 = (aan_kleur, 16) if s4 else (uit_kleur, 1.5)
        self.teken_lijn(canvas, w + 2, cy - h/2 + 28, w, cy + h/2 - 180, k4, d4, cy, schaal, ox, oy)
        self.teken_lijn(canvas, w - 1, cy - h/2 + 62, w - 9, cy + h/2 - 136, k4, d4, cy, schaal, ox, oy)
        self.teken_lijn(canvas, w + 8, cy - h/2 + 158, 8 + w, cy + h/2 - 26, k4, d4, cy, schaal, ox, oy)
        self.teken_lijn(canvas, 70, cy + 10 - 0.6*h/4, w - 22, cy - 1 - 0.3*h/2, k4, d4, cy, schaal, ox, oy)
        self.teken_lijn(canvas, w + 8, cy - h/2 + 150, w + 4, cy + h/2 - 65, k4, d4, cy, schaal, ox, oy)
        self.teken_lijn(canvas, w - 1, cy - h/2 + 120, w + 1, cy + h/2 - 75, k4, d4, cy, schaal, ox, oy)
        self.teken_lijn(canvas, 105, cy - 22 - 0.6*h/4, w + 5, cy - 30 - 0.3*h/2, k4, d4, cy, schaal, ox, oy)

    def teken_tijd(self, tijd_str):
        self.time_canvas.delete("all")
        posities = (24, 98, 198, 272)
        for idx, ch in enumerate(tijd_str):
            self.teken_4seg_cijfer(self.time_canvas, ch, self.time_on, self.time_off, 0.44, posities[idx], -10)

        if int(datetime.now().second) % 2 == 0:
            self.time_canvas.create_oval(182, 42, 189, 49, fill=self.time_on, outline="")
            self.time_canvas.create_oval(178, 68, 185, 75, fill=self.time_on, outline="")

    def teken_datum(self):
        self.date_canvas.delete("all")
        if not self.datum_zichtbaar:
            self.date_canvas.configure(bg=self.date_dark_bg)
            self.date_canvas.create_text(
                190, 48,
                text="DATUM VERBORGEN — KIES STARTSEGMENT",
                font=("Helvetica", 10, "bold"),
                fill="#4b5563"
            )
            return

        self.date_canvas.configure(bg=self.date_lit_bg)
        dag_str = f"{self.huidige_datum.day:02d}"
        maand_str = f"{self.huidige_datum.month:02d}"

        posities = (18, 78, 195, 255)
        cijfers = dag_str + maand_str
        for idx, ch in enumerate(cijfers):
            self.teken_4seg_cijfer(self.date_canvas, ch, self.date_on, self.date_off, 0.35, posities[idx], -8)

        self.date_canvas.create_line(164, 52, 178, 52, fill=self.date_on, width=4, capstyle="round")

        self.date_canvas.create_text(
            335, 48,
            text=self.huidige_datum.strftime("%d-%m\n%Y"),
            font=("Helvetica", 11, "bold"),
            fill="#a7f3d0"
        )

    def druk_knop(self, gekozen_seg):
        if self.datum_zichtbaar:
            self.status_label.configure(
                text="De datum staat al aan! Klik op 'Willekeurige dag' om nog eens te spelen.",
                fg="#a7f3d0"
            )
            return

        dag_cijfer = str(self.huidige_datum.day)[-1]
        juiste_seg = self.start_segment.get(dag_cijfer)
        self.pogingen += 1

        if gekozen_seg == juiste_seg:
            self.datum_zichtbaar = True
            self.score += 1
            self.score_label.configure(text=f"Punten: {self.score}")
            self.status_label.configure(
                text=f"Goed geraden! Dag {self.huidige_datum.day} begint met {juiste_seg} (+1 punt).",
                fg="#52e396"
            )
            self.teken_datum()
        else:
            self.status_label.configure(
                text=f"Niet {gekozen_seg} — het scherm blijft donker. Probeer nog eens!",
                fg="#fca5a5"
            )

    def nieuwe_oefendag(self):
        self.oefen_modus = True
        self.datum_zichtbaar = False
        self.pogingen = 0
        offset = random.randint(-15, 15)
        if offset == 0:
            offset = 3
        self.huidige_datum = datetime.now() + timedelta(days=offset)
        self.status_label.configure(
            text="Oefendag gekozen! Raad het startsegment van de dag van de maand.",
            fg="#ffd166"
        )
        self.teken_datum()

    def zet_vandaag(self):
        self.oefen_modus = False
        self.datum_zichtbaar = False
        self.pogingen = 0
        self.huidige_datum = datetime.now()
        self.status_label.configure(
            text="Vandaag ingesteld! Raad het startsegment van het laatste cijfer van vandaag.",
            fg="#e0e6ed"
        )
        self.teken_datum()

    def update_klok(self):
        nu = datetime.now()
        if not self.oefen_modus and nu.day != self.huidige_datum.day:
            self.huidige_datum = nu
            self.datum_zichtbaar = False

        self.teken_tijd(nu.strftime("%H%M"))
        if not self.datum_zichtbaar:
            self.teken_datum()

        self.root.after(500, self.update_klok)

if __name__ == "__main__":
    root = tk.Tk()
    app = SeniorDateTrainerClock(root)
    root.mainloop()
