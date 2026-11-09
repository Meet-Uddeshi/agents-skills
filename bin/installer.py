"""
Installer Engine for Meet AI Agents.

Handles deployment across levels:
  - Project level (-p): Deploys .agent/ and GEMINI.md into target project.
  - User level (-u): Deploys to user Antigravity profile (~/.gemini/).
  - Global level (-g): Deploys to system-wide global directory.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

PACKAGE_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = PACKAGE_DIR.parent
SOURCE_AGENT_DIR = WORKSPACE_DIR / ".agent"
SOURCE_GEMINI_MD = WORKSPACE_DIR / "GEMINI.md"
SOURCE_ENV_EXAMPLE = WORKSPACE_DIR / ".env.example"


class Installer:
    """Manages multi-level deployment of Meet AI Agents."""

    @staticmethod
    def get_user_dir() -> Path:
        """Returns the user-level Antigravity directory."""
        home = Path.home()
        return home / ".gemini"

    @staticmethod
    def get_global_dir() -> Path:
        """Returns the system-level global directory."""
        if os.name == "nt":
            all_users = os.environ.get("ALLUSERSPROFILE", r"C:\ProgramData")
            return Path(all_users) / "antigravity"
        else:
            return Path("/usr/local/share/antigravity")

    @classmethod
    def install(
        cls,
        target_level: str,
        custom_path: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Installs the agent package to the specified level.

        Args:
            target_level: 'project' (-p), 'user' (-u), or 'global' (-g).
            custom_path: Optional override directory.
            dry_run: If True, simulates without copying files.
        """
        if custom_path:
            dest_root = Path(custom_path).resolve()
        elif target_level in ("project", "p"):
            dest_root = Path.cwd().resolve()
        elif target_level in ("user", "u"):
            dest_root = cls.get_user_dir()
        elif target_level in ("global", "g"):
            dest_root = cls.get_global_dir()
        else:
            raise ValueError(f"Unknown target level: {target_level}. Must be 'project' (-p), 'user' (-u), or 'global' (-g).")

        dest_agent = dest_root / ".agent"
        dest_gemini = dest_root / "GEMINI.md"
        dest_env_example = dest_root / ".env.example"

        actions = [
            f"Deploy .agent/ directory -> {dest_agent}",
            f"Deploy GEMINI.md -> {dest_gemini}",
            f"Deploy .env.example -> {dest_env_example}",
        ]

        if not dry_run:
            dest_root.mkdir(parents=True, exist_ok=True)

            # Copy .agent directory
            if SOURCE_AGENT_DIR.exists():
                dest_agent.mkdir(parents=True, exist_ok=True)
                # Copy agents, skills, workflows, rules, context, memory
                subdirs = ["agents", "skills", "workflows", "rules", "context", "memory", "scripts", "resources"]
                for sub in subdirs:
                    src_sub = SOURCE_AGENT_DIR / sub
                    dst_sub = dest_agent / sub
                    if src_sub.exists():
                        shutil.copytree(src_sub, dst_sub, dirs_exist_ok=True)

                # Copy configuration files
                for f in ["mcp.json", "mcp_config.json", ".env.template", "ARCHITECTURE.md"]:
                    src_f = SOURCE_AGENT_DIR / f
                    if src_f.exists():
                        shutil.copy2(src_f, dest_agent / f)

            # Copy GEMINI.md
            if SOURCE_GEMINI_MD.exists():
                shutil.copy2(SOURCE_GEMINI_MD, dest_gemini)

            # Copy .env.example
            if SOURCE_ENV_EXAMPLE.exists() and not (dest_root / ".env").exists():
                shutil.copy2(SOURCE_ENV_EXAMPLE, dest_env_example)

        return {
            "target_level": target_level,
            "destination": str(dest_root),
            "dry_run": dry_run,
            "actions": actions,
            "status": "SIMULATED" if dry_run else "SUCCESS",
        }

