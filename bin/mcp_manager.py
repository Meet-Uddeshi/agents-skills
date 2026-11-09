"""
Model Context Protocol (MCP) Manager for Meet AI Agents.

Manages 3rd-party MCP integrations (GitHub, Jira, Linear, Slack, Postgres),
validates environment credentials from .env, tests tool availability,
syncs configurations across levels, and logs tool call telemetry to the Blackboard.
"""

import os
import sys
import json
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
AGENT_DIR = WORKSPACE_DIR / ".agent"
DEFAULT_MCP_JSON = AGENT_DIR / "mcp.json"
BLACKBOARD_PATH = AGENT_DIR / "context" / "BLACKBOARD.md"


class McpManager:
    """Manages MCP servers, tool telemetry, and credential validation."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or DEFAULT_MCP_JSON
        self.servers: Dict[str, Any] = {}
        self.load_config()

    def load_config(self):
        """Loads MCP servers from mcp.json if available."""
        if not self.config_path.exists():
            return
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.servers = data.get("mcpServers", {})
        except Exception as e:
            print(f"[WARN] Could not parse MCP config at {self.config_path}: {e}", file=sys.stderr)

    def get_server(self, name: str) -> Optional[Dict[str, Any]]:
        return self.servers.get(name)

    def list_servers(self) -> List[Dict[str, Any]]:
        """Lists all configured MCP servers with credential readiness status."""
        results = []
        for name, cfg in self.servers.items():
            env_vars = cfg.get("env", {})
            missing_vars = []
            for k, v in env_vars.items():
                # Extract variable name from ${VAR_NAME} pattern
                var_match = re.search(r"\$\{([^}]+)\}", str(v))
                if var_match:
                    var_name = var_match.group(1)
                    if not os.environ.get(var_name):
                        missing_vars.append(var_name)

            status = "READY" if not missing_vars else "MISSING_ENV"
            results.append({
                "name": name,
                "command": cfg.get("command", "npx"),
                "description": cfg.get("description", ""),
                "status": status,
                "missing_env": missing_vars,
                "associated_agents": cfg.get("associated_agents", []),
            })
        return results

    def test_server(self, name: str) -> Dict[str, Any]:
        """Tests command readiness and credential environment for an MCP server."""
        cfg = self.get_server(name)
        if not cfg:
            raise ValueError(f"MCP server '{name}' not found. Available: {list(self.servers.keys())}")

        cmd = cfg.get("command", "npx")
        cmd_path = shutil.which(cmd)

        missing_vars = []
        for k, v in cfg.get("env", {}).items():
            var_match = re.search(r"\$\{([^}]+)\}", str(v))
            if var_match:
                var_name = var_match.group(1)
                if not os.environ.get(var_name):
                    missing_vars.append(var_name)

        is_ready = bool(cmd_path) and len(missing_vars) == 0

        return {
            "name": name,
            "command": cmd,
            "command_found": bool(cmd_path),
            "command_path": cmd_path or "NOT_FOUND",
            "missing_env": missing_vars,
            "ready": is_ready,
            "description": cfg.get("description", ""),
            "associated_agents": cfg.get("associated_agents", []),
        }

    def sync_to_destination(self, dest_path: Path):
        """Syncs the MCP configuration to a target destination (project, user, or global)."""
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump({"mcpServers": self.servers}, f, indent=2)

    def log_tool_call(
        self,
        agent: str,
        server: str,
        tool: str,
        status: str,
        details: str = ""
    ):
        """Appends tool call telemetry to the Blackboard."""
        if not BLACKBOARD_PATH.exists():
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"\n### MCP Tool Call: {server}.{tool} [{timestamp}]\n"
            f"- **Calling Agent**: `{agent}`\n"
            f"- **MCP Server**: `{server}`\n"
            f"- **Tool**: `{tool}`\n"
            f"- **Status**: `{status}`\n"
        )
        if details:
            # Mask any accidental secrets before writing
            sanitized = re.sub(r"(token|key|secret|password)=([^\s]+)", r"\1=***", details, flags=re.IGNORECASE)
            entry += f"- **Details**: {sanitized}\n"

        try:
            with open(BLACKBOARD_PATH, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"[WARN] Could not record tool call to Blackboard: {e}", file=sys.stderr)

