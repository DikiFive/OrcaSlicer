## MODIFIED Requirements: LONGER LK10 Plus movement limits

#### Scenario: LK10 Plus movement speeds are limited per verified values
- Given the machine preset for any nozzle variant of LONGER LK10 Plus
- Then the preset MUST include the following keys with exact values (arrays of strings):
  - "machine_max_speed_x": ["500"]
  - "machine_max_speed_y": ["500"]
  - "machine_max_speed_z": ["20"]
  - "machine_max_speed_e": ["60"]

#### Scenario: LK10 Plus movement accelerations are set per verified values
- Given the machine preset for any nozzle variant of LONGER LK10 Plus
- Then the preset MUST include (arrays of strings):
  - "machine_max_acceleration_x": ["7000"]
  - "machine_max_acceleration_y": ["7000"]
  - "machine_max_acceleration_z": ["300"]
  - "machine_max_acceleration_e": ["5000"]
  - "machine_max_acceleration_extruding": ["7000"]
  - "machine_max_acceleration_retracting": ["7000"]
  - "machine_max_acceleration_travel": ["7000"]

#### Scenario: LK10 Plus nozzle variants consistency
- Given the 0.2/0.4/0.6/0.8 nozzle presets for LONGER LK10 Plus
- Then each preset MUST satisfy the two scenarios above.

#### Scenario: LK10 Plus retraction/deretraction speeds are set per verified values
- Given the machine preset for any nozzle variant of LONGER LK10 Plus
- Then the preset MUST include (arrays of strings):
  - "retraction_speed": ["35"]
  - "deretraction_speed": ["35"]

#### Scenario: LK10 Plus machine start gcode is customized
- Given the machine preset for any nozzle variant of LONGER LK10 Plus
- Then it MUST define "machine_start_gcode" that contains the tokens:
  - "PROBE_EDDY_SINGLE_HOME"
  - "G1 X161 Y-5" (tool-clean arc center near X160,Y-5)
  - "BED_MESH_PROFILE LOAD=default"
