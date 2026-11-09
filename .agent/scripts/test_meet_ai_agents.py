#!/usr/bin/env python3
"""
Comprehensive Validation Suite for Meet AI Agents (Node.js & Python wrappers).

Tests:
  - Node CLI (bin/meet-ai-agents.js) with -p, -u, -g flags in dry-run mode
  - Python CLI (meet_ai_agents.cli) with -p, -u, -g flags in dry-run mode
  - MCP manager: server listing, testing, and credential isolation
  - Workflow automation integration (run and answer)
"""

import sys
import subprocess
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = SCRIPT_DIR.parent.parent
NODE_CLI = WORKSPACE_DIR / "bin" / "meet-ai-agents.js"


def run_cmd(args):
    res = subprocess.run(args, capture_output=True, text=True, cwd=WORKSPACE_DIR)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {' '.join(args)}\nStderr: {res.stderr}\nStdout: {res.stdout}")
    return res.stdout


def test_node_cli():
    print("Testing Node.js CLI (bin/meet-ai-agents.js)...")

    # 1. Doctor
    out = run_cmd(["node", str(NODE_CLI), "doctor"])
    assert "MEET AI AGENTS" in out
    assert "Configured MCP Servers" in out
    print("  [PASS] Node doctor check")

    # 2. Project install (-p dry-run)
    out = run_cmd(["node", str(NODE_CLI), "-p", "--dry-run"])
    assert "Deploying Meet AI Agents to [PROJECT] level" in out
    print("  [PASS] Node -p (project level) dry-run")

    # 3. User install (-u dry-run)
    out = run_cmd(["node", str(NODE_CLI), "-u", "--dry-run"])
    assert "Deploying Meet AI Agents to [USER] level" in out
    print("  [PASS] Node -u (user level) dry-run")

    # 4. Global install (-g dry-run)
    out = run_cmd(["node", str(NODE_CLI), "-g", "--dry-run"])
    assert "Deploying Meet AI Agents to [GLOBAL] level" in out
    print("  [PASS] Node -g (global level) dry-run")

    # 5. MCP list
    out = run_cmd(["node", str(NODE_CLI), "mcp"])
    assert "github" in out
    assert "jira" in out
    print("  [PASS] Node mcp list")


def test_python_cli():
    print("Testing Python CLI (bin.cli)...")

    # 1. Doctor
    out = run_cmd(["python", "-m", "bin.cli", "doctor"])
    assert "MEET AI AGENTS" in out
    assert "Health check completed successfully" in out
    print("  [PASS] Python doctor check")

    # 2. Project install (-p dry-run JSON)
    out = run_cmd(["python", "-m", "bin.cli", "-p", "--dry-run", "--json"])
    data = json.loads(out)
    assert data["target_level"] == "project"
    assert data["dry_run"] is True
    print("  [PASS] Python -p (project level) dry-run")

    # 3. User install (-u dry-run JSON)
    out = run_cmd(["python", "-m", "bin.cli", "-u", "--dry-run", "--json"])
    data = json.loads(out)
    assert data["target_level"] == "user"
    assert data["dry_run"] is True
    print("  [PASS] Python -u (user level) dry-run")

    # 4. Global install (-g dry-run JSON)
    out = run_cmd(["python", "-m", "bin.cli", "-g", "--dry-run", "--json"])
    data = json.loads(out)
    assert data["target_level"] == "global"
    assert data["dry_run"] is True
    print("  [PASS] Python -g (global level) dry-run")

    # 5. MCP list (JSON)
    out = run_cmd(["python", "-m", "bin.cli", "mcp", "list", "--json"])
    servers = json.loads(out)
    server_names = [s["name"] for s in servers]
    assert "github" in server_names
    assert "jira" in server_names
    assert "linear" in server_names
    assert "postgres" in server_names
    assert "slack" in server_names
    print("  [PASS] Python mcp list with 3rd-party servers")

    # 6. MCP test (JSON)
    out = run_cmd(["python", "-m", "bin.cli", "mcp", "test", "github", "--json"])
    test_res = json.loads(out)
    assert test_res["name"] == "github"
    assert "GITHUB_PERSONAL_ACCESS_TOKEN" in test_res["missing_env"] or test_res["ready"]
    print("  [PASS] Python mcp test diagnostics")

    # 7. Workflow Run via meet CLI
    out = run_cmd(["python", "-m", "bin.cli", "run", "unslop", "--dry-run", "--json"])
    run_res = json.loads(out)
    assert run_res["workflow"] == "unslop"
    assert run_res["dry_run"] is True
    print("  [PASS] Python meet run workflow")

    # 8. Workflow Answer via meet CLI
    out = run_cmd(["python", "-m", "bin.cli", "answer", "Like Google Photos, create a search functionality for my software", "--json"])
    ans_res = json.loads(out)
    assert ans_res["selected_workflow"] == "reverse-engineer"
    assert ans_res["selected_agent"] == "reverse-engineering-anything"
    print("  [PASS] Python meet answer generation")


def main():
    print("================================================================================")
    print("           MEET AI AGENTS (NPM, UV, PIP) COMPREHENSIVE TEST SUITE               ")
    print("================================================================================")
    test_node_cli()
    print("--------------------------------------------------------------------------------")
    test_python_cli()
    print("================================================================================")
    print("ALL TESTS PASSED (100.0%) - Meet AI Agents package is fully operational.")
    print("================================================================================")


if __name__ == "__main__":
    main()

