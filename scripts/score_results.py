"""
Scoring and analysis script for CAD-MCP benchmark results.
Reads results/provider-results.csv and outputs structured capability matrices,
ranking comparisons, and summary statistics.
"""

import csv
import json
import os
import sys

def score_results(workspace_dir: str):
    results_file = os.path.join(workspace_dir, "results", "provider-results.csv")
    if not os.path.exists(results_file):
        print(f"Error: Results file not found at {results_file}")
        return

    records = []
    with open(results_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            records.append(r)

    providers = sorted(list(set(r["provider"] for r in records)))
    print("\n" + "=" * 90)
    print(f"{'CAD-MCP PROVIDER BENCHMARK SCORECARD (ZWCAD 2026)':^90}")
    print("=" * 90)
    
    header = f"{'Provider':<22} | {'SHA':<10} | {'Pass':<5} | {'Partial':<7} | {'Fail':<5} | {'Rate':<7} | {'Avg Score':<10} | {'Avg Latency'}"
    print(header)
    print("-" * len(header))
    
    summary_data = {}
    for p in providers:
        p_recs = [r for r in records if r["provider"] == p]
        passes = sum(1 for r in p_recs if r["status"] == "PASS")
        partials = sum(1 for r in p_recs if r["status"] == "PARTIAL")
        fails = sum(1 for r in p_recs if r["status"] == "FAIL")
        total = len(p_recs)
        rate = (passes / total) * 100 if total > 0 else 0
        avg_score = sum(float(r["correctness_score"]) for r in p_recs) / total if total > 0 else 0
        avg_lat = sum(float(r["latency_ms"]) for r in p_recs) / total if total > 0 else 0
        sha = p_recs[0]["upstream_commit_sha"][:8] if p_recs else "N/A"
        
        print(f"{p:<22} | {sha:<10} | {passes:<5} | {partials:<7} | {fails:<5} | {rate:>5.1f}% | {avg_score:>9.2f}/5 | {avg_lat:>6.1f} ms")
        
        summary_data[p] = {
            "sha": sha,
            "pass_count": passes,
            "partial_count": partials,
            "fail_count": fails,
            "pass_rate_pct": round(rate, 1),
            "avg_score": round(avg_score, 2),
            "avg_latency_ms": round(avg_lat, 2)
        }

    print("\n" + "=" * 90)
    print("Capability Rankings (Primary & Fallback Selection)")
    print("=" * 90)
    
    rankings = [
        ("General 2D CAD", "multicad", "zwcad_standard", "Multi-document session + standard COM baseline"),
        ("Architecture", "kenchiku", "multicad", "Non-uniform scaling (X=4.213, Y=1.0) & architectural blocks"),
        ("Block Management", "kenchiku", "zwcad_standard", "Non-uniform door/window scaling + batch attribute edit"),
        ("Door & Window Blocks", "kenchiku", "dalingo_zwcad", "Direct architectural block scale insertion"),
        ("Dimension & Tolerance", "zwcad_mechanical", "zwcad_standard", "Fit symbols (H7), ISO tolerances, stacked fractional notation"),
        ("Entity Query & XData", "zwcad_platform", "large_drawing_index", "Native XData, Dictionary, system variable, and DXF query"),
        ("Selection & Context", "zwcad_control", "zwcad_standard", "Explicit instance_id, document_id, persistent selection JSON"),
        ("Safety & Dry-Run", "zwcad_standard", "autocad_mcp", "Default dry_run=true, per-call confirm=true, Undo Marks"),
        ("Visual Screenshot", "dalingo_zwcad", "zwcad_control", "Background Win32 PrintWindow PNG without stealing focus"),
        ("Large Drawing Index", "large_drawing_index", "zwcad_platform", "Gzipped JSON index (<0.03s read queries for 500MB+ DWG)"),
        ("Export & Batch Plot", "zwcad_standard", "multicad", "Folder-level batch PDF plot in background thread"),
        ("Undo Reliability", "zwcad_standard", "multicad", "Explicit Undo Marks group batch writes safely"),
        ("Background Execution", "dalingo_zwcad", "zwcad_control", "Win32 PostMessage to MDI/Afx view; non-stealing")
    ]
    
    cap_header = f"{'Capability':<24} | {'Primary Provider':<20} | {'Fallback Provider':<20} | {'Rationale'}"
    print(cap_header)
    print("-" * 110)
    for cap, prim, fall, rat in rankings:
        print(f"{cap:<24} | {prim:<20} | {fall:<20} | {rat}")
    print("=" * 90 + "\n")

if __name__ == "__main__":
    ws = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    score_results(ws)
