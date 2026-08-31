# Third-Party Notices and Upstream Attribution

The `CAD-MCP` project coordinates, benchmarks, and provides routing guidelines for independent Model Context Protocol (MCP) servers operating on ZWCAD and related CAD engines.

In accordance with our architectural and licensing principles:
- **No upstream source code is vendored or monolithically copied into the CAD-MCP workspace repository.**
- Each upstream provider is maintained in an independent clone within `C:\cad-mcp\upstreams\<provider-name>\`.
- Open-source projects (MIT, Apache-2.0) are utilized according to their license terms.
- Projects without explicit open-source licenses are **strictly referenced for architecture, interface patterns, and idea analysis only**; no proprietary code is redistributed.

---

## Upstream Candidate Repositories

| ID | Repository | Upstream URL | Evaluated Commit SHA | License | Architectural Status |
|---|---|---|---|---|---|
| `multicad` | AnCode666/multiCAD-mcp | https://github.com/AnCode666/multiCAD-mcp | `360ec77c970ec95a962bd4d0a3238715ee78dd7c` | Apache-2.0 | Wave 1: General 2D CAD Baseline |
| `zwcad_standard` | qwtao321/zwcad-standard-mcp | https://github.com/qwtao321/zwcad-standard-mcp | `b2400f4b391cf6e6be0d1b84890859ac7c796646` | MIT | Wave 1: Safety & Dry-Run Lead |
| `dalingo_zwcad` | dalingo81/ZWCAD-MCP | https://github.com/dalingo81/ZWCAD-MCP | `49883a983e665900bbc37b9f200daf99144818e1` | Permissive Reference | Wave 1: Background File IPC & Visual Capture Lead |
| `zwcad_platform` | Jerri-Z/ZWCAD-Platform-MCP | https://github.com/Jerri-Z/ZWCAD-Platform-MCP | `1d1a31bf2f4a2bac6dec90ac210a5bde5087d430` | MIT | Wave 1: XData & System Variable Lead |
| `kenchiku` | Sora-bluesky/kenchiku-mcp | https://github.com/Sora-bluesky/kenchiku-mcp | `934fd06db220bfb5ca5ec3b964508715e1887c24` | Apache-2.0 | Wave 1: Architectural Non-Uniform Scaling Lead |
| `zwcad_mechanical` | john0909/ZWCAD-Mechanical-MCP | https://github.com/john0909/ZWCAD-Mechanical-MCP | `067b87d8704a1ed3b0a20ec4e02a59b468cbc4ff` | MIT | Wave 2: Precision Dimensions & BOM Lead |
| `large_drawing_index` | petem903/zwcad-mcp-server | https://github.com/petem903/zwcad-mcp-server | `19a5c5a8c879cf1525896dfbc08aa8e8bddc84ab` | MIT | Wave 2: Large DWG Index & Spatial Query Lead |
| `zwcad_control` | Whfkl/zwcad-control-mcp | https://github.com/Whfkl/zwcad-control-mcp | `beef1dc293738060f0fd3da284d2579666b078fd` | Unlicensed / All Rights Reserved | Wave 3: Architecture Reference (In-Process Plugin / Named Pipe) |
| `autocad_mcp` | U-C4N/Autocad-MCP | https://github.com/U-C4N/Autocad-MCP | `abc2a82e7128358b9e228a7d9442b37019aa3fe5` | MIT | Wave 3: Benchmark Reference (Tool Discovery & Quality Loop) |

---

## Benchmark & Watchlist Repositories (Architecture & Idea Reference)

The following public repositories were analyzed for design ideas, discovery models, and RPC architectures:

- **`bimwright/dwg-mcp`**: Rust/Python hybrid DWG parsing and deterministic layer taxonomy validation.
- **`codesknight/AutoCAD-MCP`**: ObjectARX native acceleration and memory buffer selection sets.
- **`bimwright/rvt-mcp`**: In-process Revit external event queues and semantic parameter extraction.
- **`Boti-Ormandi/archicad-mcp`**: Clean JSON-RPC over HTTP boundaries and parametric opening schemas.
- **`neka-nat/freecad-mcp`**: Dynamic SVG/PNG viewport rendering and OpenBIM/IFC integration.
- **`tanishqbhattad/rhino-mcp`**: RhinoCommon geometry validation and turntable rendering.
- **`Daviidro/ifcopenshell-mcp`**: OpenBIM IFC PropertySet/QuantitySet compliance verification.
- **`daobataotie/CAD-MCP`**: SQLite drawing state persistence and NLP intent routing.

---

## Intellectual Property & Clean-Room Policy

1. **Whfkl/zwcad-control-mcp**:
   - Because no explicit open-source license is granted, no source code, binaries, or compiled assets from this repository are redistributed within the `CAD-MCP` repository.
   - Conceptual elements—such as using an in-process .NET plugin with local named pipe IPC, tracking explicit CAD context (`instance_id`, `document_id`), and persisting selection sets to disk—are standard architectural patterns that may be independently authored if needed.

2. **Clean Separation**:
   - Any tools, scripts, or documentation in `CAD-MCP` are authored clean-room to serve as evaluation harnesses, configuration schemas, and routing protocols.
