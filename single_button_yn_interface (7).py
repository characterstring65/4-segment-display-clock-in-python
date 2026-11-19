import tkinter as tk
import math

class SingleButtonYNInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("1-Button Single-Window Scan & y/n Interface")
        self.root.configure(bg="#22252a")
        self.root.resizable(False, False)

        # LCD kleuren
        self.lcd_bg = '#d8e3d8'
        self.segment_aan = '#151828'
        self.segment_grijs = '#7e8984'
        self.segment_uit = '#cad6ca'

        # Geldige cijfermatrix (exacte sets van actieve segmenten)
        self.cijfer_matrix = {
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

        self.alle_segmenten = ['S1', 'S2', 'S3', 'S4']
        self.y_segmenten = {'S1', 'S2', 'S4'}  # Kleine letter y (Yes)
        self.n_segmenten = {'S2', 'S3'}        # Kleine letter n (No)

        # Status variabelen
        self.gekozen_segmenten = set()
        self.ingevoerd_getal = ""
        self.mode = "SCAN"  # SCAN, CONFIRM_Y, CONFIRM_N, OUTPUT_BLINK
        
        self.scan_volgorde = []
        self.scan_index = 0
        self.blink_aan = True
        self.output_index = 0
        self.output_aan = True
        self.timer_id = None

        self.bouw_ui()
        self.start_scan_ronde()

    def bouw_ui(self):
        # Bovenste balk: status en opgeslagen getal
        info_frame = tk.Frame(self.root, bg="#22252a", pady=10, padx=20)
        info_frame.pack(fill="x")

        tk.Label(
            info_frame, text="PROCESSOR MEMORY / ENTERED:", 
            fg="#9aa89a", bg="#22252a", font=("Consolas", 9, "bold")
        ).pack()

        self.geheugen_label = tk.Label(
            info_frame, text="[ EMPTY ]", 
            fg="#76e094", bg="#181a1e", font=("Consolas", 16, "bold"),
            width=18, pady=6, relief="sunken"
        )
        self.geheugen_label.pack(pady=5)

        # Status melding
        self.status_label = tk.Label(
            self.root, text="MODE: SCANNING SEGMENTS", 
            fg="#e0e6ed", bg="#22252a", font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(pady=(0, 8))

        # Het klikbare 1-digit LCD venster (de enige knop)
        knop_frame = tk.Frame(self.root, bg="#3a3f47", padx=6, pady=6, relief="raised", bd=3)
        knop_frame.pack(padx=30, pady=5)

        self.canvas = tk.Canvas(
            knop_frame, width=180, height=230, bg=self.lcd_bg,
            highlightthickness=2, highlightbackground="#5c636e", cursor="hand2"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.klik_op_venster)
        self.root.bind("<space>", self.klik_op_venster)

        tk.Label(
            self.root, text="Click LCD window (or press Space) when desired glyph blinks",
            fg="#9aa89a", bg="#22252a", font=("Segoe UI", 8)
        ).pack(pady=(6, 10))

        # Hulpfuncties onderaan voor testen (Reset & Add Next Digit)
        ctrl_frame = tk.Frame(self.root, bg="#22252a", pady=10)
        ctrl_frame.pack()

        self.add_btn = tk.Button(
            ctrl_frame, text="+ ADD NEXT DIGIT", command=self.volgend_cijfer,
            bg="#3b6e52", fg="white", font=("Segoe UI", 9, "bold"),
            relief="flat", padx=10, pady=4, state="disabled", cursor="hand2"
        )
        self.add_btn.pack(side="left", padx=5)

        tk.Button(
            ctrl_frame, text="RESET SYSTEM", command=self.reset_systeem,
            bg="#8c3b3b", fg="white", font=("Segoe UI", 9, "bold"),
            relief="flat", padx=10, pady=4, cursor="hand2"
        ).pack(side="left", padx=5)

    def reset_systeem(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.gekozen_segmenten = set()
        self.ingevoerd_getal = ""
        self.geheugen_label.config(text="[ EMPTY ]")
        self.add_btn.config(state="disabled")
        self.start_scan_ronde()

    def volgend_cijfer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.gekozen_segmenten = set()
        self.add_btn.config(state="disabled")
        self.start_scan_ronde()

    def start_scan_ronde(self):
        self.mode = "SCAN"
        self.scan_volgorde = [s for s in self.alle_segmenten if s not in self.gekozen_segmenten]
        if not self.scan_volgorde:
            # Alle 4 segmenten gekozen (cijfer 8) -> direct naar bevestiging
            self.start_confirm_fase()
            return
        self.scan_index = 0
        self.blink_aan = True
        self.status_label.config(text="INPUT: TAP WHEN SEGMENT BLINKS", fg="#e0e6ed")
        self.stap_lus()

    def start_confirm_fase(self):
        self.mode = "CONFIRM_Y"
        self.blink_aan = True
        cijfer = self.cijfer_matrix.get(frozenset(self.gekozen_segmenten), "?")
        self.status_label.config(text=f"DIGIT '{cijfer}' READY -> TAP 'y' TO ENTER", fg="#76e094")
        self.stap_lus()

    def stap_lus(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        if self.mode == "SCAN":
            huidig_seg = self.scan_volgorde[self.scan_index]
            zichtbaar = set(self.gekozen_segmenten)
            if self.blink_aan:
                zichtbaar.add(huidig_seg)
            self.teken_display(zichtbaar)

            if self.blink_aan:
                self.blink_aan = False
                self.timer_id = self.root.after(450, self.stap_lus)
            else:
                self.blink_aan = True
                self.scan_index += 1
                if self.scan_index >= len(self.scan_volgorde):
                    # Volledige ronde geweest: controleer of we een geldig cijfer hebben
                    if frozenset(self.gekozen_segmenten) in self.cijfer_matrix:
                        self.start_confirm_fase()
                        return
                    else:
                        self.scan_index = 0
                self.timer_id = self.root.after(200, self.stap_lus)

        elif self.mode == "CONFIRM_Y":
            # Toon UITSLUITEND de knipperende 'y' (S1 + S2 + S4) zodat de gebruiker niet in de war raakt
            self.teken_display(self.y_segmenten if self.blink_aan else set())
            if self.blink_aan:
                self.blink_aan = False
                self.timer_id = self.root.after(650, self.stap_lus)
            else:
                self.mode = "CONFIRM_N"
                self.blink_aan = True
                self.status_label.config(text="OR TAP 'n' TO CLEAR DIGIT", fg="#f0a868")
                self.timer_id = self.root.after(250, self.stap_lus)

        elif self.mode == "CONFIRM_N":
            # Toon UITSLUITEND de knipperende 'n' (S2 + S3)
            self.teken_display(self.n_segmenten if self.blink_aan else set())
            if self.blink_aan:
                self.blink_aan = False
                self.timer_id = self.root.after(650, self.stap_lus)
            else:
                # Beide y en n genegeerd -> terug naar segment-scan om cijfer af te maken
                self.timer_id = self.root.after(250, self.start_scan_ronde)

        elif self.mode == "OUTPUT_BLINK":
            # Processor knippert het ingevoerde getal continu uit
            huidig_cijfer = self.ingevoerd_getal[self.output_index]
            seg_set = set()
            for s_set, val in self.cijfer_matrix.items():
                if val == huidig_cijfer:
                    seg_set = set(s_set)
                    break

            self.teken_display(seg_set if self.output_aan else set())
            if self.output_aan:
                self.output_aan = False
                self.timer_id = self.root.after(550, self.stap_lus)
            else:
                self.output_aan = True
                self.output_index = (self.output_index + 1) % len(self.ingevoerd_getal)
                pauze = 600 if self.output_index == 0 else 250
                self.timer_id = self.root.after(pauze, self.stap_lus)

    def klik_op_venster(self, event=None):
        if self.mode == "SCAN":
            # Zet het huidige gescande segment vast
            huidig_seg = self.scan_volgorde[self.scan_index]
            self.gekozen_segmenten.add(huidig_seg)
            self.start_scan_ronde()

        elif self.mode == "CONFIRM_Y":
            # Bevestig cijfer (Yes)
            cijfer = self.cijfer_matrix.get(frozenset(self.gekozen_segmenten), "")
            if cijfer:
                self.ingevoerd_getal += cijfer
                self.geheugen_label.config(text=self.ingevoerd_getal)
                self.mode = "OUTPUT_BLINK"
                self.output_index = 0
                self.output_aan = True
                self.add_btn.config(state="normal")
                self.status_label.config(text="PROCESSOR ECHO: BLINKING RESULT", fg="#64b5f6")
                self.stap_lus()

        elif self.mode == "CONFIRM_N":
            # Wis cijfer (No) en begin opnieuw
            self.gekozen_segmenten = set()
            self.start_scan_ronde()

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

    def teken_display(self, actieve_set):
        self.canvas.delete("all")
        x_offset = 32
        w, h = 90, 175
        cy = 115

        # S1
        s1_actief = 'S1' in actieve_set
        k1 = self.segment_aan if s1_actief else self.segment_uit
        d1 = 14 if s1_actief else 1.2
        cx_boog1 = x_offset + 30 + (w - 22) / 2
        cy_boog1 = cy + (h / 2) / 2
        self.teken_schuine_boog(cx_boog1, cy_boog1, (w - 8) / 2, (h / 2) / 2, 194, 126, k1, d1)
        self.teken_schuine_lijn(x_offset + 25, cy + 77 - 0.6 * h/4, x_offset + w - 61, cy + 68 - 0.3 * h/2, k1, d1)
        self.teken_schuine_lijn(x_offset + 52, cy + 26 - 0.6 * h/4, x_offset + w - 36, cy + 26 - 0.3 * h/2, k1, d1)

        # S2
        s2_actief = 'S2' in actieve_set
        k2 = self.segment_aan if s2_actief else self.segment_uit
        d2 = 14 if s2_actief else 1.2
        cx_boog2 = x_offset + 22 + (w - 22) / 2
        cy_boog2 = (cy + 18 - h/2) + ((cy + 18) - (cy + 18 - h/2)) / 2
        self.teken_schuine_boog(cx_boog2, cy_boog2, (w - 22) / 2, ((cy + 18) - (cy + 18 - h/2)) / 2, 135, 70, k2, d2)
        self.teken_schuine_lijn(x_offset + 36, cy + 25 - 0.6 * h/4, x_offset + w - 47, cy + 25 - 0.3 * h/2, k2, d2)

        # S3
        s3_actief = 'S3' in actieve_set
        k3 = self.segment_aan if s3_actief else self.segment_uit
        d3 = 14 if s3_actief else 1.2
        self.teken_schuine_lijn(x_offset + 43, cy + 9 - h/2, x_offset + w - 4, cy + 9 - h/2, k3, d3)
        self.teken_schuine_lijn(x_offset + 36, cy - 52 - 0.6 * h/4, x_offset + w - 58, cy - 48 - 0.3 * h/2, k3, d3)
        self.teken_schuine_lijn(x_offset + 84, cy - 19 - 0.6 * h/4, x_offset + w - 4, cy - 26 - 0.3 * h/2, k3, d3)
        self.teken_schuine_lijn(x_offset + w + 2, cy - h/2 + 25, x_offset + w, cy + h/2 - 158, k3, d3)

        # S4
        s4_actief = 'S4' in actieve_set
        k4 = self.segment_aan if s4_actief else self.segment_uit
        d4 = 14 if s4_actief else 1.2
        self.teken_schuine_lijn(x_offset + w + 2, cy - h/2 + 25, x_offset + w, cy + h/2 - 158, k4, d4)
        self.teken_schuine_lijn(x_offset + w - 1, cy - h/2 + 54, x_offset + w - 8, cy + h/2 - 119, k4, d4)
        self.teken_schuine_lijn(x_offset + w + 7, cy - h/2 + 138, x_offset + 7 + w, cy + h/2 - 23, k4, d4)
        self.teken_schuine_lijn(x_offset + 63, cy + 9 - 0.6 * h/4, x_offset + w - 20, cy - 1 - 0.3 * h/2, k4, d4)
        
        # Accentstreepje S4 in dambord-lichtgrijs
        k4_accent = self.segment_grijs if s4_actief else self.segment_uit
        self.teken_schuine_lijn(x_offset + w - 9, cy + 9 - 0.6 * h/4, x_offset + w - 9, cy + 10 - 0.3 * h/2, k4_accent, d4)

        # Gedeelde dambord-overlapping tussen S2 en S4
        if s2_actief and s4_actief:
            k_ov, d_ov = self.segment_aan, 14
        elif s2_actief or s4_actief:
            k_ov, d_ov = self.segment_grijs, 14
        else:
            k_ov, d_ov = self.segment_uit, 1.2

        self.teken_schuine_lijn(x_offset + w + 7, cy - h/2 + 131, x_offset + w + 4, cy + h/2 - 57, k_ov, d_ov)
        self.teken_schuine_lijn(x_offset + w - 3, cy - h/2 + 105, x_offset + w, cy + h/2 - 66, k_ov, d_ov)

if __name__ == "__main__":
    root = tk.Tk()
    app = SingleButtonYNInterface(root)
    root.mainloop()
