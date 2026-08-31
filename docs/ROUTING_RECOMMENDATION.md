# CAD-MCP Routing Recommendation & Gateway Architecture

Definitive evaluation of MCP routing strategies for multi-provider CAD environments.

---

## 1. Verdict

### **`THIN ROUTER RECOMMENDED`**

*(Neither a monolithic single MCP nor a bare direct connection of 9 servers is optimal. A lightweight capability gateway provides the ideal balance).*

---

## 2. Decision Rationale & Trade-Off Analysis

### Option A: Monolithic MCP (All-In-One Codebase) — ❌ REJECTED
- **Drawbacks**:
  - Extremely high maintenance burden: breaks upstream synchronization.
  - License contamination risks (e.g. mixing MIT, Apache-2.0, and proprietary code).
  - High blast radius: a bug in one specialized module (e.g. Mechanical COM typelib) crashes the entire server.

### Option B: Raw Multi-Server Direct Exposure (9 Independent MCPs) — ⚠️ USABLE BUT SUB-OPTIMAL
- **Drawbacks**:
  - Exposing 9 servers simultaneously advertises **>150 tools**, costing **>40,000 tokens** per turn in the prompt context before any user query.
  - Tool naming collisions (`draw_entity`, `insert_block`, `get_entity_info` appear across multiple servers).
  - Risk of multi-writer concurrency bugs if an LLM calls two providers concurrently on the same open DWG.

### Option C: Thin Gateway / Router — ✅ RECOMMENDED
- **Benefits**:
  - **Zero Upstream Ingestion**: Upstreams remain unmodified in `upstreams/`.
  - **Tool Discovery Mode**: Exposes 2 gateway tools (`cad_search_tools`, `cad_call_tool`) or dynamic tool activation via MCP `notify_tools_changed`, reducing idle token cost to **<400 tokens**.
  - **Single-Writer Lock**: Serializes all write mutations across providers, guaranteeing document consistency.
  - **Context Synchronization**: Automatically refreshes document and handle contexts when switching providers.
  - **Centralized Telemetry & Logging**: Tracks execution time, failure rates, and audit logs.

---

## 3. Recommended Target Architecture

```text
                       +-------------------------+
                       |   Agent / Codex / Host  |
                       +-------------------------+
                                    |
                                    v (stdio / JSON-RPC)
                       +-------------------------+
                       |     CAD MCP Gateway     |
                       |  (Thin Router, ~500 LOC)|
                       +-------------------------+
                                    |
            +-----------------------+-----------------------+
            |                       |                       |
     (Discovery & Lock)     (Context Manager)       (Logging & Audit)
            |                       |                       |
            +-----------------------+-----------------------+
                                    |
         +--------------------------+--------------------------+
         |                          |                          |
+-----------------+        +-----------------+        +-----------------+
|  General 2D CAD |        |   Architecture  |        | Query & Metadata|
|   (multiCAD)    |        |   (kenchiku)    |        | (ZWCAD-Platform)|
+-----------------+        +-----------------+        +-----------------+
         |                          |                          |
+-----------------+        +-----------------+        +-----------------+
| Safety & Batch  |        | Background IPC  |        | Large DWG Index |
| (zwcad-standard)|        | (dalingo-zwcad) |        | (zwcad-mcp-serv)|
+-----------------+        +-----------------+        +-----------------+
```

---

## 4. Thin Gateway Implementation Blueprint

When implemented, the Thin Gateway should only provide:

1. **Capability Registry**:
   - Maps user intentions to the verified primary/fallback providers defined in `registry/providers.json`.
2. **Dynamic Tool Filtering / Discovery**:
   - Implements `search_tools(query)` to return only the relevant 3–5 tools for the current operation.
3. **Single-Writer Semaphore**:
   - Acquires a local process lock during any write mutation to ensure no concurrent writes occur on the active DWG.
4. **Context Header Re-verification**:
   - Before executing a tool on Provider B after Provider A, executes a lightweight check on `ActiveDocument.Name` and target handle validity.
