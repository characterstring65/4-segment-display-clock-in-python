/*
 * ============================================================================
 *  4-Segment Fluid Display Wristband — Starter Firmware for Seeed Studio XIAO
 *  File: xiao_4segment_wristband.ino
 * ============================================================================
 *  DISCLAIMER:
 *  This Arduino sketch is provided as an untested conceptual starter template
 *  for DIY makers and hardware tinkerers. Pin assignments, resistor values,
 *  and touch thresholds should be verified and tuned on your own breadboard
 *  before final wearable assembly.
 * ============================================================================
 */

// 4x4 Matrix Pin Definitions (Seeed Studio XIAO RP2040 / nRF52840 / SAMD21)
const int ROW_PINS[4] = {D0, D1, D2, D3}; // Rows 1-3: Digits 1-3 | Row 4: Extras
const int COL_PINS[4] = {D4, D5, D6, D7}; // Columns 1-4: Segments S1, S2, S3, S4

// Hybrid Wake-Up & Capacitive Touch Pins
const int WAKE_BTN_PIN  = D8; // Firm tactile switch (active LOW with internal pull-up)
const int TOUCH_PAD_PIN = D9; // Copper tape capacitive/touch sense input

// Active Window Configuration (15-second glow timer)
const unsigned long ACTIVE_TIMEOUT_MS = 15000;
unsigned long lastActivityTime = 0;
bool isAwake = false;

// Digit-to-Segment Mapping (Bitmask: bit0=S1, bit1=S2, bit2=S3, bit3=S4)
const uint8_t DIGIT_MAP[10] = {
  0b0001, // 0: S1
  0b1000, // 1: S4
  0b0101, // 2: S1 + S3
  0b1101, // 3: S1 + S3 + S4
  0b1010, // 4: S2 + S4
  0b0111, // 5: S1 + S2 + S3
  0b0011, // 6: S1 + S2
  0b1100, // 7: S3 + S4
  0b1111, // 8: S1 + S2 + S3 + S4
  0b1110  // 9: S2 + S3 + S4
};

// Display buffer for 3 digits + extra row (decimals / MSD '1')
uint8_t displayDigits[3] = {1, 2, 4};
uint8_t extraRowMask = 0b1000; // Bit 3 = MSD '1' (displays "11:24" by default)

// Multiplexing & PWM state for "Light-Gray" S2/S4 overlap simulation
uint8_t pwmPhase = 0;

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(ROW_PINS[i], OUTPUT);
    digitalWrite(ROW_PINS[i], LOW);
    pinMode(COL_PINS[i], OUTPUT);
    digitalWrite(COL_PINS[i], HIGH); // Active-LOW columns (common cathode per col)
  }

  pinMode(WAKE_BTN_PIN, INPUT_PULLUP);
  pinMode(TOUCH_PAD_PIN, INPUT);
}

void clearMatrix() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(ROW_PINS[i], LOW);
    digitalWrite(COL_PINS[i], HIGH);
  }
}

void refreshMatrixPass() {
  pwmPhase = (pwmPhase + 1) % 2; // Alternates 0 and 1 for 50% duty-cycle dimming

  for (int r = 0; r < 4; r++) {
    clearMatrix();

    uint8_t segMask = (r < 3) ? DIGIT_MAP[displayDigits[r]] : extraRowMask;
    bool s2 = (segMask & 0b0010);
    bool s4 = (segMask & 0b1000);

    // Enable active columns for this row
    for (int c = 0; c < 4; c++) {
      bool segOn = (segMask & (1 << c));

      // Simulate 50% "Light-Gray" overlap when only one of S2 or S4 is active
      if ((c == 1 || c == 3) && (s2 ^ s4)) {
        if (pwmPhase == 0) {
          segOn = false; // Dim to 50% brightness on alternating frames
        }
      }

      digitalWrite(COL_PINS[c], segOn ? LOW : HIGH);
    }

    digitalWrite(ROW_PINS[r], HIGH);
    delayMicroseconds(1200); // Multiplex dwell time (~1.2 ms per row)
  }
  clearMatrix();
}

void loop() {
  // 1. Check firm mechanical wake-up click
  if (digitalRead(WAKE_BTN_PIN) == LOW) {
    delay(25); // Simple debounce
    if (digitalRead(WAKE_BTN_PIN) == LOW) {
      isAwake = true;
      lastActivityTime = millis();
      // Cycle sample digits on button press
      displayDigits[2] = (displayDigits[2] + 1) % 10;
      while (digitalRead(WAKE_BTN_PIN) == LOW) {
        refreshMatrixPass();
      }
    }
  }

  // 2. Active 15-second glow & touch window
  if (isAwake) {
    // Check feather-light touch pad (extends 15-second glow timer)
    if (digitalRead(TOUCH_PAD_PIN) == HIGH) {
      lastActivityTime = millis();
    }

    // Check 15-second inactivity timeout
    if (millis() - lastActivityTime >= ACTIVE_TIMEOUT_MS) {
      isAwake = false;
      clearMatrix();
    } else {
      refreshMatrixPass();
    }
  } else {
    // Low-power idle state (display completely dark)
    delay(20);
  }
}
