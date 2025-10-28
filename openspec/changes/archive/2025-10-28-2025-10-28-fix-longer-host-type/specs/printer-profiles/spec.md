# Printer Profiles: LONGER LK10 family host_type compliance

## ADDED Requirements

### Requirement: Machine profiles MUST only use `host_type` values declared in `PrintHostType` enum
Profiles MUST NOT specify a `host_type` value outside the `PrintHostType` enum. Klipper-targeted machines MUST omit `host_type` and rely on `gcode_flavor: klipper`.

- Rationale: The profile validator enforces enum compliance to prevent invalid integrations and keeps Klipper machines consistent with existing vendors.

#### Scenario: LONGER LK10 and LK10 Plus omit unsupported host_type
- Given: The LONGER LK10 and LONGER LK10 Plus machine profiles target Klipper (`gcode_flavor: klipper`).
- And: `PrintHostType` enum does not include `klipper`.
- When: The profiles are validated by CI.
- Then: The profiles MUST NOT specify `host_type: klipper`.
- And: Validation passes when `host_type` is omitted.

## Notes
- Other Klipper-based vendors (Voron, TwoTrees) omit `host_type`; this change aligns with existing convention.
