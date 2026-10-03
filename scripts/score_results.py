"""Fail-closed score interface: no measured provider runner exists yet."""
import argparse

def score_results(workspace_dir=None, *, measured=False):
    if measured:
        raise ValueError("Measured export unavailable: candidate MCP invocation and independent fixture evidence are not implemented")
    return {"verification_kind": "LEGACY_SYNTHETIC", "measured_export_allowed": False,
            "provider_summary": {}, "capability_rankings": {}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--measured", action="store_true")
    args = parser.parse_args()
    try:
        print(score_results(measured=args.measured))
    except ValueError as exc:
        parser.error(str(exc))
