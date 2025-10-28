# Tasks for 2025-10-28-fix-longer-host-type

1. Inspect failing CI logs for invalid enum value [done]
2. Verify allowed `host_type` enum values in `src/libslic3r/PrintConfig.cpp` [done]
3. Update LONGER LK10/LK10 Plus machine profiles to remove `host_type: klipper` [done]
4. Push branch and re-run CI "Check profiles" to confirm pass [pushed; waiting for CI]

Validation:
- Local validator: PASS (vendor=LONGER, all vendors)
- CI: green on "Check profiles (pull_request)" [pending]
