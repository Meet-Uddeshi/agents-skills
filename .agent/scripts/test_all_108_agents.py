#!/usr/bin/env python3
"""
Comprehensive 108-Agent Test Suite
Tests every single agent with a distinct, real-world prompt.
Outputs detailed results and verification metrics.
"""

import sys
import os
import time
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from test_intelligent_routing import IntelligentRouter

# 108 Distinct Real-World Prompts (1 per agent)
PROMPTS_108 = [
    # Domain 1: Frontend, UI & Accessibility
    ("a11y-architect", "Audit this web page for accessibility, color contrast, and WCAG screen reader labels"),
    ("frontend-specialist", "Create a responsive dark mode navbar component in React with Tailwind CSS"),
    ("react-build-resolver", "Vite build error when importing dynamic server module with turbopack"),
    ("react-reviewer", "My React component is stuck in an infinite re-render loop in useEffect memo"),
    ("unslop", "Remove AI slops from my UI design and update UI properly with clean craft"),
    ("vue-reviewer", "Build a Vue 3 dashboard using Composition API and Pinia state"),

    # Domain 2: Mobile & Cross-Platform
    ("dart-build-resolver", "Flutter build error with pubspec dependencies and pod install"),
    ("flutter-reviewer", "Build a Flutter widget with Riverpod state management and BLoC"),
    ("harmonyos-app-resolver", "Develop a HarmonyOS application with ArkTS and ArkUI"),
    ("mobile-automation-engineer", "Set up Appium mobile automation test suite with WebdriverIO and Screen Object Model"),
    ("mobile-developer", "Create a mobile app screen in React Native with Expo navigation"),
    ("swift-build-resolver", "Xcode build failed with Swift compiler error and SPM dependency resolution"),
    ("swift-reviewer", "Implement SwiftUI navigation with async actor persistence and combine"),

    # Domain 3: Backend & Language Specialists
    ("backend-specialist", "Design a REST API server with middleware authentication and Express endpoints"),
    ("cpp-build-resolver", "CMake error with GCC linker undefined reference vtable during compilation"),
    ("cpp-reviewer", "Modern C++ smart pointers and RAII memory safety review"),
    ("csharp-reviewer", "C# ASP.NET Core API with Entity Framework LINQ queries"),
    ("django-build-resolver", "Django migration conflict when running makemigrations and pip conflict"),
    ("django-reviewer", "Implement Django ORM serializer with Celery background task"),
    ("fastapi-reviewer", "Create an async FastAPI router with Pydantic v2 validation"),
    ("fsharp-reviewer", "Implement F# discriminated unions with pattern matching and FsUnit tests"),
    ("go-build-resolver", "Go build error when compiling packages with go mod tidy"),
    ("go-reviewer", "Review my Golang code for goroutine leaks and channel deadlocks"),
    ("java-build-resolver", "Maven build failure with javac classpath dependency conflict"),
    ("java-reviewer", "Spring Boot REST controller with JPA Hibernate query optimization"),
    ("kotlin-build-resolver", "Kotlin compiler error in Gradle KTS build with kapt"),
    ("kotlin-reviewer", "Kotlin coroutines flow with Ktor client and KMP"),
    ("php-reviewer", "Laravel Eloquent model with artisan migration and PSR-12 standard"),
    ("python-reviewer", "Write pythonic code adhering to PEP8 with strict type hints and asyncio"),
    ("ruby-reviewer", "Ruby on Rails ActiveRecord query with RSpec tests and Gemfile"),
    ("rust-build-resolver", "Rustc compiler error: cannot borrow as mutable more than once"),
    ("rust-reviewer", "Review my Rust struct lifetimes and Tokio async tasks with cargo"),
    ("typescript-reviewer", "Complex TypeScript generics and conditional types with strict null checks"),

    # Domain 4: Database & Storage
    ("database-architect", "Design a PostgreSQL database schema with Prisma migrations and ER diagram"),
    ("database-reviewer", "Slow query optimization with EXPLAIN ANALYZE on 2M rows in Postgres"),

    # Domain 5: DevOps, Cloud & Network
    ("devops-engineer", "Create a production Dockerfile and GitHub Actions CI/CD deployment pipeline"),
    ("homelab-architect", "Configure Proxmox homelab with Pi-hole DNS and WireGuard VPN server"),
    ("network-architect", "Design enterprise network architecture with BGP routing and VPN topology"),
    ("network-config-reviewer", "Configure Cisco router ACL and switch config with netmiko automation"),
    ("network-troubleshooter", "Diagnose packet loss and DNS resolution failure on degraded interface"),

    # Domain 6: Cybersecurity & PenTest
    ("penetration-tester", "Red team penetration test with exploit payload simulation and privilege escalation"),
    ("security-auditor", "Perform an OWASP Top 10 security audit and vulnerability scan on auth endpoints"),
    ("security-reviewer", "Review code for SQL injection, XSS, and IDOR vulnerabilities"),

    # Domain 7: Testing, QA & Debugging
    ("build-error-resolver", "Resolve compilation failed syntax error during production bundle build"),
    ("debugger", "Investigate application crash with traceback and find root cause"),
    ("e2e-runner", "Run visual regression tests with headless browser run across viewports"),
    ("pr-test-analyzer", "Analyze PR test coverage gap and fix flaky tests missing assertions"),
    ("qa-automation-engineer", "Set up Playwright E2E browser automation test suite with Cypress"),
    ("silent-failure-hunter", "Detect silent failure where exception is swallowed by empty catch block"),
    ("tdd-guide", "Follow strict TDD red green refactor to write failing test first for discount calculation"),
    ("test-engineer", "Write comprehensive unit tests with mocks in pytest and vitest"),
    ("verify", "Execute verify all validation checks to prove it works before release"),

    # Domain 8: Architecture, Refactoring & Code Quality
    ("architect", "Draw high level architecture of the project with archify sequence diagram"),
    ("code-archaeologist", "Analyze legacy code to understand old codebase and reverse engineer undocumented logic"),
    ("code-architect", "Design a class diagram following OOP design principles and dependency inversion"),
    ("code-reviewer", "Perform thorough code review on this PR with security and quality checklist"),
    ("code-simplifier", "This 400-line function is too complex and overcomplicated, simplify code"),
    ("comment-analyzer", "Review code comments, ensure meaningful docstrings, and remove emojis from code"),
    ("commit-reviewer", "Review conventional commits format and validate git history messages"),
    ("refactor-cleaner", "Clean dead code, remove unused imports and remove orphan functions"),
    ("reverse-engineering-anything", "Like Google Photos, create a search functionality for my software with REA"),
    ("spec-miner", "Extract behavioral spec and openspec system invariants from tests"),
    ("type-design-analyzer", "Perform type modeling with domain invariants and strong typing guarantees"),

    # Domain 9: Exploration, Documentation & Planning
    ("code-explorer", "Trace caller hierarchy and find usages for this function across files"),
    ("conversation-analyzer", "Analyze conversation transcript to synthesize decisions and action items"),
    ("doc-updater", "Update docs and sync README with latest API changes"),
    ("docs-lookup", "Lookup docs for official syntax and usage of this new library"),
    ("documentation-writer", "Write comprehensive technical guide and user manual architecture document"),
    ("explore", "Perform read-only reconnaissance to map callers and tests for quick repo survey"),
    ("explorer-agent", "Explore codebase and map architecture boundaries across directories"),
    ("plan", "Create an adversarial plan anticipating failure modes and edge cases"),
    ("planner", "Formulate a feature planning roadmap for the upcoming refactoring phase"),
    ("product-manager", "Draft product requirements document PRD with user problem statement"),
    ("product-owner", "Refine user story backlog with testable acceptance criteria"),
    ("project-planner", "Develop 4-phase project implementation plan with milestones and task breakdown"),

    # Understand-Anything Specialist Sub-agents
    ("architecture-analyzer", "Run architecture analyzer to assign files to architectural layers"),
    ("article-analyzer", "Execute article analyzer to extract markdown graph and wiki entity relationships"),
    ("assemble-reviewer", "Run assemble reviewer to merge-batch-graphs and assemble knowledge graph"),
    ("design-analyzer", "Use design analyzer to parse Figma structural nodes from figma manifest"),
    ("domain-analyzer", "Run domain analyzer to extract business domain knowledge and process steps"),
    ("file-analyzer", "Execute file analyzer for batch file analysis and extract file symbols"),
    ("graph-reviewer", "Run graph reviewer to validate knowledge graph and render quality approval"),
    ("knowledge-graph-guide", "Consult knowledge graph guide to query knowledge graph and navigate relationships"),
    ("project-scanner", "Run project scanner to generate project inventory and framework detection"),
    ("tour-builder", "Use tour builder to design guided learning tour through codebase"),
    ("understand-anything", "I got a new project which is unknown for me, explain me project e2e and its architecture"),

    # Orchestration, Loop & Multi-Agent Swarm
    ("chief-of-staff", "Personal chief of staff to triage email and triage Slack channels"),
    ("coordinator", "Act as coordination agent for single-agent execution and task handoffs"),
    ("loop-operator", "Operate autonomous agent loop and intervene on stalled loop execution"),
    ("orchestrator", "I want a multi agent system where agents communicate and share context on runtime complexity"),

    # Quality, Evaluation & Open Source Packaging
    ("agent-evaluator", "Perform agent evaluation using 5-axis quality rubric to score agent output"),
    ("gan-evaluator", "Run GAN evaluator in GAN harness to score application against spec"),
    ("gan-generator", "Run GAN generator to implement from GAN spec according to evaluation"),
    ("gan-planner", "Run GAN planner to expand one-line prompt into full product spec"),
    ("harness-optimizer", "Execute harness optimizer to tune agent-harness config using eval-driven grading"),
    ("opensource-forker", "Use opensource forker to fork for open-sourcing and strip secrets for fork"),
    ("opensource-packager", "Use opensource packager to prepare open-source release with packaging"),
    ("opensource-sanitizer", "Use opensource sanitizer to sanitize open-source fork and scan for leaked secrets"),

    # Specialized Domains & Fallbacks
    ("bengali-reviewer", "Review Bengali text for bangla conjuncts and unicode normalization"),
    ("game-developer", "Build a 2D arcade game in Phaser with physics and sprite animation"),
    ("healthcare-reviewer", "Audit clinical health data pipeline for HIPAA compliance and PHI security"),
    ("ai-engineer", "Build an agentic framework in LangGraph with human-in-the-loop, vectorless PageIndex RAG, and vLLM inference engineering"),
    ("ml-engineer", "Implement custom multi-head attention with FlashAttention, RoPE positional encoding, and QLoRA fine-tuning"),
    ("marketing-agent", "Write high converting marketing copy and audience research for marketing campaign"),
    ("mle-reviewer", "Review machine learning engineering training loop and model eval dataset contract"),
    ("performance-optimizer", "Profile performance and fix memory leak causing high CPU spikes"),
    ("pytorch-build-resolver", "Fix PyTorch error with CUDA out of memory and tensor mismatch"),
    ("rag-pipeline-reviewer", "Design RAG pipeline with vector DB embeddings and semantic chunking"),
    ("seo-specialist", "Optimize Core Web Vitals, JSON-LD Schema.org, and technical SEO metadata"),
    ("general", "Answer this general programming question about basic algorithm principles")
]

def run_108_test_suite():
    print("=" * 80)
    print(f"      ANTIGRAVITY 110-AGENT COMPREHENSIVE INTELLIGENT ROUTING TEST SUITE      ")
    print("=" * 80)
    print(f"Total Agents to Validate: {len(PROMPTS_108)}")
    print("-" * 80)

    passed_count = 0
    failed_count = 0
    results = []

    start_time = time.time()

    for idx, (expected_agent, prompt) in enumerate(PROMPTS_108, 1):
        routed_agent, skills, method = IntelligentRouter.route(prompt)
        is_pass = (routed_agent == expected_agent)

        status_str = "[PASS]" if is_pass else "[FAIL]"
        if is_pass:
            passed_count += 1
        else:
            failed_count += 1

        results.append({
            "id": idx,
            "expected_agent": expected_agent,
            "routed_agent": routed_agent,
            "passed": is_pass,
            "skills": skills,
            "prompt": prompt,
            "method": method
        })

        skills_str = ", ".join(skills[:2]) if skills else "none"
        if is_pass:
            print(f"{idx:3d}. {status_str} {expected_agent:<28} <- '{prompt[:45]}...' ({skills_str})")
        else:
            print(f"{idx:3d}. {status_str} EXPECTED: {expected_agent:<20} GOT: {routed_agent:<20} <- '{prompt[:40]}...'")

    duration = time.time() - start_time
    print("=" * 80)
    print(f"TEST RUN COMPLETED in {duration:.3f}s")
    print(f"Passed: {passed_count} / {len(PROMPTS_108)} ({passed_count/len(PROMPTS_108)*100:.1f}%)")
    print(f"Failed: {failed_count} / {len(PROMPTS_108)}")
    print("=" * 80)

    # Save structured results
    report_file = Path(".agent/scripts/test_results_108.json")
    report_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Detailed JSON results written to {report_file}")

    return passed_count == len(PROMPTS_108)

if __name__ == "__main__":
    success = run_108_test_suite()
    sys.exit(0 if success else 1)

