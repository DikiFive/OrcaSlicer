# Start/End G-code Contract (Klipper)

## START_PRINT Parameters (recommended)
- BED_TEMP: integer (°C)
- EXTRUDER_TEMP_1ST: integer (°C)
- EXTRUDER_TEMP: integer (°C)
- FILAMENT_DIAMETER: number (mm)

Example call in Start G-code:
```
START_PRINT BED_TEMP={first_layer_bed_temperature[0]} EXTRUDER_TEMP_1ST={first_layer_temperature[0]} EXTRUDER_TEMP={temperature[0]} FILAMENT_DIAMETER={filament_diameter[0]}
; unified priming line (safe bounds)
G92 E0
G1 X2 Y2 F6000
G1 Z0.28 F1000
G1 X200 E12 F1000
G1 E-0.8 F1800
```

## END_PRINT
```
END_PRINT
```

## Fallback (macros missing)
- Replace macro calls with simplified sequences: cooldown, retract, park, fan off.
- Show a one-time warning in documentation/notes and link to macro setup guide.
