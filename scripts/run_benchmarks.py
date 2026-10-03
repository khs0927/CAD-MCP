"""
CAD-MCP Automated Benchmark Runner & ZWCAD Test Harness
Generates LEGACY_SYNTHETIC examples from hardcoded provider/test assumptions.
Does not invoke candidate MCP providers; no output is measured evidence.
"""

import csv
import json
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

# Upstream Commit SHAs as recorded
UPSTREAM_SHAS = {
    "multicad": "360ec77c970ec95a962bd4d0a3238715ee78dd7c",
    "zwcad_standard": "b2400f4b391cf6e6be0d1b84890859ac7c796646",
    "dalingo_zwcad": "49883a983e665900bbc37b9f200daf99144818e1",
    "zwcad_platform": "1d1a31bf2f4a2bac6dec90ac210a5bde5087d430",
    "kenchiku": "934fd06db220bfb5ca5ec3b964508715e1887c24",
    "zwcad_mechanical": "067b87d8704a1ed3b0a20ec4e02a59b468cbc4ff",
    "large_drawing_index": "19a5c5a8c879cf1525896dfbc08aa8e8bddc84ab",
    "zwcad_control": "beef1dc293738060f0fd3da284d2579666b078fd",
    "autocad_mcp": "abc2a82e7128358b9e228a7d9442b37019aa3fe5"
}

PROVIDERS = [
    "multicad",
    "zwcad_standard",
    "dalingo_zwcad",
    "zwcad_platform",
    "kenchiku",
    "zwcad_mechanical",
    "large_drawing_index",
    "zwcad_control",
    "autocad_mcp"
]

TEST_DESCRIPTIONS = {
    "T01": "Active Document & Connection Verification",
    "T02": "Metadata Read (Layers, Blocks, Extents, Units)",
    "T03": "Entity Query (Count, Handle, Type Filtering)",
    "T04": "Property Read (Color, Layer, Coordinates, Area)",
    "T05": "Layer Create (WAL1, COL, DOOR, WIN, DIM, TEXT)",
    "T06": "Line & Polyline Draw (6m x 8m room boundaries)",
    "T07": "Modify & Transform (Move, Rotate, Scale, Copy)",
    "T08": "Block Insert (Standard Architectural Block)",
    "T09": "Door Block Insertion (900mm Swing Door)",
    "T10": "Window Block Insertion (1800mm Window)",
    "T11": "Non-Uniform Block Scale (X=4.213, Y=1.0)",
    "T12": "Dimension Creation (Linear, Aligned, Tolerance)",
    "T13": "Text & Annotation (MText, Labels, Placement)",
    "T14": "Table & Title Block Generation / Management",
    "T15": "Block Attribute Read & Update",
    "T16": "XData & System Variable Read/Write",
    "T17": "Selection Set Operation (Window/Crossing)",
    "T18": "Screenshot Capture & Viewport Inspection",
    "T19": "Save Document to DWG",
    "T20": "Save / Export Document to DXF",
    "T21": "Export Layout to PDF",
    "T22": "Undo Transaction & State Restoration Verification",
    "T23": "Multi-Document Management & Switching",
    "T24": "Provider Context Switch & Re-query Protocol",
    "T25": "Full Architectural Room Workflow End-to-End",
    "T26": "Failure Recovery & Fault Rejection",
    "T27": "Dry-Run & Two-Phase Confirmation Safety",
    "T28": "Background Execution Without Focus Stealing",
    "T29": "Visual Screenshot Evidence Verification",
    "T30": "Large Drawing Streaming Index & Spatial Query",
    "T31": "Discovery Mode & Tool Profile Token Budget",
    "T32": "Batch Folder Plot & Multi-Drawing Export",
    "T33": "Cross-Provider Entity Identifier Re-resolution",
    "T34": "Comprehensive Architectural Capability Evaluation"
}

class ZWCADTestHarness:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.results_dir = os.path.join(workspace_root, "results", "synthetic")
        self.evidence_dir = os.path.join(workspace_root, "evidence")
        self.screenshots_dir = os.path.join(self.evidence_dir, "screenshots")
        self.logs_dir = os.path.join(self.evidence_dir, "logs")
        
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        self.zwcad_app = None
        self.zwcad_doc = None
        self.zwcad_version = "ZWCAD 2026"
        # Synthetic generation must never attach to or mutate a CAD host.

    def _init_com(self):
        try:
            import win32com.client
            self.zwcad_app = win32com.client.Dispatch("ZWCAD.Application")
            if self.zwcad_app.Documents.Count == 0:
                self.zwcad_doc = self.zwcad_app.Documents.Add()
            else:
                self.zwcad_doc = self.zwcad_app.ActiveDocument
            self.zwcad_version = f"ZWCAD {self.zwcad_app.Version}"
            print(f"[COM] Successfully attached to {self.zwcad_app.Name} {self.zwcad_app.Version}")
        except Exception as e:
            print(f"[COM WARNING] Could not attach to live ZWCAD COM: {e}")
            self.zwcad_app = None
            self.zwcad_doc = None

    def capture_screenshot(self, filename: str) -> str:
        out_path = os.path.join(self.screenshots_dir, filename)
        try:
            from PIL import ImageGrab
            # Grab screenshot of full screen or active window
            im = ImageGrab.grab()
            im.save(out_path, "PNG")
            return out_path
        except Exception as e:
            # Create a placeholder evidence file if image grab fails
            with open(out_path + ".txt", "w", encoding="utf-8") as f:
                f.write(f"Screenshot capture attempt: {datetime.now()}\nStatus: {e}")
            return out_path + ".txt"

    def execute_live_zwcad_action(self, action: str, **kwargs):
        """Execute action directly on ZWCAD COM or verify capability."""
        if not self.zwcad_doc:
            return False, "No active ZWCAD document"
        
        try:
            msp = self.zwcad_doc.ModelSpace
            if action == "get_doc_info":
                return True, {
                    "name": self.zwcad_doc.Name,
                    "path": self.zwcad_doc.Path,
                    "count": msp.Count,
                    "layers": [l.Name for l in self.zwcad_doc.Layers]
                }
            elif action == "create_layer":
                name = kwargs.get("name", "TEST_LAYER")
                color = kwargs.get("color", 1)
                layer = self.zwcad_doc.Layers.Add(name)
                layer.color = color
                return True, f"Layer {name} created with color {color}"
            elif action == "draw_line":
                p1 = kwargs.get("p1", [0.0, 0.0, 0.0])
                p2 = kwargs.get("p2", [100.0, 100.0, 0.0])
                import win32com.client
                import pythoncom
                # Convert points to COM variants
                line = msp.AddLine(win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, p1),
                                   win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, p2))
                return True, {"handle": line.Handle, "length": line.Length}
            elif action == "get_count":
                return True, msp.Count
            elif action == "undo":
                self.zwcad_doc.SendCommand("_.UNDO 1\n")
                time.sleep(0.3)
                return True, "Undo command executed"
            elif action == "get_sysvar":
                var_name = kwargs.get("name", "INSUNITS")
                val = self.zwcad_doc.GetVariable(var_name)
                return True, {var_name: val}
            return True, "Action simulated"
        except Exception as e:
            return False, str(e)

    def run_all_benchmarks(self):
        records = []
        summary = {
            "timestamp": datetime.now().isoformat(),
            "zwcad_version": self.zwcad_version,
            "total_providers": len(PROVIDERS),
            "total_tests_per_provider": len(TEST_DESCRIPTIONS),
            "provider_scores": {},
            "capability_rankings": {},
            "verdict": ""
        }
        
        print("=" * 80)
        print("Starting CAD-MCP Benchmark Suite T01-T34")
        print("=" * 80)

        # Baseline count before tests
        success, pre_doc = self.execute_live_zwcad_action("get_doc_info")
        initial_entity_count = pre_doc["count"] if success else 0
        print(f"[Initial CAD State] Active Document Entities: {initial_entity_count}")

        for provider in PROVIDERS:
            p_records = self._evaluate_provider(provider)
            records.extend(p_records)

        # Write CSV
        csv_file = os.path.join(self.results_dir, "provider-results.csv")
        fieldnames = [
            "verification_kind", "measured_export_allowed", "legacy_assumed_status", "legacy_assumed_score", "provider", "test_id", "test_name", "zwcad_version", "status",
            "latency_ms", "correctness_score", "geometry_correctness", "layer_correctness",
            "context_stability", "selection_stability", "undo_reliability", "save_reliability",
            "screenshot_availability", "manual_intervention_count", "repair_step_count",
            "error_message_quality", "notes", "evidence_path", "upstream_commit_sha"
        ]
        
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow(r)
        print(f"\n[RESULTS] CSV report written to: {csv_file}")

        # Compute Summary
        summary = self._compute_summary(records)
        json_file = os.path.join(self.results_dir, "provider-summary.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"[RESULTS] JSON summary written to: {json_file}")
        
        return records, summary

    def _evaluate_provider(self, provider: str):
        print(f"\nEvaluating Provider: [{provider}] (SHA: {UPSTREAM_SHAS[provider][:8]})")
        records = []
        log_file = os.path.join(self.logs_dir, f"{provider}_eval.log")
        
        with open(log_file, "w", encoding="utf-8") as logf:
            logf.write(f"Evaluation Log for {provider}\nDate: {datetime.now()}\nSHA: {UPSTREAM_SHAS[provider]}\n\n")
            
            for test_id, test_name in TEST_DESCRIPTIONS.items():
                t0 = time.time()
                result = self._run_test_case(provider, test_id, test_name, logf)
                latency = round((time.time() - t0) * 1000, 2)
                result["latency_ms"] = None
                records.append(result)
                logf.write(f"[{test_id}] {test_name}: {result['status']} ({latency}ms) - {result['notes']}\n")
                print(f"  {test_id} {test_name[:35]:<36} : {result['status']:<7} [{latency:>6.1f}ms]")

        return records

    def _run_test_case(self, provider: str, test_id: str, test_name: str, logf) -> dict:
        sha = UPSTREAM_SHAS.get(provider, "UNKNOWN")
        evidence_shot = f"{provider}_{test_id}.png"
        
        # Base record structure
        rec = {
            "provider": provider,
            "test_id": test_id,
            "test_name": test_name,
            "zwcad_version": self.zwcad_version,
            "status": "PASS",
            "latency_ms": 0.0,
            "correctness_score": 5,
            "geometry_correctness": 1,
            "layer_correctness": 1,
            "context_stability": 1,
            "selection_stability": 1,
            "undo_reliability": 1,
            "save_reliability": 1,
            "screenshot_availability": 0,
            "manual_intervention_count": 0,
            "repair_step_count": 0,
            "error_message_quality": 5,
            "notes": "",
            "evidence_path": f"evidence/screenshots/{evidence_shot}",
            "upstream_commit_sha": sha
        }

        # Detailed evaluation logic per provider and test_id
        if provider == "multicad":
            if test_id in ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T13", "T17", "T19", "T20", "T22", "T23", "T24"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "Native multiCAD COM adapter operational; robust layer, entity, and block creation."
            elif test_id in ["T09", "T10"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 4
                rec["notes"] = "Door/window inserted via standard block reference."
            elif test_id == "T11":
                rec["status"] = "PARTIAL"
                rec["correctness_score"] = 2
                rec["notes"] = "multiCAD only supports uniform block scaling (e.g. scale=1.5), lacks X/Y non-uniform scaling."
            elif test_id in ["T18", "T29"]:
                rec["status"] = "PARTIAL"
                rec["screenshot_availability"] = 0
                rec["notes"] = "Web dashboard available (port 8888) but lacks direct MCP image screenshot tool return."
            elif test_id in ["T27", "T28", "T30", "T31"]:
                rec["status"] = "PARTIAL"
                rec["notes"] = "Standard COM execution; lacks dry-run confirm, background IPC, indexing, and discovery mode."
            else:
                rec["status"] = "PASS"
                rec["notes"] = "General 2D CAD operations verified."

        elif provider == "zwcad_standard":
            if test_id in ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T12", "T13", "T14", "T15", "T17", "T19", "T20", "T21", "T22", "T23", "T24", "T26", "T27", "T32"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "Outstanding write safety with dry_run=true default, explicit confirm=true, and batch job plot."
            elif test_id in ["T09", "T10"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 4
                rec["notes"] = "Inserted architectural blocks with batch entity tools."
            elif test_id == "T11":
                rec["status"] = "PARTIAL"
                rec["correctness_score"] = 3
                rec["notes"] = "Uniform block scaling standard; non-uniform requires individual property update."
            elif test_id in ["T18", "T29"]:
                rec["status"] = "PARTIAL"
                rec["notes"] = "Exports PDF and validates files, but does not provide direct Win32 viewport screenshot."
            elif test_id in ["T28", "T30", "T31"]:
                rec["status"] = "PARTIAL"
                rec["notes"] = "Batch jobs run in background thread; large drawing indexing not built-in."
            else:
                rec["status"] = "PASS"
                rec["notes"] = "Highly reliable standard CAD operations."

        elif provider == "dalingo_zwcad":
            rec["screenshot_availability"] = 1
            if test_id in ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T12", "T13", "T18", "T19", "T20", "T21", "T22", "T25", "T28", "T29"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "File IPC (PostMessage + LISP dispatch) allows background execution without stealing focus + Win32 PrintWindow screenshot."
            elif test_id == "T11":
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "execute_lisp escape hatch allows direct (command \"_.INSERT\" ... scale_x scale_y) for non-uniform scale."
            elif test_id in ["T16", "T34"]:
                rec["status"] = "PASS"
                rec["notes"] = "execute_lisp provides unlimited LISP/ActiveX query and mutation power."
            elif test_id in ["T30", "T31"]:
                rec["status"] = "PARTIAL"
                rec["notes"] = "ezdxf fallback mode available, but lacks dedicated spatial indexing and discovery mode."
            else:
                rec["status"] = "PASS"
                rec["notes"] = "Solid File IPC and AutoLISP execution."

        elif provider == "zwcad_platform":
            if test_id in ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T12", "T13", "T14", "T15", "T16", "T17", "T22", "T23"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "Exceptional deep entity metadata: XData, Dictionary, system variables, selection sets, and dimension queries."
            elif test_id in ["T09", "T10", "T11"]:
                rec["status"] = "PARTIAL"
                rec["correctness_score"] = 3
                rec["notes"] = "General block insertion; lacks specialized architectural door/window parameters."
            elif test_id in ["T18", "T28", "T29", "T30", "T31"]:
                rec["status"] = "PARTIAL"
                rec["notes"] = "Focused on COM API / comtypes; lacks screenshot capture and spatial indexer."
            else:
                rec["status"] = "PASS"
                rec["notes"] = "Advanced metadata and system variable inspection verified."

        elif provider == "kenchiku":
            if test_id in ["T01", "T02", "T05", "T06", "T08", "T09", "T10", "T11", "T22", "T25", "T34"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "Top-tier architectural suitability: native non-uniform scale (e.g. 4.213x1.0), stderr logging safety, door/window blocks."
            elif test_id in ["T14", "T15", "T16"]:
                rec["status"] = "PARTIAL"
                rec["correctness_score"] = 3
                rec["notes"] = "Optimized for architectural geometry; lacks advanced XData and BOM tables."
            elif test_id in ["T18", "T28", "T30", "T31"]:
                rec["status"] = "PARTIAL"
                rec["notes"] = "Lacks Win32 screenshot, background IPC, large drawing index."
            else:
                rec["status"] = "PASS"
                rec["notes"] = "Architectural CAD workflow verified."

        elif provider == "zwcad_mechanical":
            if test_id in ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T12", "T13", "T14", "T15", "T16", "T17", "T22"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "Best-in-class dimensioning (tolerances, fit symbols H7, limits), tables, frames, and BOM."
            elif test_id in ["T09", "T10", "T11"]:
                rec["status"] = "PARTIAL"
                rec["correctness_score"] = 3
                rec["notes"] = "Mechanical focus; architectural blocks possible via general insert_block."
            elif test_id in ["T18", "T28", "T30", "T31"]:
                rec["status"] = "PARTIAL"
                rec["notes"] = "Mechanical tools require ZwmToolKit for specialized BOM features."
            else:
                rec["status"] = "PASS"
                rec["notes"] = "High-precision drafting verified."

        elif provider == "large_drawing_index":
            if test_id in ["T02", "T03", "T04", "T19", "T20", "T30"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "Best-in-class large DWG/DXF streaming indexer (<0.03s read), spatial queries (blocks_near, whats_at), and text search."
            elif test_id in ["T18", "T29"]:
                rec["status"] = "PASS"
                rec["screenshot_availability"] = 1
                rec["notes"] = "Matplotlib headless rendering preview."
            elif test_id in ["T01", "T05", "T06", "T07", "T08", "T11", "T12", "T22"]:
                rec["status"] = "PARTIAL"
                rec["correctness_score"] = 3
                rec["notes"] = "Operates via DXF copy round-tripped with ZWCAD COM; slower for fine-grained interactive single-entity writes."
            else:
                rec["status"] = "PARTIAL"
                rec["notes"] = "Specialist indexer for large plant/facility layouts."

        elif provider == "zwcad_control":
            rec["screenshot_availability"] = 1
            if test_id in ["T01", "T02", "T17", "T18", "T24", "T28", "T29", "T33"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 5
                rec["notes"] = "Outstanding architecture: In-process C# plugin, named pipe, explicit instance_id & document_id context, persistent selection JSON."
            elif test_id in ["T05", "T06", "T07", "T08", "T11", "T12", "T13", "T22"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 4
                rec["notes"] = "Operations executed via run_lisp or run_csharp; requires C# script compilation or LISP snippets."
            else:
                rec["status"] = "PASS"
                rec["notes"] = "Context stability and named pipe execution verified."

        elif provider == "autocad_mcp":
            if test_id in ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T12", "T13", "T17", "T22", "T31"]:
                rec["status"] = "PASS"
                rec["correctness_score"] = 4
                rec["notes"] = "Tested with CAD_PROGID=ZWCAD.Application; basic COM methods succeed; outstanding Discovery Mode (40k -> 356 tokens)."
            elif test_id in ["T09", "T10", "T11", "T14"]:
                rec["status"] = "PARTIAL"
                rec["correctness_score"] = 3
                rec["notes"] = "AutoCAD-specific COM properties/methods cause occasional COM errors on ZWCAD; not recommended for deep porting."
            elif test_id in ["T18", "T29"]:
                rec["status"] = "PASS"
                rec["screenshot_availability"] = 1
                rec["notes"] = "Window capture supported via Pillow."
            else:
                rec["status"] = "PARTIAL"
                rec["notes"] = "Architectural benchmark reference for Tool Discovery and Quality Loop."

        # Preserve assumptions explicitly, never expose them as measured outcomes.
        rec["verification_kind"] = "LEGACY_SYNTHETIC"
        rec["measured_export_allowed"] = False
        rec["legacy_assumed_status"] = rec["status"]
        rec["legacy_assumed_score"] = rec["correctness_score"]
        rec["status"] = "UNVERIFIED"
        for key in ("latency_ms", "correctness_score", "geometry_correctness",
                    "layer_correctness", "context_stability", "selection_stability",
                    "undo_reliability", "save_reliability", "screenshot_availability",
                    "manual_intervention_count", "repair_step_count", "error_message_quality"):
            rec[key] = None
        rec["evidence_path"] = ""
        rec["notes"] = "Unverified legacy assumption: " + rec["notes"]

        return rec

    def _compute_summary(self, records: list) -> dict:
        return {
            "verification_kind": "LEGACY_SYNTHETIC",
            "measured_export_allowed": False,
            "record_count": len(records),
            "provider_summary": {},
            "capability_rankings": {},
            "notice": "No provider was invoked. No measured scores or rankings exist."
        }

if __name__ == "__main__":
    workspace = str(Path(__file__).resolve().parent.parent)
    ZWCADTestHarness(workspace).run_all_benchmarks()
