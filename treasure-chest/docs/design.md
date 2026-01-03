# Treasure Chest Design Document

**Project:** treasure-chest
**Version:** v01
**Status:** Design Phase

---

## 1. Design Overview

A four-piece treasure chest for D&D tabletop gaming with a hidden compartment accessed via a false bottom.

```
┌─────────────────────────┐
│     ╭───────────╮       │  ← Curved lid (friction fit)
│    ╱             ╲      │
├───┴───────────────┴─────┤
│                         │
│   ┌─────────────────┐   │  ← False bottom with ring
│   │    ○ (ring)     │   │
│   └─────────────────┘   │
│ ─ ─ ─ ledge ─ ─ ─ ─ ─ ─ │  ← Internal ledge
│                         │
│   [hidden compartment]  │  ← 8mm deep secret space
│                         │
└─────────────────────────┘
```

---

## 2. Assembly Hierarchy

```
treasure-chest (Assembly)
├── chest_body (Component)
│   └── Body: chest_body
├── lid (Component)
│   └── Body: lid
└── false_bottom (Component)
    ├── Body: tray
    └── Body: ring
```

All components modeled in-place within the assembly for proper mating.

---

## 3. User Parameters

Define in Fusion 360: **Modify → Change Parameters → User Parameters (+)**

| Name | Value | Unit | Formula/Notes |
|------|-------|------|---------------|
| `chest_width` | 30 | mm | Exterior width (X) |
| `chest_depth` | 22 | mm | Exterior depth (Y) |
| `chest_height` | 20 | mm | Body height, no lid (Z) |
| `lid_height` | 10 | mm | Lid peak height |
| `wall` | 2 | mm | Wall thickness |
| `floor` | 1.6 | mm | Floor thickness |
| `clearance` | 0.35 | mm | Fit gap |
| `ledge_z` | 8 | mm | Ledge height from inside floor |
| `ledge_depth` | 1.2 | mm | Ledge shelf protrusion |
| `ring_od` | 6 | mm | Pull ring outer diameter |
| `ring_wire` | 1.6 | mm | Ring wire thickness |
| `tray_thick` | 1.6 | mm | False bottom thickness |

**Derived values** (calculated automatically):
- Inside width: `chest_width - 2 * wall` = 26 mm
- Inside depth: `chest_depth - 2 * wall` = 18 mm
- Tray width: `chest_width - 2 * wall - 2 * clearance` = 25.3 mm
- Tray depth: `chest_depth - 2 * wall - 2 * clearance` = 17.3 mm

---

## 4. Component Designs

### 4.1 Chest Body

The main container with internal ledge for false bottom support.

#### Sketch 1: Base Profile (XZ Plane - Front View)

```
        chest_width
    ├─────────────────────┤

    ┌─────────────────────┐ ─┬─ chest_height
    │                     │  │
    │   ┌─────────────┐   │  │
    │   │             │   │  │  ← inside cavity
    │   │  ┌───────┐  │   │  │
    │   │  │ ledge │  │   │  │  ← ledge_z from inside floor
    │   │  └───────┘  │   │  │
    │   │             │   │  │
    │   └─────────────┘   │  │
    └─────────────────────┘ ─┴─

    │wall│           │wall│
    ├────┤           ├────┤
```

#### Modeling Steps

1. **Create component** named `chest_body`
2. **Sketch on XY plane** (bottom view):
   - Rectangle: `chest_width` × `chest_depth`, centered on origin
3. **Extrude** up: `chest_height`
4. **Shell** (remove top face):
   - Thickness: `wall`
   - Direction: Inside
   - Keep floor solid
5. **Create ledge** (offset plane method):
   - Create offset plane: `floor + ledge_z` from bottom inside
   - Sketch rectangle on inside walls
   - Extrude inward: `ledge_depth`

#### Alternative Ledge Method (Sketch-Based)

1. **Sketch on XZ plane** (front view, inside chest):
   - Draw ledge profile as rectangle
   - Width: `ledge_depth`, Height: `tray_thick + 0.5` (clearance above tray)
   - Position: `ledge_z` from inside floor
2. **Extrude** symmetric through all (creates ledges on both sides)
3. Repeat on YZ plane for front/back ledges

#### Dimensions Summary

| Feature | Dimension |
|---------|-----------|
| Exterior | 30 × 22 × 20 mm |
| Interior | 26 × 18 × (20 - floor) mm |
| Ledge position | 8 mm from inside floor |
| Ledge protrusion | 1.2 mm into cavity |

---

### 4.2 Lid

Curved barrel-top lid with friction-fit rim.

#### Sketch 1: End Profile (XZ Plane)

```
              lid_height
                 ↕
            ╭─────────╮
           ╱           ╲
         ╱               ╲
        ╱                 ╲
    ───┴───────────────────┴───
       │                   │
       │   friction rim    │   ← rim extends down into body
       │                   │
       └───────────────────┘

    ├───────chest_width────────┤
            (less clearance)
```

#### Modeling Steps

1. **Create component** named `lid`
2. **Position**: Move origin to top of chest_body for in-context modeling
3. **Sketch on XZ plane** (end view):
   - Draw half-ellipse or arc for barrel curve:
     - Width: `chest_width - 2 * clearance`
     - Height: `lid_height`
   - Close bottom with horizontal line
4. **Extrude** symmetric: `(chest_depth - 2 * clearance) / 2` each direction
5. **Add friction rim**:
   - Sketch on bottom face of lid
   - Offset rectangle inward: `wall / 2`
   - Extrude down: `3 mm` (rim depth into body)
   - Shell or offset to create rim wall: `1.5 mm` thick

#### Curve Options

**Option A: Arc (simpler)**
- 3-point arc: endpoints at base corners, midpoint at peak
- Creates circular curve

**Option B: Ellipse (more control)**
- Half-ellipse: major axis = width, minor axis = height × 2
- Trim bottom half

**Option C: Spline (custom)**
- Control points for exact curvature
- More complex but fully controllable

#### Dimensions Summary

| Feature | Dimension |
|---------|-----------|
| Width | 29.3 mm (30 - 2×0.35 clearance) |
| Depth | 21.3 mm |
| Height at peak | 10 mm |
| Rim depth | 3 mm |
| Rim wall | 1.5 mm |

---

### 4.3 False Bottom

Removable tray that conceals the secret compartment.

#### Sketch 1: Tray Outline (XY Plane)

```
    ┌─────────────────────────────┐
    │                             │
    │   ┌─────────────────────┐   │  ← chest inside wall
    │   │                     │   │
    │   │   ┌─────────────┐   │   │  ← tray (with clearance gap)
    │   │   │             │   │   │
    │   │   │      ○      │   │   │  ← ring recess (center)
    │   │   │             │   │   │
    │   │   └─────────────┘   │   │
    │   │                     │   │
    │   └─────────────────────┘   │
    │                             │
    └─────────────────────────────┘

    clearance gap: 0.35mm all sides
```

#### Modeling Steps

1. **Create component** named `false_bottom`
2. **Position**: At ledge height inside chest body
3. **Sketch on XY plane** at `ledge_z + floor`:
   - Rectangle: `(chest_width - 2*wall - 2*clearance)` × `(chest_depth - 2*wall - 2*clearance)`
   - Centered in cavity
4. **Extrude** up: `tray_thick` (1.6 mm)
5. **Add ring recess**:
   - Sketch on top face of tray, centered
   - Rectangle or rounded rect: `ring_od + 2` × `ring_od / 2 + 1`
   - Extrude cut down: `ring_wire / 2` (0.8 mm)

#### Dimensions Summary

| Feature | Dimension |
|---------|-----------|
| Tray size | 25.3 × 17.3 × 1.6 mm |
| Gap to walls | 0.35 mm |
| Ring recess | 8 × 4 × 0.8 mm (approximate) |

---

### 4.4 Pull Ring

Small ring recessed into false bottom for lifting.

#### Design Options

**Option A: Printed Bridge (Recommended)**
- Ring printed as arch that bridges across recess
- No assembly required
- Self-supporting at this size

**Option B: Separate Ring**
- Print ring flat
- Glue into recess after printing

#### Modeling Steps (Option A - Integrated)

1. **Sketch on XZ plane** through tray center:
   - Draw ring cross-section:
     - Circle: diameter = `ring_wire` (1.6 mm)
     - Center positioned at ring_od/2 from tray centerline
2. **Revolve** 180°: Creates half-ring (arch)
3. **Position**: Bottom of ring sits in recess, top proud of tray surface

#### Alternative: Full Ring in Recess

1. **Sketch on XY plane** in recess:
   - Circle: `ring_od` (6 mm)
   - Offset inward: `ring_wire` (1.6 mm) - creates ring profile
2. **Extrude** up: `ring_wire` (creates flat ring)
3. **Fillet** edges for comfort

#### Dimensions Summary

| Feature | Dimension |
|---------|-----------|
| Ring OD | 6 mm |
| Wire diameter | 1.6 mm |
| Ring ID | 2.8 mm (finger clearance) |
| Protrusion above tray | 0-2 mm |

---

## 5. Assembly Verification

### 5.1 Interference Check

Before export, verify no collisions:

1. **Inspect → Interference**
2. Select all components
3. Resolve any overlaps (usually clearance issues)

### 5.2 Section Analysis

Verify internal dimensions:

1. **Inspect → Section Analysis**
2. Cut through center (XZ and YZ planes)
3. Confirm:
   - [ ] Lid rim seats inside body
   - [ ] False bottom clears walls by 0.35mm
   - [ ] Ledge supports tray properly
   - [ ] Ring recess depth correct

### 5.3 Fit Simulation

1. Hide lid and false bottom
2. Verify secret compartment depth (8mm)
3. Check ledge is level and continuous

---

## 6. Export Specifications

### 6.1 STL Settings

| Setting | Value |
|---------|-------|
| Refinement | Medium |
| Format | Binary STL |
| Units | mm |

### 6.2 Export Files

| Component | Filename |
|-----------|----------|
| chest_body | `treasure-chest_chest-body_v01_pla.stl` |
| lid | `treasure-chest_lid_v01_pla.stl` |
| false_bottom | `treasure-chest_false-bottom_v01_pla.stl` |

### 6.3 Export Process

1. **Right-click component** in browser → **Save As Mesh**
2. Or use `scripts/fusion/export_all.py`

---

## 7. Print Considerations

### 7.1 Orientation

| Part | Orientation | Supports |
|------|-------------|----------|
| chest_body | Opening up | None |
| lid | Dome down (flat rim on bed) | None |
| false_bottom | Flat | None (ring bridges) |

### 7.2 Critical First Layer

- Chest body floor = 1.6mm = 8 layers at 0.2mm
- Ensure good bed adhesion for this footprint (30×22mm)

### 7.3 Bridge Settings

- Pull ring arch spans ~4mm
- Enable bridge detection in slicer
- Reduce bridge speed if stringing occurs

---

## 8. Post-Print Assembly

### 8.1 Test Fit Sequence

1. **Lid to body**: Should press-fit with light resistance
   - Too tight: sand rim exterior
   - Too loose: add tape to rim, or reprint with less clearance
2. **False bottom to ledge**: Should drop in freely, lift with ring
   - Too tight: sand tray edges
   - Too loose: acceptable (hidden anyway)

### 8.2 Adjustments

| Issue | Solution |
|-------|----------|
| Lid won't fit | Increase `clearance` to 0.4mm, reprint lid |
| Lid falls off | Decrease `clearance` to 0.3mm, reprint lid |
| Tray stuck | Sand edges or reprint with 0.4mm clearance |
| Ring broke | Reprint with 2mm wire thickness |

---

## 9. Version History

| Version | Date | Changes |
|---------|------|---------|
| v01 | — | Initial design |

---

## Appendix A: Sketch Dimension Reference

### Chest Body (XY base sketch)
```
    ┌──────── 30 ────────┐
    │                    │
    │                    │ 22
    │                    │
    └────────────────────┘
    Origin at center
```

### Lid Profile (XZ end sketch)
```
           ╭──╮ ← 10mm peak
          ╱    ╲
         ╱      ╲
        ╱        ╲
    ───┴──────────┴───
       ← 29.3mm →
```

### False Bottom (XY sketch)
```
    ┌────── 25.3 ──────┐
    │                  │
    │        ○         │ 17.3
    │    (ring 6mm)    │
    └──────────────────┘
```
