# CAD-MCP: Independent Multi-Provider Evaluation & Verification Framework for ZWCAD

**CAD-MCP** is an open evaluation framework, benchmark test harness, and architectural routing guideline for CAD Model Context Protocol (MCP) servers on **ZWCAD 2026**.

Rather than forcibly merging disparate CAD MCPs into a fragile monolithic codebase, **CAD-MCP maintains each upstream MCP in its native, independent repository form**, documents proposed standardized CAD tests (T01–T34). A measured provider comparison is not implemented.

---

## Key Principles

1. **Independent Upstreams**: Each MCP provider lives in its own directory (`C:\cad-mcp\upstreams\<provider>`), preserving upstream git tracking and clean licensing.
2. **Evidence First**: Historical scores are synthetic and cannot establish provider quality.
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

## Evidence status

The old provider PASS rates, scores, latencies and rankings were generated from hardcoded assumptions, not candidate MCP calls. They are withdrawn as empirical claims. Checked-in results are **LEGACY_SYNTHETIC**, retained only for historical inspection. They must not be imported as measured evidence or used to select an executor.

`run_benchmarks.py` generates synthetic examples under `results/synthetic/` without connecting to CAD. `score_results.py --measured` rejects export until a real provider runner and independently verified fixture evidence exist. CI checks code and headless fixture generation; it does not validate a CAD host.

Registry URLs, pins, declared capabilities and transport candidates remain useful discovery metadata; licenses and pins require independent verification.

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

### 3. Generate synthetic test examples (no CAD connection) (T01–T34)
```powershell
python .\scripts\run_benchmarks.py
```

### 4. Inspect evidence status
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
