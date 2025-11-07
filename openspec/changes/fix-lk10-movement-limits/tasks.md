# Tasks: Fix LK10/LK10 Plus Movement Limits

1. Edit LK10 machine JSONs to add/override movement limits
   - files: 
     - resources/profiles/LONGER/machine/LONGER LK10 (0.2 nozzle).json
     - resources/profiles/LONGER/machine/LONGER LK10 (0.4 nozzle).json
     - resources/profiles/LONGER/machine/LONGER LK10 (0.6 nozzle).json
     - resources/profiles/LONGER/machine/LONGER LK10 (0.8 nozzle).json
   - set values:
     - machine_max_speed_x/y/z/e = ["500"], ["500"], ["20"], ["60"]
     - machine_max_acceleration_x/y/z/e = ["7000"], ["7000"], ["300"], ["5000"]
   - machine_max_acceleration_extruding/retracting/travel = ["7000"] each
   - retraction_speed = ["35"], deretraction_speed = ["35"]

2. Edit LK10 Plus machine JSONs to add/override movement limits
   - files: 
     - resources/profiles/LONGER/machine/LONGER LK10 Plus (0.2 nozzle).json
     - resources/profiles/LONGER/machine/LONGER LK10 Plus (0.4 nozzle).json
     - resources/profiles/LONGER/machine/LONGER LK10 Plus (0.6 nozzle).json
     - resources/profiles/LONGER/machine/LONGER LK10 Plus (0.8 nozzle).json
   - same values as step 1

3. Validate
   - Run: openspec validate fix-lk10-movement-limits --strict (if CLI available)
   - Quick grep checks:
     - rg -n "machine_max_speed_x":\s*\["500"\] resources/profiles/LONGER/machine
   - rg -n "machine_max_acceleration_y":\s*\["7000"\] resources/profiles/LONGER/machine
   - rg -n "retraction_speed":\s*\["35"\] resources/profiles/LONGER/machine

4. Sanity test in UI
   - Launch OrcaSlicer, add LK10 & LK10 Plus printers across nozzle variants.
   - Confirm movement limit panels reflect the values.

5. PR & Notes
   - Mention this change proposal.
   - Include screenshot from the reference panel.