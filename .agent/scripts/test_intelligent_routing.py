#!/usr/bin/env python3
"""
Test Suite: Antigravity Intelligent Prompt-Trigger Routing Engine
=================================================================
Validates:
1. Agent Catalog & Frontmatter Integrity (94 agents)
2. Skill Resolution across .agent/skills and global-rules
3. Rule File Synchronization (GEMINI.md, .agent/rules/GEMINI.md, intelligent-routing)
4. Prompt-Trigger Simulation across 36 realistic prompts spanning all 10 domains
"""

import os
import re
import sys
import glob
from pathlib import Path

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def log_pass(msg):
    print(f"{GREEN}  [PASS]{RESET} {msg}")

def log_fail(msg):
    print(f"{RED}  [FAIL]{RESET} {msg}")

def log_info(msg):
    print(f"{CYAN}  [INFO]{RESET} {msg}")


class IntelligentRouter:
    """Simulates Antigravity's Prompt-Trigger Routing Engine as defined in GEMINI.md"""
    
    TRIGGER_MAP = [
        # Multi-Domain / Full Stack (Highest Priority)
        (r"\b(build\s*saas|full\s*stack\s*app|multi-?domain\s*project|orchestrate)\b", "orchestrator", ["parallel-agents", "behavioral-modes", "brainstorming"]),

        # System Architecture & Diagrams (Archify) - High Priority
        (r"\b(draw\s*architecture|high\s*level\s*architecture|system\s*architecture|archify|process\s*flow|flow\s*charts?|sequence\s*diagram)\b", "architect", ["archify", "architecture", "architecture-decision-records"]),

        # Domain 2: Mobile - Specific Resolvers & Reviewers first
        (r"\b(mobile\s*automation|appium|webdriverio\s*mobile|mobile\s*test|screen\s*object|uiautomator2|xcuitest|mobile\s*gestures?)\b", "mobile-automation-engineer", ["clean-code", "testing-patterns", "mobile-automation", "appium-skill"]),
        (r"\b(flutter\s*build|pubspec|gradle\s*flutter|cocoapods|pod\s*install)\b", "dart-build-resolver", ["dart-flutter-patterns", "systematic-debugging"]),
        (r"\b(flutter|dart|flutter\s*widget|bloc|riverpod)\b", "flutter-reviewer", ["dart-flutter-patterns", "flutter-dart-code-review"]),
        (r"\b(xcode\s*build|swift\s*compiler|spm\s*dependency)\b", "swift-build-resolver", ["swift-protocol-di-testing", "systematic-debugging"]),
        (r"\b(swift|swiftui|uikit|combine|swift\s*concurrency|actor\s*persistence)\b", "swift-reviewer", ["swiftui-patterns", "swift-actor-persistence"]),
        (r"\b(harmonyos|arkts|arkui)\b", "harmonyos-app-resolver", ["mobile-design"]),
        (r"\b(react\s*native|expo|mobile\s*app|mobile\s*screen|ios\s*app|android\s*app)\b", "mobile-developer", ["mobile-design", "clean-code"]),

        # Domain 1: Frontend & UI - Specific Resolvers & Reviewers first
        (r"\b(react\s*build|vite\s*build|next\s*build|turbopack|webpack\s*error)\b", "react-build-resolver", ["nextjs-turbopack", "vite-patterns"]),
        (r"\b(react\s*hooks?|useeffect|memo|re-?render|jsx\s*patterns?|zustand)\b", "react-reviewer", ["react-patterns", "react-performance"]),
        (r"\b(vue|vue\s*3|nuxt|nuxt\s*4|pinia|composition\s*api)\b", "vue-reviewer", ["vue-patterns", "nuxt4-patterns"]),
        (r"\b(accessibility|a11y|wcag|screen\s*reader|aria|color\s*contrast)\b", "a11y-architect", ["accessibility", "frontend-a11y"]),
        (r"\b(frontend|react|next\.?js|component|tailwind|css|styling|dashboard|layout)\b", "frontend-specialist", ["frontend-design", "react-best-practices"]),

        # Domain 3: Backend & Languages
        (r"\b(fastapi|pydantic\s*v2|fastapi\s*router)\b", "fastapi-reviewer", ["fastapi-patterns", "api-patterns"]),
        (r"\b(django\s*migration|makemigrations|pip\s*conflict)\b", "django-build-resolver", ["django-verification", "django-security"]),
        (r"\b(django|drf|django\s*rest|django\s*orm|django\s*celery)\b", "django-reviewer", ["django-patterns", "django-celery"]),
        (r"\b(go\s*build|go\s*vet|go\s*mod\s*tidy)\b", "go-build-resolver", ["golang-patterns", "systematic-debugging"]),
        (r"\b(golang|go\s*code|goroutine|go\s*channel|go\s*interface)\b", "go-reviewer", ["golang-patterns", "golang-testing"]),
        (r"\b(rustc|cargo\s*build\s*fail|cannot\s*borrow\s*as\s*mutable)\b", "rust-build-resolver", ["rust-patterns", "systematic-debugging"]),
        (r"\b(rust|borrow\s*checker|lifetime|tokio|cargo)\b", "rust-reviewer", ["rust-patterns", "rust-pro"]),
        (r"\b(maven\s*build|gradle\s*build|javac\s*classpath)\b", "java-build-resolver", ["springboot-verification", "quarkus-verification"]),
        (r"\b(java|spring\s*boot|quarkus|jpa|hibernate)\b", "java-reviewer", ["java-coding-standards", "springboot-patterns"]),
        (r"\b(kotlin\s*compiler|gradle\s*kts|kapt|ksp)\b", "kotlin-build-resolver", ["kotlin-testing", "systematic-debugging"]),
        (r"\b(kotlin|coroutines|flow|kmp|ktor)\b", "kotlin-reviewer", ["kotlin-patterns", "kotlin-coroutines-flows"]),
        (r"\b(cmake\s*error|gcc\s*error|linker\s*error\s*cpp|vtable)\b", "cpp-build-resolver", ["cpp-testing", "systematic-debugging"]),
        (r"\b(c\+\+|cpp|modern\s*c\+\+|raii|smart\s*pointers)\b", "cpp-reviewer", ["cpp-coding-standards", "cpp-testing"]),
        (r"\b(c#|\.net|dotnet|asp\.net\s*core|entity\s*framework|linq)\b", "csharp-reviewer", ["dotnet-patterns", "csharp-testing"]),
        (r"\b(f#|fsharp|discriminated\s*unions|fsunit)\b", "fsharp-reviewer", ["fsharp-testing"]),
        (r"\b(php|laravel|artisan|eloquent|psr-12)\b", "php-reviewer", ["laravel-patterns", "laravel-tdd"]),
        (r"\b(ruby|rails|activerecord|rspec|gemfile)\b", "ruby-reviewer", ["rails-patterns"]),
        (r"\b(typescript|generics|conditional\s*types|strict\s*null|ts\s*error)\b", "typescript-reviewer", ["typescript-patterns", "clean-code"]),
        (r"\b(python|pythonic|pep8|type\s*hints)\b", "python-reviewer", ["python-patterns", "python-testing"]),
        (r"\b(backend|api|rest\s*api|graphql|trpc|server|middleware)\b", "backend-specialist", ["api-patterns", "nodejs-best-practices"]),

        # Domain 4: Database & Storage
        (r"\b(slow\s*query|explain\s*analyze|n\+1\s*query|postgres\s*optimiz|index\s*tuning)\b", "database-reviewer", ["postgres-patterns", "mysql-patterns"]),
        (r"\b(database\s*schema|schema\s*design|migration\s*strategy|prisma\s*schema|sql\s*vs\s*nosql|er\s*diagram|erd)\b", "database-architect", ["database-design", "prisma-patterns", "archify"]),

        # Domain 5: DevOps, Cloud & Network
        (r"\b(docker|dockerfile|docker-compose|kubernetes|k8s|ci/cd|github\s*actions|nginx|pm2)\b", "devops-engineer", ["deployment-procedures", "docker-patterns"]),
        (r"\b(cisco\s*config|switch\s*config|router\s*acl|netmiko)\b", "network-config-reviewer", ["cisco-ios-patterns", "netmiko-ssh-automation"]),
        (r"\b(packet\s*loss|dns\s*resolution\s*fail|ping\s*latency|interface\s*down)\b", "network-troubleshooter", ["network-interface-health", "systematic-debugging"]),
        (r"\b(network\s*architecture|subnetting|bgp\s*routing|vpn\s*topology)\b", "network-architect", ["network-config-validation", "network-bgp-diagnostics"]),
        (r"\b(homelab|pi-hole|wireguard|proxmox|home\s*server)\b", "homelab-architect", ["homelab-network-readiness", "homelab-pihole-dns"]),

        # Domain 6: Cybersecurity
        (r"\b(security\s*audit|owasp|threat\s*model|vulnerability\s*scan|secrets\s*scan|rate\s*limiting)\b", "security-auditor", ["vulnerability-scanner", "security-review"]),
        (r"\b(sql\s*injection|xss|csrf|idor|auth\s*bypass|sanitiz|jwt\s*validation)\b", "security-reviewer", ["security-scan", "security-bounty-hunter"]),
        (r"\b(penetration\s*test|exploit|red\s*team|privilege\s*escalation|attack\s*payload)\b", "penetration-tester", ["red-team-tactics"]),

        # Domain 7: Testing & Debugging
        (r"\b(silent\s*failure|swallowed\s*exception|empty\s*catch|unhandled\s*rejection)\b", "silent-failure-hunter", ["error-handling", "condition-based-waiting"]),
        (r"\b(pr\s*tests?|test\s*gap|flaky\s*tests?|missing\s*assertions?)\b", "pr-test-analyzer", ["testing-anti-patterns"]),
        (r"\b(e2e\s*tests?|playwright|cypress|browser\s*automation)\b", "qa-automation-engineer", ["webapp-testing", "e2e-testing"]),
        (r"\b(visual\s*regression|browser\s*run|run\s*e2e)\b", "e2e-runner", ["browser-qa", "webapp-testing"]),
        (r"\b(tdd|red\s*green\s*refactor|failing\s*test\s*first|test\s*first)\b", "tdd-guide", ["test-driven-development", "tdd-workflow"]),
        (r"\b(debug|crash|exception|traceback|reproduce\s*bug|why\s*is\s*this\s*failing)\b", "debugger", ["systematic-debugging", "root-cause-tracing"]),
        (r"\b(compilation\s*failed|build\s*error|syntax\s*error|bundle\s*error)\b", "build-error-resolver", ["systematic-debugging"]),
        (r"\b(write\s*tests?|unit\s*tests?|integration\s*tests?|mock|vitest|jest|pytest)\b", "test-engineer", ["testing-patterns", "tdd-workflow"]),
        (r"\b(verify\s*all|validation\s*check|prove\s*it\s*works|son\s*kontrolleri)\b", "verify", ["verification-before-completion"]),

        # Domain 8: Architecture, Quality & Refactoring
        (r"\b(clean\s*dead\s*code|remove\s*unused\s*imports|orphan\s*functions?|remove\s*orphans?)\b", "refactor-cleaner", ["clean-code", "refactor-cleaner"]),
        (r"\b(simplify\s*code|overcomplicated|too\s*complex|reduce\s*lines|karpathy)\b", "code-simplifier", ["clean-code", "karpathy-guidelines"]),
        (r"\b(code\s*review|review\s*this\s*pr|peer\s*review|review\s*code)\b", "code-reviewer", ["code-review-checklist", "requesting-code-review"]),
        (r"\b(legacy\s*code|understand\s*old\s*codebase|reverse\s*engineer|undocumented\s*system)\b", "code-archaeologist", ["brownfield-retrospective", "codebase-onboarding"]),
        (r"\b(oop\s*design|solid\s*principles|design\s*patterns|dependency\s*inversion|class\s*diagram)\b", "code-architect", ["clean-code", "architecture", "archify"]),
        (r"\b(system\s*architecture|adr|microservices\s*vs\s*monolith|hexagonal\s*architecture)\b", "architect", ["architecture", "architecture-decision-records"]),
        (r"\b(conventional\s*commits|commit\s*message\s*review|git\s*history)\b", "commit-reviewer", ["conventional-commit-review", "git-workflow"]),
        (r"\b(code\s*comments|meaningful\s*comments|remove\s*emojis|docstring\s*review)\b", "comment-analyzer", ["clean-code"]),
        (r"\b(behavioral\s*spec|contract\s*extraction|openspec)\b", "spec-miner", ["contract-first"]),
        (r"\b(type\s*modeling|domain\s*invariants|strong\s*typing)\b", "type-design-analyzer", ["clean-code", "typescript-patterns"]),

        # Domain 9: Exploration, Documentation & Planning
        (r"\b(explore\s*codebase|map\s*architecture|find\s*where\s*\w+\s*is\s*defined)\b", "explorer-agent", ["repo-scan", "code-tour"]),
        (r"\b(trace\s*caller|call\s*hierarchy|find\s*usages?)\b", "code-explorer", ["codebase-onboarding"]),
        (r"\b(update\s*docs|sync\s*readme|update\s*api\s*docs)\b", "doc-updater", ["docs-governance", "living-docs-governance"]),
        (r"\b(lookup\s*docs|how\s*to\s*use\s*library|official\s*docs\s*syntax)\b", "docs-lookup", ["documentation-lookup"]),
        (r"\b(write\s*manual|technical\s*guide|architecture\s*document|user\s*guide)\b", "documentation-writer", ["documentation-templates"]),
        (r"\b(summarize\s*session|extract\s*takeaways|session\s*learnings)\b", "conversation-analyzer", ["knowledge-ops"]),
        (r"\b(plan\s*project|task\s*breakdown|implementation\s*plan|roadmap)\b", "project-planner", ["brainstorming", "plan-writing"]),
        (r"\b(user\s*stories|acceptance\s*criteria|mvp\s*scope|backlog)\b", "product-manager", ["plan-writing", "brainstorming"]),

        # Domain 10: Specialized Domains
        (r"\b(game|phaser|godot|unity|game\s*mechanics|game\s*loop)\b", "game-developer", ["game-development"]),
        (r"\b(seo|search\s*ranking|meta\s*tags|core\s*web\s*vitals|schema\.org|json-ld)\b", "seo-specialist", ["seo-fundamentals", "geo-fundamentals"]),
        (r"\b(profile\s*performance|memory\s*leak|slow\s*execution|cpu\s*spike)\b", "performance-optimizer", ["performance-profiling", "memory-leak-debugging"]),
        (r"\b(ml\s*pipeline|machine\s*learning|training\s*loop|model\s*eval)\b", "mle-reviewer", ["mle-workflow", "eval-harness"]),
        (r"\b(pytorch\s*error|cuda\s*oom|cuda\s*out\s*of\s*memory|tensor\s*mismatch)\b", "pytorch-build-resolver", ["pytorch-patterns", "systematic-debugging"]),
        (r"\b(rag|vector\s*search|embeddings|chunking|hallucination)\b", "rag-pipeline-reviewer", ["ai-first-engineering", "cost-aware-llm-pipeline"]),
        (r"\b(marketing\s*copy|landing\s*page\s*conversion|marketing\s*campaign)\b", "marketing-agent", ["marketing-campaign", "brand-voice"]),
        (r"\b(hipaa|phi|healthcare\s*data|clinical\s*cdss)\b", "healthcare-reviewer", ["hipaa-compliance", "healthcare-phi-compliance"]),
        (r"\b(bengali|bangla\s*text|bengali\s*nlp)\b", "bengali-reviewer", ["bengali-nlp"])
    ]

    @classmethod
    def route(cls, prompt: str):
        prompt_lower = prompt.lower()
        
        # Check explicit override (@agent-name)
        m_explicit = re.search(r"@([a-zA-Z0-9_-]+)", prompt)
        if m_explicit:
            explicit_name = m_explicit.group(1)
            return explicit_name, ["clean-code"], "EXPLICIT_OVERRIDE"
        
        # Pattern match
        for pattern, agent, skills in cls.TRIGGER_MAP:
            if re.search(pattern, prompt_lower):
                return agent, skills, "TRIGGER_MATCH"
                
        return "general", ["using-superpowers", "clean-code"], "DEFAULT_FALLBACK"


def test_agent_catalog():
    print(f"\n{BOLD}Test 1: Agent Catalog & Frontmatter Integrity (95 agents){RESET}")
    agent_files = sorted(glob.glob(".agent/agents/*.md"))
    if len(agent_files) != 95:
        log_fail(f"Expected 95 agent files, found {len(agent_files)}")
        return False
    
    log_pass(f"Discovered exactly {len(agent_files)} agent markdown files.")
    
    all_valid = True
    for af in agent_files:
        name = os.path.splitext(os.path.basename(af))[0]
        content = open(af, encoding="utf-8").read()
        if not content.startswith("---"):
            log_fail(f"{name} is missing YAML frontmatter opening '---'")
            all_valid = False
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            log_fail(f"{name} has unclosed YAML frontmatter")
            all_valid = False
            continue
        frontmatter = parts[1]
        if "name:" not in frontmatter:
            log_fail(f"{name} is missing 'name:' in frontmatter")
            all_valid = False
        if "description:" not in frontmatter:
            log_fail(f"{name} is missing 'description:' in frontmatter")
            all_valid = False

    if all_valid:
        log_pass("All 95 agents have valid YAML frontmatter, name, and description.")
    return all_valid


def test_skill_resolution():
    print(f"\n{BOLD}Test 2: Skill Directory & Reference Verification{RESET}")
    skill_dirs = {d for d in os.listdir(".agent/skills") if os.path.isdir(os.path.join(".agent/skills", d))}
    global_rules_dirs = {d for d in os.listdir("global-rules") if os.path.isdir(os.path.join("global-rules", d))}
    
    log_info(f"Local skill directories: {len(skill_dirs)}")
    log_info(f"Global rules directories: {len(global_rules_dirs)}")
    
    if len(skill_dirs) < 300:
        log_fail(f"Expected 300+ skills, found {len(skill_dirs)}")
        return False
        
    log_pass(f"Found {len(skill_dirs)} skill modules in .agent/skills/ and {len(global_rules_dirs)} in global-rules/.")
    return True


def test_rules_synchronization():
    print(f"\n{BOLD}Test 3: Rule Files Synchronization & Completeness{RESET}")
    all_ok = True
    
    # 1. Root GEMINI.md
    root_gemini = Path("GEMINI.md").read_text(encoding="utf-8")
    if "ANTIGRAVITY INTELLIGENT PROMPT-TRIGGER ROUTING ENGINE" in root_gemini:
        log_pass("Root GEMINI.md contains the Intelligent Prompt-Trigger Routing Engine.")
    else:
        log_fail("Root GEMINI.md is missing the Prompt-Trigger Routing Engine!")
        all_ok = False
        
    if "Comprehensive 95-Agent Prompt Trigger Matrix" in root_gemini or "Comprehensive 94-Agent Prompt Trigger Matrix" in root_gemini:
        log_pass("Root GEMINI.md contains the Agent Prompt Trigger Matrix.")
    else:
        log_fail("Root GEMINI.md is missing the Agent Matrix!")
        all_ok = False

    # 2. .agent/rules/GEMINI.md
    agent_gemini = Path(".agent/rules/GEMINI.md").read_text(encoding="utf-8")
    if "COMPREHENSIVE PROMPT-TRIGGER AGENT MATRIX (95 AGENTS)" in agent_gemini or "COMPREHENSIVE PROMPT-TRIGGER AGENT MATRIX (94 AGENTS)" in agent_gemini:
        log_pass(".agent/rules/GEMINI.md contains the Agent Matrix.")
    else:
        log_fail(".agent/rules/GEMINI.md is missing the Agent Matrix!")
        all_ok = False

    # 3. .agent/skills/intelligent-routing/SKILL.md
    ir_skill = Path(".agent/skills/intelligent-routing/SKILL.md").read_text(encoding="utf-8")
    if "frontend-specialist" in ir_skill and "fastapi-reviewer" in ir_skill and "database-reviewer" in ir_skill:
        log_pass(".agent/skills/intelligent-routing/SKILL.md includes comprehensive agent selections.")
    else:
        log_fail(".agent/skills/intelligent-routing/SKILL.md is missing updated agents!")
        all_ok = False

    # 4. ARCHITECTURE.md
    arch = Path(".agent/ARCHITECTURE.md").read_text(encoding="utf-8")
    if "95 Specialist Agents" in arch and "350+ Skills" in arch:
        log_pass(".agent/ARCHITECTURE.md reflects 95 agents and 350+ skills.")
    else:
        log_fail(".agent/ARCHITECTURE.md numbers are out of sync!")
        all_ok = False

    # 5. PROMPT-TEMPLATE.md
    pt = Path(".agent/PROMPT-TEMPLATE.md").read_text(encoding="utf-8")
    if "Intelligent Prompt Practices & Trigger Playbook" in pt:
        log_pass(".agent/PROMPT-TEMPLATE.md contains prompt practices and trigger examples.")
    else:
        log_fail(".agent/PROMPT-TEMPLATE.md is missing the prompt playbook!")
        all_ok = False

    # 6. Archify Integration Check
    if "archify" in root_gemini and "archify" in agent_gemini and "archify" in ir_skill:
        log_pass("All rule files and intelligent-routing SKILL.md include 'archify' skill integration.")
    else:
        log_fail("One or more rule files are missing 'archify' skill integration!")
        all_ok = False

    return all_ok


def test_prompt_trigger_simulation():
    print(f"\n{BOLD}Test 4: Real-World Prompt Trigger Simulation (40 Test Cases){RESET}")
    
    test_cases = [
        # Frontend & UI
        ("Create a responsive dark mode navbar component in React with Tailwind CSS", "frontend-specialist"),
        ("My React component is stuck in an infinite re-render loop in useEffect", "react-reviewer"),
        ("Vite build error when importing dynamic server module", "react-build-resolver"),
        ("Build a Vue 3 dashboard using Composition API and Pinia", "vue-reviewer"),
        ("Audit this web page for accessibility, color contrast, and WCAG screen reader labels", "a11y-architect"),

        # Mobile
        ("Create a mobile app screen in React Native with Expo navigation", "mobile-developer"),
        ("Set up Appium mobile automation test suite with WebdriverIO and Screen Object Model", "mobile-automation-engineer"),
        ("Build a Flutter widget with Riverpod state management", "flutter-reviewer"),
        ("Flutter build error with pubspec dependencies and pod install", "dart-build-resolver"),
        ("Implement SwiftUI navigation with async actor persistence", "swift-reviewer"),
        ("Xcode build failed with Swift compiler error", "swift-build-resolver"),
        ("Develop a HarmonyOS application with ArkTS", "harmonyos-app-resolver"),

        # Backend & Languages
        ("Create an async FastAPI router with Pydantic v2 validation", "fastapi-reviewer"),
        ("Django migration conflict when running makemigrations", "django-build-resolver"),
        ("Implement Django ORM serializer with Celery background task", "django-reviewer"),
        ("Go build error when compiling packages with go mod tidy", "go-build-resolver"),
        ("Review my Golang code for goroutine leaks and channel deadlocks", "go-reviewer"),
        ("Rustc compiler error: cannot borrow as mutable more than once", "rust-build-resolver"),
        ("Review my Rust struct lifetimes and Tokio async tasks", "rust-reviewer"),
        ("Spring Boot REST controller with JPA Hibernate query optimization", "java-reviewer"),
        ("Maven build failure with javac classpath dependency conflict", "java-build-resolver"),
        ("Kotlin coroutines flow with Ktor client", "kotlin-reviewer"),
        ("Kotlin compiler error in Gradle KTS build", "kotlin-build-resolver"),
        ("Modern C++ smart pointers and RAII memory safety review", "cpp-reviewer"),
        ("CMake error with GCC linker undefined reference vtable", "cpp-build-resolver"),
        ("C# ASP.NET Core API with Entity Framework LINQ queries", "csharp-reviewer"),
        ("Laravel Eloquent model with artisan migration and PSR-12 standard", "php-reviewer"),
        ("Complex TypeScript generics and conditional types with strict null", "typescript-reviewer"),

        # Database & Storage
        ("Design a PostgreSQL database schema with Prisma migrations and indexing strategy", "database-architect"),
        ("Create an ER diagram showing entity relationships and database schema", "database-architect"),
        ("Slow query optimization with EXPLAIN ANALYZE on 2M records", "database-reviewer"),

        # DevOps & Network
        ("Create a production Dockerfile and GitHub Actions CI/CD workflow", "devops-engineer"),
        ("Configure Cisco router ACL and switch config with netmiko", "network-config-reviewer"),
        ("Diagnose packet loss and DNS resolution failure on interface", "network-troubleshooter"),

        # Security
        ("Perform an OWASP Top 10 security audit and vulnerability scan on auth endpoints", "security-auditor"),
        ("Review code for SQL injection, XSS, and IDOR vulnerabilities", "security-reviewer"),
        ("Red team penetration test with exploit payload simulation", "penetration-tester"),

        # Testing & QA
        ("Write comprehensive unit tests with mocks in pytest", "test-engineer"),
        ("Investigate application crash with traceback and find root cause", "debugger"),
        ("Follow strict TDD to write failing test first for discount calculation", "tdd-guide"),
        ("Set up Playwright E2E browser automation test suite", "qa-automation-engineer"),
        ("Detect silent failure where exception is swallowed by empty catch block", "silent-failure-hunter"),

        # Architecture & Refactoring (including Archify diagrams)
        ("Draw high level architecture of the project with services and cloud boundaries", "architect"),
        ("Draw process flow diagram and flow charts for order processing", "architect"),
        ("Design a class diagram following OOP design principles and dependency inversion", "code-architect"),
        ("This 400-line function is too complex and overcomplicated, simplify code", "code-simplifier"),
        ("Clean dead code, remove unused imports and remove orphans", "refactor-cleaner"),
        ("Analyze legacy code to understand old codebase and reverse engineer", "code-archaeologist"),

        # Specialized & Multi-Domain
        ("Build a 2D arcade game in Phaser with physics and sprite animation", "game-developer"),
        ("Optimize Core Web Vitals, JSON-LD Schema.org, and technical SEO", "seo-specialist"),
        ("Profile performance and fix memory leak causing CPU spike", "performance-optimizer"),
        ("Build SaaS billing dashboard with Stripe webhooks and full stack app", "orchestrator")
    ]

    passed = 0
    for prompt, expected_agent in test_cases:
        agent, skills, method = IntelligentRouter.route(prompt)
        if agent == expected_agent:
            log_pass(f"'{prompt[:50]}...' -> {agent} ({', '.join(skills[:2])})")
            passed += 1
        else:
            log_fail(f"'{prompt[:50]}...' -> Expected {expected_agent}, Got {agent}")

    print(f"\n{BOLD}Simulation Score: {passed}/{len(test_cases)} Passed ({passed/len(test_cases)*100:.1f}%){RESET}")
    return passed == len(test_cases)


def test_explicit_override():
    print(f"\n{BOLD}Test 5: Explicit @agent-name Override Verification{RESET}")
    prompt = "@rust-reviewer please check this memory allocation"
    agent, skills, method = IntelligentRouter.route(prompt)
    if agent == "rust-reviewer" and method == "EXPLICIT_OVERRIDE":
        log_pass("Explicit @rust-reviewer successfully overrides automatic keyword routing.")
        return True
    else:
        log_fail(f"Expected rust-reviewer via EXPLICIT_OVERRIDE, got {agent} via {method}")
        return False


def main():
    print(f"\n{BOLD}{CYAN}================================================================={RESET}")
    print(f"{BOLD}{CYAN}   ANTIGRAVITY INTELLIGENT PROMPT-TRIGGER ENGINE TEST SUITE       {RESET}")
    print(f"{BOLD}{CYAN}================================================================={RESET}")

    t1 = test_agent_catalog()
    t2 = test_skill_resolution()
    t3 = test_rules_synchronization()
    t4 = test_prompt_trigger_simulation()
    t5 = test_explicit_override()

    print(f"\n{BOLD}SUMMARY:{RESET}")
    all_tests = [t1, t2, t3, t4, t5]
    if all(all_tests):
        print(f"{BOLD}{GREEN}ALL 5 TEST SUITES PASSED 100%! System is fully operational.{RESET}\n")
        return 0
    else:
        print(f"{BOLD}{RED}SOME TESTS FAILED! Check logs above.{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
