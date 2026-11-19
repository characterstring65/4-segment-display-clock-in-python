import tkinter as tk
import math

class WristPhoneDialer:
    def __init__(self, root):
        self.root = root
        self.root.title("4-Segment Fat-Finger Wrist Dialer")
        self.root.configure(bg='#1e2229')
        self.root.resizable(False, False)

        # Authentic LCD colors
        self.lcd_bg = '#d8e3d8'
        self.seg_on = '#151828'
        self.seg_gray = '#7e8984'  # 50% checkerboard overlap simulation
        self.seg_off = '#cad6ca'

        self.phone_number = ""
        self.active_segments = set()

        # Mapping of segment combinations to digits 0-9
        self.pattern_to_digit = {
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

        self.setup_ui()
        self.update_displays()

    def setup_ui(self):
        # --- TOP: Main Phone Number Display ---
        top_frame = tk.Frame(self.root, bg='#1e2229', pady=12, padx=15)
        top_frame.pack(fill='x')

        tk.Label(
            top_frame,
            text="DIALED NUMBER (4-SEGMENT DISPLAY)",
            fg='#9aa89a',
            bg='#1e2229',
            font=("Segoe UI", 9, "bold")
        ).pack(anchor='w', pady=(0, 4))

        self.main_canvas = tk.Canvas(
            top_frame,
            width=460,
            height=85,
            bg=self.lcd_bg,
            highlightthickness=2,
            highlightbackground="#4a5459"
        )
        self.main_canvas.pack()

        # Status / Feedback banner
        self.status_label = tk.Label(
            top_frame,
            text="Ready: Tap segments to draw digit (S2 first for 4,5,6,8,9)",
            fg='#61afef',
            bg='#1e2229',
            font=("Segoe UI", 9)
        )
        self.status_label.pack(anchor='w', pady=(6, 0))

        # --- CENTER: Equal 2x2 Fat-Finger Grid matching segment positions ---
        # Top-Left: S2 (Clickable 1-Digit LCD Window) | Top-Right: S3
        # Bottom-Left: S1                            | Bottom-Right: S4
        pad_frame = tk.Frame(self.root, bg='#1e2229', padx=15, pady=5)
        pad_frame.pack()

        tile_w = 215
        tile_h = 165

        # 1. TOP-LEFT: S2 (The Clickable 1-Digit LCD Window)
        self.s2_outer = tk.Frame(
            pad_frame,
            width=tile_w,
            height=tile_h,
            bg='#3b4252',
            bd=3,
            relief='raised',
            cursor='hand2'
        )
        self.s2_outer.grid(row=0, column=0, padx=6, pady=6)
        self.s2_outer.grid_propagate(False)

        self.input_canvas = tk.Canvas(
            self.s2_outer,
            width=tile_w - 10,
            height=tile_h - 10,
            bg=self.lcd_bg,
            highlightthickness=0,
            cursor='hand2'
        )
        self.input_canvas.pack(expand=True, fill='both', padx=2, pady=2)
        self.input_canvas.bind("<Button-1>", lambda e: self.on_s2_window_click())

        # 2. TOP-RIGHT: S3 Button
        self.btn_s3 = tk.Button(
            pad_frame,
            text="S3\n(Top Bar)",
            font=("Segoe UI", 12, "bold"),
            bg='#2e3440',
            fg='#eceff4',
            activebackground='#4c566a',
            activeforeground='#ffffff',
            relief='raised',
            bd=3,
            cursor='hand2',
            command=lambda: self.toggle_segment('S3')
        )
        self.btn_s3.grid(row=0, column=1, padx=6, pady=6, sticky='nsew')
        pad_frame.grid_columnconfigure(0, minsize=tile_w + 12)
        pad_frame.grid_columnconfigure(1, minsize=tile_w + 12)
        pad_frame.grid_rowconfigure(0, minsize=tile_h + 12)
        pad_frame.grid_rowconfigure(1, minsize=tile_h + 12)

        # 3. BOTTOM-LEFT: S1 Button
        self.btn_s1 = tk.Button(
            pad_frame,
            text="S1\n(Lower-Left Curve)",
            font=("Segoe UI", 12, "bold"),
            bg='#2e3440',
            fg='#eceff4',
            activebackground='#4c566a',
            activeforeground='#ffffff',
            relief='raised',
            bd=3,
            cursor='hand2',
            command=lambda: self.toggle_segment('S1')
        )
        self.btn_s1.grid(row=1, column=0, padx=6, pady=6, sticky='nsew')

        # 4. BOTTOM-RIGHT: S4 Button
        self.btn_s4 = tk.Button(
            pad_frame,
            text="S4\n(Right Stem)",
            font=("Segoe UI", 12, "bold"),
            bg='#2e3440',
            fg='#eceff4',
            activebackground='#4c566a',
            activeforeground='#ffffff',
            relief='raised',
            bd=3,
            cursor='hand2',
            command=lambda: self.toggle_segment('S4')
        )
        self.btn_s4.grid(row=1, column=1, padx=6, pady=6, sticky='nsew')

        # --- BOTTOM: Utility Action Bar ---
        action_frame = tk.Frame(self.root, bg='#1e2229', pady=12, padx=15)
        action_frame.pack(fill='x')

        tk.Button(
            action_frame,
            text="CLEAR DIGIT",
            font=("Segoe UI", 9, "bold"),
            bg='#434c5e',
            fg='#eceff4',
            width=13,
            pady=6,
            cursor='hand2',
            command=self.clear_current_digit
        ).pack(side='left', padx=(0, 6))

        tk.Button(
            action_frame,
            text="BACKSPACE",
            font=("Segoe UI", 9, "bold"),
            bg='#bf616a',
            fg='#ffffff',
            width=13,
            pady=6,
            cursor='hand2',
            command=self.backspace
        ).pack(side='left', padx=6)

        tk.Button(
            action_frame,
            text="CALL",
            font=("Segoe UI", 9, "bold"),
            bg='#a3be8c',
            fg='#1e2229',
            width=15,
            pady=6,
            cursor='hand2',
            command=self.dial_call
        ).pack(side='right')

    def toggle_segment(self, seg):
        if seg in self.active_segments:
            self.active_segments.remove(seg)
        else:
            self.active_segments.add(seg)
        self.status_label.config(
            text=f"Drawing: {sorted(list(self.active_segments))} — Tap S2 window to confirm",
            fg='#ebcb8b'
        )
        self.update_displays()

    def on_s2_window_click(self):
        # S2-First Protocol:
        # 1. If window is completely empty, pressing S2 turns segment S2 ON.
        # 2. If segments are already visible, pressing S2 confirms and enters the digit.
        if len(self.active_segments) == 0:
            self.active_segments.add('S2')
            self.status_label.config(
                text="S2 activated! Add other segments or tap S2 window again to confirm 'S2'",
                fg='#ebcb8b'
            )
            self.update_displays()
        else:
            self.confirm_digit()

    def confirm_digit(self):
        pattern = frozenset(self.active_segments)
        if pattern in self.pattern_to_digit:
            digit = self.pattern_to_digit[pattern]
            if len(self.phone_number) < 12:
                self.phone_number += digit
                self.status_label.config(
                    text=f"Entered digit '{digit}'! Ready for next digit.",
                    fg='#a3be8c'
                )
            else:
                self.status_label.config(text="Maximum 12 digits reached.", fg='#bf616a')
            self.active_segments.clear()
        else:
            self.status_label.config(
                text="Invalid segment pattern! Adjust or press CLEAR DIGIT.",
                fg='#bf616a'
            )
        self.update_displays()

    def clear_current_digit(self):
        self.active_segments.clear()
        self.status_label.config(text="Current digit cleared.", fg='#9aa89a')
        self.update_displays()

    def backspace(self):
        if self.active_segments:
            self.active_segments.clear()
            self.status_label.config(text="Cleared active drawing.", fg='#9aa89a')
        elif self.phone_number:
            removed = self.phone_number[-1]
            self.phone_number = self.phone_number[:-1]
            self.status_label.config(text=f"Removed '{removed}'.", fg='#9aa89a')
        self.update_displays()

    def dial_call(self):
        if not self.phone_number:
            self.status_label.config(text="Enter a number first before calling.", fg='#bf616a')
        else:
            self.status_label.config(text=f"Dialing {self.phone_number} ...", fg='#88c0d0')

    # --- Drawing routines (matching the pure 4-segment geometry) ---
    def transform_point(self, x, y, scale, ox, oy, cy=150, shear=0.20):
        nx = x + shear * (cy - y)
        return ox + nx * scale, oy + y * scale

    def draw_line(self, canvas, x1, y1, x2, y2, color, width, scale, ox, oy):
        tx1, ty1 = self.transform_point(x1, y1, scale, ox, oy)
        tx2, ty2 = self.transform_point(x2, y2, scale, ox, oy)
        canvas.create_line(tx1, ty1, tx2, ty2, fill=color, width=max(1.2, width * scale), capstyle='round')

    def draw_arc(self, canvas, cx, cy, rx, ry, start_deg, extent_deg, color, width, scale, ox, oy):
        pts = []
        steps = 24
        for i in range(steps + 1):
            rad = math.radians(start_deg + (extent_deg * i / steps))
            px = cx + rx * math.cos(rad)
            py = cy - ry * math.sin(rad)
            pts.append(self.transform_point(px, py, scale, ox, oy))
        w = max(1.2, width * scale)
        for i in range(len(pts) - 1):
            canvas.create_line(pts[i], pts[i+1], fill=color, width=w, capstyle='round', joinstyle='round')

    def draw_4seg_digit(self, canvas, active_set, scale, ox, oy):
        w, h, cy = 100, 200, 150
        s1 = 'S1' in active_set
        s2 = 'S2' in active_set
        s3 = 'S3' in active_set
        s4 = 'S4' in active_set

        # S1
        c1 = self.seg_on if s1 else self.seg_off
        t1 = 16 if s1 else 1.5
        self.draw_arc(canvas, 34 + (w - 25)/2, cy + h/4, (w - 10)/2, h/4, 194, 126, c1, t1, scale, ox, oy)
        self.draw_line(canvas, 28, cy + 88 - 0.6*h/4, w - 68, cy + 78 - 0.3*h/2, c1, t1, scale, ox, oy)
        self.draw_line(canvas, 58, cy + 30 - 0.6*h/4, w - 40, cy + 30 - 0.3*h/2, c1, t1, scale, ox, oy)

        # S2
        c2 = self.seg_on if s2 else self.seg_off
        t2 = 16 if s2 else 1.5
        cy_b = (cy + 20 - h/2) + ((cy + 20) - (cy + 20 - h/2)) / 2
        ry_b = ((cy + 20) - (cy + 20 - h/2)) / 2
        self.draw_arc(canvas, 25 + (w - 25)/2, cy_b, (w - 25)/2, ry_b, 135, 70, c2, t2, scale, ox, oy)
        self.draw_line(canvas, 40, cy + 28 - 0.6*h/4, w - 52, cy + 28 - 0.3*h/2, c2, t2, scale, ox, oy)

        # S3
        c3 = self.seg_on if s3 else self.seg_off
        t3 = 16 if s3 else 1.5
        self.draw_line(canvas, 48, cy + 10 - h/2, w - 5, cy + 10 - h/2, c3, t3, scale, ox, oy)
        self.draw_line(canvas, 40, cy - 60 - 0.6*h/4, w - 65, cy - 55 - 0.3*h/2, c3, t3, scale, ox, oy)
        self.draw_line(canvas, 93, cy - 22 - 0.6*h/4, w - 4, cy - 30 - 0.3*h/2, c3, t3, scale, ox, oy)
        self.draw_line(canvas, w + 2, cy - h/2 + 28, w, cy + h/2 - 180, c3, t3, scale, ox, oy)

        # S4
        c4 = self.seg_on if s4 else self.seg_off
        t4 = 16 if s4 else 1.5
        self.draw_line(canvas, w + 2, cy - h/2 + 28, w, cy + h/2 - 180, c4, t4, scale, ox, oy)
        self.draw_line(canvas, w - 1, cy - h/2 + 62, w - 9, cy + h/2 - 136, c4, t4, scale, ox, oy)
        self.draw_line(canvas, w + 8, cy - h/2 + 158, w + 8, cy + h/2 - 26, c4, t4, scale, ox, oy)
        self.draw_line(canvas, 70, cy + 10 - 0.6*h/4, w - 22, cy - 1 - 0.3*h/2, c4, t4, scale, ox, oy)

        # S4 Inner accent stroke (rendered with checkerboard light-gray when active)
        c4_acc = self.seg_gray if s4 else self.seg_off
        self.draw_line(canvas, w - 10, cy + 10 - 0.6*h/4, w - 10, cy + 11 - 0.3*h/2, c4_acc, t4, scale, ox, oy)

        # Shared S2/S4 Checkerboard Overlap
        if s2 and s4:
            co, to = self.seg_on, 16
        elif s2 or s4:
            co, to = self.seg_gray, 16
        else:
            co, to = self.seg_off, 1.5
        self.draw_line(canvas, w + 8, cy - h/2 + 150, w + 4, cy + h/2 - 65, co, to, scale, ox, oy)
        self.draw_line(canvas, w - 3, cy - h/2 + 120, w, cy + h/2 - 75, co, to, scale, ox, oy)

    def update_displays(self):
        # 1. Update button visual highlights
        btn_map = {'S1': self.btn_s1, 'S3': self.btn_s3, 'S4': self.btn_s4}
        for seg, btn in btn_map.items():
            if seg in self.active_segments:
                btn.config(bg='#5e81ac', fg='#ffffff', relief='sunken')
            else:
                btn.config(bg='#2e3440', fg='#eceff4', relief='raised')

        # 2. Update Clickable S2 1-Digit Input Window (Top-Left)
        self.input_canvas.delete("all")
        cw = int(self.input_canvas['width'])
        ch = int(self.input_canvas['height'])

        # Clear dashed square border inside the clickable LCD tile so it's unmistakably a button
        self.input_canvas.create_rectangle(
            6, 6, cw - 6, ch - 6,
            outline='#5c6b63',
            dash=(4, 3),
            width=1.5
        )
        self.input_canvas.create_text(
            cw // 2, 16,
            text="S2 / CONFIRM (TAP)",
            fill='#3b4a42',
            font=("Segoe UI", 8, "bold")
        )

        # Draw the single active digit centered in the S2 window
        self.draw_4seg_digit(self.input_canvas, self.active_segments, scale=0.46, ox=68, oy=16)

        # 3. Update Main Phone Number Display (Top)
        self.main_canvas.delete("all")
        if not self.phone_number:
            self.main_canvas.create_text(
                230, 42,
                text="— — — — — — — — — —",
                fill='#9aa89a',
                font=("Segoe UI", 14, "bold")
            )
        else:
            digit_to_segs = {v: k for k, v in self.pattern_to_digit.items()}
            for idx, ch_digit in enumerate(self.phone_number):
                segs = digit_to_segs.get(ch_digit, set())
                self.draw_4seg_digit(self.main_canvas, segs, scale=0.28, ox=12 + idx * 36, oy=0)

if __name__ == "__main__":
    root = tk.Tk()
    app = WristPhoneDialer(root)
    root.mainloop()
