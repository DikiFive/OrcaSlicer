# longer.materials Specification

## Purpose
Define the baselines and vendor-specific overrides for LONGER-branded filament presets so they remain aligned with the Elegoo tuning they are cloned from and stay compatible with LK10 / LK10 Plus machines.
## Requirements
### Requirement: LONGER base filament presets reuse Elegoo tuning
LONGER filament baselines MUST mirror the Elegoo shared tuning so that vendor-specific generics inherit an identical starting point.

#### Scenario: LONGER fdm_filament_common matches Elegoo defaults
- Given the file `resources/profiles/LONGER/filament/fdm_filament_common.json`
- Then it MUST define the same baseline keys and values as Elegoo, including:
  - Bed temperatures (cool/eng/hot/textured and initial layer) all set to "60"
  - Cooling defaults: "overhang_fan_threshold" = "95%", "overhang_fan_speed" = "100", "close_fan_the_first_x_layers" = "3"
  - Flow defaults: "filament_flow_ratio" = "1", "filament_diameter" = "1.75"
  - Fan behavior: "fan_cooling_layer_time" = "60", "fan_max_speed" = "100", "fan_min_speed" = "35"
  - Ramp controls: "slow_down_for_layer_cooling" = "1", "slow_down_min_speed" = "10", "slow_down_layer_time" = "8"
  - Start/end snippets: "filament_start_gcode" = "; Filament gcode\n" and "filament_end_gcode" = "; filament end gcode \n"
  - Baseline nozzle profile: "nozzle_temperature" = "200", "nozzle_temperature_initial_layer" = "200", "temperature_vitrification" = "100"

#### Scenario: LONGER fdm_filament_pla inherits and aligns with Elegoo
- Given the file `resources/profiles/LONGER/filament/fdm_filament_pla.json`
- Then it MUST inherit from `fdm_filament_common`
- And it MUST set the Elegoo PLA overrides exactly:
  - "fan_cooling_layer_time" = "100"
  - "filament_max_volumetric_speed" = "15"
  - "filament_density" = "1.24"
  - "filament_cost" = "20"
  - "nozzle_temperature_initial_layer" = "210"
  - "reduce_fan_stop_start_freq" = "1"
  - "slow_down_for_layer_cooling" = "1"
  - "fan_max_speed" = "100"
  - "fan_min_speed" = "100"
  - "overhang_fan_speed" = "100"
  - "overhang_fan_threshold" = "50%"
  - "close_fan_the_first_x_layers" = "1"
  - "nozzle_temperature" = "205"
  - "temperature_vitrification" = "60"
  - "nozzle_temperature_range_low" = "205"
  - "nozzle_temperature_range_high" = "210"
  - "slow_down_min_speed" = "10"
  - "slow_down_layer_time" = "4"
  - "additional_cooling_fan_speed" = "70"
  - "filament_start_gcode" = "; filament start gcode\n"

#### Scenario: LONGER fdm_filament_pet inherits and aligns with Elegoo
- Given the file `resources/profiles/LONGER/filament/fdm_filament_pet.json`
- Then it MUST inherit from `fdm_filament_common`
- And it MUST set the Elegoo PETG overrides exactly:
  - "fan_cooling_layer_time" = "20"
  - "fan_min_speed" = "20"
  - "filament_density" = "1.27"
  - "filament_max_volumetric_speed" = "12"
  - "hot_plate_temp" and "textured_plate_temp" (and their initial layer variants) = "80"
  - "nozzle_temperature" and "nozzle_temperature_initial_layer" = "250"
  - "nozzle_temperature_range_low" = "220"
  - "nozzle_temperature_range_high" = "260"
  - "reduce_fan_stop_start_freq" = "1"
  - "temperature_vitrification" = "70"
  - "filament_start_gcode" = "; Filament start gcode\n"
  - "filament_end_gcode" = "; filament end gcode \n"

### Requirement: LONGER LK10 generic filaments mirror Elegoo tuning
LONGER LK10 filament presets MUST reuse the Elegoo generic PLA and PETG tuning while mapping compatibility to every LK10 nozzle variant.

#### Scenario: Generic PLA for LK10 reproduces Elegoo values
- Given the filament preset file `resources/profiles/LONGER/filament/Generic PLA @LONGER LK10.json`
- Then it MUST set `type` to "filament", `inherits` to "fdm_filament_pla", `from` to "system", and `instantiation` to "true"
- And it MUST copy the Elegoo Generic PLA overrides without modification:
  - "filament_flow_ratio": ["0.98"]
  - "filament_max_volumetric_speed": ["15"]
  - "nozzle_temperature_initial_layer": ["210"]
  - "slow_down_layer_time": ["8"]
- And its `compatible_printers` MUST exactly contain:
  - "LONGER LK10 (0.2 nozzle)"
  - "LONGER LK10 (0.4 nozzle)"
  - "LONGER LK10 (0.6 nozzle)"
  - "LONGER LK10 (0.8 nozzle)"

#### Scenario: Generic PETG for LK10 reproduces Elegoo values
- Given the filament preset file `resources/profiles/LONGER/filament/Generic PETG @LONGER LK10.json`
- Then it MUST set `type` to "filament", `inherits` to "fdm_filament_pet", `from` to "system", and `instantiation` to "true"
- And it MUST copy the Elegoo Generic PETG overrides without modification:
  - "reduce_fan_stop_start_freq": ["1"]
  - "slow_down_for_layer_cooling": ["1"]
  - "fan_cooling_layer_time": ["30"]
  - "overhang_fan_speed": ["90"]
  - "overhang_fan_threshold": ["25%"]
  - "nozzle_temperature_initial_layer": ["240"]
  - "fan_max_speed": ["50"]
  - "fan_min_speed": ["20"]
  - "slow_down_min_speed": ["10"]
  - "slow_down_layer_time": ["8"]
  - "filament_flow_ratio": ["0.95"]
  - "filament_max_volumetric_speed": ["10"]
  - "filament_start_gcode": ["; filament start gcode\n"]
- And its `compatible_printers` MUST exactly contain:
  - "LONGER LK10 (0.2 nozzle)"
  - "LONGER LK10 (0.4 nozzle)"
  - "LONGER LK10 (0.6 nozzle)"
  - "LONGER LK10 (0.8 nozzle)"

### Requirement: LONGER LK10 Plus generic filaments mirror Elegoo tuning
LONGER LK10 Plus filament presets MUST mirror the same Elegoo generic PLA/PETG settings while covering every LK10 Plus nozzle variant.

#### Scenario: Generic PLA for LK10 Plus reproduces Elegoo values
- Given the filament preset file `resources/profiles/LONGER/filament/Generic PLA @LONGER LK10 Plus.json`
- Then it MUST set `type` to "filament", `inherits` to "fdm_filament_pla", `from` to "system", and `instantiation` to "true"
- And it MUST copy the Elegoo Generic PLA overrides without modification:
  - "filament_flow_ratio": ["0.98"]
  - "filament_max_volumetric_speed": ["15"]
  - "nozzle_temperature_initial_layer": ["210"]
  - "slow_down_layer_time": ["8"]
- And its `compatible_printers` MUST exactly contain:
  - "LONGER LK10 Plus (0.2 nozzle)"
  - "LONGER LK10 Plus (0.4 nozzle)"
  - "LONGER LK10 Plus (0.6 nozzle)"
  - "LONGER LK10 Plus (0.8 nozzle)"

#### Scenario: Generic PETG for LK10 Plus reproduces Elegoo values
- Given the filament preset file `resources/profiles/LONGER/filament/Generic PETG @LONGER LK10 Plus.json`
- Then it MUST set `type` to "filament", `inherits` to "fdm_filament_pet", `from` to "system", and `instantiation` to "true"
- And it MUST copy the Elegoo Generic PETG overrides without modification:
  - "reduce_fan_stop_start_freq": ["1"]
  - "slow_down_for_layer_cooling": ["1"]
  - "fan_cooling_layer_time": ["30"]
  - "overhang_fan_speed": ["90"]
  - "overhang_fan_threshold": ["25%"]
  - "nozzle_temperature_initial_layer": ["240"]
  - "fan_max_speed": ["50"]
  - "fan_min_speed": ["20"]
  - "slow_down_min_speed": ["10"]
  - "slow_down_layer_time": ["8"]
  - "filament_flow_ratio": ["0.95"]
  - "filament_max_volumetric_speed": ["10"]
  - "filament_start_gcode": ["; filament start gcode\n"]
- And its `compatible_printers` MUST exactly contain:
  - "LONGER LK10 Plus (0.2 nozzle)"
  - "LONGER LK10 Plus (0.4 nozzle)"
  - "LONGER LK10 Plus (0.6 nozzle)"
  - "LONGER LK10 Plus (0.8 nozzle)"

