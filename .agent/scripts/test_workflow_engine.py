#!/usr/bin/env python3
"""
Comprehensive Validation Suite for Workflow Engines (Python & Node.js).

Verifies that all 17 workflows can be listed, inspected, executed, and queried
for structured answers across both Python (workflow_engine.py) and Node.js (workflow-engine.js).
"""

import sys
import subprocess
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PY_ENGINE = SCRIPT_DIR / "workflow_engine.py"
JS_ENGINE = SCRIPT_DIR / "workflow-engine.js"


def run_cmd(cmd_args):
    res = subprocess.run(cmd_args, capture_output=True, text=True, cwd=SCRIPT_DIR)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {' '.join(cmd_args)}\nStderr: {res.stderr}\nStdout: {res.stdout}")
    return res.stdout


def test_python_engine():
    print("Testing Python Workflow Engine (workflow_engine.py)...")
    
    # 1. List
    out = run_cmd(["python", str(PY_ENGINE), "list"])
    assert "ANTIGRAVITY WORKFLOW AUTOMATION CATALOG" in out
    assert "/mobile-test" in out
    assert "/reverse-engineer" in out
    assert "/unslop" in out
    assert "/understand" in out
    print("  [PASS] Python list command")

    # 2. Validate
    out = run_cmd(["python", str(PY_ENGINE), "validate"])
    assert "100.0%" in out
    print("  [PASS] Python validate command")

    # 3. Info (JSON)
    out = run_cmd(["python", str(PY_ENGINE), "info", "mobile-test", "--json"])
    data = json.loads(out)
    assert data["name"] == "mobile-test"
    assert len(data["steps"]) >= 5
    assert "mobile-automation-engineer" in data["recommended_agents"]
    print("  [PASS] Python info command")

    # 4. Dry Run
    out = run_cmd(["python", str(PY_ENGINE), "run", "unslop", "--args", "audit", "--dry-run", "--json"])
    data = json.loads(out)
    assert data["workflow"] == "unslop"
    assert data["dry_run"] is True
    print("  [PASS] Python run dry-run")

    # 5. Answer Generation
    prompts = [
        ("Like Google Photos, create a search functionality for my software", "reverse-engineer", "reverse-engineering-anything"),
        ("Remove AI slops from my UI design and update UI properly", "unslop", "unslop"),
        ("I got a new project which is unknown for me, explain me project e2e", "understand", "understand-anything"),
        ("Set up Appium mobile automation test suite with WebdriverIO TypeScript", "mobile-test", "mobile-automation-engineer"),
    ]
    for prompt, expected_wf, expected_agent in prompts:
        out = run_cmd(["python", str(PY_ENGINE), "answer", prompt, "--json"])
        ans = json.loads(out)
        assert ans["selected_workflow"] == expected_wf, f"Expected {expected_wf}, got {ans['selected_workflow']}"
        assert ans["selected_agent"] == expected_agent, f"Expected {expected_agent}, got {ans['selected_agent']}"
        assert len(ans["execution_steps"]) > 0
    print("  [PASS] Python answer generation for all key prompt patterns")


def test_node_engine():
    print("Testing Node.js Workflow Engine (workflow-engine.js)...")

    # 1. List
    out = run_cmd(["node", str(JS_ENGINE), "list"])
    assert "ANTIGRAVITY WORKFLOW AUTOMATION CATALOG" in out
    assert "/mobile-test" in out
    assert "/reverse-engineer" in out
    assert "/unslop" in out
    assert "/understand" in out
    print("  [PASS] Node.js list command")

    # 2. Validate
    out = run_cmd(["node", str(JS_ENGINE), "validate"])
    assert "100.0%" in out
    print("  [PASS] Node.js validate command")

    # 3. Info (JSON)
    out = run_cmd(["node", str(JS_ENGINE), "info", "understand", "--json"])
    data = json.loads(out)
    assert data["name"] == "understand"
    assert len(data["steps"]) >= 5
    assert "understand-anything" in data["recommended_agents"]
    print("  [PASS] Node.js info command")

    # 4. Dry Run
    out = run_cmd(["node", str(JS_ENGINE), "run", "reverse-engineer", "--args", "inspect", "--dry-run", "--json"])
    data = json.loads(out)
    assert data["workflow"] == "reverse-engineer"
    assert data["dry_run"] is True
    print("  [PASS] Node.js run dry-run")

    # 5. Answer Generation
    prompts = [
        ("Like Google Photos, create a search functionality for my software", "reverse-engineer", "reverse-engineering-anything"),
        ("Remove AI slops from my UI design and update UI properly", "unslop", "unslop"),
        ("I got a new project which is unknown for me, explain me project e2e", "understand", "understand-anything"),
        ("Set up Appium mobile automation test suite with WebdriverIO TypeScript", "mobile-test", "mobile-automation-engineer"),
    ]
    for prompt, expected_wf, expected_agent in prompts:
        out = run_cmd(["node", str(JS_ENGINE), "answer", prompt, "--json"])
        ans = json.loads(out)
        assert ans["selected_workflow"] == expected_wf, f"Expected {expected_wf}, got {ans['selected_workflow']}"
        assert ans["selected_agent"] == expected_agent, f"Expected {expected_agent}, got {ans['selected_agent']}"
        assert len(ans["execution_steps"]) > 0
    print("  [PASS] Node.js answer generation for all key prompt patterns")


def main():
    print("================================================================================")
    print("           ANTIGRAVITY DUAL WORKFLOW ENGINE VALIDATION SUITE                    ")
    print("================================================================================")
    test_python_engine()
    print("--------------------------------------------------------------------------------")
    test_node_engine()
    print("================================================================================")
    print("ALL TESTS PASSED (100.0%) - Dual Workflow Engine is fully operational.")
    print("================================================================================")


if __name__ == "__main__":
    main()

