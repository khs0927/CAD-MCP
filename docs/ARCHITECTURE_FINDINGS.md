# CAD-MCP Architectural Findings & System Insights

Deep architectural evaluation of CAD MCP architectures, IPC mechanisms, discovery protocols, and safety models across all tested providers and benchmark systems.

---

## 1. IPC & Execution Architecture Comparison

| Architecture Model | Representative Providers | Latency | Focus Stealing | Native Object Access | Crash Resilience | Setup Complexity |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **In-Process Plugin (.NET / C#)** | `zwcad_control`, `codesknight` | **<0.1 ms** | None | 100% (Direct Database & Editor API) | Low (Crashes CAD process on fatal bug) | High (`NETLOAD` required) |
| **ActiveX / COM Automation** | `multicad`, `zwcad_standard`, `zwcad_platform`, `kenchiku`, `zwcad_mechanical` | **~0.5 - 2 ms** | Occasional | ~90% (ActiveX object model) | High (Separate process, survives CAD disconnect) | **Zero (Native Windows COM)** |
| **File IPC + Window PostMessage** | `dalingo_zwcad` | **~2 - 5 ms** | **Zero (Completely non-blocking)** | 100% (Via AutoLISP / Visual LISP) | High (Separate process + JSON handshake) | Low (Load LISP via `APPLOAD`) |
| **Streaming Index + DXF Bridge** | `large_drawing_index` | **<0.03 ms (Read)** / ~3s (Write) | None | 100% DXF (Stripped attributes) | Maximum (Headless, no CAD process needed) | Low (Pure Python `ezdxf`) |

### Key Takeaways:
1. **COM Automation is the Best General Baseline**:
   - Zero installation overhead for users on Windows.
   - Fast enough (<1ms per call) for interactive AI drawing tasks.
2. **File IPC is the Ultimate Background Operator**:
   - `dalingo_zwcad` demonstrates that injecting `(c:zwmcp-dispatch)` via `PostMessageW(WM_CHAR)` to the drawing window enables true background AI drawing without stealing user keyboard focus.
3. **In-Process Plugins Provide Ultimate Context Stability**:
   - `zwcad_control` provides explicit `instance_id` and `document_id` tracking, ensuring an Agent never writes to the wrong document when multiple CAD windows are open.

---

## 2. Tool Discovery & Token Budget Optimization

From the deep analysis of `Autocad-MCP (U-C4N)`:
- **The Token Cost Problem**: Exposing 150+ granular CAD tools consumes **40,305 tokens** on every model prompt turn before the user even types a request.
- **The Solution (Discovery Mode)**:
  - Expose only 2 meta-tools: `search_tools` and `call_tool`.
  - Idle token cost drops from **40,305 to 356 tokens (99.1% reduction)**.
  - An authored semantic corpus of AutoCAD/ZWCAD commands and synonyms (e.g. `FILLET`, `BPOLY`, `QSELECT`, `CHSPACE`) enables exact top-1 search ranking.
- **Application to CAD-MCP**:
  - For thin routers or gateways, implementing `search_tools` with dynamic capability matching prevents context window exhaustion.

---

## 3. Safety Models & Transactional Rollback

| Safety Pattern | Source | Mechanism | Practical Benefit |
|---|---|---|---|
| **Two-Phase Dry-Run** | `zwcad_standard` | Write tools execute with `dry_run=true` returning preview JSON; execution requires `confirm=true`. | Prevents unintended mass modifications by LLMs. |
| **CAD Undo Marks** | `zwcad_standard` | Groups batch operations into single named Undo groups (`_.UNDO _BEGIN` ... `_.UNDO _END`). | Allows user to roll back 50 AI operations in a single `Ctrl+Z`. |
| **Timestamped Backups** | `large_drawing_index` | Saves `_backups/<timestamp>_<file>.dxf` before any destructive mutation; restores via `undo_last_save`. | Guarantees zero data loss on large plant layouts. |
| **Quality Loop** | `autocad_mcp` | `preflight` → `plan` → `critique` → `refine` → `deliver`. | Automated rule-checking (0 critique issues) before final output delivery. |

---

## 4. Architectural Geometry & Non-Uniform Scaling

From `kenchiku-mcp`:
- Standard CAD COM implementations expose only uniform `scale` (e.g., `1.5`), causing doors and windows to scale proportionally in both width and depth.
- Architectural openings require independent width and depth scaling (e.g. 1800mm opening with 200mm wall thickness: $X=4.213, Y=1.0$).
- `kenchiku` solves this cleanly via string notation (`"4.213x1.0"`) and direct COM `XScaleFactor` / `YScaleFactor` assignment.
- **Logging Guard**: `kenchiku` redirects stdout logging to stderr, preventing accidental corruption of stdio JSON-RPC streams.

---

## 5. Large Drawing Streaming Index Architecture

From `petem903/zwcad-mcp-server`:
- Traditional CAD COM traversals hang or take minutes when querying 500MB+ industrial layout drawings with 600,000+ entities.
- **Streaming Iterator Solution**:
  - Iterates entities directly from DXF streams (`ezdxf.addons.iterdxf`) without loading full DOM into memory.
  - Builds a compact spatial index serialized as gzipped JSON (~63 KB).
  - Spatial radius queries (`blocks_near`), K-nearest neighbors (`nearest_blocks`), and text lookups return in **<0.03 seconds**.

---

## 6. Visual Verification Models

| Provider | Method | Latency | Quality | Background Support |
|---|---|:---:|:---:|:---:|
| `dalingo_zwcad` | Win32 `PrintWindow` API | **~30 ms** | High (Exact CAD Viewport) | ✅ Yes (Minimized / Occluded) |
| `large_drawing_index` | Matplotlib render of DXF | ~200 ms | Medium (Vector wireframe) | ✅ Yes (Headless, no CAD needed) |
| `autocad_mcp` | Pillow Window Grab | ~50 ms | High | ⚠️ Partial (Requires visible window) |

**Recommendation for CAD Agents**:
Pair structured entity verification (`query_entities`) with `dalingo_zwcad.view(operation="get_screenshot")` for deterministic closed-loop visual QA.
