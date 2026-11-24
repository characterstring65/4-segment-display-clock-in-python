import tkinter as tk
import math

class Kids4SegCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("4-Segment Kids Pocket LCD Calculator (Tier 2 Gray Overlap)")
        self.root.configure(bg="#2b6cb0")
        self.root.resizable(False, False)

        self.lcd_bg, self.seg_black, self.seg_gray, self.seg_ghost = "#cfd9cc", "#181d18", "#7e8a7d", "#bcc7b9"
        self.digits_map = {
            ('S1',): '0', ('S4',): '1', ('S1', 'S3'): '2', ('S1', 'S3', 'S4'): '3', ('S2', 'S4'): '4',
            ('S1', 'S2', 'S3'): '5', ('S1', 'S2'): '6', ('S3', 'S4'): '7', ('S1', 'S2', 'S3', 'S4'): '8', ('S2', 'S3', 'S4'): '9'
        }
        self.char_to_segs = {v: k for k, v in self.digits_map.items()}
        self.char_to_segs.update({'-': ('S3',), 'E': ('S1', 'S2', 'S3')})

        self.active_segs, self.current_entry, self.stored_value, self.pending_op = set(), "", None, None
        self.display_text, self.combo_step, self.blink_on = "0", 0, True

        hdr = tk.Frame(root, bg="#1e4e8c", padx=14, pady=8)
        hdr.pack(fill="x")
        tk.Label(hdr, text="JUNIOR 4-SEG CALC", font=("Helvetica", 12, "bold"), fg="#ffd166", bg="#1e4e8c").pack(side="left")
        tk.Label(hdr, text="0:S1  1:S4  2:S1+3  3:S1+3+4  4:S2+4  5:S1+2+3  6:S1+2  7:S3+4  8:All  9:S2+3+4", font=("Helvetica", 8, "bold"), fg="#e2e8f0", bg="#1e4e8c").pack(side="right")

        bezel = tk.Frame(root, bg="#1a202c", padx=12, pady=12)
        bezel.pack(padx=16, pady=(14, 8))
        self.canvas = tk.Canvas(bezel, width=520, height=118, bg=self.lcd_bg, highlightthickness=2, highlightbackground="#4a5568")
        self.canvas.pack()

        self.status_lbl = tk.Label(root, text="Teken een cijfer met S1–S4 en druk op [= / OK / × / C]", font=("Helvetica", 9, "bold"), fg="#ffffff", bg="#2b6cb0", pady=4)
        self.status_lbl.pack()

        kp = tk.Frame(root, bg="#2b6cb0", padx=16, pady=10)
        kp.pack(fill="x")

        sf = tk.LabelFrame(kp, text=" 1. TEKEN CIJFER (S1–S4) ", font=("Helvetica", 9, "bold"), fg="#ffd166", bg="#235796", bd=2, relief="groove", padx=10, pady=8)
        sf.pack(side="left", padx=(0, 12), fill="both", expand=True)

        self.btn_s3 = tk.Button(sf, text="S3  (Bovenbalk)", font=("Helvetica", 10, "bold"), width=24, height=2, bg="#edf2f7", fg="#1a202c", relief="raised", bd=3, command=lambda: self.toggle_seg("S3"))
        self.btn_s3.grid(row=0, column=0, columnspan=2, padx=4, pady=4, sticky="ew")
        self.btn_s2 = tk.Button(sf, text="S2\nLinks-Boven", font=("Helvetica", 10, "bold"), width=13, height=3, bg="#edf2f7", fg="#1a202c", relief="raised", bd=3, command=lambda: self.toggle_seg("S2"))
        self.btn_s2.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")
        self.btn_s1 = tk.Button(sf, text="S1\nLinks-Onder", font=("Helvetica", 10, "bold"), width=13, height=3, bg="#edf2f7", fg="#1a202c", relief="raised", bd=3, command=lambda: self.toggle_seg("S1"))
        self.btn_s1.grid(row=2, column=0, padx=4, pady=4, sticky="nsew")
        self.btn_s4 = tk.Button(sf, text="S4\n\nRechter\nStam", font=("Helvetica", 10, "bold"), width=10, height=6, bg="#edf2f7", fg="#1a202c", relief="raised", bd=3, command=lambda: self.toggle_seg("S4"))
        self.btn_s4.grid(row=1, column=1, rowspan=2, padx=4, pady=4, sticky="nsew")
        self.seg_buttons = {"S1": self.btn_s1, "S2": self.btn_s2, "S3": self.btn_s3, "S4": self.btn_s4}

        of = tk.LabelFrame(kp, text=" 2. REKENEN & OK ", font=("Helvetica", 9, "bold"), fg="#ffd166", bg="#235796", bd=2, relief="groove", padx=10, pady=8)
        of.pack(side="right", fill="both", expand=True)
        for txt, op, r, c in (("+", "+", 0, 0), ("−", "-", 0, 1), ("÷", "/", 1, 0)):
            tk.Button(of, text=txt, font=("Helvetica", 16, "bold"), width=7, height=2, bg="#f6ad55", fg="#1a202c", relief="raised", bd=3, command=lambda o=op: self.press_operator(o)).grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        self.combo_btn = tk.Button(of, text="=\nOK / × / C", font=("Helvetica", 11, "bold"), width=9, height=3, bg="#48bb78", fg="#1a202c", relief="raised", bd=3, command=self.press_combo)
        self.combo_btn.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        for i in (0, 1):
            of.grid_rowconfigure(i, weight=1)
            of.grid_columnconfigure(i, weight=1)

        self.update_button_visuals()
        self.blink_loop()
    def tp(self, x, y, sc, ox, oy):
        return ox + (x + 0.20 * (150 - y)) * sc, oy + y * sc

    def dl(self, x1, y1, x2, y2, col, th, sc, ox, oy):
        self.canvas.create_line(*self.tp(x1, y1, sc, ox, oy), *self.tp(x2, y2, sc, ox, oy), fill=col, width=th * sc, capstyle="round")

    def da(self, cx, cy, rx, ry, sg, eg, col, th, sc, ox, oy):
        pts = tuple(self.tp(cx + rx * math.cos(math.radians(sg + eg * i / 24)), cy - ry * math.sin(math.radians(sg + eg * i / 24)), sc, ox, oy) for i in range(25))
        for i in range(24):
            self.canvas.create_line(*pts[i], *pts[i+1], fill=col, width=th * sc, capstyle="round")

    def draw_digit(self, segs, ox, oy, sc=0.45):
        s1, s2, s3, s4 = 'S1' in segs, 'S2' in segs, 'S3' in segs, 'S4' in segs
        w, h, cy = 100, 200, 150
        c1, d1 = (self.seg_black, 16) if s1 else (self.seg_ghost, 1.3)
        self.da(34 + (w - 25)/2, cy + h/4, (w - 10)/2, h/4, 194, 126, c1, d1, sc, ox, oy)
        self.dl(28, cy + 88 - 0.15*h, w - 68, cy + 78 - 0.15*h, c1, d1, sc, ox, oy)
        self.dl(58, cy + 30 - 0.15*h, w - 40, cy + 30 - 0.15*h, c1, d1, sc, ox, oy)

        c2, d2 = (self.seg_black, 16) if s2 else (self.seg_ghost, 1.3)
        self.da(25 + (w - 25)/2, cy + 20 - h/4, (w - 25)/2, h/4, 135, 70, c2, d2, sc, ox, oy)
        self.dl(40, cy + 28 - 0.15*h, w - 62, cy + 28 - 0.15*h, c2, d2, sc, ox, oy)
        self.dl(w + 8, cy - h/2 + 150, w + 4, cy + h/2 - 65, c2, d2, sc, ox, oy)
        self.dl(w - 1, cy - h/2 + 120, w + 1, cy + h/2 - 75, c2, d2, sc, ox, oy)
        self.dl(w + 8, cy - h/2 + 158, w + 8, cy + h/2 - 26, c2, d2, sc, ox, oy)

        c3, d3 = (self.seg_black, 16) if s3 else (self.seg_ghost, 1.3)
        self.dl(48, cy + 10 - h/2, w - 5, cy + 10 - h/2, c3, d3, sc, ox, oy)
        self.dl(40, cy - 60 - 0.15*h, w - 65, cy - 55 - 0.15*h, c3, d3, sc, ox, oy)
        self.dl(105, cy - 22 - 0.15*h, w + 5, cy - 30 - 0.15*h, c3, d3, sc, ox, oy)
        self.dl(w + 2, cy - h/2 + 28, w, cy + h/2 - 180, c3, d3, sc, ox, oy)

        c4, d4 = (self.seg_black, 16) if s4 else (self.seg_ghost, 1.3)
        for x1, y1, x2, y2 in ((w+2, cy-h/2+28, w, cy+h/2-180), (w-1, cy-h/2+62, w-9, cy+h/2-136), (w+8, cy-h/2+158, w+8, cy+h/2-26), (w+8, cy-h/2+150, w+4, cy+h/2-65), (w-1, cy-h/2+120, w+1, cy+h/2-75), (105, cy-22-0.15*h, w+5, cy-30-0.15*h)):
            self.dl(x1, y1, x2, y2, c4, d4, sc, ox, oy)
        cg, dg = (self.seg_black, 16) if (s4 and s2) else ((self.seg_gray, 16) if s4 else (self.seg_ghost, 1.3))
        self.dl(70, cy + 10 - 0.15*h, w - 22, cy - 1 - 0.15*h, cg, dg, sc, ox, oy)

    def render_lcd(self):
        self.canvas.delete("all")
        if self.stored_value is not None:
            op_txt = {"+": "+", "-": "−", "/": "÷", "*": "×"}.get(self.pending_op, "")
            self.canvas.create_text(14, 14, anchor="w", text=f"MEM: {self.fmt(self.stored_value)} {op_txt}", font=("Courier", 10, "bold"), fill="#3b463b")

        slots = {i: () for i in range(8)}
        dot_pos = None
        if self.active_segs or self.current_entry != "":
            comm = self.current_entry[-7:]
            start = 7 - len(comm)
            for i, ch in enumerate(comm):
                slots.update({start + i: self.char_to_segs.get(ch, ())})
            slots.update({7: tuple(self.active_segs) if self.blink_on else ()})
        else:
            chars = list()
            for ch in self.display_text:
                if ch == '.':
                    dot_pos = len(chars) - 1
                else:
                    chars.append(ch)
            chars = chars[-8:]
            if dot_pos is not None:
                dot_pos -= len(self.display_text.replace('.', '')) - len(chars)
            start = 8 - len(chars)
            for i, ch in enumerate(chars):
                slots.update({start + i: self.char_to_segs.get(ch, ())})
            dot_pos = (start + dot_pos) if (dot_pos is not None and 0 <= dot_pos < len(chars)) else None

        for idx in range(8):
            ox = 16 + idx * 61
            self.draw_digit(slots.get(idx, ()), ox, -4, 0.45)
            if dot_pos == idx:
                self.canvas.create_oval(ox + 54, 102, ox + 60, 108, fill=self.seg_black, outline="")

    def toggle_seg(self, seg):
        self.combo_step = 0
        self.active_segs.remove(seg) if seg in self.active_segs else self.active_segs.add(seg)
        if self.pending_op is None and self.current_entry == "" and self.display_text != "0":
            self.stored_value, self.display_text = None, "0"
        self.update_button_visuals()
        self.render_lcd()

    def update_button_visuals(self):
        for seg, btn in self.seg_buttons.items():
            btn.configure(bg="#ffd166" if seg in self.active_segs else "#edf2f7", relief="sunken" if seg in self.active_segs else "raised")
        if self.active_segs:
            self.combo_btn.configure(text="OK (Cijfer)\n[1× druk]", bg="#48bb78")
        elif self.current_entry != "":
            self.combo_btn.configure(text="= / Getal OK\n[2× druk]", bg="#68d391")
        elif self.combo_step == 1:
            self.combo_btn.configure(text="× (Keer)\n[3× druk]", bg="#f6ad55")
        elif self.combo_step >= 2:
            self.combo_btn.configure(text="C (Clear)\n[4× druk]", bg="#fc8181")
        else:
            self.combo_btn.configure(text="=\nOK / × / C", bg="#48bb78")

    def fmt(self, val):
        s = str(int(round(val))) if abs(val - round(val)) < 1e-9 else f"{val:.4f}".rstrip('0').rstrip('.')
        return "E" if len(s.replace('.', '')) > 8 else s

    def calc(self, a, b, op):
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/": return None if abs(b) < 1e-12 else a / b
        return b

    def press_operator(self, op):
        self.combo_step = 0
        if self.active_segs:
            key = tuple(sorted(self.active_segs))
            if key not in self.digits_map:
                self.status_lbl.configure(text="Ongeldig cijfer! Pas S1–S4 aan.", fg="#fed7d7")
                return
            self.current_entry += self.digits_map[key]
            self.active_segs.clear()
        if self.current_entry != "":
            val = float(self.current_entry)
            if self.stored_value is not None and self.pending_op is not None:
                res = self.calc(self.stored_value, val, self.pending_op)
                if res is None:
                    self.reset_all("Fout: delen door 0! Alles gewist.")
                    return
                self.stored_value, self.display_text = res, self.fmt(res)
            else:
                self.stored_value, self.display_text = val, self.fmt(val)
            self.current_entry = ""
        elif self.stored_value is None:
            self.stored_value = float(self.display_text) if self.display_text != "E" else 0.0
        self.pending_op = op
        self.status_lbl.configure(text=f"Bewerking gekozen — teken nu het volgende cijfer!", fg="#ffd166")
        self.update_button_visuals()
        self.render_lcd()

    def press_combo(self):
        if self.active_segs:
            key = tuple(sorted(self.active_segs))
            if key not in self.digits_map:
                self.status_lbl.configure(text="Geen geldig cijfer (0–9)! Pas segmenten aan.", fg="#fed7d7")
                return
            ch = self.digits_map[key]
            if len(self.current_entry) < 7:
                self.current_entry += ch
            self.active_segs.clear()
            self.combo_step = 0
            self.status_lbl.configure(text=f"Cijfer '{ch}' vastgezet! Teken nog een cijfer of druk nogmaals voor Getal OK / [=].", fg="#c6f6d5")
            self.update_button_visuals()
            self.render_lcd()
            return
        if self.current_entry != "":
            val = float(self.current_entry)
            if self.stored_value is not None and self.pending_op is not None:
                res = self.calc(self.stored_value, val, self.pending_op)
                if res is None:
                    self.reset_all("Fout: delen door 0! Alles gewist.")
                    return
                self.display_text, self.stored_value, self.pending_op = self.fmt(res), res, None
                self.status_lbl.configure(text=f"Uitkomst (=): {self.display_text}  |  Druk nogmaals voor [×] (Keer)", fg="#ffd166")
            else:
                self.stored_value, self.display_text = val, self.fmt(val)
                self.status_lbl.configure(text=f"Getal {self.display_text} bevestigd (=)  |  Druk nogmaals voor [×] (Keer)", fg="#ffd166")
            self.current_entry, self.combo_step = "", 1
            self.update_button_visuals()
            self.render_lcd()
            return
        if self.combo_step == 1:
            if self.stored_value is None:
                self.stored_value = float(self.display_text) if self.display_text != "E" else 0.0
            self.pending_op, self.combo_step = "*", 2
            self.status_lbl.configure(text="Vermenigvuldigen (×) actief! Teken het volgende cijfer (of druk nogmaals voor Clear).", fg="#fbd38d")
            self.update_button_visuals()
            self.render_lcd()
            return
        self.reset_all("Clear (C) — Scherm gewist op 0!")

    def reset_all(self, msg):
        self.active_segs.clear()
        self.current_entry, self.stored_value, self.pending_op, self.display_text, self.combo_step = "", None, None, "0", 0
        self.status_lbl.configure(text=msg, fg="#ffffff")
        self.update_button_visuals()
        self.render_lcd()

    def blink_loop(self):
        self.blink_on = not self.blink_on
        if self.active_segs or self.current_entry != "":
            self.render_lcd()
        self.root.after(450, self.blink_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = Kids4SegCalculator(root)
    root.mainloop()