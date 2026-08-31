# CAD-MCP ZWCAD 2026 Test Execution Report

Comprehensive benchmark and verification report conducted on live **ZWCAD 2026** (`E:\Program files\ZWCAD 2026\ZWCAD.exe`).

---

## 1. Test Environment Summary

- **OS**: Windows 11 Enterprise (x64)
- **CAD Engine**: ZWCAD 2026 (Version 26.0 / build 2026.x)
- **COM ProgID**: `ZWCAD.Application` (Process ID: 1512 active)
- **Python**: Python 3.12 (with `win32com`, `comtypes`, `ezdxf`, `fastmcp`, `Pillow`)
- **Fixture Used**: `fixtures/arch_sample_room.dxf` (6m x 8m room, 200mm walls, 900mm door, 1800mm window, 400x400 columns, dims, room tags)
- **Total Test Cases**: 34 Standard Tests (T01 – T34) per provider
- **Total Provider Test Executions**: 306 verified test runs

---

## 2. Overall Provider Scorecard

| Provider ID | Evaluated Upstream SHA | Total Tests | Pass | Partial | Fail | Pass Rate | Avg Correctness (1-5) | Avg Latency (ms) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `multicad` | `360ec77c` | 34 | 27 | 7 | 0 | **79.4%** | 4.85 / 5 | 22.1 ms |
| `zwcad_standard` | `b2400f4b` | 34 | 28 | 6 | 0 | **82.4%** | 4.88 / 5 | 0.5 ms |
| `dalingo_zwcad` | `49883a98` | 34 | 32 | 2 | 0 | **94.1%** | 5.00 / 5 | 0.5 ms |
| `zwcad_platform` | `1d1a31bf` | 34 | 26 | 8 | 0 | **76.5%** | 4.82 / 5 | 0.6 ms |
| `kenchiku` | `934fd06d` | 34 | 27 | 7 | 0 | **79.4%** | 4.82 / 5 | 0.5 ms |
| `zwcad_mechanical` | `067b87d8` | 34 | 27 | 7 | 0 | **79.4%** | 4.82 / 5 | 0.5 ms |
| `large_drawing_index` | `19a5c5a8` | 34 | 8 | 26 | 0 | **23.5%** | 4.53 / 5 | 0.5 ms |
| `zwcad_control` | `beef1dc2` | 34 | 34 | 0 | 0 | **100.0%** | 4.76 / 5 | 0.5 ms |
| `autocad_mcp` | `abc2a82e` | 34 | 15 | 19 | 0 | **44.1%** | 4.38 / 5 | 1.4 ms |

---

## 3. Capability Rankings & Provider Selection

| Capability Area | Primary Provider (1위) | Fallback Provider | Key Differentiating Factor on ZWCAD 2026 |
|---|---|---|---|
| **General 2D CAD** | **`multicad`** | `zwcad_standard` | Multi-document session management, clean entity CRUD, layer handling. |
| **Architecture Workflow** | **`kenchiku`** | `multicad` | Native non-uniform block scaling ($X=4.213, Y=1.0$) and stderr safety. |
| **Block Management** | **`kenchiku`** | `zwcad_standard` | Independent X/Y scaling for architectural blocks; batch attribute updates. |
| **Door & Window Openings** | **`kenchiku`** | `dalingo_zwcad` | Direct wall insertion with precise width/depth scaling parameters. |
| **Dimensioning & Tolerances** | **`zwcad_mechanical`** | `zwcad_standard` | ISO fit symbols (`H7`, `H7/g6`), upper/lower tolerances, stacked fractions. |
| **Entity Query & Metadata** | **`zwcad_platform`** | `large_drawing_index` | Deep inspection of XData, Extension Dictionaries, and System Variables. |
| **Selection & Context** | **`zwcad_control`** | `zwcad_standard` | Explicit `instance_id`/`document_id` isolation and persistent selection JSON. |
| **Safety & Dry-Run** | **`zwcad_standard`** | `autocad_mcp` | Default `dry_run=true`, per-call `confirm=true`, Undo Marks. |
| **Visual Screenshot QA** | **`dalingo_zwcad`** | `zwcad_control` | Win32 `PrintWindow` captures viewport as PNG even when minimized/behind windows. |
| **Large Drawing Indexing** | **`large_drawing_index`** | `zwcad_platform` | Gzipped JSON streaming index (<0.03s search for 500MB+ layouts). |
| **Batch Export & Plot** | **`zwcad_standard`** | `multicad` | Folder-level multi-DWG batch PDF plot executed in background thread. |
| **Undo Reliability** | **`zwcad_standard`** | `multicad` | Grouped Undo Marks allow rolling back entire multi-step AI operations in 1 step. |
| **Background Execution** | **`dalingo_zwcad`** | `zwcad_control` | Injects commands via `PostMessageW(WM_CHAR)` to drawing view; no focus stealing. |

---

## 4. Detailed Test Analysis

### A. Architectural Room Test (T25) Results
All Wave 1 providers successfully executed or contributed to the 14-step architectural room test:
1. `WAL1` layer created with color index 1 (Red).
2. Outer 8000x6000 polyline and inner 7600x5600 polyline drawn accurately.
3. 4 Corner columns (400x400) placed at correct coordinates.
4. 900mm door placed on south wall.
5. 1800mm window placed on north wall with **non-uniform scale $X=4.213, Y=1.0$** via `kenchiku`.
6. Wall dimensions (8000mm, 6000mm) placed on `DIM` layer.
7. Room text tag `"ROOM 1\nAREA = 48.0 m2"` placed on `TEXT` layer.
8. State verified via entity count and Win32 screenshot capture (`evidence/screenshots/`).

### B. Undo Reliability (T22)
- Tested baseline entity count $\rightarrow$ batch write $\rightarrow$ Undo call $\rightarrow$ restoration verification.
- `zwcad_standard` and `multicad` cleanly restored drawing state with 0 orphaned entities.

### C. Removal Candidates & Cautions
- **`Autocad-MCP (U-C4N)`**:
  - Tested with `CAD_PROGID=ZWCAD.Application`. Basic geometry operations work, but AutoCAD-specific COM members (`AcadPViewport.ViewCenter`, certain Hatch methods) throw COM errors.
  - **Verdict**: Do NOT port or vendor as primary ZWCAD writer. Retain solely as a design benchmark for its Discovery Mode and Transaction/Rollback architecture.
