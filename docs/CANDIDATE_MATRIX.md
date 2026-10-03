> Evidence correction: historical PASS rates, scores, rankings and performance claims in this document are unverified legacy assumptions (LEGACY_SYNTHETIC). They are not candidate MCP execution evidence. Do not use them to authorize execution.

# CAD-MCP Candidate Matrix

Comprehensive technical matrix comparing all 9 candidate CAD MCP servers and 8 benchmark architectures evaluated for ZWCAD integration.

---

## 1. Candidate Comparison Matrix

| Provider ID | Upstream Repository | Wave | Architecture Type | IPC / Transport | ZWCAD Native Support | Tool Count | Safety Model | Visual Verification |
|---|---|:---:|---|---|:---:|:---:|---|---|
| `multicad` | AnCode666/multiCAD-mcp | 1 | COM Direct (pywin32) | stdio | ✅ Native | 7 (Grouped) | Implicit | Web Dashboard (Port 8888) |
| `zwcad_standard` | qwtao321/zwcad-standard-mcp | 1 | COM Transactional | stdio | ✅ Native (Std) | 37 | Default `dry_run=true`, per-call `confirm=true`, Undo Marks | PDF Export & Validation |
| `dalingo_zwcad` | dalingo81/ZWCAD-MCP | 1 | File IPC + AutoLISP Dispatch | stdio + Win32 WM_CHAR | ✅ Native (Std/Pro) | 8 (Grouped) | Post-validation + ezdxf fallback | Win32 `PrintWindow` PNG |
| `zwcad_platform` | Jerri-Z/ZWCAD-Platform-MCP | 1 | COM comtypes Interface | stdio | ✅ Native | 26 | Direct write | COM View Extents |
| `kenchiku` | Sora-bluesky/kenchiku-mcp | 1 | COM Architectural | stdio (stderr safe) | ✅ Native | 7 (Grouped) | Direct write | Web Viewer |
| `zwcad_mechanical` | john0909/ZWCAD-Mechanical-MCP | 2 | COM Mechanical (ZwmToolKit) | stdio | ✅ Native (Mech) | 37 | Diagnostics probe | COM View Extents |
| `large_drawing_index` | petem903/zwcad-mcp-server | 2 | Streaming Index (ezdxf) + COM Bridges | stdio | ✅ Via Bridge | 35 | Auto-backup DXF + Undo restore | Matplotlib Headless PNG |
| `zwcad_control` | Whfkl/zwcad-control-mcp | 3 | In-Process .NET Plugin | Named Pipe | ✅ Native | 5 | Context check (`instance_id`) | Selection/Window PNG Capture |
| `autocad_mcp` | U-C4N/Autocad-MCP | 3 | Dual Engine (COM + ezdxf) | stdio / HTTP | ⚠️ Partial (`CAD_PROGID`) | 154 (Lean: 47, Disc: 2) | Quality Loop (Preflight → Plan → Critique → Deliver) | Matplotlib / Pillow Window Capture |

---

## 2. In-Depth Candidate Profiles

### A. `multicad` (AnCode666/multiCAD-mcp)
- **Role**: General 2D CAD Baseline & Multi-Document Operations.
- **Strengths**:
  - Extremely clean Python mixin architecture (`drawing`, `entity`, `layer`, `block`, `export`, `session`).
  - Automatic active document detection and multi-document switching (`manage_session`).
  - Built-in web dashboard on port 8888.
- **Weaknesses**:
  - Tools are coarsely aggregated into 7 meta-tools, making fine-grained argument validation heavier for small LLMs.
  - Lacks non-uniform block scaling (only single float `scale` supported).
  - No built-in dry-run or transaction guardrails.

### B. `zwcad_standard` (qwtao321/zwcad-standard-mcp)
- **Role**: Standard Drawing Safety, Attribute Blocks, and Batch Plotting.
- **Strengths**:
  - **Best-in-class safety model**: All write tools default to `dry_run=true`, requiring explicit `confirm=true` per invocation. Deletion requires `second_confirm=true`.
  - Groups batch mutations into named CAD **Undo Marks** for single-step user rollback.
  - Full folder-level batch PDF printing (`scan_cad_folder` → `create_batch_job` → `get_batch_job_status`).
  - Comprehensive title block attribute querying and updating.
- **Weaknesses**:
  - Lacks direct Win32 viewport screenshot capture tool.
  - Queries iterate COM collections; large drawings (>50k entities) experience query latency.

### C. `dalingo_zwcad` (dalingo81/ZWCAD-MCP)
- **Role**: Background Execution, Visual Feedback, and AutoLISP Escape Hatch.
- **Strengths**:
  - **Non-blocking background execution**: Posts `(c:zwmcp-dispatch)` via `PostMessageW(WM_CHAR)` to the drawing view (`AfxFrameOrView`), allowing CAD operations without stealing user keyboard/mouse focus.
  - **Win32 `PrintWindow` capture**: Captures the exact CAD viewport as PNG even when minimized or occluded.
  - **`execute_lisp` escape hatch**: Allows dynamic execution of arbitrary AutoLISP / Visual LISP (`entmake`, `ssget`, `vlax-*`), providing 100% CAD feature coverage.
  - Dual-mode: Automatic fallback to headless `ezdxf` when CAD seat is closed.
- **Weaknesses**:
  - Requires loading `lisp-code/zwcad_mcp_dispatch.lsp` into CAD via `APPLOAD` or startup suite.
  - High-concurrency rapid calls rely on filesystem JSON polling.

### D. `zwcad_platform` (Jerri-Z/ZWCAD-Platform-MCP)
- **Role**: Deep Metadata, Dictionaries, XData, and System Variables.
- **Strengths**:
  - Native inspection and mutation of CAD Extension Dictionaries (`manage_dictionary`) and Entity XData (`manage_xdata`).
  - Read/write access to all ZWCAD system variables (`get_variable`, `set_variable`).
  - DXF-filtered dimension querying (`query_dimensions`), orders of magnitude faster than iterating full entity sets.
  - Basic 3D solid modeling tools (`box`, `cylinder`, `cone`, `sphere`).
- **Weaknesses**:
  - Requires `comtypes` and memory typelib generation.
  - Lacks visual screenshot capture tool.

### E. `kenchiku` (Sora-bluesky/kenchiku-mcp)
- **Role**: Architectural Modeling & Non-Uniform Block Scaling.
- **Strengths**:
  - **Native Non-Uniform Block Scaling**: Supports `scale_x` x `scale_y` (e.g. `4.213x1.0`), essential for parametric architectural doors and windows.
  - **Stderr Logging Safety**: Redirects logging to `stderr` to prevent JSON-RPC stdio protocol corruption.
  - Streamlined architectural tool parameters (door/window placement, wall polylines).
- **Weaknesses**:
  - Inherits multiCAD's aggregated 7-tool structure.
  - Does not support mechanical BOM or deep dictionary metadata.

### F. `zwcad_mechanical` (john0909/ZWCAD-Mechanical-MCP)
- **Role**: High-Precision Dimensions, Tolerances, Fit Symbols, and BOM.
- **Strengths**:
  - Unmatched dimensioning capabilities: fit symbols (`fit_symbol="H7"`), ISO 286 tolerances, stacked fractions, and prefix/suffix control.
  - Mechanical frame generation (`create_frame`), title blocks, and BOM partlist management (`manage_bom`).
  - Automatic 5-level fallback strategy for `ZwmToolKit.tlb` COM typelib loading.
- **Weaknesses**:
  - Advanced mechanical tools require ZWCAD Mechanical edition and loaded typelib.
  - Heavy specialized vocabulary tailored for manufacturing rather than building architecture.

### G. `large_drawing_index` (petem903/zwcad-mcp-server)
- **Role**: Massive Drawing Indexing, Spatial Search, and Headless Analysis.
- **Strengths**:
  - **Streaming Indexer**: Uses `ezdxf.addons.iterdxf` to index large drawings (500MB+, 600k+ entities) into compact gzipped JSON in one pass.
  - **Sub-30ms Read Queries**: Instant responses for text search, layer summaries, and spatial radius queries (`blocks_near`, `whats_at`, `nearest_blocks`).
  - Non-destructive DXF editing copy with automatic timestamped backup and rollback (`undo_last_save`).
  - Matplotlib headless rendering preview.
- **Weaknesses**:
  - Write mutations trigger full DXF reload; fine-grained interactive entity manipulation is slower than direct COM.
  - Block attributes are stripped during standard DWG→DXF conversion.

### H. `zwcad_control` (Whfkl/zwcad-control-mcp)
- **Role**: In-Process CAD Context, Selection Persistence, and C# / LISP Scripting.
- **Strengths**:
  - **Explicit Context Isolation**: Strictly passes `instance_id` and `document_id` to prevent modifying unintended open drawings.
  - **Persistent Selection Sets**: Saves user-selected or preselected entities to disk as JSON with opaque `selection_id`.
  - In-process C# script compilation (`run_csharp`) and LISP execution (`run_lisp`) directly inside CAD command context via local named pipe.
- **Weaknesses**:
  - Unlicensed / proprietary repository (architectural reference only, not vendored).
  - Requires loading `Zwcad.ControlMcp.Plugin.dll` via `NETLOAD`.

### I. `autocad_mcp` (U-C4N/Autocad-MCP)
- **Role**: Benchmark Reference for Tool Discovery, Token Budgeting, and Quality Loops.
- **Strengths**:
  - **Tool Discovery Mode**: Reduces context token budget from **40,305 tokens (149 tools)** down to **356 tokens (2 tools: `search_tools` + `call_tool`)**.
  - **Quality Delivery Loop**: `drawing_preflight` → `drawing_plan` → `drawing_critique` → `drawing_refine` → `drawing_deliver` with SHA-256 manifest.
  - Full transaction and rollback architecture across COM and ezdxf.
- **Weaknesses**:
  - Built specifically for AutoCAD ActiveX API; running against `CAD_PROGID=ZWCAD.Application` encounters occasional property discrepancies (e.g. `AcadPViewport.ViewCenter`).
  - Not recommended as primary ZWCAD writer, but serves as the premier architectural reference.
