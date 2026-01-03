# 3D Models

## Project Overview

*[One paragraph: what the object is and what it's for.]*

## Status

- **Version:** v01
- **Last export:** —
- **Readiness:** Prototype

## Hardware + Materials

- **Printer:** FlashForge Adventurer 5M Pro
- **Nozzle:** 0.4mm
- **Filament:** PLA

## Design Source of Truth

- **Fusion Hub:** *[Hub name]*
- **Fusion Project:** *[Project name]*
- **Fusion Design:** *[Design name]*

Note: Fusion cloud is the working source of truth. This repo holds exports and documentation.

## Repo Contents

- `docs/` — Design notes, print runbook, assembly instructions, troubleshooting
- `exports/stl/` — Per-component STLs for printing
- `exports/step/` — STEP exports for interoperability/manufacturing
- `exports/f3d_snapshots/` — Optional milestone archival snapshots
- `exports/images/` — Screenshots and renders
- `parameters/` — User parameters and fit/clearance documentation
- `scripts/` — Fusion scripts and helper tools
- `tests/` — Fit coupons and interface test pairs

## Versioning + Naming Conventions

Export naming: `{assembly}_{component}_vNN_{material}.stl`

Examples:
- `bracket_base_v01_pla.stl`
- `bracket_lid_v01_pla.stl`

Rule: each physical printed piece is one component, exported individually.

## Print Settings Baseline

| Setting | Value |
|---------|-------|
| Layer height | 0.20mm |
| Walls/perimeters | 3 |
| Infill | 15% |
| Supports | As needed for overhangs >45° |

## Fit & Tolerance

Default clearance: `0.35 mm`

- Slot width = tab width + clearance
- Hole diameter = pin diameter + clearance

See `parameters/fit-clearance.md` for details.

## Assembly Strategy

- Use pins, shoulders, or steps for alignment—never hand alignment
- Fasteners: *[document as needed]*

## Release Checklist

- [ ] Export all components to `exports/stl/`
- [ ] Export STEP to `exports/step/`
- [ ] Generate screenshots to `exports/images/`
- [ ] Update CHANGELOG.md
- [ ] Print interface test pair first
- [ ] Tag release in git
