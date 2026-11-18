import tkinter as tk
import math

class PolsTelefoonKiezer:
    def __init__(self, root):
        self.root = root
        self.root.title("4-Segment Polstelefoon Kiezer (S2-First Protocol)")
        self.root.geometry("420x580")
        self.root.configure(bg="#1c1f26")
        self.root.resizable(False, False)

        # Kleurenpalet (Smartwatch / LCD stijl)
        self.bg_horloge = "#252932"
        self.lcd_bg = "#d8e3d8"
        self.segment_aan = "#151828"
        self.segment_grijs = "#7e8984"
        self.segment_uit = "#cad6ca"
        self.knop_bg = "#323846"
        self.knop_actief = "#4a5368"

        # Status variabelen
        self.telefoonnummer = ""
        self.actieve_segmenten = set()
        self.s2_is_eerste = False

        # Cijfer-lookup voor herkenning van getekende segmenten
        self.patroon_naar_cijfer = {
            frozenset(['S1']): '0',
            frozenset(['S4']): '1',
            frozenset(['S1', 'S3']): '2',
            frozenset(['S1', 'S3', 'S4']): '3',
            frozenset(['S2', 'S4']): '4',
            frozenset(['S1', 'S2', 'S3']): '5',
            frozenset(['S1', 'S2']): '6',
            frozenset(['S3', 'S4']): '7',
            frozenset(['S1', 'S2', 'S3', 'S4']): '8',
            frozenset(['S2', 'S3', 'S4']): '9'
        }

        self.cijfer_naar_patroon = {v: list(k) for k, v in self.patroon_naar_cijfer.items()}

        self.bouw_ui()
        self.teken_alles()

    def bouw_ui(self):
        # Buitenrand van het horloge
        horloge_frame = tk.Frame(self.root, bg=self.bg_horloge, bd=3, relief="ridge")
        horloge_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Titel / Instructie bovenin
        lbl_titel = tk.Label(
            horloge_frame,
            text="4-SEGMENT WRIST DIALER",
            font=("Helvetica", 11, "bold"),
            fg="#a0aab8",
            bg=self.bg_horloge
        )
        lbl_titel.pack(pady=(12, 6))

        # 1. GROOT DISPLAY VOOR HET TELEFOONNUMMER
        self.nummer_canvas = tk.Canvas(
            horloge_frame,
            width=340,
            height=95,
            bg=self.lcd_bg,
            highlightthickness=2,
            highlightbackground="#8a998a"
        )
        self.nummer_canvas.pack(pady=(5, 10))

        # Statusbalk voor directe feedback
        self.status_label = tk.Label(
            horloge_frame,
            text="Teken een cijfer (klik op het venster voor S2 of Enter)",
            font=("Helvetica", 9),
            fg="#8fd19e",
            bg=self.bg_horloge
        )
        self.status_label.pack(pady=(0, 10))

        # 2. INVOERZONE: KLEIN 1-DIGIT KLIK-VENSTER (S2) MET 3 KNOPPEN EROMHEEN
        invoer_frame = tk.Frame(horloge_frame, bg=self.bg_horloge)
        invoer_frame.pack(pady=5)

        # Bovenste knop: S3 (Bovenbalk)
        self.btn_s3 = tk.Button(
            invoer_frame,
            text="S3\n(Boven)",
            font=("Helvetica", 10, "bold"),
            width=12,
            height=2,
            bg=self.knop_bg,
            fg="white",
            activebackground=self.knop_actief,
            activeforeground="white",
            relief="raised",
            bd=3,
            command=lambda: self.toggle_segment('S3')
        )
        self.btn_s3.grid(row=0, column=1, pady=(0, 8))

        # Linker knop: S1 (Onderboog)
        self.btn_s1 = tk.Button(
            invoer_frame,
            text="S1\n(Onder)",
            font=("Helvetica", 10, "bold"),
            width=8,
            height=5,
            bg=self.knop_bg,
            fg="white",
            activebackground=self.knop_actief,
            activeforeground="white",
            relief="raised",
            bd=3,
            command=lambda: self.toggle_segment('S1')
        )
        self.btn_s1.grid(row=1, column=0, padx=(0, 10))

        # MIDDEN: HET KLIKBARE 1-DIGIT LCD VENSTER (S2 + BEVESTIG)
        # Met een duidelijk vierkant kader zodat direct zichtbaar is dat dit een knop is
        venster_container = tk.Frame(
            invoer_frame,
            bg="#4f5b6e",
            bd=4,
            relief="raised",
            cursor="hand2"
        )
        venster_container.grid(row=1, column=1)

        self.digit_canvas = tk.Canvas(
            venster_container,
            width=96,
            height=130,
            bg=self.lcd_bg,
            highlightthickness=2,
            highlightbackground="#151828",
            cursor="hand2"
        )
        self.digit_canvas.pack(padx=3, pady=3)

        lbl_klik_hint = tk.Label(
            venster_container,
            text="[ KLIK: S2 / OK ]",
            font=("Helvetica", 7, "bold"),
            fg="#ffffff",
            bg="#4f5b6e",
            cursor="hand2"
        )
        lbl_klik_hint.pack(fill="x", pady=(0, 2))

        # Klik-events koppelen aan het kleine display-venster
        self.digit_canvas.bind("<Button-1>", self.klik_op_venster)
        lbl_klik_hint.bind("<Button-1>", self.klik_op_venster)
        venster_container.bind("<Button-1>", self.klik_op_venster)

        # Rechter knop: S4 (Rechter stam)
        self.btn_s4 = tk.Button(
            invoer_frame,
            text="S4\n(Rechts)",
            font=("Helvetica", 10, "bold"),
            width=8,
            height=5,
            bg=self.knop_bg,
            fg="white",
            activebackground=self.knop_actief,
            activeforeground="white",
            relief="raised",
            bd=3,
            command=lambda: self.toggle_segment('S4')
        )
        self.btn_s4.grid(row=1, column=2, padx=(10, 0))

        # 3. ACTIEKNOPPEN ONDERAAN (Wissen & Bellen)
        actie_frame = tk.Frame(horloge_frame, bg=self.bg_horloge)
        actie_frame.pack(pady=(18, 10))

        btn_wis = tk.Button(
            actie_frame,
            text="⌫ Wis",
            font=("Helvetica", 10, "bold"),
            width=10,
            height=2,
            bg="#8c3b3b",
            fg="white",
            command=self.wis_laatste
        )
        btn_wis.grid(row=0, column=0, padx=8)

        btn_bel = tk.Button(
            actie_frame,
            text="📞 Bellen",
            font=("Helvetica", 10, "bold"),
            width=12,
            height=2,
            bg="#2e7d47",
            fg="white",
            command=self.start_gesprek
        )
        btn_bel.grid(row=0, column=1, padx=8)

    def toggle_segment(self, seg):
        if seg in self.actieve_segmenten:
            self.actieve_segmenten.remove(seg)
        else:
            self.actieve_segmenten.add(seg)
        self.update_status_tekst()
        self.teken_alles()

    def klik_op_venster(self, event=None):
        # S2-First Protocol:
        # 1. Als het scherm nog helemaal leeg is -> S2 aanzetten (eerste segment van 4, 5, 6, 8, 9)
        if len(self.actieve_segmenten) == 0:
            self.actieve_segmenten.add('S2')
            self.s2_is_eerste = True
            self.update_status_tekst()
            self.teken_alles()
            return

        # 2. Als er al segmenten op het scherm staan -> Bevestigen / Invoeren!
        herkend_cijfer = self.patroon_naar_cijfer.get(frozenset(self.actieve_segmenten))
        if herkend_cijfer is not None:
            if len(self.telefoonnummer) < 12:
                self.telefoonnummer += herkend_cijfer
                self.status_label.config(text=f"Cijfer '{herkend_cijfer}' ingevoerd!", fg="#8fd19e")
            else:
                self.status_label.config(text="Maximaal aantal cijfers bereikt", fg="#f0ad4e")
            self.actieve_segmenten.clear()
            self.s2_is_eerste = False
        else:
            self.status_label.config(text="Ongeldige vorm! Pas segmenten aan.", fg="#ff7675")

        self.teken_alles()

    def wis_laatste(self):
        if len(self.actieve_segmenten) > 0:
            self.actieve_segmenten.clear()
            self.s2_is_eerste = False
            self.status_label.config(text="Tekening gewist", fg="#a0aab8")
        elif len(self.telefoonnummer) > 0:
            self.telefoonnummer = self.telefoonnummer[:-1]
            self.status_label.config(text="Laatste cijfer gewist", fg="#a0aab8")
        self.teken_alles()

    def start_gesprek(self):
        if self.telefoonnummer:
            self.status_label.config(text=f"Bellen naar {self.telefoonnummer}...", fg="#55efc4")
        else:
            self.status_label.config(text="Voer eerst een nummer in!", fg="#ff7675")

    def update_status_tekst(self):
        if not self.actieve_segmenten:
            self.status_label.config(text="Teken een cijfer (klik venster voor S2)", fg="#a0aab8")
            return
        herkend = self.patroon_naar_cijfer.get(frozenset(self.actieve_segmenten))
        if herkend is not None:
            self.status_label.config(text=f"Vorm = '{herkend}' -> Klik op venster om in te voeren", fg="#8fd19e")
        else:
            self.status_label.config(text="Bezig met tekenen... (nog geen geldig cijfer)", fg="#ffeaa7")

    # --- TEKENFUNCTIES VOOR DE 4-SEGMENTEN CIJFERS ---
    def transformeer_punt(self, x, y, schaal, offset_x, offset_y, cy=150, schuinte=0.20):
        nieuw_x = x + schuinte * (cy - y)
        return offset_x + nieuw_x * schaal, offset_y + y * schaal

    def teken_lijn(self, canvas, x1, y1, x2, y2, kleur, dikte, schaal, ox, oy):
        tx1, ty1 = self.transformeer_punt(x1, y1, schaal, ox, oy)
        tx2, ty2 = self.transformeer_punt(x2, y2, schaal, ox, oy)
        canvas.create_line(tx1, ty1, tx2, ty2, fill=kleur, width=max(1.2, dikte * schaal), capstyle='round')

    def teken_boog(self, canvas, cx, cy_b, rx, ry, start_g, extent_g, kleur, dikte, schaal, ox, oy):
        punten = []
        stappen = 24
        for i in range(stappen + 1):
            rad = math.radians(start_g + (extent_g * i / stappen))
            px = cx + rx * math.cos(rad)
            py = cy_b - ry * math.sin(rad)
            punten.append(self.transformeer_punt(px, py, schaal, ox, oy))
        w = max(1.2, dikte * schaal)
        for i in range(len(punten) - 1):
            canvas.create_line(punten[i], punten[i+1], fill=kleur, width=w, capstyle='round', joinstyle='round')

    def teken_4seg_digit(self, canvas, actieve_segs, schaal, ox, oy):
        w, h = 100, 200
        cy = 150

        # S1
        s1_aan = 'S1' in actieve_segs
        k1 = self.segment_aan if s1_aan else self.segment_uit
        d1 = 16 if s1_aan else 1.5
        self.teken_boog(canvas, 34 + (w - 25)/2, cy + (h/2)/2, (w - 10)/2, (h/2)/2, 194, 126, k1, d1, schaal, ox, oy)
        self.teken_lijn(canvas, 28, cy + 88 - 0.6*h/4, w - 68, cy + 78 - 0.3*h/2, k1, d1, schaal, ox, oy)
        self.teken_lijn(canvas, 58, cy + 30 - 0.6*h/4, w - 40, cy + 30 - 0.3*h/2, k1, d1, schaal, ox, oy)

        # S2
        s2_aan = 'S2' in actieve_segs
        k2 = self.segment_aan if s2_aan else self.segment_uit
        d2 = 16 if s2_aan else 1.5
        cy_b2 = (cy + 20 - h/2) + ((cy + 20) - (cy + 20 - h/2))/2
        ry2 = ((cy + 20) - (cy + 20 - h/2))/2
        self.teken_boog(canvas, 25 + (w - 25)/2, cy_b2, (w - 25)/2, ry2, 135, 70, k2, d2, schaal, ox, oy)
        self.teken_lijn(canvas, 40, cy + 28 - 0.6*h/4, w - 52, cy + 28 - 0.3*h/2, k2, d2, schaal, ox, oy)

        # S3
        s3_aan = 'S3' in actieve_segs
        k3 = self.segment_aan if s3_aan else self.segment_uit
        d3 = 16 if s3_aan else 1.5
        self.teken_lijn(canvas, 48, cy + 10 - h/2, w - 5, cy + 10 - h/2, k3, d3, schaal, ox, oy)
        self.teken_lijn(canvas, 40, cy - 60 - 0.6*h/4, w - 65, cy - 55 - 0.3*h/2, k3, d3, schaal, ox, oy)
        self.teken_lijn(canvas, 93, cy - 22 - 0.6*h/4, w - 4, cy - 30 - 0.3*h/2, k3, d3, schaal, ox, oy)
        self.teken_lijn(canvas, w + 2, cy - h/2 + 28, w, cy + h/2 - 180, k3, d3, schaal, ox, oy)

        # S4
        s4_aan = 'S4' in actieve_segs
        k4 = self.segment_aan if s4_aan else self.segment_uit
        d4 = 16 if s4_aan else 1.5
        self.teken_lijn(canvas, w + 2, cy - h/2 + 28, w, cy + h/2 - 180, k4, d4, schaal, ox, oy)
        self.teken_lijn(canvas, w - 1, cy - h/2 + 62, w - 9, cy + h/2 - 136, k4, d4, schaal, ox, oy)
        self.teken_lijn(canvas, w + 8, cy - h/2 + 158, 8 + w, cy + h/2 - 26, k4, d4, schaal, ox, oy)
        self.teken_lijn(canvas, 70, cy + 10 - 0.6*h/4, w - 22, cy - 1 - 0.3*h/2, k4, d4, schaal, ox, oy)

        # Lichtgrijs binnenaccent van S4
        k4_accent = self.segment_grijs if s4_aan else self.segment_uit
        self.teken_lijn(canvas, w - 10, cy + 10 - 0.6*h/4, w - 10, cy + 11 - 0.3*h/2, k4_accent, d4, schaal, ox, oy)

        # Gedeelde dambord-overlapping S2 & S4
        if s2_aan and s4_aan:
            k_ov, d_ov = self.segment_aan, 16
        elif s2_aan or s4_aan:
            k_ov, d_ov = self.segment_grijs, 16
        else:
            k_ov, d_ov = self.segment_uit, 1.5
        self.teken_lijn(canvas, w + 8, cy - h/2 + 150, w + 4, cy + h/2 - 65, k_ov, d_ov, schaal, ox, oy)
        self.teken_lijn(canvas, w - 3, cy - h/2 + 120, w, cy + h/2 - 75, k_ov, d_ov, schaal, ox, oy)

    def teken_alles(self):
        # 1. Teken het kleine klikbare 1-digit invoervenster
        self.digit_canvas.delete("all")
        # Subtiel stippel-vierkantje binnenin als extra visuele hint dat het een knop is
        self.digit_canvas.create_rectangle(6, 6, 90, 124, outline="#7e8984", dash=(3, 3), width=1.5)
        self.teken_4seg_digit(self.digit_canvas, self.actieve_segmenten, schaal=0.45, ox=16, oy=-2)

        # 2. Teken het grote telefoonnummer-display
        self.nummer_canvas.delete("all")
        if not self.telefoonnummer:
            self.nummer_canvas.create_text(
                170, 48,
                text="VOER NUMMER IN...",
                font=("Courier", 13, "bold"),
                fill="#7e8984"
            )
        else:
            # Maximaal 10-12 cijfers netjes naast elkaar tekenen
            schaal_groot = 0.22
            stap_x = 26
            start_x = 8
            for idx, cijfer in enumerate(self.telefoonnummer):
                segs = self.cijfer_naar_patroon.get(cijfer, [])
                self.teken_4seg_digit(self.nummer_canvas, segs, schaal=schaal_groot, ox=start_x + idx * stap_x, oy=14)

if __name__ == "__main__":
    root = tk.Tk()
    app = PolsTelefoonKiezer(root)
    root.mainloop()
