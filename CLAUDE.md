# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is a Fusion 360 (Personal) 3D-printing project repository. Fusion 360 design files live in the Autodesk cloud (Hub/Project). This Git repo tracks exported artifacts, scripts, documentation, and print/runbook notes.

**Key principles:**
- The `.f3d` working file is NOT stored locally—Fusion cloud is the modeling source of truth
- This Git repo is the source of truth for printing and reproducibility via exports and docs
- Assembly-first modeling: one master assembly, derived components, no manual alignment

## Printer Constraints

- **Printer:** FlashForge Adventurer 5M Pro
- **Material:** PLA
- **Build volume:** 220 × 220 × 220 mm per component
- Larger designs must split into printable components that assemble precisely

## Repository Structure

```
.
├── README.md
├── CHANGELOG.md
├── docs/
│   ├── design-notes.md
│   ├── print-runbook.md
│   ├── assembly.md
│   └── troubleshooting.md
├── exports/
│   ├── stl/           # Per-component STLs for printing
│   ├── step/          # STEP exports for interoperability
│   ├── f3d_snapshots/ # Optional milestone archival snapshots
│   └── images/        # Screenshots/renders for docs
├── parameters/
│   ├── user-parameters.md
│   └── fit-clearance.md
├── scripts/
│   ├── fusion/
│   └── tools/
└── tests/
    ├── fit-coupons/
    └── interface-pairs/
```

## Naming Conventions

Export naming: `{assembly}_{component}_vNN_{material}.stl`

Each physical printed piece = one component, exported individually.

## Fit & Tolerance

Default clearance: `0.35 mm`
- Slot = tab width + clearance
- Hole = pin diameter + clearance

## Working With This Repo

**When asked to "organize the repo":**
- Output folder tree, README.md, starter CHANGELOG.md, and docs stubs

**When asked to "update the repo for vNN":**
- Update README status + version
- Append to CHANGELOG
- Add/adjust folders/files as needed
- Provide git commit message suggestion

## Behavioral Guidelines

- Choose sensible defaults when info is missing; label them as defaults
- Prefer checklists and short sections
- Never recommend storing the working `.f3d` as primary source in Git
- Enforce assembly-first rules: all mating geometry must be designed together in the master assembly
