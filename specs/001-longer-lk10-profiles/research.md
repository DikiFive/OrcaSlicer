# Research

This document consolidates key decisions, rationale, and alternatives for the LONGER LK10/LK10 Pro profiles feature.

## Decisions

1) Host type default: Klipper (host_type=klipper)
- Rationale: User preference, alignment with similar profiles, reduces template divergence.
- Alternatives: OctoPrint; Offline export.

2) Printable height: LK10=220mm; LK10 Pro=330mm
- Rationale: Matches build volumes chosen; reduces slicing boundary errors.
- Alternatives: Lower conservative values; leave unset (rejected: harms UX/testability).

3) Defaults: Generic PLA @System + 0.20mm Standard @model (0.4 nozzle)
- Rationale: Minimal surprise, consistent UX, easy validation.
- Alternatives: Vendor-specific PLA/process; no defaults (rejected due to friction).

4) Start/End G-code strategy: Mixed (Klipper macros + unified priming/line segment)
- Rationale: Keep device workflow in firmware macros; small slicer-side line improves first layer reliability.
- Alternatives: Macro-only; slicer-only; empty.

5) Fallback when macros missing: Auto fallback to simplified Start/End with one-time warning
- Rationale: Minimize first-run failure; clear guidance to set up macros later.
- Alternatives: Hard fail; silent continue; wizard-only.

## Open Implementation Notes

A) Macro presence detection feasibility in OrcaSlicer
- Constraint: Profiles are static JSON; runtime detection requires app logic.
- Plan: Ship two process presets (macro-based default; simplified fallback) and a small external helper (optional) to switch default if macros absent, plus a clear one-time warning via documentation. Full automated detection inside app would require C++ changes (out of scope for this config-only feature).

B) Priming line safety
- Ensure the line stays within printable_area for both 220x220 and 330x330 beds; choose conservative path (e.g., along X at Y=2..5).

C) Parameter naming for macros
- Use common macros: START_PRINT BED_TEMP, EXTRUDER_TEMP_1ST, EXTRUDER_TEMP; document mapping from slicer variables.

## Consolidated Outcomes
- All prior NEEDS CLARIFICATION resolved at spec level.
- Any app-level automation for macro detection is deferred and documented.
