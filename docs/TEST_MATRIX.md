> Evidence correction: historical PASS rates, scores, rankings and performance claims in this document are unverified legacy assumptions (LEGACY_SYNTHETIC). They are not candidate MCP execution evidence. Do not use them to authorize execution.

# CAD-MCP Test Matrix Specification (T01 – T34)

Standardized test matrix for validating CAD MCP servers on live ZWCAD 2026 and related CAD engines.

---

## Matrix Overview

| Test ID | Category | Test Name | Target Capability | Verification Method |
|:---:|---|---|---|---|
| **T01** | Session | Active Document & Connection | `session.connect`, `doc.name` | Read document name, path, state |
| **T02** | Inspection | Metadata & Extents Read | `doc.layers`, `doc.blocks`, `extents` | Query layer list, block count, drawing limits |
| **T03** | Query | Entity Query & Filtering | `entity.count`, `entity.type` | Filter entities by layer/type, compare counts |
| **T04** | Inspection | Entity Property Read | `handle`, `color`, `coordinates`, `area` | Read geometry coordinates and calculate area |
| **T05** | Drafting | Layer Creation & Setup | `layer.create`, `layer.color` | Create `WAL1`, `COL`, `DOOR`, `WIN`, `DIM`, `TEXT` |
| **T06** | Drafting | Line & Polyline Draw | `draw.line`, `draw.lwpolyline` | Draw 8000x6000 outer & 7600x5600 inner wall |
| **T07** | Transform | Entity Modification | `entity.move`, `entity.rotate`, `scale` | Translate column block by +200mm, verify coords |
| **T08** | Block | Standard Block Insertion | `block.insert` | Insert standard 400x400 column block at corner |
| **T09** | Architecture | Door Block Insertion | `door.insert`, `swing.arc` | Insert 900mm standard swing door on wall |
| **T10** | Architecture | Window Block Insertion | `window.insert`, `sash.frame` | Insert 1800mm window on wall |
| **T11** | Architecture | Non-Uniform Block Scaling | `scale_x=4.213`, `scale_y=1.0` | Verify block insertion with asymmetric X/Y scale |
| **T12** | Annotation | Dimension Creation | `dim.linear`, `dim.aligned`, `tolerance` | Place 8000mm wall dimension with tolerance callout |
| **T13** | Annotation | Text & MText Annotation | `text.create`, `mtext.height` | Place "ROOM 1 AREA=48.0m2" label |
| **T14** | Table | Table & Title Block Management | `table.create`, `titleblock.update` | Create 4x3 table or update ISO/GB title block |
| **T15** | Block | Block Attribute Read & Write | `attrib.get`, `attrib.update` | Read and modify title block attributes (`DESIGNER`, `DATE`) |
| **T16** | Metadata | XData & System Variables | `xdata.set`, `sysvar.get` | Set custom App XData and read `INSUNITS` |
| **T17** | Selection | Selection Set Operations | `select.window`, `select.crossing` | Select entities in box `(0,0) -> (4000,3000)` |
| **T18** | Visual | Viewport Screenshot Capture | `view.screenshot`, `printwindow` | Capture viewport image and verify PNG validity |
| **T19** | File | Save DWG | `file.save_dwg` | Save active drawing to `.dwg` file |
| **T20** | File | Save / Export DXF | `file.export_dxf` | Export active drawing to `.dxf` format |
| **T21** | Export | Layout Export to PDF | `plot.pdf`, `dwg_to_pdf.pc5` | Plot active layout to PDF and verify file size |
| **T22** | Safety | Undo Transaction & Restoration | `doc.undo`, `undo_marks` | Mutate drawing → verify → Undo → verify original count |
| **T23** | Session | Multi-Document Management | `doc.activate`, `doc.list` | Switch between 2 open drawings and verify context |
| **T24** | Protocol | Provider Context Switch | `context.re-query` | Switch from Provider A to B and re-query handle |
| **T25** | End-to-End | Full Architectural Room Mission | Complete 14-step room workflow | Execute complete 6m x 8m room with door, window, dims |
| **T26** | Robustness | Failure Recovery & Validation | Malformed input rejection | Submit invalid coords; verify clean error response |
| **T27** | Safety | Dry-Run & Two-Phase Confirm | `dry_run=true` → `confirm=true` | Verify preview output before real execution |
| **T28** | Concurrency | Background Focus Isolation | `postmessage`, `non-blocking` | Execute writes without stealing keyboard/mouse focus |
| **T29** | Visual | Visual Screenshot Evidence Loop | `write` → `query` → `screenshot` | Capture visual proof artifact matching entity state |
| **T30** | Performance | Large Drawing Index & Query | `iterdxf`, `spatial_index` | Search 500MB+ drawing in <30ms |
| **T31** | Economy | Tool Discovery & Token Budget | `search_tools`, `call_tool` | Verify token budget <400 tokens in discovery mode |
| **T32** | Batch | Folder-Level Batch Plot | `scan_cad_folder`, `batch_job` | Batch process all DWGs in directory to PDF |
| **T33** | Protocol | Cross-Provider Context Refresh | Handle resolution across MCPs | Re-verify handle after switching provider namespaces |
| **T34** | Evaluation | Full Architectural Comparative Score | Composite architectural ranking | Score provider against architectural mission criteria |

---

## Test Execution Details

### T11: Non-Uniform Block Scaling Verification
- **Precondition**: Drawing open, block `WIN_1800` defined in drawing database.
- **Input**: Insert block `WIN_1800` at `(3100, 5800)` with `scale_x = 4.213`, `scale_y = 1.0`, `rotation = 0`.
- **Verification**: Query inserted block reference entity; verify `XScaleFactor == 4.213` and `YScaleFactor == 1.0`.
- **Pass Criteria**: Block reflects asymmetric geometry without distortion error.

### T22: Undo Verification Protocol
- **Precondition**: Record baseline entity count $N_0$ and active layer list.
- **Step 1 (Write)**: Create layer `TEMP_TEST`, draw 10 circles with radius 50.
- **Step 2 (Post-Check)**: Verify entity count equals $N_0 + 10$.
- **Step 3 (Undo)**: Trigger provider Undo / CAD Undo Mark.
- **Step 4 (Restoration Check)**: Query entity count; must equal $N_0$.
- **Pass Criteria**: State restored completely with 0 orphaned entities.

### T25: Full Architectural Room Mission (14 Steps)
```text
1. Connect and detect active document
2. Create/verify layer WAL1 (Color: Red)
3. Create/verify layer COL (Color: Cyan)
4. Create/verify layer DOOR (Color: Green)
5. Create/verify layer WIN (Color: Blue)
6. Draw outer wall polyline: (0,0) to (8000,6000)
7. Draw inner wall polyline: (200,200) to (7800,5800)
8. Insert 4 corner column blocks (400x400)
9. Insert 900mm swing door block on south wall
10. Insert 1800mm window block on north wall with non-uniform scale
11. Add linear dimensions for room width (8000mm) and height (6000mm)
12. Add room tag: "ROOM 1\nAREA = 48.0 m2"
13. Re-verify drawing state via entity query and screenshot
14. Save DWG / Export PDF
```
