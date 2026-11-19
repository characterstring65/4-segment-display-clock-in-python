import tkinter as tk
import math

class SingleButtonYNInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("1-Button Single-Window Scan & y/n Interface")
        self.root.configure(bg='#22252a')
        self.root.resizable(False, False)

        self.lcd_bg = '#d8e3d8'
        self.segment_aan = '#151828'
        self.segment_grijs = '#7e8984'
        self.segment_uit = '#cad6ca'

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

        self.alle_segmenten = ['S1', 'S2', 'S3', 'S4']
        self.gekozen_segmenten = []
        self.ingevoerd_getal = ""

        # Toestanden: 'SCAN', 'CONFIRM_Y', 'CONFIRM_N', 'READOUT_LOOP'
        self.modus = 'SCAN'
        self.scan_index = 0
        self.blink_aan = True
        self.scan_stappen_sinds_actie = 0

        self.readout_index = 0
        self.readout_fase = 'SHOW'  # 'SHOW', 'PAUSE_DIGIT', 'PAUSE_CYCLE'

        self.timer_id = None
        self.scan_snelheid_ms = 650

        self.bouw_ui()
        self.centreer_venster(420, 490)
        self.start_lus()

    def centreer_venster(self, b, h):
        sb = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sb // 2) - (b // 2)
        y = (sh // 2) - (h // 2)
        self.root.geometry(f"{b}x{h}+{x}+{y}")

    def bouw_ui(self):
        # Bovenbalk: Ingevoerd getal & reset
        top_frame = tk.Frame(self.root, bg='#22252a', pady=12)
        top_frame.pack(fill='x', padx=20)

        tk.Label(
            top_frame, text="ENTERED / PROCESSOR VALUE:",
            font=("Helvetica", 9, "bold"), fg="#9aa89a", bg="#22252a"
        ).pack(anchor='w')

        val_row = tk.Frame(top_frame, bg='#22252a')
        val_row.pack(fill='x', pady=(4, 0))

        self.lbl_waarde = tk.Label(
            val_row, text="---", font=("Courier", 20, "bold"),
            fg="#e0eee0", bg="#181a1e", width=12, anchor='w', padx=10, pady=4
        )
        self.lbl_waarde.pack(side='left')

        btn_clear = tk.Button(
            val_row, text="RESET", font=("Helvetica", 10, "bold"),
            bg="#4a2c2c", fg="#f0d0d0", activebackground="#6b3e3e",
            relief='flat', padx=14, pady=6, cursor="hand2",
            command=self.reset_alles
        )
        btn_clear.pack(side='right')

        # Status-indicator
        self.lbl_status = tk.Label(
            self.root, text="MODE: SCANNING SEGMENTS (Tap window to lock)",
            font=("Helvetica", 10, "bold"), fg="#a8d8a8", bg="#22252a", pady=8
        )
        self.lbl_status.pack()

        # Het enkele 1-digit klikbare LCD venster (de enige knop)
        bezel = tk.Frame(
            self.root, bg='#3a3f47', bd=4, relief='raised',
            padx=12, pady=12, cursor="hand2"
        )
        bezel.pack(pady=8)

        self.canvas = tk.Canvas(
            bezel, width=180, height=230, bg=self.lcd_bg,
            highlightthickness=2, highlightbackground="#6c7a6c", cursor="hand2"
        )
        self.canvas.pack()

        self.lbl_knop_hint = tk.Label(
            bezel, text="[ SINGLE BUTTON / 1-DIGIT WINDOW ]",
            font=("Helvetica", 8, "bold"), fg="#d0dcd0", bg="#3a3f47", pady=4
        )
        self.lbl_knop_hint.pack()

        # Klik-events koppelen aan venster, rand en spatiebalk
        for widget in (bezel, self.canvas, self.lbl_knop_hint):
            widget.bind("<Button-1>", self.verwerk_klik)
        self.root.bind("<space>", self.verwerk_klik)

        # Onderste balk: Uitleg & Extra cijfer invoegen
        bot_frame = tk.Frame(self.root, bg='#22252a', pady=10)
        bot_frame.pack(fill='x', padx=20)

        self.btn_next_digit = tk.Button(
            bot_frame, text="+ ADD NEXT DIGIT", font=("Helvetica", 9, "bold"),
            bg="#2d3b32", fg="#c8e6c8", activebackground="#3d5244",
            relief='flat', padx=12, pady=6, cursor="hand2",
            command=self.start_nieuw_cijfer
        )
        self.btn_next_digit.pack()

        tk.Label(
            self.root,
            text="Scan: Tap when S1..S4 blinks to lock. Ignore y/n to keep building.\n"
                 "Confirm: Tap on 'y' (S1+S2+S4) to enter, or 'n' (S2+S3) to clear.\n"
                 "After entry: Digit blinks continuously until RESET (or + ADD NEXT DIGIT).",
            font=("Helvetica", 8), fg="#8c969e", bg="#22252a", justify="center", pady=6
        ).pack()

    def herken_cijfer(self, segs):
        doel = sorted(segs)
        for cijfer, patroon in self.cijfer_matrix.items():
            if sorted(patroon) == doel:
                return cijfer
        return None

    def beschikbare_segmenten(self):
        return [s for s in self.alle_segmenten if s not in self.gekozen_segmenten]

    def reset_alles(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.gekozen_segmenten = []
        self.ingevoerd_getal = ""
        self.lbl_waarde.config(text="---")
        self.modus = 'SCAN'
        self.scan_index = 0
        self.scan_stappen_sinds_actie = 0
        self.blink_aan = True
        self.start_lus()

    def start_nieuw_cijfer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.gekozen_segmenten = []
        self.modus = 'SCAN'
        self.scan_index = 0
        self.scan_stappen_sinds_actie = 0
        self.blink_aan = True
        self.start_lus()

    def verwerk_klik(self, event=None):
        if self.modus == 'READOUT_LOOP':
            # Tijdens continu knipperen van de processor-uitvoer is reset of +next digit nodig
            return

        if self.modus == 'SCAN':
            vrije = self.beschikbare_segmenten()
            if not vrije:
                return
            huidig_seg = vrije[self.scan_index % len(vrije)]
            if huidig_seg not in self.gekozen_segmenten:
                self.gekozen_segmenten.append(huidig_seg)
                self.scan_stappen_sinds_actie = 0
                self.blink_aan = True

            # Als alle 4 segmenten vaststaan (cijfer 8), direct naar bevestiging
            if len(self.gekozen_segmenten) == 4:
                self.modus = 'CONFIRM_Y'
                self.blink_aan = True
            else:
                # Doorgaan met scannen langs de overgebleven segmenten
                nieuwe_vrije = self.beschikbare_segmenten()
                if nieuwe_vrije:
                    self.scan_index = self.scan_index % len(nieuwe_vrije)
            self.teken_scherm()

        elif self.modus == 'CONFIRM_Y':
            # Bevestigd met 'y' (Yes)!
            cijfer = self.herken_cijfer(self.gekozen_segmenten)
            if cijfer is not None:
                self.ingevoerd_getal += cijfer
                self.lbl_waarde.config(text=self.ingevoerd_getal)
                self.gekozen_segmenten = []
                # Start continue processor-knipperuitvoer tot RESET
                self.modus = 'READOUT_LOOP'
                self.readout_index = 0
                self.readout_fase = 'SHOW'
                if self.timer_id:
                    self.root.after_cancel(self.timer_id)
                self.lus_stap()

        elif self.modus == 'CONFIRM_N':
            # Gewist met 'n' (No)!
            self.gekozen_segmenten = []
            self.modus = 'SCAN'
            self.scan_index = 0
            self.scan_stappen_sinds_actie = 0
            self.blink_aan = True
            self.teken_scherm()

    def start_lus(self):
        self.teken_scherm()
        self.timer_id = self.root.after(self.scan_snelheid_ms, self.lus_stap)

    def lus_stap(self):
        if self.modus == 'SCAN':
            vrije = self.beschikbare_segmenten()
            if not vrije:
                self.modus = 'CONFIRM_Y'
                self.blink_aan = True
            else:
                if self.blink_aan:
                    self.blink_aan = False
                else:
                    self.blink_aan = True
                    self.scan_index = (self.scan_index + 1) % len(vrije)
                    self.scan_stappen_sinds_actie += 1

                    # Na een volledige ronde langs alle vrije segmenten zonder nieuwe klik:
                    # als er een geldig cijfer staat, vraag dan bevestiging via y / n
                    geldig = self.herken_cijfer(self.gekozen_segmenten)
                    if geldig is not None and self.scan_stappen_sinds_actie >= len(vrije):
                        self.modus = 'CONFIRM_Y'
                        self.blink_aan = True

            self.teken_scherm()
            self.timer_id = self.root.after(self.scan_snelheid_ms, self.lus_stap)

        elif self.modus == 'CONFIRM_Y':
            if self.blink_aan:
                self.blink_aan = False
                self.teken_scherm()
                self.timer_id = self.root.after(450, self.lus_stap)
            else:
                # Gebruiker heeft 'y' genegeerd -> ga naar 'n'
                self.modus = 'CONFIRM_N'
                self.blink_aan = True
                self.teken_scherm()
                self.timer_id = self.root.after(750, self.lus_stap)

        elif self.modus == 'CONFIRM_N':
            if self.blink_aan:
                self.blink_aan = False
                self.teken_scherm()
                self.timer_id = self.root.after(450, self.lus_stap)
            else:
                # Gebruiker heeft ook 'n' genegeerd -> keer direct terug naar segment-scan
                self.modus = 'SCAN'
                self.scan_index = 0
                self.scan_stappen_sinds_actie = 0
                self.blink_aan = True
                self.teken_scherm()
                self.timer_id = self.root.after(self.scan_snelheid_ms, self.lus_stap)

        elif self.modus == 'READOUT_LOOP':
            if not self.ingevoerd_getal:
                self.reset_alles()
                return

            if self.readout_fase == 'SHOW':
                c = self.ingevoerd_getal[self.readout_index]
                self.lbl_status.config(
                    text=f"PROCESSOR OUTPUT (Blinking continuously): Digit '{c}' — Press RESET",
                    fg="#ffdf80"
                )
                self.teken_segmenten_op_canvas(self.cijfer_matrix[c])
                self.readout_fase = 'PAUSE_DIGIT'
                self.timer_id = self.root.after(550, self.lus_stap)

            elif self.readout_fase == 'PAUSE_DIGIT':
                self.teken_segmenten_op_canvas([])
                self.readout_index += 1
                if self.readout_index >= len(self.ingevoerd_getal):
                    # Einde van het hele getal bereikt -> iets langere pauze voor herhaling
                    self.readout_index = 0
                    self.readout_fase = 'SHOW'
                    self.timer_id = self.root.after(750, self.lus_stap)
                else:
                    # Korte pauze tussen de cijfers van het getal
                    self.readout_fase = 'SHOW'
                    self.timer_id = self.root.after(300, self.lus_stap)

    def teken_scherm(self):
        actief = list(self.gekozen_segmenten)

        if self.modus == 'SCAN':
            vrije = self.beschikbare_segmenten()
            huidig_seg = vrije[self.scan_index % len(vrije)] if vrije else ""
            geldig = self.herken_cijfer(self.gekozen_segmenten)
            hint = f" (Valid '{geldig}')" if geldig else ""
            self.lbl_status.config(
                text=f"SCANNING: {huidig_seg}{hint} — Tap to lock",
                fg="#a8d8a8"
            )
            if vrije and self.blink_aan:
                actief.append(huidig_seg)

        elif self.modus == 'CONFIRM_Y':
            geldig = self.herken_cijfer(self.gekozen_segmenten)
            self.lbl_status.config(
                text=f"CONFIRM '{geldig}'? Tap on 'y' (Yes)",
                fg="#80e5ff"
            )
            actief = ['S1', 'S2', 'S4'] if self.blink_aan else []

        elif self.modus == 'CONFIRM_N':
            self.lbl_status.config(
                text="CLEAR DIGIT? Tap on 'n' (No) — or wait to resume scan",
                fg="#ff9999"
            )
            actief = ['S2', 'S3'] if self.blink_aan else []

        self.teken_segmenten_op_canvas(actief)

    def transformeer_punt(self, x, y, cy=115, schuinte=0.20):
        nieuw_x = x + schuinte * (cy - y)
        return nieuw_x, y

    def teken_schuine_lijn(self, x1, y1, x2, y2, kleur, dikte):
        tx1, ty1 = self.transformeer_punt(x1, y1)
        tx2, ty2 = self.transformeer_punt(x2, y2)
        self.canvas.create_line(tx1, ty1, tx2, ty2, fill=kleur, width=dikte, capstyle='round')

    def teken_schuine_boog(self, cx, cy, r_x, r_y, start_graden, extent_graden, kleur, dikte):
        punten = []
        stappen = 30
        for i in range(stappen + 1):
            hoek_rad = math.radians(start_graden + (extent_graden * i / stappen))
            px = cx + r_x * math.cos(hoek_rad)
            py = cy - r_y * math.sin(hoek_rad)
            tx, ty = self.transformeer_punt(px, py)
            punten.append((tx, ty))
        for i in range(len(punten) - 1):
            self.canvas.create_line(punten[i], punten[i+1], fill=kleur, width=dikte, capstyle='round', joinstyle='round')

    def teken_segmenten_op_canvas(self, actieve_segmenten):
        self.canvas.delete("all")
        x_offset = 25
        w, h = 100, 180
        cy = 115

        # S1
        s1_aan = 'S1' in actieve_segmenten
        k1 = self.segment_aan if s1_aan else self.segment_uit
        d1 = 14 if s1_aan else 1.5
        cx_boog1 = x_offset + 34 + (w - 25) / 2
        cy_boog1 = cy + (h / 2) / 2
        self.teken_schuine_boog(cx_boog1, cy_boog1, (w - 10) / 2, (h / 2) / 2, 194, 126, k1, d1)
        self.teken_schuine_lijn(x_offset + 28, cy + 80 - 0.6 * h/4, x_offset + w - 68, cy + 70 - 0.3 * h/2, k1, d1)
        self.teken_schuine_lijn(x_offset + 58, cy + 26 - 0.6 * h/4, x_offset + w - 40, cy + 26 - 0.3 * h/2, k1, d1)

        # S2
        s2_aan = 'S2' in actieve_segmenten
        k2 = self.segment_aan if s2_aan else self.segment_uit
        d2 = 14 if s2_aan else 1.5
        cx_boog2 = x_offset + 25 + (w - 25) / 2
        cy_boog2 = (cy + 18 - h/2) + ((cy + 18) - (cy + 18 - h/2)) / 2
        self.teken_schuine_boog(cx_boog2, cy_boog2, (w - 25) / 2, ((cy + 18) - (cy + 18 - h/2)) / 2, 135, 70, k2, d2)
        self.teken_schuine_lijn(x_offset + 40, cy + 25 - 0.6 * h/4, x_offset + w - 52, cy + 25 - 0.3 * h/2, k2, d2)

        # S3
        s3_aan = 'S3' in actieve_segmenten
        k3 = self.segment_aan if s3_aan else self.segment_uit
        d3 = 14 if s3_aan else 1.5
        self.teken_schuine_lijn(x_offset + 48, cy + 10 - h/2, x_offset + w - 5, cy + 10 - h/2, k3, d3)
        self.teken_schuine_lijn(x_offset + 40, cy - 54 - 0.6 * h/4, x_offset + w - 65, cy - 49 - 0.3 * h/2, k3, d3)
        self.teken_schuine_lijn(x_offset + 93, cy - 20 - 0.6 * h/4, x_offset + w - 4, cy - 27 - 0.3 * h/2, k3, d3)
        self.teken_schuine_lijn(x_offset + w + 2, cy - h/2 + 25, x_offset + w, cy + h/2 - 162, k3, d3)

        # S4
        s4_aan = 'S4' in actieve_segmenten
        k4 = self.segment_aan if s4_aan else self.segment_uit
        d4 = 14 if s4_aan else 1.5
        self.teken_schuine_lijn(x_offset + w + 2, cy - h/2 + 25, x_offset + w, cy + h/2 - 162, k4, d4)
        self.teken_schuine_lijn(x_offset + w - 1, cy - h/2 + 56, x_offset + w - 9, cy + h/2 - 122, k4, d4)
        self.teken_schuine_lijn(x_offset + w + 8, cy - h/2 + 142, x_offset + 8 + w, cy + h/2 - 23, k4, d4)
        self.teken_schuine_lijn(x_offset + 70, cy + 10 - 0.6 * h/4, x_offset + w - 22, cy - 1 - 0.3 * h/2, k4, d4)

        k4_accent = self.segment_grijs if s4_aan else self.segment_uit
        self.teken_schuine_lijn(x_offset + w - 10, cy + 10 - 0.6 * h/4, x_offset + w - 10, cy + 11 - 0.3 * h/2, k4_accent, d4)

        # Overlapping S2 en S4 (dambord lichtgrijs bij één actief, zwart bij beide)
        if s2_aan and s4_aan:
            k_ov = self.segment_aan
            d_ov = 14
        elif s2_aan or s4_aan:
            k_ov = self.segment_grijs
            d_ov = 14
        else:
            k_ov = self.segment_uit
            d_ov = 1.5

        self.teken_schuine_lijn(x_offset + w + 8, cy - h/2 + 135, x_offset + w + 4, cy + h/2 - 58, k_ov, d_ov)
        self.teken_schuine_lijn(x_offset + w - 3, cy - h/2 + 108, x_offset + w, cy + h/2 - 67, k_ov, d_ov)

if __name__ == "__main__":
    root = tk.Tk()
    app = SingleButtonYNInterface(root)
    root.mainloop()
