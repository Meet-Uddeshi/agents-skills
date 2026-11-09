#!/usr/bin/env python3
"""
Multi-Agent Blackboard Manager
Manages the shared context blackboard for multi-agent workflows.
"""

import argparse
import json
import os
import sys
from pathlib import Path

BLACKBOARD_FILE = Path(".agent/context/BLACKBOARD.md")

def read_blackboard():
    if not BLACKBOARD_FILE.exists():
        return ""
    return BLACKBOARD_FILE.read_text(encoding="utf-8")

def write_blackboard(content):
    BLACKBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    BLACKBOARD_FILE.write_text(content, encoding="utf-8")

def init_blackboard(objective, orchestrator="orchestrator"):
    content = f"""# Active Multi-Agent Blackboard

This file serves as the live coordination blackboard for multi-agent workflows.

## Current Execution Session

- **Session Objective:** {objective}
- **Orchestrator:** `{orchestrator}`
- **Active Agents:** []
- **Current Phase:** PLANNING

## Discovered Invariants & Context Facts
- Initialized for objective: {objective}

## Agent Work Items & Status
| Work Item | Assigned Agent | Status | Artifact / Output |
| :--- | :--- | :--- | :--- |
| Planning & Task Breakdown | `project-planner` | PENDING | - |

## Known Blockers & Session Failures
- None recorded.

## Context Handoff Artifacts
- None.
"""
    write_blackboard(content)
    print(f"Blackboard initialized with objective: {objective}")

def add_invariant(key, value):
    content = read_blackboard()
    marker = "## Discovered Invariants & Context Facts\n"
    if marker in content:
        parts = content.split(marker, 1)
        new_entry = f"- **{key}:** {value}\n"
        content = parts[0] + marker + new_entry + parts[1]
        write_blackboard(content)
        print(f"Added invariant: {key} -> {value}")
    else:
        print("Marker not found in blackboard.")

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Blackboard Manager")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize blackboard")
    init_parser.add_argument("--objective", required=True, help="Session goal")
    init_parser.add_argument("--orchestrator", default="orchestrator", help="Lead orchestrator agent")

    inv_parser = subparsers.add_parser("add-invariant", help="Add discovered fact")
    inv_parser.add_argument("--key", required=True, help="Invariant key")
    inv_parser.add_argument("--value", required=True, help="Invariant value")

    args = parser.parse_args()
    if args.command == "init":
        init_blackboard(args.objective, args.orchestrator)
    elif args.command == "add-invariant":
        add_invariant(args.key, args.value)
    else:
        print(read_blackboard())

if __name__ == "__main__":
    main()

