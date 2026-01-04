# Treasure Chest with Hidden Compartment

**Project:** treasure-chest
**Version:** v01
**Purpose:** Beginner Fusion 360 learning project
**Scale:** D&D tabletop (28-32mm miniature scale)

---

## 1. Functional Requirements (FR)

### 1.1 Core Functionality

| ID | Requirement | Rationale |
|----|-------------|-----------|
| FR-01 | Chest shall have a removable lid | Access to main compartment |
| FR-02 | Lid shall friction-fit onto body (no hardware) | Simple assembly, reliable at small scale |
| FR-03 | Chest shall contain a hidden compartment | Core feature for D&D gameplay |
| FR-04 | Hidden compartment shall be concealed by a false bottom | Discrete, not obvious when lid removed |
| FR-05 | False bottom shall be removable by hand | User access to secret compartment |
| FR-06 | False bottom shall include a pull ring for removal | Finger grip at small scale |

### 1.2 Concealment

| ID | Requirement | Rationale |
|----|-------------|-----------|
| FR-07 | Hidden compartment shall not be visible when lid is removed | Maintains secret |
| FR-08 | False bottom shall rest flush on internal ledge | No visible gap revealing compartment |
| FR-09 | Pull ring shall be recessed or flush with tray surface | Minimizes detection |
| FR-13 | Coin pile shall cover and conceal the pull ring | Hides removal mechanism |
| FR-14 | Coin pile shall be removable by hand to access pull ring | User can reveal ring when needed |
| FR-15 | Coin pile shall appear as stacked/scattered gold coins | Thematic prop for D&D |
| FR-16 | Coin pile shall be printed as single fused piece | No loose parts to lose |

### 1.3 Assembly

| ID | Requirement | Rationale |
|----|-------------|-----------|
| FR-10 | All components shall assemble without tools or adhesive | Print-and-play simplicity |
| FR-11 | Lid shall stay in place when chest is handled | Usable during gameplay |
| FR-12 | Lid shall be removable with one hand | Easy access |

---

## 2. Non-Functional Requirements (NFR)

### 2.1 Physical Dimensions

| ID | Requirement | Value | Rationale |
|----|-------------|-------|-----------|
| NFR-01 | Exterior width | 30 mm | D&D tabletop scale |
| NFR-02 | Exterior depth | 22 mm | Proportional to width |
| NFR-03 | Body height (no lid) | 20 mm | Room for compartments |
| NFR-04 | Lid height at peak | 10 mm | Classic barrel-top profile |
| NFR-05 | Total assembled height | ≤ 35 mm | Tabletop appropriate |
| NFR-06 | Hidden compartment depth | 8 mm | Usable secret storage |

### 2.2 Structural

| ID | Requirement | Value | Rationale |
|----|-------------|-------|-----------|
| NFR-07 | Wall thickness | 2.0 mm | 5 perimeters @ 0.4mm nozzle |
| NFR-08 | Floor thickness | 1.6 mm | 8 layers @ 0.2mm height |
| NFR-09 | Ledge protrusion | 1.2 mm | 3 perimeters, supports tray |
| NFR-10 | False bottom thickness | 1.6 mm | Rigid, matches floor |
| NFR-11 | Pull ring wire diameter | 1.6 mm | 4 perimeters, won't snap |
| NFR-12 | Pull ring outer diameter | 6.0 mm | Finger accessible |

### 2.3 Fit & Tolerance

| ID | Requirement | Value | Rationale |
|----|-------------|-------|-----------|
| NFR-13 | Lid-to-body clearance | 0.35 mm | Friction fit, snug but removable |
| NFR-14 | Tray-to-wall clearance | 0.35 mm | Easy lift-out |
| NFR-15 | Minimum feature size | 0.8 mm | 2 perimeters minimum |

### 2.4 Manufacturing

| ID | Requirement | Rationale |
|----|-------------|-----------|
| NFR-16 | All components shall print on FlashForge Adventurer 5M Pro | Target printer |
| NFR-17 | Material shall be PLA | Standard, easy to print |
| NFR-18 | Nozzle size shall be 0.4 mm | Standard nozzle |
| NFR-19 | Chest body shall print without supports | Upright orientation |
| NFR-20 | Lid shall print without supports | Dome-down orientation |
| NFR-21 | False bottom shall print without supports | Flat, ring bridges |
| NFR-22 | Total print time shall be under 2 hours | Practical iteration |

### 2.5 Aesthetics

| ID | Requirement | Rationale |
|----|-------------|-----------|
| NFR-23 | Lid shall have curved barrel-top profile | Classic treasure chest look |
| NFR-24 | Proportions shall match D&D miniature scale (28-32mm) | Visual consistency with minis |

### 2.6 Coin Pile

| ID | Requirement | Value | Rationale |
|----|-------------|-------|-----------|
| NFR-25 | Coin diameter | 4.0 mm | Scale-appropriate gold coins |
| NFR-26 | Coin thickness | 0.8 mm | Visible stacking, printable |
| NFR-27 | Pile footprint | ≤ 18 × 14 mm | Fits inside chest with clearance |
| NFR-28 | Pile height | ≤ 8 mm | Clears lid when closed |
| NFR-29 | Coin pile shall print without supports | Coins fused, no overhangs > 45° |

---

## 3. Components

| # | Component | Description | Satisfies |
|---|-----------|-------------|-----------|
| 1 | chest_body | Main container with internal ledge | FR-03, FR-08, NFR-01–03, NFR-07–09 |
| 2 | lid | Curved barrel-top, friction fits | FR-01, FR-02, FR-11, FR-12, NFR-04, NFR-23 |
| 3 | false_bottom | Tray concealing hidden compartment | FR-04, FR-05, FR-07, FR-08, NFR-10, NFR-14 |
| 4 | pull_ring | Ring for lifting false bottom | FR-06, FR-09, NFR-11, NFR-12 |
| 5 | coin_pile | Fused pile of gold coins, covers pull ring | FR-13, FR-14, FR-15, FR-16, NFR-25–29 |

---

## 4. User Parameters (Fusion 360)

| Parameter | Value | Unit | Traces To |
|-----------|-------|------|-----------|
| `chest_width` | 30 | mm | NFR-01 |
| `chest_depth` | 22 | mm | NFR-02 |
| `chest_height` | 20 | mm | NFR-03 |
| `lid_height` | 10 | mm | NFR-04 |
| `wall` | 2 | mm | NFR-07 |
| `floor` | 1.6 | mm | NFR-08 |
| `clearance` | 0.35 | mm | NFR-13, NFR-14 |
| `ledge_z` | 8 | mm | NFR-06 |
| `ledge_depth` | 1.2 | mm | NFR-09 |
| `ring_od` | 6 | mm | NFR-12 |
| `ring_wire` | 1.6 | mm | NFR-11 |
| `tray_thick` | 1.6 | mm | NFR-10 |
| `coin_dia` | 4.0 | mm | NFR-25 |
| `coin_thick` | 0.8 | mm | NFR-26 |
| `ledge_thick` | 0.5 | mm | (design detail) |
| `rim_depth` | 3.0 | mm | (design detail) |
| `rim_wall` | 1.5 | mm | (design detail) |

---

## 5. Export Naming

```
treasure-chest_{component}_v01_pla.stl
```

| Component | Filename |
|-----------|----------|
| chest_body | `treasure-chest_chest-body_v01_pla.stl` |
| lid | `treasure-chest_lid_v01_pla.stl` |
| false_bottom | `treasure-chest_false-bottom_v01_pla.stl` |
| coin_pile | `treasure-chest_coin-pile_v01_pla.stl` |

> **Note:** `pull_ring` is modeled separately but printed as one piece with `false_bottom` (bridged attachment, no supports).

---

## 6. Verification Checklist

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

## 7. Revision History

| Version | Date | Changes |
|---------|------|---------|
| v01 | 2026-01-03 | Initial requirements |
| v01.1 | 2026-01-03 | Added coin pile component (FR-13–16, NFR-25–29) |
| v01.2 | 2026-01-03 | Fixed NFR-08 layer calc (8 layers), added design params (ledge_thick, rim_depth, rim_wall) |
