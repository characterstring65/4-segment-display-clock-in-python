import tkinter as tk
import math

class SingleButtonYNInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("1-Button Single-Window Scan & y/n Interface")
        self.root.configure(bg='#2b2f36')
        self.root.resizable(False, False)

        self.lcd_bg = '#d8e3d8'
        self.segment_aan = '#151828'
        self.segment_grijs = '#7e8984'
        self.segment_uit = '#cad6ca'

        # Geldige cijfer-combinaties
        self.geldige_cijfers = {
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

        # Toestanden: 'SCAN', 'CONFIRM_Y', 'CONFIRM_N', 'OUTPUT_BLINK'
        self.state = 'SCAN'
        self.vastgezette_segmenten = set()
        self.ingevoerde_reeks = ""
        
        self.alle_segmenten = ['S1', 'S2', 'S3', 'S4']
        self.scan_index = 0
        self.blink_aan = True
        self.scan_blink_teller = 0
        self.max_blinks_per_segment = 3  # 3x knipperen per segment
        self.knippers_in_deze_ronde = 0
        
        self.yn_teller = 0
        self.output_index = 0
        self.output_blink_aan = True
        self.timer_id = None

        self.bouw_ui()
        self.start_scan_lus()

    def bouw_ui(self):
        # Bovenbalk: Opgeslagen getal
        top_frame = tk.Frame(self.root, bg='#1e2126', pady=10, padx=16)
        top_frame.pack(fill='x')

        tk.Label(
            top_frame,
            text="STORED VALUE:",
            font=("Helvetica", 9, "bold"),
            fg="#8c96a6",
            bg="#1e2126"
        ).pack(side='left')

        self.reeks_label = tk.Label(
            top_frame,
            text="—",
            font=("Courier", 16, "bold"),
            fg="#76e094",
            bg="#1e2126"
        )
        self.reeks_label.pack(side='right')

        # Status-balk
        self.status_label = tk.Label(
            self.root,
            text="MODE: SCANNING SEGMENTS (CLICK WINDOW TO LOCK)",
            font=("Helvetica", 9, "bold"),
            fg="#e0e6ed",
            bg="#2b2f36",
            pady=8
        )
        self.status_label.pack()

        # Het enkele klikbare 1-Digit LCD Venster (De enige knop!)
        bezel = tk.Frame(self.root, bg='#181a1f', padx=14, pady=14, relief='raised', bd=4)
        bezel.pack(padx=40, pady=6)

        self.canvas = tk.Canvas(
            bezel,
            width=180,
            height=240,
            bg=self.lcd_bg,
            highlightthickness=2,
            highlightbackground="#6c7a6c",
            cursor="hand2"
        )
        self.canvas.pack()

        # Klik op het venster of druk op spatiebalk = De enige fysieke knop
        self.canvas.bind("<Button-1>", lambda e: self.knop_ingedrukt())
        self.root.bind("<space>", lambda e: self.knop_ingedrukt())

        # Hulplabel onder het scherm
        self.hint_label = tk.Label(
            self.root,
            text="[ CLICK LCD WINDOW OR PRESS SPACE ]",
            font=("Helvetica", 8, "bold"),
            fg="#9aa5b4",
            bg="#2b2f36",
            pady=6
        )
        self.hint_label.pack()

        # Onderste bedieningsbalk (alleen voor simulatie-reset / extra cijfer)
        btn_frame = tk.Frame(self.root, bg='#2b2f36', pady=10)
        btn_frame.pack(fill='x', padx=20)

        self.next_btn = tk.Button(
            btn_frame,
            text="+ ADD NEXT DIGIT",
            font=("Helvetica", 9, "bold"),
            bg="#3b6e8c",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.voeg_volgend_cijfer_toe,
            state="disabled"
        )
        self.next_btn.pack(side='left', expand=True, fill='x', padx=(0, 5))

        reset_btn = tk.Button(
            btn_frame,
            text="RESET",
            font=("Helvetica", 9, "bold"),
            bg="#8c3b3b",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.volledige_reset
        )
        reset_btn.pack(side='right', expand=True, fill='x', padx=(5, 0))

    def stop_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def volledige_reset(self):
        self.stop_timer()
        self.vastgezette_segmenten = set()
        self.ingevoerde_reeks = ""
        self.reeks_label.config(text="—")
        self.next_btn.config(state="disabled")
        self.start_scan_lus()

    def voeg_volgend_cijfer_toe(self):
        self.stop_timer()
        self.vastgezette_segmenten = set()
        self.next_btn.config(state="disabled")
        self.start_scan_lus()

    def start_scan_lus(self):
        self.stop_timer()
        self.state = 'SCAN'
        self.blink_aan = True
        self.scan_blink_teller = 0
        self.knippers_in_deze_ronde = 0
        self.status_label.config(text="INPUT: CLICK WHEN SEGMENT BLINKS (3x EACH)", fg="#76e094")
        
        # Zorg dat scan_index wijst naar een vrij segment
        vrije = [s for s in self.alle_segmenten if s not in self.vastgezette_segmenten]
        if not vrije:
            # Alle 4 zijn vastgezet (= cijfer 8), ga direct naar y/n
            self.start_yn_bevestiging()
            return
            
        while self.alle_segmenten[self.scan_index] in self.vastgezette_segmenten:
            self.scan_index = (self.scan_index + 1) % 4
            
        self.scan_stap()

    def scan_stap(self):
        if self.state != 'SCAN':
            return

        vrije = [s for s in self.alle_segmenten if s not in self.vastgezette_segmenten]
        if not vrije:
            self.start_yn_bevestiging()
            return

        huidig_seg = self.alle_segmenten[self.scan_index]
        while huidig_seg in self.vastgezette_segmenten:
            self.scan_index = (self.scan_index + 1) % 4
            huidig_seg = self.alle_segmenten[self.scan_index]

        # Teken vastgezette segmenten + eventueel het knipperende segment
        actief = set(self.vastgezette_segmenten)
        if self.blink_aan:
            actief.add(huidig_seg)
        self.teken_display(actief)

        if self.blink_aan:
            self.blink_aan = False
            self.timer_id = self.root.after(360, self.scan_stap)
        else:
            self.blink_aan = True
            self.scan_blink_teller += 1
            
            # Pas na 3x knipperen van dit segment naar het volgende vrije segment
            if self.scan_blink_teller >= self.max_blinks_per_segment:
                self.scan_blink_teller = 0
                self.knippers_in_deze_ronde += 1
                
                # Als we alle nog vrije segmenten in deze ronde 3x hebben laten zien
                # én er staat een geldig cijfer: ga naar y / n bevestiging
                if self.knippers_in_deze_ronde >= len(vrije) and frozenset(self.vastgezette_segmenten) in self.geldige_cijfers:
                    self.start_yn_bevestiging()
                    return
                
                self.scan_index = (self.scan_index + 1) % 4
                while self.alle_segmenten[self.scan_index] in self.vastgezette_segmenten:
                    self.scan_index = (self.scan_index + 1) % 4
                    
            self.timer_id = self.root.after(260, self.scan_stap)

    def start_yn_bevestiging(self):
        self.stop_timer()
        cijfer = self.geldige_cijfers.get(frozenset(self.vastgezette_segmenten), '?')
        self.state = 'CONFIRM_Y'
        self.yn_teller = 0
        self.status_label.config(text=f"DIGIT '{cijfer}' READY -> CLICK ON 'y' TO ENTER", fg="#ffd166")
        self.yn_stap()

    def yn_stap(self):
        if self.state not in ('CONFIRM_Y', 'CONFIRM_N'):
            return

        # Laat uitsluitend de losse 'y' (S1+S2+S4) of 'n' (S2+S3) knipperen
        if self.state == 'CONFIRM_Y':
            if self.yn_teller % 2 == 0:
                self.teken_display({'S1', 'S2', 'S4'})  # 'y' aan
            else:
                self.teken_display(set())               # leeg
            self.yn_teller += 1
            if self.yn_teller >= 6:  # 3x knipperen van 'y'
                self.state = 'CONFIRM_N'
                self.yn_teller = 0
                self.status_label.config(text="CLICK ON 'n' TO CLEAR (OR WAIT TO ADD MORE)", fg="#ff758f")
            self.timer_id = self.root.after(380, self.yn_stap)

        elif self.state == 'CONFIRM_N':
            if self.yn_teller % 2 == 0:
                self.teken_display({'S2', 'S3'})        # 'n' aan
            else:
                self.teken_display(set())               # leeg
            self.yn_teller += 1
            if self.yn_teller >= 6:  # 3x knipperen van 'n'
                # Beide genegeerd -> direct terug naar segment-scan om cijfer af te maken!
                self.start_scan_lus()
                return
            self.timer_id = self.root.after(380, self.yn_stap)

    def knop_ingedrukt(self):
        if self.state == 'SCAN':
            huidig_seg = self.alle_segmenten[self.scan_index]
            if huidig_seg not in self.vastgezette_segmenten:
                self.stop_timer()
                self.vastgezette_segmenten.add(huidig_seg)
                
                # Teken direct het vastgezette resultaat
                self.teken_display(self.vastgezette_segmenten)
                
                vrije = [s for s in self.alle_segmenten if s not in self.vastgezette_segmenten]
                if not vrije:
                    # Alle 4 vastgezet (= cijfer 8), ga na korte pauze naar y/n
                    self.timer_id = self.root.after(400, self.start_yn_bevestiging)
                    return

                # Reset de rondeteller zodat overige vrije segmenten weer een eerlijke kans krijgen
                self.knippers_in_deze_ronde = 0
                self.scan_blink_teller = 0
                self.blink_aan = True
                
                # Ga naar het eerstvolgende vrije segment
                self.scan_index = (self.scan_index + 1) % 4
                while self.alle_segmenten[self.scan_index] in self.vastgezette_segmenten:
                    self.scan_index = (self.scan_index + 1) % 4
                    
                self.timer_id = self.root.after(400, self.scan_stap)

        elif self.state == 'CONFIRM_Y':
            # Bevestig cijfer (Enter) en start continu uitknipperen van de gehele reeks!
            self.stop_timer()
            cijfer = self.geldige_cijfers.get(frozenset(self.vastgezette_segmenten), '')
            self.ingevoerde_reeks += cijfer
            self.reeks_label.config(text=self.ingevoerde_reeks)
            self.vastgezette_segmenten = set()
            self.next_btn.config(state="normal")
            self.start_continu_uitknipperen()

        elif self.state == 'CONFIRM_N':
            # Wis het huidige cijfer en begin opnieuw met scannen
            self.stop_timer()
            self.vastgezette_segmenten = set()
            self.start_scan_lus()

    def start_continu_uitknipperen(self):
        self.stop_timer()
        self.state = 'OUTPUT_BLINK'
        self.output_index = 0
        self.output_blink_aan = True
        self.status_label.config(text=f"PROCESSOR ECHO: BLINKING '{self.ingevoerde_reeks}' (PRESS RESET)", fg="#64dfdf")
        self.continu_output_stap()

    def continu_output_stap(self):
        if self.state != 'OUTPUT_BLINK' or not self.ingevoerde_reeks:
            return

        if self.output_index >= len(self.ingevoerde_reeks):
            # Korte pauze tussen herhalingen van het getal
            self.teken_display(set())
            self.output_index = 0
            self.output_blink_aan = True
            self.timer_id = self.root.after(650, self.continu_output_stap)
            return

        huidig_cijfer = self.ingevoerde_reeks[self.output_index]
        if self.output_blink_aan:
            self.teken_display(set(self.cijfer_matrix[huidig_cijfer]))
            self.output_blink_aan = False
            self.timer_id = self.root.after(450, self.continu_output_stap)
        else:
            self.teken_display(set())
            self.output_blink_aan = True
            self.output_index += 1
            self.timer_id = self.root.after(250, self.continu_output_stap)

    # --- TEKENFUNCTIES VOOR HET 4-SEGMENTEN LCD VENSTER ---
    def transformeer_punt(self, x, y, cy=120, schuinte=0.20, schaal=0.85, ox=35, oy=25):
        nieuw_x = x + schuinte * (cy - y)
        return ox + nieuw_x * schaal, oy + y * schaal

    def teken_schuine_lijn(self, x1, y1, x2, y2, kleur, dikte):
        tx1, ty1 = self.transformeer_punt(x1, y1)
        tx2, ty2 = self.transformeer_punt(x2, y2)
        self.canvas.create_line(tx1, ty1, tx2, ty2, fill=kleur, width=dikte * 0.85, capstyle='round')

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
            self.canvas.create_line(punten[i], punten[i+1], fill=kleur, width=dikte * 0.85, capstyle='round', joinstyle='round')

    def teken_display(self, actieve_segmenten):
        self.canvas.delete("all")
        w, h = 100, 200
        cy = 150

        s1 = 'S1' in actieve_segmenten
        s2 = 'S2' in actieve_segmenten
        s3 = 'S3' in actieve_segmenten
        s4 = 'S4' in actieve_segmenten

        # S1
        k1 = self.segment_aan if s1 else self.segment_uit
        d1 = 16 if s1 else 1.2
        self.teken_schuine_boog(34 + (w - 25) / 2, cy + (h / 2) / 2, (w - 10) / 2, (h / 2) / 2, 194, 126, k1, d1)
        self.teken_schuine_lijn(28, cy + 88 - 0.6 * h/4, w - 68, cy + 78 - 0.3 * h/2, k1, d1)
        self.teken_schuine_lijn(58, cy + 30 - 0.6 * h/4, w - 40, cy + 30 - 0.3 * h/2, k1, d1)

        # S2 (Alleen de bovenboog en middenaanzet; geen rechterstam-overlap als S4 uit staat!)
        k2 = self.segment_aan if s2 else self.segment_uit
        d2 = 16 if s2 else 1.2
        self.teken_schuine_boog(25 + (w - 25) / 2, (cy + 20 - h/2) + ((cy + 20) - (cy + 20 - h/2)) / 2, (w - 25) / 2, ((cy + 20) - (cy + 20 - h/2)) / 2, 135, 70, k2, d2)
        self.teken_schuine_lijn(40, cy + 28 - 0.6 * h/4, w - 52, cy + 28 - 0.3 * h/2, k2, d2)

        # S3
        k3 = self.segment_aan if s3 else self.segment_uit
        d3 = 16 if s3 else 1.2
        self.teken_schuine_lijn(48, cy + 10 - h/2, w - 5, cy + 10 - h/2, k3, d3)
        self.teken_schuine_lijn(40, cy - 60 - 0.6 * h/4, w - 65, cy - 55 - 0.3 * h/2, k3, d3)
        self.teken_schuine_lijn(93, cy - 22 - 0.6 * h/4, w - 4, cy - 30 - 0.3 * h/2, k3, d3)
        self.teken_schuine_lijn(w + 2, cy - h/2 + 28, w, cy + h/2 - 180, k3, d3)

        # S4
        k4 = self.segment_aan if s4 else self.segment_uit
        d4 = 16 if s4 else 1.2
        self.teken_schuine_lijn(w + 2, cy - h/2 + 28, w, cy + h/2 - 180, k4, d4)
        self.teken_schuine_lijn(w - 1, cy - h/2 + 62, w - 9, cy + h/2 - 136, k4, d4)
        self.teken_schuine_lijn(w + 8, cy - h/2 + 158, 8 + w, cy + h/2 - 26, k4, d4)
        self.teken_schuine_lijn(70, cy + 10 - 0.6 * h/4, w - 22, cy - 1 - 0.3 * h/2, k4, d4)

        k4_accent = self.segment_grijs if s4 else self.segment_uit
        d4_accent = 16 if s4 else 1.2
        self.teken_schuine_lijn(w - 10, cy + 10 - 0.6 * h/4, w - 10, cy + 11 - 0.3 * h/2, k4_accent, d4_accent)

        # Overlapping S2 & S4: Alleen tekenen wanneer S4 ook echt meedoet (zodat S1+S2 voor '6' 100% zuiver blijft)
        if s2 and s4:
            k_ov = self.segment_aan
            d_ov = 16
        elif s2 or s4:
            k_ov = self.segment_grijs
            d_ov = 16
        else:
            k_ov = self.segment_uit
            d_ov = 1.2
        self.teken_schuine_lijn(w + 8, cy - h/2 + 150, w + 4, cy + h/2 - 65, k_ov, d_ov)
        self.teken_schuine_lijn(w - 3, cy - h/2 + 120, w, cy + h/2 - 75, k_ov, d_ov)

if __name__ == "__main__":
    root = tk.Tk()
    app = SingleButtonYNInterface(root)
    root.mainloop()
