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

    # Close with baseline (reverse direction to ensure closed loop)
    baseline = lines.addByTwoPoints(right, left)

    # Add coincident constraints to ensure closure
    constraints = sketch.geometricConstraints
    constraints.addCoincident(arc.endSketchPoint, baseline.startSketchPoint)
    constraints.addCoincident(baseline.endSketchPoint, arc.startSketchPoint)

    RETURN sketch.profiles.item(0)
```

### 5.3 Find Top Face

```
FUNCTION find_top_face(body):
    """Find the face with highest Z centroid"""
    max_z = -INFINITY
    top_face = NULL

    FOR face IN body.faces:
        centroid = face.centroid
        IF centroid.z > max_z:
            max_z = centroid.z
            top_face = face

    RETURN top_face
```

### 5.4 Find Bottom Face

```
FUNCTION find_bottom_face(body):
    """Find the face with lowest Z centroid"""
    min_z = INFINITY
    bottom_face = NULL

    FOR face IN body.faces:
        centroid = face.centroid
        IF centroid.z < min_z:
            min_z = centroid.z
            bottom_face = face

    RETURN bottom_face
```

### 5.5 Find Ring Profile (between nested rectangles)

```
FUNCTION find_ring_profile(sketch):
    """Find the ring-shaped profile between two nested rectangles"""
    # After sketching nested rectangles, Fusion creates multiple profiles:
    # - Profile 0: inner rectangle
    # - Profile 1: ring between inner and outer
    # - Profile 2: outer rectangle (if not bounded)

    # The ring profile has area between inner and outer
    FOR i IN range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        # Ring profile is typically index 1 for nested rectangles
        IF i == 1:
            RETURN profile

    # Fallback: return largest non-outer profile
    RETURN sketch.profiles.item(1)
```

### 5.6 Create Offset Plane

```
FUNCTION create_offset_plane(component, z_offset):
    """Create XY plane offset by z_offset in Z direction"""
    planes = component.constructionPlanes
    plane_input = planes.createInput()
    plane_input.setByOffset(
        component.xYConstructionPlane,
        ValueInput.createByReal(z_offset)
    )
    RETURN planes.add(plane_input)
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
    body = body_feature.bodies.item(0)

    # 5. Shell (remove top AND bottom faces to create open box)
    shells = comp.features.shellFeatures
    top_face = find_top_face(body)
    bottom_face = find_bottom_face(body)
    shell_input = shells.createInput([top_face, bottom_face])
    shell_input.insideThickness = ValueInput.createByReal(wall)
    shells.add(shell_input)

    # 6. Add floor back (fills bottom opening with correct thickness)
    floor_sketch = comp.sketches.add(comp.xYConstructionPlane)
    floor_profile = sketch_centered_rect(floor_sketch,
                                          width - 2 * wall,
                                          depth - 2 * wall)
    floor_input = extrudes.createInput(floor_profile, FeatureOperations.JoinFeatureOperation)
    floor_input.setDistanceExtent(False, ValueInput.createByReal(floor_t))
    extrudes.add(floor_input)

    # 7. Create ledge - offset plane method
    ledge_thickness = 0.5  # mm, thickness of ledge shelf
    planes = comp.constructionPlanes
    plane_input = planes.createInput()
    offset = floor_t + ledge_z
    plane_input.setByOffset(comp.xYConstructionPlane, ValueInput.createByReal(offset))
    ledge_plane = planes.add(plane_input)

    # 8. Sketch ledge profile (inward rectangle on all sides)
    ledge_sketch = comp.sketches.add(ledge_plane)
    inside_w = width - 2 * wall
    inside_d = depth - 2 * wall
    outer_rect = sketch_centered_rect(ledge_sketch, inside_w, inside_d)
    inner_rect = sketch_centered_rect(ledge_sketch,
                                       inside_w - 2 * ledge_depth,
                                       inside_d - 2 * ledge_depth)
    # Get ring profile between rectangles
    ledge_profile = find_ring_profile(ledge_sketch)

    # 9. Extrude ledge up (thin shelf for tray support)
    ledge_input = extrudes.createInput(ledge_profile, FeatureOperations.JoinFeatureOperation)
    ledge_input.setDistanceExtent(False, ValueInput.createByReal(ledge_thickness))
    extrudes.add(ledge_input)

    RETURN comp, ledge_thickness  # Return ledge_thickness for tray positioning
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
FUNCTION create_false_bottom(root_comp, params, ledge_thickness):
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

    # Tray sits ON TOP of ledge (ledge_z + ledge_thickness)
    tray_z = floor_t + ledge_z + ledge_thickness

    # 3. Position at ledge top
    transform = Matrix3D()
    transform.translation = Vector3D(0, 0, tray_z)
    occ.transform = transform

    # 4. Sketch tray rectangle on XY plane (component local origin)
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
    recess_depth_dim = ring_od / 2 + 1
    recess_profile = sketch_centered_rect(recess_sketch, recess_width, recess_depth_dim)

    recess_input = extrudes.createInput(recess_profile, FeatureOperations.CutFeatureOperation)
    recess_input.setDistanceExtent(False, ValueInput.createByReal(-ring_wire / 2))
    extrudes.add(recess_input)

    # 7. Create pull ring using SWEEP (not revolve)
    # This creates an arch that bridges across the recess

    ring_radius = ring_od / 2 - ring_wire / 2

    # 7a. Create path - semicircular arc at tray top surface
    # Path plane at tray_thick height (top of tray, in local coords)
    path_plane = create_offset_plane(comp, tray_thick)
    path_sketch = comp.sketches.add(path_plane)
    arcs = path_sketch.sketchCurves.sketchArcs

    # Arc endpoints at ring anchors, peak at ring top
    # Arc spans from (-ring_radius, 0) to (ring_radius, 0) in XY
    # with peak at (0, ring_radius) - this creates arch in Y direction
    start_pt = Point3D(-ring_radius, 0, 0)
    peak_pt = Point3D(0, ring_radius, 0)
    end_pt = Point3D(ring_radius, 0, 0)
    path_arc = arcs.addByThreePoints(start_pt, peak_pt, end_pt)

    # 7b. Create wire profile - circle perpendicular to path start
    # Profile plane at path start point, perpendicular to path
    profile_plane = create_perpendicular_plane(comp, path_arc.startSketchPoint)
    wire_sketch = comp.sketches.add(profile_plane)
    circles = wire_sketch.sketchCurves.sketchCircles

    # Circle centered at path start, radius = ring_wire / 2
    wire_center = Point3D(0, 0, 0)  # Center at sketch origin (on path)
    wire_circle = circles.addByCenterRadius(wire_center, ring_wire / 2)
    wire_profile = wire_sketch.profiles.item(0)

    # 7c. Sweep wire along path
    sweeps = comp.features.sweepFeatures
    sweep_input = sweeps.createInput(wire_profile, path_arc,
                                      FeatureOperations.JoinFeatureOperation)
    ring_feature = sweeps.add(sweep_input)

    RETURN occ  # Return occurrence for assembly positioning
```

#### Helper: Create Perpendicular Plane

```
FUNCTION create_perpendicular_plane(comp, sketch_point):
    """Create plane perpendicular to curve at sketch point"""
    planes = comp.constructionPlanes
    plane_input = planes.createInput()
    # Use tangent plane at point - perpendicular to path
    plane_input.setByTangentAtPoint(sketch_point.parentSketch, sketch_point)
    RETURN planes.add(plane_input)
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
FUNCTION create_coin_pile(root_comp, params, tray_top_z):
    # 1. Create component
    occ = root_comp.occurrences.addNewComponent(Matrix3D())
    comp = occ.component
    comp.name = "coin_pile"

    # 2. Get parameters
    coin_dia = params.itemByName("coin_dia").value
    coin_thick = params.itemByName("coin_thick").value

    # Pile constraints (must fit inside chest and under lid)
    max_width = 18.0   # mm
    max_depth = 14.0   # mm
    max_height = 8.0   # mm

    # 3. Position coin pile on top of false bottom
    transform = Matrix3D()
    transform.translation = Vector3D(0, 0, tray_top_z)
    occ.transform = transform

    # 4. Define coin positions (x, y, z offset from base)
    # Arranged to look like scattered/stacked pile covering the ring area
    coin_positions = [
        # Base layer (z = 0) - covers pull ring area
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

    # 5. Create all coins as separate bodies first
    extrudes = comp.features.extrudeFeatures
    bodies = []

    FOR (x, y, z) IN coin_positions:
        # Verify within bounds
        IF abs(x) + coin_dia/2 > max_width/2: CONTINUE
        IF abs(y) + coin_dia/2 > max_depth/2: CONTINUE
        IF z + coin_thick > max_height: CONTINUE

        # Create offset plane at z height (or reuse if same z)
        plane = create_offset_plane(comp, z)

        # Sketch coin circle
        sketch = comp.sketches.add(plane)
        circles = sketch.sketchCurves.sketchCircles
        center = Point3D(x, y, 0)
        circles.addByCenterRadius(center, coin_dia / 2)

        profile = sketch.profiles.item(0)

        # Extrude coin as new body
        ext_input = extrudes.createInput(profile, FeatureOperations.NewBodyFeatureOperation)
        ext_input.setDistanceExtent(False, ValueInput.createByReal(coin_thick))
        coin_feature = extrudes.add(ext_input)

        bodies.append(coin_feature.bodies.item(0))

    # 6. Combine all bodies into one using single combine operation
    IF len(bodies) > 1:
        combines = comp.features.combineFeatures

        # Create collection of tool bodies (all except first)
        tool_bodies = ObjectCollection.create()
        FOR i IN range(1, len(bodies)):
            tool_bodies.add(bodies[i])

        # Combine: target = first body, tools = all others
        combine_input = combines.createInput(bodies[0], tool_bodies)
        combine_input.operation = FeatureOperations.JoinFeatureOperation
        combine_input.isKeepToolBodies = False  # Delete tool bodies after combine
        combines.add(combine_input)

    # 7. Name the final unified body
    final_body = comp.bRepBodies.item(0)
    final_body.name = "coin_pile"

    RETURN occ  # Return occurrence for assembly
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
│  Create chest_body  │──→ Returns ledge_thickness
└──────────┬──────────┘
           │ ledge_thickness
           ▼
┌─────────────────────┐
│  Create lid         │──→ Positioned at chest_height
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Create false_bottom│──→ Positioned at ledge_z + ledge_thickness
└──────────┬──────────┘
           │ tray_top_z
           ▼
┌─────────────────────┐
│  Create coin_pile   │──→ Positioned at tray_top_z
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

        # Pre-calculate key dimensions for component positioning
        floor_t = params.itemByName("floor").value
        ledge_z = params.itemByName("ledge_z").value
        tray_thick = params.itemByName("tray_thick").value

        # Generate components in order (passing derived positions)

        # 1. Chest body (returns ledge_thickness for tray positioning)
        chest_occ, ledge_thickness = create_chest_body(root, params)

        # 2. Lid (positions itself at chest_height)
        lid_occ = create_lid(root, params)

        # 3. False bottom (sits on top of ledge)
        tray_occ = create_false_bottom(root, params, ledge_thickness)

        # 4. Coin pile (sits on top of false bottom)
        # Calculate tray top Z position
        tray_top_z = floor_t + ledge_z + ledge_thickness + tray_thick
        coins_occ = create_coin_pile(root, params, tray_top_z)

        # Verify assembly
        interference = check_interference(design)
        IF interference:
            ui.messageBox("Warning: Component interference detected")

        ui.messageBox("Treasure chest generated successfully!\n" +
                      f"Components: chest_body, lid, false_bottom, coin_pile")

    EXCEPT Exception as e:
        ui.messageBox(f"Error: {traceback.format_exc()}")
```

---

## 8. Assembly Verification

### 8.1 Interference Check

```
FUNCTION check_interference(design):
    app = Application.get()
    ui = app.userInterface
    root = design.rootComponent
    bodies = []

    # Collect all bodies from all components
    FOR occ IN root.allOccurrences:
        FOR body IN occ.bRepBodies:
            bodies.append(body)

    # Check each pair
    interference_found = False
    interference_list = []

    FOR i IN range(len(bodies)):
        FOR j IN range(i+1, len(bodies)):
            result = bodies[i].interferesWith(bodies[j])
            IF result:
                interference_found = True
                interference_list.append(f"{bodies[i].name} vs {bodies[j].name}")

    # Report any interferences found
    IF interference_found:
        ui.messageBox("Interference detected:\n" + "\n".join(interference_list))

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
| v01.1 | 2026-01-03 | Fixed: shell operation (add floor back), pull ring (sweep not revolve), component positioning, helper functions, coin union strategy |

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
