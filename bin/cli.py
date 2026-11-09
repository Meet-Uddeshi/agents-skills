#!/usr/bin/env python3
"""
Meet AI Agents - Unified Command Line Interface.

Usage:
  meet -p                       # Deploy to current project (./.agent/ & GEMINI.md)
  meet -u                       # Deploy to user profile (~/.gemini/)
  meet -g                       # Deploy to system global level
  meet install [-p|-u|-g]       # Explicit install command
  meet mcp list                 # List configured MCP servers & credential readiness
  meet mcp test <server>        # Test MCP server configuration & tools
  meet mcp sync [-p|-u|-g]      # Sync MCP config to target level
  meet run <workflow>           # Execute workflow automation
  meet answer "<query>"         # Generate structured workflow answer
  meet list [workflows|agents]  # List catalog entries
  meet doctor                   # Health check of workspace, agents & MCP
"""

import sys
import os
import argparse
import json
from pathlib import Path

try:
    from bin.installer import Installer
    from bin.mcp_manager import McpManager
    from bin.memory_manager import MemoryManager
except ImportError:
    from installer import Installer
    from mcp_manager import McpManager
    from memory_manager import MemoryManager

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = SCRIPT_DIR.parent
AGENT_DIR = WORKSPACE_DIR / ".agent"
SCRIPTS_DIR = AGENT_DIR / "scripts"

# Import workflow engine if available
sys.path.insert(0, str(SCRIPTS_DIR))
try:
    from workflow_engine import WorkflowEngine
except ImportError:
    WorkflowEngine = None


def format_header():
    print("================================================================================")
    print("            MEET AI AGENTS - MULTI-AGENT & MCP AUTOMATION PLATFORM              ")
    print("================================================================================")


def handle_install(level: str, custom_path=None, dry_run=False, json_output=False):
    res = Installer.install(target_level=level, custom_path=custom_path, dry_run=dry_run)
    if json_output:
        print(json.dumps(res, indent=2))
    else:
        mode_str = "[DRY-RUN] " if dry_run else ""
        print(f"\n{mode_str}Successfully deployed Meet AI Agents to [{level.upper()}] level.")
        print(f"Destination: {res['destination']}")
        print("Actions taken:")
        for action in res["actions"]:
            print(f"  - {action}")
        print()


def handle_mcp(args):
    manager = McpManager()
    subcmd = args.mcp_command

    if subcmd == "list":
        servers = manager.list_servers()
        if args.json:
            print(json.dumps(servers, indent=2))
        else:
            print(f"\nConfigured MCP Servers ({len(servers)}):\n")
            for s in servers:
                status_display = "[READY]" if s["status"] == "READY" else f"[MISSING: {', '.join(s['missing_env'])}]"
                agents_display = ", ".join(s["associated_agents"][:2])
                print(f"- {s['name']:<14} | Status: {status_display:<26} | Agents: {agents_display}")
                print(f"  Command: {s['command']} | Desc: {s['description']}")
            print()

    elif subcmd == "test":
        target = args.server
        try:
            res = manager.test_server(target)
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"\nMCP Server Diagnostics: {target}")
                print(f"- Status: {'[READY]' if res['ready'] else '[NOT READY]'}")
                print(f"- Command: {res['command']} (Found at: {res['command_path']})")
                if res["missing_env"]:
                    print(f"- Missing Environment Variables: {', '.join(res['missing_env'])}")
                    print(f"  Please add them to your .env file (see .env.example)")
                else:
                    print("- Environment Credentials: All verified.")
                print(f"- Associated Agents: {', '.join(res['associated_agents'])}\n")
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)

    elif subcmd == "sync":
        level = args.level or "project"
        if level in ("p", "project"):
            dest = Path.cwd() / ".agent" / "mcp.json"
        elif level in ("u", "user"):
            dest = Installer.get_user_dir() / "antigravity" / "mcp_config.json"
        else:
            dest = Installer.get_global_dir() / "mcp_config.json"

        manager.sync_to_destination(dest)
        print(f"\nSynced MCP configuration to {dest}\n")

    else:
        print("Usage: meet mcp [list|test <server>|sync [-p|-u|-g]]")


def handle_memory(args):
    manager = MemoryManager()
    subcmd = args.memory_command

    if subcmd == "init":
        print(f"\nInitialized SQLite Memory Database: {manager.db_path}\n")

    elif subcmd == "log":
        tags_list = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
        meta = json.loads(args.metadata) if args.metadata else {}
        row_id = manager.log_memory(
            key=args.key,
            content=args.content,
            category=args.category,
            agent=args.agent,
            tags=tags_list,
            metadata=meta,
        )
        if args.json:
            print(json.dumps({"success": True, "id": row_id, "key": args.key}))
        else:
            print(f"\nStored memory: key='{args.key}' [Category: {args.category}, Agent: {args.agent}]\n")

    elif subcmd == "query":
        results = manager.query_memories(
            search_term=args.term,
            category=args.category,
            agent=args.agent,
            tag=args.tag,
            limit=args.limit,
        )
        if args.json:
            print(json.dumps(results, indent=2, default=str))
        else:
            term_str = f" for '{args.term}'" if args.term else ""
            print(f"\nBounded Memory Query Results{term_str} (Limit: {args.limit}, Found: {len(results)}):\n")
            for idx, r in enumerate(results, start=1):
                cat = r.get("category", "general")
                agt = r.get("agent", "system")
                print(f"{idx}. Key: {r['key']} [Category: {cat}, Agent: {agt}]")
                content_preview = r['content'].strip().replace("\n", " ")
                if len(content_preview) > 120:
                    content_preview = content_preview[:117] + "..."
                print(f"   {content_preview}\n")

    elif subcmd == "sync":
        direction = args.direction or "both"
        imported = {}
        if direction in ("import", "both"):
            imported = manager.sync_from_markdown()
        if direction in ("export", "both"):
            manager.sync_to_markdown()

        if args.json:
            print(json.dumps({"direction": direction, "imported": imported}))
        else:
            print(f"\nDual-Mode Memory Synchronization Completed (Direction: {direction}):")
            if imported:
                print(f"- Synced Invariants from ARCHITECTURE_MEMORY.md: {imported.get('synced_invariants', 0)}")
                print(f"- Synced Events from BLACKBOARD.md: {imported.get('synced_events', 0)}")
            print("- Synchronized markdown files with SQLite storage.\n")

    elif subcmd == "stats":
        stats = manager.get_stats()
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("\nSQLite Memory & Context Engineering Stats:")
            print(f"- Database Path: {stats['db_path']}")
            print(f"- Database Size: {stats['size_kb']} KB ({stats['size_bytes']} bytes)")
            print(f"- Total Memories: {stats['total_memories']}")
            print(f"- Total Blackboard Events: {stats['total_events']}")
            print("- Categories Breakdown:")
            for cat, count in stats.get("categories", {}).items():
                print(f"  * {cat}: {count}")
            print()

    elif subcmd == "prune":
        count = manager.prune(max_age_days=args.days, keep_invariants=not args.all)
        if args.json:
            print(json.dumps({"pruned_records": count, "max_age_days": args.days}))
        else:
            print(f"\nPruned {count} historical records older than {args.days} days.\n")

    elif subcmd == "events":
        events = manager.query_events(
            session_id=args.session,
            agent=args.agent,
            event_type=args.type,
            limit=args.limit,
        )
        if args.json:
            print(json.dumps(events, indent=2, default=str))
        else:
            print(f"\nRecent Blackboard & Coordination Events (Limit: {args.limit}, Found: {len(events)}):\n")
            for idx, e in enumerate(events, start=1):
                print(f"{idx}. [{e['created_at']}] [{e['agent']}] ({e['event_type']})")
                print(f"   {e['description']}\n")
    else:
        print("Usage: meet memory [init|log|query|sync|stats|prune|events]")


def handle_run(args):
    if not WorkflowEngine:
        print("[ERROR] WorkflowEngine could not be loaded from .agent/scripts", file=sys.stderr)
        sys.exit(1)
    engine = WorkflowEngine()
    try:
        res = engine.run_workflow(
            workflow_name=args.workflow,
            args=args.args,
            agent_name=args.agent,
            dry_run=args.dry_run
        )
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            mode_str = "[DRY-RUN]" if args.dry_run else "[EXECUTED]"
            print(f"\n{mode_str} Workflow /{res['workflow']} run completed successfully.")
            print(f"- Executing Agent: {res['agent']}")
            print(f"- Steps loaded: {len(res['steps'])}")
            print(f"- Blackboard updated: {'No (dry-run)' if args.dry_run else 'Yes'}\n")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def handle_answer(args):
    if not WorkflowEngine:
        print("[ERROR] WorkflowEngine could not be loaded", file=sys.stderr)
        sys.exit(1)
    engine = WorkflowEngine()
    ans = engine.generate_answer(query=args.query, explicit_agent=args.agent)
    if args.json:
        print(json.dumps(ans, indent=2))
    else:
        from workflow_engine import format_answer_markdown
        print("\n" + format_answer_markdown(ans) + "\n")


def handle_list(args):
    target = args.target or "workflows"
    if target == "mcp":
        manager = McpManager()
        servers = manager.list_servers()
        print(f"\nMCP Servers ({len(servers)}): " + ", ".join(s["name"] for s in servers) + "\n")
    else:
        if not WorkflowEngine:
            print("[ERROR] WorkflowEngine could not be loaded", file=sys.stderr)
            sys.exit(1)
        engine = WorkflowEngine()
        wf_list = engine.list_workflows()
        print(f"\nAvailable Workflows ({len(wf_list)}):")
        for wf in wf_list:
            print(f"  - /{wf['name']:<18} | {wf['description'][:60]}...")
        print()


def handle_doctor():
    format_header()
    print("Running Meet AI Agents System Health Check...")
    print(f"- Workspace root: {WORKSPACE_DIR}")
    print(f"- .agent bundle: {'[OK]' if AGENT_DIR.exists() else '[FAIL]'}")
    print(f"- GEMINI.md: {'[OK]' if (WORKSPACE_DIR / 'GEMINI.md').exists() else '[FAIL]'}")
    print(f"- .env.example: {'[OK]' if (WORKSPACE_DIR / '.env.example').exists() else '[FAIL]'}")

    manager = McpManager()
    servers = manager.list_servers()
    print(f"- Configured MCP Servers: {len(servers)}")
    for s in servers:
        print(f"  * {s['name']}: {s['status']}")

    try:
        mem_mgr = MemoryManager()
        stats = mem_mgr.get_stats()
        print(f"- SQLite Memory DB: [OK] ({stats['size_kb']} KB, {stats['total_memories']} memories, {stats['total_events']} events)")
    except Exception as e:
        print(f"- SQLite Memory DB: [FAIL] ({e})")

    if WorkflowEngine:
        engine = WorkflowEngine()
        print(f"- Registered Workflows: {len(engine.list_workflows())}")
    print("Health check completed successfully.\n")


def main():
    parser = argparse.ArgumentParser(
        prog="meet",
        description="Meet AI Agents - Multi-Agent System & Automation Platform"
    )

    # Top-level direct deployment flags
    parser.add_argument("-p", "--project", action="store_true", help="Deploy to current project level (./.agent/ & GEMINI.md)")
    parser.add_argument("-u", "--user", action="store_true", help="Deploy to user profile level (~/.gemini/)")
    parser.add_argument("-g", "--global", dest="global_level", action="store_true", help="Deploy to system global level")
    parser.add_argument("--dry-run", action="store_true", help="Simulate deployment without modifying disk")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommands")

    # Subcommand: install
    install_parser = subparsers.add_parser("install", help="Deploy Meet AI Agents to target level")
    install_parser.add_argument("-p", "--project", action="store_true", help="Target current project")
    install_parser.add_argument("-u", "--user", action="store_true", help="Target user profile (~/.gemini/)")
    install_parser.add_argument("-g", "--global", dest="global_level", action="store_true", help="Target system global")
    install_parser.add_argument("--path", type=str, default=None, help="Custom target directory")
    install_parser.add_argument("--dry-run", action="store_true", help="Simulate without copying")
    install_parser.add_argument("--json", action="store_true", help="Output in JSON")

    # Subcommand: mcp
    mcp_parser = subparsers.add_parser("mcp", help="Manage MCP servers & 3rd-party integrations")
    mcp_sub = mcp_parser.add_subparsers(dest="mcp_command", help="MCP action")
    list_p = mcp_sub.add_parser("list", help="List configured MCP servers")
    list_p.add_argument("--json", action="store_true", help="Output in JSON")
    test_p = mcp_sub.add_parser("test", help="Test specific MCP server")
    test_p.add_argument("server", type=str, help="MCP server name (e.g. github, jira)")
    test_p.add_argument("--json", action="store_true", help="Output in JSON")
    sync_p = mcp_sub.add_parser("sync", help="Sync MCP config to destination")
    sync_p.add_argument("-l", "--level", choices=["project", "user", "global"], default="project", help="Destination level")

    # Subcommand: run
    run_parser = subparsers.add_parser("run", help="Run workflow automation")
    run_parser.add_argument("workflow", type=str, help="Workflow name (e.g. mobile-test, unslop)")
    run_parser.add_argument("--args", type=str, default="", help="Workflow arguments")
    run_parser.add_argument("--agent", type=str, default=None, help="Agent override")
    run_parser.add_argument("--dry-run", action="store_true", help="Simulate run without blackboard log")
    run_parser.add_argument("--json", action="store_true", help="Output in JSON")

    # Subcommand: answer
    answer_parser = subparsers.add_parser("answer", help="Generate structured workflow answer")
    answer_parser.add_argument("query", type=str, help="User prompt or query")
    answer_parser.add_argument("--agent", type=str, default=None, help="Agent override")
    answer_parser.add_argument("--json", action="store_true", help="Output in JSON")

    # Subcommand: list
    list_parser = subparsers.add_parser("list", help="List workflows or MCP servers")
    list_parser.add_argument("target", nargs="?", choices=["workflows", "mcp"], default="workflows")

    # Subcommand: memory
    mem_parser = subparsers.add_parser("memory", help="SQLite persistent memory, bounded query & context engineering")
    mem_sub = mem_parser.add_subparsers(dest="memory_command", help="Memory action")
    
    mem_init = mem_sub.add_parser("init", help="Initialize SQLite memory database")
    mem_init.add_argument("--json", action="store_true", help="Output in JSON")
    
    mem_log = mem_sub.add_parser("log", help="Store or update indexed memory")
    mem_log.add_argument("--key", type=str, required=True, help="Unique memory key (e.g. invariant:name, note:topic)")
    mem_log.add_argument("--content", type=str, required=True, help="Memory content / invariant rule")
    mem_log.add_argument("--category", type=str, default="general", help="Category (invariant, architecture, decision, failure)")
    mem_log.add_argument("--agent", type=str, default="system", help="Author agent name")
    mem_log.add_argument("--tags", type=str, default="", help="Comma-separated tags")
    mem_log.add_argument("--metadata", type=str, default="{}", help="JSON metadata string")
    mem_log.add_argument("--json", action="store_true", help="Output in JSON")

    mem_query = mem_sub.add_parser("query", help="Bounded memory query & FTS5 search")
    mem_query.add_argument("term", nargs="?", type=str, default=None, help="Search query string")
    mem_query.add_argument("--category", type=str, default=None, help="Filter by category")
    mem_query.add_argument("--agent", type=str, default=None, help="Filter by agent")
    mem_query.add_argument("--tag", type=str, default=None, help="Filter by tag substring")
    mem_query.add_argument("--limit", type=int, default=5, help="Maximum records to return (default: 5)")
    mem_query.add_argument("--json", action="store_true", help="Output in JSON")

    mem_sync = mem_sub.add_parser("sync", help="Dual-mode sync between SQLite and Markdown files")
    mem_sync.add_argument("-d", "--direction", choices=["import", "export", "both"], default="both", help="Sync direction")
    mem_sync.add_argument("--json", action="store_true", help="Output in JSON")

    mem_stats = mem_sub.add_parser("stats", help="Show SQLite database size, counts, and category statistics")
    mem_stats.add_argument("--json", action="store_true", help="Output in JSON")

    mem_prune = mem_sub.add_parser("prune", help="Prune older historical records")
    mem_prune.add_argument("--days", type=int, default=30, help="Days threshold (default: 30)")
    mem_prune.add_argument("--all", action="store_true", help="Also prune non-invariant memories")
    mem_prune.add_argument("--json", action="store_true", help="Output in JSON")

    mem_ev = mem_sub.add_parser("events", help="List recent blackboard and coordination events")
    mem_ev.add_argument("--session", type=str, default=None, help="Filter by session ID")
    mem_ev.add_argument("--agent", type=str, default=None, help="Filter by agent")
    mem_ev.add_argument("--type", type=str, default=None, help="Filter by event type")
    mem_ev.add_argument("--limit", type=int, default=10, help="Maximum events to return (default: 10)")
    mem_ev.add_argument("--json", action="store_true", help="Output in JSON")

    # Subcommand: doctor
    subparsers.add_parser("doctor", help="Run system diagnostics")

    args = parser.parse_args()

    # Handle direct flags (-p, -u, -g)
    if args.project:
        handle_install("project", dry_run=args.dry_run, json_output=args.json)
        return
    elif args.user:
        handle_install("user", dry_run=args.dry_run, json_output=args.json)
        return
    elif args.global_level:
        handle_install("global", dry_run=args.dry_run, json_output=args.json)
        return

    # Handle subcommands
    if args.subcommand == "install":
        level = "project"
        if args.user:
            level = "user"
        elif args.global_level:
            level = "global"
        handle_install(level, custom_path=args.path, dry_run=args.dry_run, json_output=args.json)
    elif args.subcommand == "mcp":
        handle_mcp(args)
    elif args.subcommand == "run":
        handle_run(args)
    elif args.subcommand == "answer":
        handle_answer(args)
    elif args.subcommand == "list":
        handle_list(args)
    elif args.subcommand == "memory":
        handle_memory(args)
    elif args.subcommand == "doctor":
        handle_doctor()
    else:
        format_header()
        parser.print_help()


if __name__ == "__main__":
    main()

