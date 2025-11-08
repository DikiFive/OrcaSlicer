## Why
LONGER LK10 and LK10 Plus presets currently ship without tuned filament profiles, forcing users to guess baseline parameters.

## What Changes
- Clone the Elegoo generic PLA/PETG recipes and adapt them for the LONGER LK10 and LONGER LK10 Plus machines.
- Register the new filament presets in the LONGER vendor index so every nozzle variant can see and select them.
- Align naming and compatibility lists with the existing LONGER machine naming conventions.

## Impact
- Affected specs: longer.materials
- Affected data: resources/profiles/LONGER/filament/*.json, resources/profiles/LONGER.json
- Tooling: profile validation/packaging scripts must continue to pass
