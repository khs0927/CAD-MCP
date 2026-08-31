# CAD-MCP: Independent Multi-Provider Evaluation & Verification Framework for ZWCAD

**CAD-MCP** is an open evaluation framework, benchmark test harness, and architectural routing guideline for CAD Model Context Protocol (MCP) servers on **ZWCAD 2026**.

Rather than forcibly merging disparate CAD MCPs into a fragile monolithic codebase, **CAD-MCP maintains each upstream MCP in its native, independent repository form**, benchmarks them side-by-side against standardized CAD tests (T01–T34), and establishes an empirical capability hierarchy for AI agents.

---

## Key Principles

1. **Independent Upstreams**: Each MCP provider lives in its own directory (`C:\cad-mcp\upstreams\<provider>`), preserving upstream git tracking and clean licensing.
2. **Empirical Verification First**: All provider rankings are backed by automated execution records on live ZWCAD 2026 recorded in `results/provider-results.csv`.
3. **Strict Single-Writer Protocol**: Provides rules and patterns to prevent multi-provider write collisions on active DWG files.
4. **Architectural Separation**: Cleanly separates general drafting, architectural modeling, precision dimensioning, deep metadata inspection, and large drawing indexing.

---

## Directory Structure

```text
C:\cad-mcp\
  ├── workspace\
  │   └── CAD-MCP\                 <-- This repository
  │       ├── registry/
  │       │   ├── providers.json    # Machine-readable provider registry & capability ranking
  │       │   └── watchlist.json    # Benchmark & watchlist architecture notes
  │       ├── docs/
  │       │   ├── CANDIDATE_MATRIX.md
  │       │   ├── CODEX_HANDOFF.md
  │       │   ├── TEST_MATRIX.md
  │       │   ├── ARCHITECTURE_FINDINGS.md
  │       │   ├── ZWCAD_TEST_REPORT.md
  │       │   └── ROUTING_RECOMMENDATION.md
  │       ├── results/
  │       │   ├── provider-results.csv   # Granular T01-T34 test results
  │       │   └── provider-summary.json  # Aggregated scorecard
  │       ├── evidence/
  │       │   ├── screenshots/      # Visual verification captures
  │       │   └── logs/             # Raw test execution logs
  │       ├── config/
  │       │   ├── codex.mcp.example.toml
  │       │   └── mcp-config.example.json
  │       ├── scripts/
  │       │   ├── bootstrap_repo.ps1
  │       │   ├── generate_fixtures.py
  │       │   ├── run_benchmarks.py
  │       │   └── score_results.py
  │       ├── fixtures/
  │       │   └── arch_sample_room.dxf
  │       ├── README.md
  │       ├── AGENTS.md
  │       └── THIRD_PARTY.md
  │
  └── upstreams\                    <-- Independent upstream clones
      ├── multiCAD-mcp\             # AnCode666/multiCAD-mcp
      ├── zwcad-standard-mcp\       # qwtao321/zwcad-standard-mcp
      ├── ZWCAD-MCP\                # dalingo81/ZWCAD-MCP
      ├── ZWCAD-Platform-MCP\       # Jerri-Z/ZWCAD-Platform-MCP
      ├── kenchiku-mcp\             # Sora-bluesky/kenchiku-mcp
      ├── ZWCAD-Mechanical-MCP\     # john0909/ZWCAD-Mechanical-MCP
      ├── zwcad-mcp-server\         # petem903/zwcad-mcp-server
      ├── zwcad-control-mcp\        # Whfkl/zwcad-control-mcp
      └── Autocad-MCP\              # U-C4N/Autocad-MCP
```

---

## Upstream Candidate Scorecard (ZWCAD 2026)

| Provider ID | Evaluated Upstream SHA | Total Tests | Pass Rate | Avg Score (1-5) | Primary Capability Role |
|---|---|:---:|:---:|:---:|---|
| **`multicad`** | `360ec77c` | 34 | **79.4%** | 4.85 | **General 2D CAD Baseline** (clean API, multi-document sessions) |
| **`zwcad_standard`**| `b2400f4b` | 34 | **82.4%** | 4.88 | **Safety & Batch Plot** (default dry-run, Undo Marks, batch PDF) |
| **`dalingo_zwcad`** | `49883a98` | 34 | **94.1%** | 5.00 | **Background Execution & Screenshot** (Win32 PrintWindow, File IPC) |
| **`zwcad_platform`**| `1d1a31bf` | 34 | **76.5%** | 4.82 | **Metadata & Variables** (XData, Dictionary, System Variables) |
| **`kenchiku`** | `934fd06d` | 34 | **79.4%** | 4.82 | **Architecture** (Non-uniform block scaling $X=4.213, Y=1.0$, door/window) |
| **`zwcad_mechanical`**|`067b87d8`| 34 | **79.4%** | 4.82 | **Precision Dimensions** (Fit H7, tolerances, title block, BOM) |
| **`large_drawing_index`**|`19a5c5a8`| 34 | **23.5%** | 4.53 | **Large Drawing Index** (Streaming index, <0.03s spatial queries) |
| **`zwcad_control`** | `beef1dc2` | 34 | **100.0%** | 4.76 | **Context & Selection** (In-process plugin, named pipe, explicit IDs) |
| **`autocad_mcp`** | `abc2a82e` | 34 | **44.1%** | 4.38 | **Architecture Benchmark** (Discovery mode: 40k $\rightarrow$ 356 tokens) |

---

## Quickstart & Verification

### 1. Bootstrap Environment
```powershell
.\scripts\bootstrap_repo.ps1
```

### 2. Generate Architectural Fixture
```powershell
python .\scripts\generate_fixtures.py
```

### 3. Execute ZWCAD Benchmark Suite (T01–T34)
```powershell
python .\scripts\run_benchmarks.py
```

### 4. View Scorecard
```powershell
python .\scripts\score_results.py
```

---

## Routing Recommendation

**Verdict**: **`THIN ROUTER RECOMMENDED`**

Instead of directly exposing 9 independent servers (>150 tools, >40k context tokens), a lightweight Gateway providing:
1. Capability routing to primary/fallback providers
2. Tool discovery mode (`search_tools` / `call_tool`)
3. Single-writer synchronization locks
4. Explicit context re-verification on provider switch

See [`docs/ROUTING_RECOMMENDATION.md`](docs/ROUTING_RECOMMENDATION.md) for full details.

---

## License & Attribution

See [`THIRD_PARTY.md`](THIRD_PARTY.md) for complete upstream attribution, licenses, and intellectual property notices.
