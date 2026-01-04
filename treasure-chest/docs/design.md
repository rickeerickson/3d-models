# Treasure Chest Design Document

**Project:** treasure-chest
**Version:** v01
**Status:** Design Phase
**Approach:** Fusion 360 Python API Scripting

---

## 1. Design Overview

A four-piece treasure chest for D&D tabletop gaming with a hidden compartment accessed via a false bottom. All geometry is generated programmatically using Fusion 360 Python scripts.

```
┌─────────────────────────┐
│     ╭───────────╮       │  ← Curved lid (friction fit)
│    ╱             ╲      │
├───┴───────────────┴─────┤
│   [coin pile ○○○]       │  ← Covers pull ring
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

## 2. Script Architecture

```
scripts/fusion/
├── generate_all.py              # Orchestrator - builds entire assembly
├── components/
│   ├── __init__.py
│   ├── chest_body.py            # Main container with ledge
│   ├── lid.py                   # Barrel-top lid with rim
│   ├── false_bottom.py          # Tray with integrated pull ring
│   └── coin_pile.py             # Decorative coin stack
└── utils/
    ├── __init__.py
    ├── parameters.py            # User parameter definitions
    └── sketches.py              # Common sketch helpers
```

### 2.1 Module Responsibilities

| Module | Purpose | Satisfies |
|--------|---------|-----------|
| `parameters.py` | Define/update all user parameters | Parametric design |
| `sketches.py` | Rectangle, arc, circle sketch helpers | Code reuse |
| `chest_body.py` | Main container with internal ledge | FR-03, FR-08, NFR-01–03 |
| `lid.py` | Curved lid with friction-fit rim | FR-01, FR-02, FR-11, FR-12, NFR-04, NFR-23 |
| `false_bottom.py` | Tray + integrated pull ring | FR-04–09, NFR-10–12, NFR-14 |
| `coin_pile.py` | Fused coin stack | FR-13–16, NFR-25–29 |
| `generate_all.py` | Orchestrate full assembly | FR-10, NFR-16–22 |

---

## 3. User Parameters

All dimensions are defined as Fusion user parameters for easy iteration.

| Parameter | Value | Unit | Formula/Notes |
|-----------|-------|------|---------------|
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
| `coin_dia` | 4.0 | mm | Coin diameter |
| `coin_thick` | 0.8 | mm | Coin thickness |

### 3.1 Derived Values

```
inside_width  = chest_width - 2 * wall           # 26 mm
inside_depth  = chest_depth - 2 * wall           # 18 mm
tray_width    = inside_width - 2 * clearance     # 25.3 mm
tray_depth    = inside_depth - 2 * clearance     # 17.3 mm
lid_width     = chest_width - 2 * clearance      # 29.3 mm
lid_depth     = chest_depth - 2 * clearance      # 21.3 mm
```

---

## 4. Parameter Management (utils/parameters.py)

### 4.1 Algorithm

```
FUNCTION ensure_parameters(design):
    params = {
        "chest_width": 30,
        "chest_depth": 22,
        "chest_height": 20,
        ...
    }

    FOR name, value IN params:
        existing = design.userParameters.itemByName(name)
        IF existing IS NULL:
            design.userParameters.add(name, value, "mm", "")
        ELSE:
            existing.value = value  # Update if needed

    RETURN design.userParameters
```

### 4.2 Usage Pattern

```
# In any component script:
params = design.userParameters
width = params.itemByName("chest_width").value  # Returns cm internally
```

---

## 5. Sketch Helpers (utils/sketches.py)

### 5.1 Centered Rectangle

```
FUNCTION sketch_centered_rect(sketch, width, height):
    lines = sketch.sketchCurves.sketchLines

    half_w = width / 2
    half_h = height / 2

    # Draw rectangle centered on origin
    p1 = Point3D(-half_w, -half_h, 0)
    p2 = Point3D(half_w, -half_h, 0)
    p3 = Point3D(half_w, half_h, 0)
    p4 = Point3D(-half_w, half_h, 0)

    lines.addByTwoPoints(p1, p2)
    lines.addByTwoPoints(p2, p3)
    lines.addByTwoPoints(p3, p4)
    lines.addByTwoPoints(p4, p1)

    RETURN sketch.profiles.item(0)
```

### 5.2 Arc Profile (for lid)

```
FUNCTION sketch_barrel_arc(sketch, width, height):
    arcs = sketch.sketchCurves.sketchArcs
    lines = sketch.sketchCurves.sketchLines

    # Three-point arc: left base, peak, right base
    left = Point3D(-width/2, 0, 0)
    peak = Point3D(0, height, 0)
    right = Point3D(width/2, 0, 0)

    arc = arcs.addByThreePoints(left, peak, right)

    # Close with baseline
    lines.addByTwoPoints(left, right)

    RETURN sketch.profiles.item(0)
```

---

## 6. Component Designs

### 6.1 Chest Body (components/chest_body.py)

Main container with internal ledge for false bottom support.

#### Sketch Diagram

```
        chest_width (30mm)
    ├─────────────────────┤

    ┌─────────────────────┐ ─┬─ chest_height (20mm)
    │                     │  │
    │   ┌─────────────┐   │  │
    │   │             │   │  │  ← inside cavity
    │   │  ┌───────┐  │   │  │
    │   │  │ ledge │  │   │  │  ← ledge_z (8mm) from floor
    │   │  └───────┘  │   │  │
    │   │             │   │  │
    │   └─────────────┘   │  │
    └─────────────────────┘ ─┴─

    │wall│           │wall│
      2mm             2mm
```

#### Algorithm

```
FUNCTION create_chest_body(root_comp, params):
    # 1. Create new component
    occ = root_comp.occurrences.addNewComponent(Matrix3D())
    comp = occ.component
    comp.name = "chest_body"

    # 2. Get parameters
    width = params.itemByName("chest_width").value
    depth = params.itemByName("chest_depth").value
    height = params.itemByName("chest_height").value
    wall = params.itemByName("wall").value
    floor_t = params.itemByName("floor").value
    ledge_z = params.itemByName("ledge_z").value
    ledge_depth = params.itemByName("ledge_depth").value

    # 3. Base sketch on XY plane
    sketch = comp.sketches.add(comp.xYConstructionPlane)
    profile = sketch_centered_rect(sketch, width, depth)

    # 4. Extrude up
    extrudes = comp.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, FeatureOperations.NewBodyFeatureOperation)
    ext_input.setDistanceExtent(False, ValueInput.createByReal(height))
    body_feature = extrudes.add(ext_input)

    # 5. Shell (remove top face, keep floor)
    shells = comp.features.shellFeatures
    top_face = find_top_face(body_feature.bodies.item(0))
    shell_input = shells.createInput([top_face])
    shell_input.insideThickness = ValueInput.createByReal(wall)
    shells.add(shell_input)

    # 6. Create ledge - offset plane method
    planes = comp.constructionPlanes
    plane_input = planes.createInput()
    offset = floor_t + ledge_z
    plane_input.setByOffset(comp.xYConstructionPlane, ValueInput.createByReal(offset))
    ledge_plane = planes.add(plane_input)

    # 7. Sketch ledge profile (inward rectangle on all sides)
    ledge_sketch = comp.sketches.add(ledge_plane)
    inside_w = width - 2 * wall
    inside_d = depth - 2 * wall
    outer_rect = sketch_centered_rect(ledge_sketch, inside_w, inside_d)
    inner_rect = sketch_centered_rect(ledge_sketch,
                                       inside_w - 2 * ledge_depth,
                                       inside_d - 2 * ledge_depth)
    # Get ring profile between rectangles
    ledge_profile = find_ring_profile(ledge_sketch)

    # 8. Extrude ledge up (small height for support surface)
    ledge_input = extrudes.createInput(ledge_profile, FeatureOperations.JoinFeatureOperation)
    ledge_input.setDistanceExtent(False, ValueInput.createByReal(0.5))  # thin ledge
    extrudes.add(ledge_input)

    RETURN comp
```

#### Print Orientation
- Opening facing up
- No supports needed
- First layer = floor (1.6mm = 8 layers @ 0.2mm)

---

### 6.2 Lid (components/lid.py)

Curved barrel-top lid with friction-fit rim.

#### Sketch Diagram

```
              lid_height (10mm)
                 ↕
            ╭─────────╮
           ╱           ╲
         ╱               ╲
        ╱                 ╲
    ───┴───────────────────┴───
       │                   │
       │   friction rim    │   ← 3mm deep into body
       │     (1.5mm wall)  │
       └───────────────────┘

    ├───────lid_width─────────┤
           (29.3mm)
```

#### Algorithm

```
FUNCTION create_lid(root_comp, params):
    # 1. Create component
    occ = root_comp.occurrences.addNewComponent(Matrix3D())
    comp = occ.component
    comp.name = "lid"

    # 2. Get parameters
    chest_width = params.itemByName("chest_width").value
    chest_depth = params.itemByName("chest_depth").value
    chest_height = params.itemByName("chest_height").value
    lid_height = params.itemByName("lid_height").value
    clearance = params.itemByName("clearance").value
    wall = params.itemByName("wall").value

    lid_width = chest_width - 2 * clearance
    lid_depth = chest_depth - 2 * clearance
    rim_depth = 3.0  # mm, how far rim extends into body
    rim_wall = 1.5   # mm, rim wall thickness

    # 3. Position at top of chest body
    transform = Matrix3D()
    transform.translation = Vector3D(0, 0, chest_height)
    occ.transform = transform

    # 4. Sketch barrel arc on XZ plane (end profile)
    sketch = comp.sketches.add(comp.xZConstructionPlane)
    profile = sketch_barrel_arc(sketch, lid_width, lid_height)

    # 5. Extrude symmetric in Y direction
    extrudes = comp.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, FeatureOperations.NewBodyFeatureOperation)
    ext_input.setSymmetricExtent(ValueInput.createByReal(lid_depth / 2), True)
    dome_feature = extrudes.add(ext_input)

    # 6. Add friction rim
    # Sketch on bottom face of dome
    bottom_face = find_bottom_face(dome_feature.bodies.item(0))
    rim_sketch = comp.sketches.add(bottom_face)

    # Outer rectangle (full lid size)
    outer = sketch_centered_rect(rim_sketch, lid_width, lid_depth)

    # Inner rectangle (rim wall inset)
    inner = sketch_centered_rect(rim_sketch,
                                  lid_width - 2 * rim_wall,
                                  lid_depth - 2 * rim_wall)

    rim_profile = find_ring_profile(rim_sketch)

    # 7. Extrude rim downward
    rim_input = extrudes.createInput(rim_profile, FeatureOperations.JoinFeatureOperation)
    rim_input.setDistanceExtent(False, ValueInput.createByReal(-rim_depth))
    extrudes.add(rim_input)

    RETURN comp
```

#### Print Orientation
- Dome facing down (flat rim on build plate)
- No supports needed

---

### 6.3 False Bottom (components/false_bottom.py)

Removable tray with integrated pull ring for accessing hidden compartment.

#### Sketch Diagram

```
    ┌─────────────────────────────┐
    │                             │
    │   ┌─────────────────────┐   │  ← chest inside wall
    │   │      0.35mm gap     │   │
    │   │   ┌─────────────┐   │   │  ← tray (25.3 × 17.3mm)
    │   │   │             │   │   │
    │   │   │   ╭─────╮   │   │   │  ← ring arch (6mm OD)
    │   │   │   ╰─────╯   │   │   │
    │   │   │   [recess]  │   │   │  ← recessed slot for ring
    │   │   └─────────────┘   │   │
    │   │                     │   │
    │   └─────────────────────┘   │
    │                             │
    └─────────────────────────────┘
```

#### Algorithm

```
FUNCTION create_false_bottom(root_comp, params):
    # 1. Create component
    occ = root_comp.occurrences.addNewComponent(Matrix3D())
    comp = occ.component
    comp.name = "false_bottom"

    # 2. Get parameters
    chest_width = params.itemByName("chest_width").value
    chest_depth = params.itemByName("chest_depth").value
    wall = params.itemByName("wall").value
    floor_t = params.itemByName("floor").value
    clearance = params.itemByName("clearance").value
    ledge_z = params.itemByName("ledge_z").value
    tray_thick = params.itemByName("tray_thick").value
    ring_od = params.itemByName("ring_od").value
    ring_wire = params.itemByName("ring_wire").value

    tray_width = chest_width - 2 * wall - 2 * clearance
    tray_depth = chest_depth - 2 * wall - 2 * clearance
    tray_z = floor_t + ledge_z  # Z position where tray sits

    # 3. Position at ledge height
    transform = Matrix3D()
    transform.translation = Vector3D(0, 0, tray_z)
    occ.transform = transform

    # 4. Sketch tray rectangle on XY plane
    sketch = comp.sketches.add(comp.xYConstructionPlane)
    profile = sketch_centered_rect(sketch, tray_width, tray_depth)

    # 5. Extrude tray
    extrudes = comp.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, FeatureOperations.NewBodyFeatureOperation)
    ext_input.setDistanceExtent(False, ValueInput.createByReal(tray_thick))
    tray_feature = extrudes.add(ext_input)
    tray_body = tray_feature.bodies.item(0)
    tray_body.name = "tray"

    # 6. Create ring recess (cut into top surface)
    top_face = find_top_face(tray_body)
    recess_sketch = comp.sketches.add(top_face)

    # Recess is rounded rectangle, sized for ring to sit in
    recess_width = ring_od + 2
    recess_depth = ring_od / 2 + 1
    recess_profile = sketch_centered_rect(recess_sketch, recess_width, recess_depth)

    recess_input = extrudes.createInput(recess_profile, FeatureOperations.CutFeatureOperation)
    recess_input.setDistanceExtent(False, ValueInput.createByReal(-ring_wire / 2))
    extrudes.add(recess_input)

    # 7. Create pull ring (bridged arch)
    # Sketch ring cross-section on XZ plane
    ring_sketch = comp.sketches.add(comp.xZConstructionPlane)
    circles = ring_sketch.sketchCurves.sketchCircles

    # Circle center at ring radius from tray center, at tray surface
    ring_radius = ring_od / 2 - ring_wire / 2
    center = Point3D(ring_radius, tray_thick, 0)
    wire_circle = circles.addByCenterRadius(center, ring_wire / 2)

    ring_profile = ring_sketch.profiles.item(0)

    # 8. Revolve 180 degrees to create arch
    revolves = comp.features.revolveFeatures
    # Axis is Z-axis at tray center
    axis = comp.zConstructionAxis
    rev_input = revolves.createInput(ring_profile, axis, FeatureOperations.NewBodyFeatureOperation)
    rev_input.setAngleExtent(False, ValueInput.createByReal(math.pi))  # 180 degrees
    ring_feature = revolves.add(rev_input)
    ring_body = ring_feature.bodies.item(0)
    ring_body.name = "ring"

    RETURN comp
```

#### Print Orientation
- Flat (tray on build plate)
- Ring bridges across recess (~4mm span)
- No supports needed

---

### 6.4 Coin Pile (components/coin_pile.py)

Decorative fused pile of gold coins that covers the pull ring.

#### Sketch Diagram

```
    Top view:                    Side view:

    ┌──────────────┐             ○○○ ← top coins
    │  ○  ○○  ○    │              ○○○○
    │ ○○○○ ○○ ○○   │             ○○○○○ ← base coins
    │  ○○ ○○○ ○    │            ────────
    │   ○  ○○      │            (tray surface)
    └──────────────┘

    Footprint: ≤ 18 × 14 mm
    Height: ≤ 8 mm
```

#### Algorithm

```
FUNCTION create_coin_pile(root_comp, params):
    # 1. Create component
    occ = root_comp.occurrences.addNewComponent(Matrix3D())
    comp = occ.component
    comp.name = "coin_pile"

    # 2. Get parameters
    coin_dia = params.itemByName("coin_dia").value
    coin_thick = params.itemByName("coin_thick").value

    # Pile constraints
    max_width = 18.0   # mm
    max_depth = 14.0   # mm
    max_height = 8.0   # mm

    # 3. Define coin positions (x, y, z offset from base)
    # Arranged to look like scattered/stacked pile
    coin_positions = [
        # Base layer (z = 0)
        (-3, -2, 0), (0, -3, 0), (3, -2, 0), (5, 0, 0),
        (-4, 1, 0), (-1, 0, 0), (2, 1, 0), (4, 3, 0),
        (-2, 3, 0), (1, 4, 0), (-5, -1, 0),

        # Second layer (z = coin_thick, offset for stacking)
        (-2, -1, coin_thick), (1, 0, coin_thick), (3, 1, coin_thick),
        (-3, 2, coin_thick), (0, 3, coin_thick), (4, -1, coin_thick),

        # Third layer
        (-1, 0, 2*coin_thick), (2, 1, 2*coin_thick), (0, 2, 2*coin_thick),

        # Top coins
        (0, 1, 3*coin_thick), (1, 0, 4*coin_thick),
    ]

    # 4. Create each coin and union
    extrudes = comp.features.extrudeFeatures
    combines = comp.features.combineFeatures
    bodies = []

    FOR (x, y, z) IN coin_positions:
        # Verify within bounds
        IF abs(x) + coin_dia/2 > max_width/2: CONTINUE
        IF abs(y) + coin_dia/2 > max_depth/2: CONTINUE
        IF z + coin_thick > max_height: CONTINUE

        # Create offset plane at z height
        plane = create_offset_plane(comp, z)

        # Sketch coin circle
        sketch = comp.sketches.add(plane)
        circles = sketch.sketchCurves.sketchCircles
        center = Point3D(x, y, 0)
        circles.addByCenterRadius(center, coin_dia / 2)

        profile = sketch.profiles.item(0)

        # Extrude coin
        IF bodies IS EMPTY:
            operation = FeatureOperations.NewBodyFeatureOperation
        ELSE:
            operation = FeatureOperations.JoinFeatureOperation

        ext_input = extrudes.createInput(profile, operation)
        ext_input.setDistanceExtent(False, ValueInput.createByReal(coin_thick))
        coin_feature = extrudes.add(ext_input)

        bodies.append(coin_feature.bodies.item(0))

    # 5. All coins are now unioned into single body
    final_body = bodies[0]
    final_body.name = "coin_pile"

    RETURN comp
```

#### Print Orientation
- Flat (base coins on build plate)
- Stacked coins self-support (each layer offsets slightly)
- No supports needed (no overhangs > 45°)

---

## 7. Orchestrator (generate_all.py)

### 7.1 Flow Diagram

```
┌─────────────────────┐
│  Start Script       │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Get Active Design  │──→ Error if none
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Ensure Parameters  │──→ Create/update user params
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Create Root Comp   │──→ "treasure-chest"
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Create chest_body  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Create lid         │──→ Positioned at chest_height
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Create false_bottom│──→ Positioned at ledge_z
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Create coin_pile   │──→ Positioned on false_bottom
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Interference Check │──→ Warn if collisions
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Report Success     │
└─────────────────────┘
```

### 7.2 Algorithm

```
FUNCTION run(context):
    app = Application.get()
    ui = app.userInterface

    TRY:
        # Get or create design
        design = app.activeProduct
        IF design IS NULL:
            ui.messageBox("No active design")
            RETURN

        # Initialize parameters
        ensure_parameters(design)
        params = design.userParameters

        # Get root component
        root = design.rootComponent
        root.name = "treasure-chest"

        # Generate components in order
        chest = create_chest_body(root, params)
        lid = create_lid(root, params)
        tray = create_false_bottom(root, params)
        coins = create_coin_pile(root, params)

        # Verify assembly
        interference = check_interference(design)
        IF interference:
            ui.messageBox("Warning: Component interference detected")

        ui.messageBox("Treasure chest generated successfully!")

    EXCEPT Exception as e:
        ui.messageBox(f"Error: {traceback.format_exc()}")
```

---

## 8. Assembly Verification

### 8.1 Interference Check

```
FUNCTION check_interference(design):
    root = design.rootComponent
    bodies = []

    # Collect all bodies from all components
    FOR occ IN root.allOccurrences:
        FOR body IN occ.bRepBodies:
            bodies.append(body)

    # Check each pair
    interference_found = False
    FOR i IN range(len(bodies)):
        FOR j IN range(i+1, len(bodies)):
            result = bodies[i].interferesWith(bodies[j])
            IF result:
                interference_found = True
                LOG(f"Interference: {bodies[i].name} vs {bodies[j].name}")

    RETURN interference_found
```

### 8.2 Section Analysis

After generation, verify manually:

1. **Inspect → Section Analysis**
2. Cut through center (XZ and YZ planes)
3. Confirm:
   - [ ] Lid rim seats inside body with 0.35mm gap
   - [ ] False bottom clears walls by 0.35mm
   - [ ] Ledge supports tray properly
   - [ ] Ring sits in recess, arch proud of surface
   - [ ] Coin pile covers ring area

---

## 9. Export Specifications

### 9.1 STL Settings

| Setting | Value |
|---------|-------|
| Refinement | Medium |
| Format | Binary STL |
| Units | mm |

### 9.2 Export Files

| Component | Filename |
|-----------|----------|
| chest_body | `treasure-chest_chest-body_v01_pla.stl` |
| lid | `treasure-chest_lid_v01_pla.stl` |
| false_bottom | `treasure-chest_false-bottom_v01_pla.stl` |
| coin_pile | `treasure-chest_coin-pile_v01_pla.stl` |

> **Note:** `pull_ring` is integrated with `false_bottom` (bridged arch, no separate export).

---

## 10. Print Considerations

### 10.1 Orientation Summary

| Part | Orientation | Supports |
|------|-------------|----------|
| chest_body | Opening up | None |
| lid | Dome down (flat rim on bed) | None |
| false_bottom | Flat (ring bridges) | None |
| coin_pile | Base coins on bed | None |

### 10.2 Critical Settings

- **Layer height:** 0.2mm (0.16mm for finer coins)
- **Nozzle:** 0.4mm
- **Bridge detection:** Enabled (for pull ring)
- **Infill:** 15-20% (structural parts)

### 10.3 Estimated Print Time

| Part | Time |
|------|------|
| chest_body | ~25 min |
| lid | ~20 min |
| false_bottom | ~15 min |
| coin_pile | ~20 min |
| **Total** | **< 2 hours** (NFR-22) |

---

## 11. Verification Checklist

### Functional Requirements

| ID | Test | Pass |
|----|------|------|
| FR-01 | Lid removes from body by hand | [ ] |
| FR-02 | Lid stays seated without hardware | [ ] |
| FR-03 | Hidden space exists below false bottom | [ ] |
| FR-04 | False bottom covers hidden compartment | [ ] |
| FR-05 | False bottom lifts out by hand | [ ] |
| FR-06 | Pull ring provides adequate grip | [ ] |
| FR-07 | Compartment not visible with lid off | [ ] |
| FR-08 | False bottom sits flush on ledge | [ ] |
| FR-09 | Pull ring not obviously visible | [ ] |
| FR-10 | No tools/glue needed for assembly | [ ] |
| FR-11 | Lid stays on during normal handling | [ ] |
| FR-12 | Lid removable with one hand | [ ] |
| FR-13 | Coin pile covers pull ring when placed | [ ] |
| FR-14 | Coin pile lifts out by hand | [ ] |
| FR-15 | Coin pile visually resembles stacked coins | [ ] |
| FR-16 | Coin pile is single fused piece | [ ] |

### Non-Functional Requirements

| ID | Test | Pass |
|----|------|------|
| NFR-01–05 | Measure exterior dimensions | [ ] |
| NFR-06 | Measure hidden compartment depth ≥ 8mm | [ ] |
| NFR-13 | Lid friction fit: holds when tilted 45°, removable by hand | [ ] |
| NFR-14 | Tray lifts out with finger through ring (no tools) | [ ] |
| NFR-19–21 | All parts printed without supports | [ ] |
| NFR-22 | Total print time < 2 hours | [ ] |
| NFR-27 | Coin pile fits inside chest with clearance | [ ] |
| NFR-28 | Coin pile height ≤ 8mm (clears lid) | [ ] |
| NFR-29 | Coin pile prints without supports | [ ] |

---

## 12. Error Handling

### 12.1 Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| No active design | Script run without document | Create new design first |
| Parameter not found | User parameter deleted | Re-run ensure_parameters() |
| Extrude failed | Profile not closed | Check sketch geometry |
| Shell failed | Wall too thick | Reduce wall parameter |
| Interference detected | Clearance too small | Increase clearance parameter |

### 12.2 Recovery Strategy

```
TRY:
    # Component creation
EXCEPT:
    # Log error with component name
    # Continue to next component
    # Report partial success at end
```

---

## 13. Version History

| Version | Date | Changes |
|---------|------|---------|
| v01 | 2026-01-03 | Initial scripted design |

---

## Appendix A: Fusion 360 API Reference

### Key Classes

| Class | Purpose |
|-------|---------|
| `Application` | Entry point, access to UI and documents |
| `Design` | Active design document |
| `Component` | Container for bodies and sketches |
| `Sketch` | 2D geometry for profiles |
| `ExtrudeFeature` | Create bodies from profiles |
| `ShellFeature` | Hollow out bodies |
| `RevolveFeature` | Rotate profiles around axis |
| `UserParameter` | Named parametric values |

### Units

- Internal: centimeters (cm)
- Display: millimeters (mm)
- Conversion: `value_mm = value_cm * 10`

### Coordinate System

- X: Width (left-right)
- Y: Depth (front-back)
- Z: Height (up)
- Origin: Center of chest base
