#include <LedControl.h>

// Pin for MAX7219: DataIn, CLK, LOAD, # of MAX7219s
LedControl lc = LedControl(12, 11, 10, 1);

void setup() {
  Serial.begin(9600);
  lc.shutdown(0, false);
  lc.setIntensity(0, 8);
  lc.clearDisplay(0);
}

void loop() {
  if (Serial.available() >= 8) {  // Wait until 8 bytes (1 frame) are available
    for (int i = 0; i < 8; i++) {
      byte rowData = Serial.read();  // Read each row byte
      lc.setRow(0, i, rowData);      // Display the row on the LED matrix
    }
  }
}