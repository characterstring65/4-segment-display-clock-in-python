<img width="181" height="199" alt="S2" src="https://github.com/user-attachments/assets/ec2c0bbe-62b8-4576-bf3f-a0f4e6543e7a" />

<img width="1400" height="1020" alt="tier1_all_digits_clock_style" src="https://github.com/user-attachments/assets/33272eef-a16a-4f20-8273-aebc8e23e82b" />

# 4-Segment Display Architecture (The 6 Visual Tiers)

An ultra-minimalist numeric display architecture built in Python and engineered for low-pin-count hardware, optical wearables, mechanical club scoreboards, and tactile interfaces. Using a custom, fluid **4-segment matrix** ($2^4 = 16$ states), it achieves effortless legibility at the absolute mathematical minimum required to distinguish the digits `0` through `9`.

Rather than organizing this project around an ever-growing list of individual gadgets and novelties, the architecture is structured around **6 distinct graphical expressions (Visual Tiers)**—ranging from the raw, non-overlapping 4-stroke foundation up to decoded, calligraphically complete typography.

---

## 1. The 6 Visual Tiers (Graphical Taxonomy)

Every simulator, printable test sheet, and hardware implementation in this repository belongs to one of six graphical tiers:

| Tier | Graphical Expression | Visual Character | Representative Implementations & Files |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Raw Non-Overlapping 4-Stroke** | Pure `S1`–`S4` strokes with no overlap shading; clean, open, and direct. | Desktop clock (`clock.py`), basic micro-LCD (`LCD_like_python_clock.py`), Senior Date-Trainer (`senior_date_trainer_clock.py`). |
| **Tier 2** | **50% Dithered Gray Overlap** | Single-layer LCD with a 50% micro-checkerboard at `S2`/`S4` (light gray when single-active, black when dual-active). | Checkerboard micro-LCD (`micro_lcd_checkerboard_clock.py`), 8-wire 4×4 probe pen, 1-button scanner (`single_button_yn_interface.py`), 1:1 print sheet (`4segment_multidigit_lcd_sheet.pdf`). |
| **Tier 3** | **Solid-Black Intersection** | Same 4 strokes, but `S2`/`S4` intersections turn solid black with full single-layer viewing angles. | Flip-up pen with rear zener mini-PCB, 4-wire "Zero-COM" dual-layer LCD, 4-piece calligraphy stamp set (ink overprint). |
| **Tier 4** | **Short-Stroke `+L1 / +L2` Compromise** | Core 4 segments + 2 compact auxiliary strokes (`+L1` 60° arc on `0,2,6,8`; `+L2` waist on `2`) for effortless mechanical travel. | Easy-build club scoreboard (`scoreboard_lever_digits.py`), tiny `74HC00` logic helper PCB for LED displays. |
| **Tier 5** | **Advanced Multi-Lever Mechanical** *(Future)* | Further refined closed-loop silhouettes pushed as far as sliding mechanical lamellae and linkages allow. | Advanced mechanical scoreboard (Option B with full `180°` lower-loop closure and refined linkage mechanics). |
| **Tier 6** | **Iconic & Calligraphically Complete** | An onboard decoder chip translates the 4 drive lines into many finely shaped sub-segments for textbook typography. | High-end multi-segment LCD modules preserving the simple 4-wire external interface. |

### Core Stroke & Digit Definitions
* **S1:** Fluid lower-left curve (solo `S1` forms **`0`**, seated directly on the baseline at half-height).
* **S2:** Fluid upper-left curve.
* **S3:** Shortened top horizontal bar with dynamic design accents.
* **S4:** Sharp right-side vertical stem featuring subtle calligraphic detail artifacts.

`0`: `S1` | `1`: `S4` | `2`: `S1+S3` | `3`: `S1+S3+S4` | `4`: `S2+S4` | `5`: `S1+S2+S3` | `6`: `S1+S2` | `7`: `S3+S4` | `8`: `S1+S2+S3+S4` | `9`: `S2+S3+S4`

---

## 2. Applications Grouped by Visual Tier

### Tier 1: Raw Non-Overlapping 4-Stroke
* **Fluid Desktop Clock (`clock.py`):** Borderless, always-on-top transparent desktop widget.
* **"Fat-Finger" Wrist Phone Dialer (`wrist_phone_dialer.py`):** Divides tiny touchscreens into four oversized 2×2 spatial touch zones (`S2/Confirm` top-left preview window, `S3` top-right, `S1` bottom-left, `S4` bottom-right).
* **4-Button Direct-Draw Calculator Input:** Replaces cramped 10-key pads on calculator watches with 4 tactile stroke buttons (`S1`–`S4`) plus the existing Mode button as Enter.
* **Senior Memory & Date-Recall Wall Clock (`senior_date_trainer_clock.py`):** A dignified daily memory game for older adults. While the wall clock always displays the time, the date window stays dark until the user presses the **single starting stroke** of today's final day digit (`S3` top wide bar for `2,5,9`; `S2` upper-left for `4,8`; `S1` lower-left for `0,3,6`; `S4` tall right stem for `1,7`) on an anatomical 4-button remote—building effortless muscle memory for 4-button numeric entry.

### Tier 2: 50% Dithered Gray Overlap (Single-Layer LCD Standard)
* **8-Wire 4×4 Passive Matrix (100% Pin Efficiency):** Drives a full 3½-digit display (3 digits × 4 segments + 3 decimal points + 1 MSD `'1'` = **16 elements**) over **4 rows + 4 columns = 8 wires** with zero internal driver chips.
* **50% Micro-Checkerboard Mask (`micro_lcd_checkerboard_clock.py`):** Etched within standard 0.05–0.1 mm glass rules so single-active crossings appear soft light gray and dual-active crossings (`4, 8, 9`) turn solid black at **$0.00 extra tooling cost**.
* **"Fluid Time" 5-Second Loop & Zero-Wire Status LED:** Alternates `HH:MM` (1s) and `MM:SS` (4s) on 4-digit rings/pens, while a direct-view SMD status LED across two matrix lines fires via microsecond high-voltage strobe pulses during blanking without disturbing the slow LCD crystals.
* **SMD Kelvin Probe Pen & Modular Shunt:** Uses a 9-conductor retractable cable (8 display wires + 1 Kelvin Sense wire), whole-display blinking for negative polarity, and a separate pocket-carried external shunt cable ($I = U / R$) to keep heat out of the pen.
* **1-Button "Single-Window Scan & y/n Confirm" (`single_button_yn_interface.py`):** Scans `S1 → S2 → S3 → S4` (3 blinks each) on a single clickable 1-digit window, confirming via `y` (`S1+S2+S4`) or clearing via `n` (`S2+S3`), backed by a hybrid mechanical-wake + capacitive-touch switch.
* **Wearable Optical-Contact 2FA Key & Smart Sticker Mode:** Uses a gold contact pad + optical camera readout of the 4 LCD segments for two-way challenge-response authentication, or a trickle-charged SMD capacitor for zero-standby press-to-read adhesive labels.
* **Ultra-Compact Kids' Calculator Watch (`kids_4seg_calculator.py`) — *(Tier 2)*:**  
    Traditional calculator watches cram 16 or more pinhead-sized buttons onto a tiny bezel—making them nearly impossible to use on a child's narrow wrist. This Python simulator models an **ultra-miniature, low-cost kids' LCD calculator watch** built around just **8 generous, tactile keys**:
    * **Anatomical 4-Key Digit Builder (`S1`–`S4`):** Four buttons arranged in the physical shape of a digit (`S3` top bar, `S2` upper-left, `S1` lower-left, `S4` tall right stem) let children "draw" each numeral directly onto a classic greenish-gray **Tier 2 reflective LCD** (complete with 50% gray `S2`/`S4` overlap shading).
    * **4-Key Math Cluster (`+`, `−`, `÷`, and the 4-Stage `= / OK / × / C` Multi-Tap Key):** Saves even more space on the tiny watch case by combining four actions into one smart button—**1st press:** confirm digit; **2nd press:** confirm full number / calculate (`=`); **3rd press:** multiply (`×`); **4th press:** clear (`C`).

<img width="1110" height="1200" alt="4segment_12_glyphs_overview" src="https://github.com/user-attachments/assets/d9043960-f300-462b-af84-aeb73ccbb571" />


### Tier 3: Solid-Black Intersection
* **Flip-Up Pen LCD with Rear Semi-Circular Mini-PCB (Zero Extra Hinge Wires):**  
  Designed for an 8 mm pen chassis (6 mm internal hinge zone + 2 mm transition bridge), the display leaves a natural **semi-circular cavity** behind the glass when recessed halfway into the barrel. By etching the `S2`/`S4` intersection as a **single solid island** and routing just **3 short local pins** (`S2`, `S4`, and the shared island) from the rear edge of the glass to a tiny SMD zener-bridge strip PCB in that cavity, the intersection turns **solid black** with full single-layer viewing angles and **zero extra wires** through the hinge:
  ```text
  S2 ──[ Z1 ]──┬──► Shared Intersection Island (Solid Black)
  S4 ──[ Z2 ]──┘         └──[ ~1–2 MΩ ITO Bleed ]──► Backplane (COM)
  ```
* **4-Wire "Zero-COM" Single-Digit Dual-Layer LCD:** Cross-wires two stacked thin LCD cells in a closed loop across 4 external terminals (`W1`–`W4`), eliminating the `COM` line while achieving true solid-black overlaps without silicon chips.
* **Modular 4-Piece Calligraphy Stamp Set:** Four transparent acrylic stamp blocks (`S1`–`S4`) aligned with an L-guide naturally deposit a **double layer of ink** where `S2` and `S4` overlap, creating rich letterpress tonal depth.

### Tier 4 & Tier 5: Mechanical Scoreboard Linkages & Logic Helper PCBs
* **Mechanical Club Scoreboard (`scoreboard_lever_digits.py`):** Uses a flat, wind-proof front cutout mask with 4 counterweighted sliding lamellae driven by a **2-motor plotter shuttle** along a 32-pin bottom bus (saving 14 motors). Passive pivoting wooden levers behind the mask drive auxiliary filler pieces with zero extra motors or code:
  * **Tier 4 (Option A — Short-Stroke Compromise):** A compact `60°` upper-left arc (`+L1` for `0, 2, 6, 8`) and short diagonal waist (`+L2` for `2`) that glide lightly with minimal travel for easy club assembly.
  * **Tier 5 (Option B — Advanced Multi-Lever Closure):** Extended guide tracks and linkages (such as a `180°` lower-loop closure on `0, 6, 8`) for workshops seeking an even more closed silhouette within the physical limits of sliding lamellae.
* **Tiny Logic Helper PCB for LED Displays (Tier 4 Electronic Equivalent):** A postage-stamp `74HC00` quad-NAND board listening to `S1`–`S4` automatically drives hand-ground acrylic LED lenses for `L1` and `L2`:
  * $\text{L1} = S1 \land (\neg S3 \lor (\neg S2 \land \neg S4))$
  * $\text{L2} = S1 \land S3 \land \neg S2 \land \neg S4$

<img width="1344" height="972" alt="scoreboard_lever_digits (6)" src="https://github.com" />

### Tier 6: Iconic & Calligraphically Complete (High-End Decoded LCDs)
* **Scalable to Premium Multi-Segment Modules:** This 4-line encoding also serves as a clean, low-pin-count foundation for higher-end LCD designs—where an onboard decoder chip translates the four incoming drive wires into a larger array of finely tailored sub-segments, delivering near-ideal, calligraphically complete typography without increasing external pin count.

---

## 3. Repository Index & Running the Simulators

> **💡 Intermezzo — A Geeky Mnemonic & Binary Finger Joke ($U = I \times R$):**  
> Before jumping into the DIY workbench, here is a playful easter egg for the multimeter shunt equation mentioned earlier. Spoken aloud with a calm, dramatic pause—*"U... I-R"* (sounding like *"You... I times R"*)—Ohm's Law already has a nice ring to it. Better yet, you can "count" it out in binary on a standard QWERTY keyboard:  
> 1. Count **1** (`01` in binary) by resting your right index finger straight forward—landing right on **`U`**.  
> 2. Count **2** (`10` in binary) by lifting your index finger and raising your right middle finger *(strictly for binary counting purposes, of course!)*—landing right on **`I`**.  
> 3. Having exhausted both finger states on that hand, carry over to your left index finger—landing straight on **`R`**.  
> **U — I — R** ($U = I \times R$). Completely unnecessary, yet mathematically undeniable!

### Quick Start
All Python simulators run on standard Python 3 with `tkinter` (only `generate_multidigit_lcd_sheet.py` requires `pip install reportlab`):
```bash
git clone https://github.com
cd 4-segment-display-clock-in-python
python micro_lcd_checkerboard_clock.py
```

| File | Tier | Description |
| :--- | :--- | :--- |
| `clock.py` | Tier 1 | Borderless floating desktop clock. |
| `LCD_like_python_clock.py` | Tier 1 | Scalable reflective micro-LCD simulator (4–12 mm). |
| `wrist_phone_dialer.py` | Tier 1 | 2×2 spatial touch dialer for tiny wrist screens. |
Wees voorzichtig met code.
| senior_date_trainer_clock.py | Tier 1 | Wall clock & anatomical 4-button remote memory game. |
| micro_lcd_checkerboard_clock.py | Tier 2 | Micro-LCD simulator with 50% dithered S2/S4 overlap. |
| single_button_yn_interface.py | Tier 2 | 1-button single-window segment scanner & y/n confirm. |
| generate_multidigit_lcd_sheet.py | Tier 2 / 4 | Generates 1:1 scale A4 vector PDFs (reportlab). |
| 4segment_multidigit_lcd_sheet.pdf | Tier 2 / 4 | Ready-to-print 1:1 multi-digit LCD legibility test sheet. |
| scoreboard_lever_digits.py | Tier 4 | Visualizes the 4 lamellae + short-stroke levers (+L1, +L2). |
| xiao_4segment_wristband.ino | Tier 2 | Starter Arduino sketch for Seeed XIAO 4×4 LED wristband. |
💡 Intermezzo — Binary Finger Mnemonic for Ohm's Law ($U = I \times R$):
Spoken aloud with a calm pause—"U... I-R" ("You... I times R")—Ohm's Law can also be counted in binary on a QWERTY keyboard: count 1 (01) with your right index finger on U, count 2 (10) with your right middle finger on I, and carry over to your left index finger on R. U — I — R ($U = I \times R$).

## 4. Maker's Corner: Fun & Low-Cost DIY Tips

Building a prototype at home does not require custom factory glass. Here are nine simple, rewarding weekend projects for tinkerers, crafters, and clubs—each tagged with its corresponding **Visual Tier**:

1. **Hand-Ground Acrylic LED Lenses (Zero-Tooling Display) — *(Tier 2 & Tier 3)*:**  
   Build the 4×4 matrix using inexpensive individual SMD LEDs on a simple PCB, then file and polish tiny lightguide lenses out of clear acrylic (PMMA) into the exact curves of **S1–S4**. Placed over the LEDs, they diffuse light into a warm, organic glow. You can recreate the **two-tone light-gray overlap (Tier 2)** without code by feeding the shared `S2`/`S4` overlap LED from both lines through two resistors and isolating diodes (one line active = soft half-brightness; both lines active = full brightness), or use `analogWrite` PWM on a microcontroller (or drive it at full brightness for a **Tier 3 solid-black/solid-glow** look). A status LED can also be added across two matrix lines using simple resistor-diode voltage-drop balancing so the status LED lights at lower drive thresholds while higher-threshold green/blue segment LEDs stay off.
2. **Through-Glass Status LED on Any Standard LCD — *(Tier 2)*:**  
   Take an off-the-shelf reflective LCD and carefully scrape away a tiny 2 × 2 mm spot of the outer silver/gray **reflective foil** on the back in an unused corner (**keep the clear polarizing film underneath intact!**). Glue a miniature `0402` or `0603` SMD LED behind this window and wire it across two matrix lines using the voltage-threshold trick for a through-glass indicator with zero extra wires.
3. **Instant Full-Screen Backlight — *(Tier 1 & Tier 2)*:**  
   Gently peel the entire outer reflector foil off the back of a standard reflective LCD and replace it with a piece of **plain white paper or frosted plastic** as a diffuser. Place a small LED at the edge or behind it to turn any passive LCD into a softly backlit screen.
4. **Driving from a Standard 7-Segment Clock IC (No Code Needed) — *(Tier 1)*:**  
   Want to retrofit an old digital alarm clock or `CD4511` / `74LS47` driver chip? Connect 7-segment outputs `b`, `d`, and `f` directly to **S4**, **S1**, and **S2**. For **S3** (active on `2, 3, 5, 7, 8, 9`, omitting `0` and `6`), use a single tiny logic gate combining lines `a`, `b`, and `e`:
   $$\text{S3} = a \land (b \lor \neg e)$$
   *(i.e., **S3 = a AND (b OR NOT e)** — Note: This logic works directly on DC-driven LEDs. For AC-driven static LCD drivers, decode the phase against the `COM` signal first using XOR gates, or route line `a` through a simple `CD4066` analog bilateral switch.)*
5. **Wearable "Glow-on-Wake" LED Jewelry (15-Second Active Window) — *(Tier 1 & Tier 2)*:**  
   For DIY wearables like a custom LED ring or pendant using hand-ground acrylic segments, pair a **firm mechanical wake-up click** with a **capacitive touch surface** and a short **15-second active timer**. Pressing the piece firmly wakes the circuit, illuminating the glowing LED segments while enabling feather-light touch input (resetting the 15-second timer with each tap). Once left untouched for 15 seconds, both the LEDs and touch sensor automatically power down—preventing pocket triggers while turning the readout into an eye-catching, battery-saving piece of jewelry.
6. **Complete DIY Wristband Project: Hand-Filed Acrylic LEDs + Mini-MCU — *(Tier 2)*:**  
   Driving custom-filed acrylic LED segments directly from a tiny microcontroller is far simpler and more compact than wiring up legacy 7-segment decoders and external timers. Two great wrist-sized controller options are:
   * **ATtiny85 (SOIC-8 SMD):** Ultra-flat (`5 × 6 mm`), ideal for ultra-thin rings using a 5-pin Charlieplexed LED setup and a coin cell.
   * **Seeed Studio XIAO (RP2040 or nRF52840):** Thumbnail-sized (`21 × 17.5 mm`) with a completely flat underside, built-in USB-C programming, and enough I/O pins to drive the **8-wire 4×4 LED matrix** directly.
   **How to Build the XIAO Wristband:**
   1. **LED Matrix & Hand-Filed Lenses:** Mount 16 miniature SMD LEDs (`0603` or `0805`) on a slim strip of perfboard or flex-PCB wired in the standard **4×4 matrix** (4 rows + 4 columns with current-limiting resistors), and glue your hand-filed, polished acrylic (**PMMA**) segment lenses directly over the LEDs.
   2. **Direct 8-Wire Connection:** Solder the 4 row wires and 4 column wires straight to 8 digital pins (`D0`–`D7`) on the flat XIAO board. Use software PWM on the microcontroller to dim the `S2`/`S4` overlap LEDs to 50% brightness for that signature "light-gray" depth effect.
   3. **Hybrid Wake-Up & 15-Second Glow:** Mount a thin tactile push-button (`D8`) underneath the display module for the firm wake-up click, and place a small piece of copper tape (`D9`, capacitive touch) under the acrylic bezel. A firm press wakes the XIAO from deep sleep, lighting up the glowing segments for **15 seconds** of feather-light touch input before automatically powering back down.
   4. **Wearable Mounting:** Attach a flat CR2032 coin-cell holder (or micro-LiPo battery) alongside the XIAO onto a leather or silicone watch strap for a sleek, glowing timepiece or secret wrist keypad.
   * **Starter Firmware (`xiao_4segment_wristband.ino`):** A ready-to-compile Arduino sketch implementing the 4×4 matrix multiplexing, 50% PWM "light-gray" overlap dimming, and the 15-second wake-on-click glow timer is included in this repository *(note: provided as a conceptual starter template and not yet tested on physical hardware)*.
7. **Large-Scale Mechanical Club Scoreboard (Community Build & Plotter Multiplexing) — *(Tier 4 & Tier 5)*:**  
   Commercial multi-meter scoreboards easily cost thousands of euros, putting them out of reach for many local sports clubs. Because this architecture requires only **4 segments per digit** (instead of 7), it becomes an ideal, budget-friendly **community club project** where everyone can pitch in: members can donate or repurpose sheet materials, youth players and kids can paint the giant segment lamellae in club colors, and one local electronics tinkerer can wire up a basic Arduino to bring it to life:
   * **Flat, Wind-Proof Sliding Design:** Rather than hinged flaps that catch wind and require deep housings, the front face is a rigid **cutout mask** with the 4 fluid segment openings (`S1`–`S4`). Behind this mask, four flat sliding plates (lamellae) slide inward from the outer perimeter into their respective slots.
   * **Zero-Collision Outer Routing & Layered Overlaps:** Because `S1`, `S2`, `S3`, and `S4` enter from distinct outer edges of the character frame, each sliding plate has ample room on the outside without interfering with neighboring segments. At the intersection of **S2** and **S4**, the sliding plates simply run in parallel tracks one behind the other—cleanly covering the overlap in solid contrast (or using a light-gray rear lamella behind a solid front lamella to recreate the two-tone depth effect).
   * **Ultra-Low-Cost "Plotter-Carriage" Mechanical Multiplexing (2 Motors Instead of 16):**  
     Because a 4-digit scoreboard in this architecture requires only **16 segments** (instead of 28 on a 7-segment board), makers can eliminate 14 motors by splitting the build into two simple, non-critical assemblies:
     1. **Counterweighted Lamella Board + 32-Pin Bottom Bus:** Each of the 16 sliding lamellae is balanced with small counterweights (so gravity and friction remain minimal) and connects via simple levers or cords to a neat row of **32 actuation pins** protruding from the bottom edge of the frame (16 pins to push segments *closed/active*, and 16 pins to push them *open/inactive*).
     2. **2-Motor Plotter Shuttle:** Using standard DIY 3D-printer/plotter parts (one belt-driven stepper motor to slide horizontally along the 32-pin row, and a second small motor/cam to push the selected pin upward), an Arduino rapidly updates only the segments that need to change—saving 14 motors while keeping mechanical alignment forgiving and reliable.
   * **Mechanical Linkage "Logic Levers" for a More Familiar, Closed-Form Look:**  
     Whenever a club committee or volunteer group debates building a custom scoreboard, there is inevitably a strong voice concerned about aesthetics—asking whether a minimalist 4-segment typeface looks familiar enough for spectators. Because a large wooden or plastic scoreboard has ample room behind the front mask, club tinkerers can resolve this using simple pivoting levers and connecting rods between the four main lamellae—requiring **zero extra motors or code**—to give the digits **a much more familiar, closed-form look** without abandoning the 4-segment foundation. Building and tuning these mechanical linkages certainly takes patience and elbow grease, yet it is entirely achievable—and putting in collective effort to overcome a challenge is, after all, the very definition of sport:
     * **Option A — Tier 4 Short-Stroke Compromise (`+L1` 60° Arc & `+L2` Waist, Shown Below):** Uses a compact `60°` upper-left arc extension (`+L1` for `0`, `2`, `6`, `8`) and a short diagonal waist (`+L2` for `2`). Because the travel distance is tiny, the auxiliary lamellae glide lightly and are much easier for club volunteers to align and build.
     * **Option B — Tier 5 Advanced Multi-Lever Closure:** For clubs willing to invest extra workshop time in longer guide tracks, `+L1` can be extended into a full `180°` lower-right loop (`0`, `6`, `8`) and further refined within the physical limits of sliding lamellae for an even more closed silhouette.
     * **Best of Both Worlds:** Behind the scenes, the board still runs on the ultra-cheap 4-segment mechanical drive, while on the front, those few extra wooden linkages bridge just enough gaps to satisfy the traditionalists in the club.
8. **Tiny Logic Helper PCB for Enhanced LED Digits (Electronic Equivalent of Tier 4 Levers) — (Tier 4):
For LED displays using hand-ground acrylic lenses, the exact same visual refinements used on the mechanical scoreboard (L1 extending the upper-left arc of S1 for 0, 2, 6, 8, and L2 adding a center waist stroke for 2) can be driven automatically by a postage-stamp-sized logic board listening directly to the four existing segment lines (S1–S4)—requiring zero changes to the main driver or code:
Upper-Left Arc Extension (L1 for 0, 2, 6, 8): $\text{L1} = S1 \land (\neg S3 \lor (\neg S2 \land \neg S4))$
Center Waist Accent (L2 for 2): $\text{L2} = S1 \land S3 \land \neg S2 \land \neg S4$
(Easily implemented on a tiny auxiliary PCB using standard quad-NAND logic gates such as a 74HC00, keeping the core 4-line drive intact while giving larger stationary LED displays a fuller, more familiar silhouette.)
9. **Modular 4-Piece Calligraphy Stamp Set (Natural Ink-Overprint Depth) — (Tier 3):
Instead of carving or buying ten separate number stamps, makers can create a pocket-sized set of just four transparent acrylic stamp blocks—one for each fluid stroke (S1, S2, S3, and S4)—aligned against a simple L-shaped corner guide:
Authentic Overprint Shading: Just like a solid-black overlap, stamping S2 and S4 over the same spot (for digits 4, 8, and 9) naturally deposits a double layer of ink at the intersection—creating a rich, darker tonal overlap that mimics traditional letterpress and hand-lettered calligraphy.
Endless Creative Styling: Because the four stamps can be inked in different colors (such as a light-gray or pastel S2 paired with a bold black S4), crafters can stamp custom, fluid numerals onto journals, numbered art prints, and packaging using only four small blocks.
10. **Tactile Relay-Driven Numeric Display for Blind & Visually Impaired Users — *(Tier 1)*:**  
    Standard 7-segment electromechanical displays become overly bulky and expensive when built with off-the-shelf relays, as seven coils must be packed beneath every single digit. With only **4 segments per digit (`S1`–`S4`)**, four sturdy relays fit comfortably beneath a compact, finger-sized tactile cell:
    * **Direct Armature Mounting:** Lightweight, smooth-edged segment bars (`S1`–`S4`) are mounted directly onto the moving armature arms of four standard relays, rising cleanly through slots in the faceplate when energized so users can read the fluid numeral shapes by touch.
    * **Parallel Alignment Stops (Nubs):** Small mechanical stop nubs beneath the faceplate catch each lightweight segment as the relay releases, ensuring every stroke settles back into an exact, parallel resting position without wobble or complex linear guides.

License

This project is licensed under the MIT License. Feel free to use, modify, and build upon this architecture for your own hardware or software display projects! 
