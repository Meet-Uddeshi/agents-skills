---
trigger: always_on
---

# ANTIGRAVITY INTELLIGENT PROMPT-TRIGGER ROUTING ENGINE & SPECIALIST MATRIX

> **MANDATORY AUTO-ROUTING PROTOCOL**: Before generating any response or taking any action, Antigravity MUST automatically analyze the user's prompt, match trigger keywords and intent, and auto-activate the appropriate specialist agent(s) and skill(s). This applies universally in single projects and across global multi-project environments.

---

## 1. Auto-Activation Execution Protocol

Whenever a user prompt is received:
1. **Analyze (Silent)**: Scan the prompt for keywords, technical stack, problem domain, and complexity.
2. **Fast-Path vs Specialist Activation**:
   - **Fast-Path (User-Provided Solutions, Questions, Trivial Edits)**: If the prompt contains the fix/solution, is a simple question, or is a small edit, respond directly, immediately, and concisely with ZERO skill loading, ZERO agent headers, and ZERO thinking loops.
   - **Specialist Path (Complex Code, Architecture, Debugging, Multi-file without Solution)**: Select specialist agent(s) and skill(s), output the announcement header, and apply specialist rigor.
3. **Mandatory Announcement Header (Specialist Path Only)**: Output the specialist declaration:
   ```markdown
   🤖 **Applying knowledge of @[agent-name]...**
   I am using the [Skill Name] skill to [specific action].
   ```
4. **Load Knowledge & Enforce Constraints**: For specialist path tasks, read the agent instructions from `.agent/agents/{agent}.md` (or global `~/.gemini/config/agents/{agent}.md`) and skill instructions from `.agent/skills/{skill}/SKILL.md` (or global `~/.gemini/config/skills/{skill}/SKILL.md` or `global-rules/{skill}/SKILL.md`).
5. **Apply Strict Persona & Workflow**: Embody the specialist's depth, adherence to standards, and verification rigor.

---

## 2. Universal Request Classifier

| Request Classification | Trigger Patterns & Keywords | Primary Mode / Tier | Action & Output Requirement |
| :--- | :--- | :--- | :--- |
| **QUESTION / EXPLAIN** | "what is", "how does", "explain", "compare", "why does" | Direct Insight | Concise technical explanation with examples; no unnecessary file mutations. |
| **SURVEY / RECON** | "analyze", "list files", "overview", "map architecture", "explore" | Explorer Mode | Comprehensive reconnaissance; caller/callee graphs; no code mutation. |
| **BUG / INCIDENT** | "error", "bug", "fails", "crash", "401/403/500", "broken", "issue" | Debugging Tier | Systematic 4-phase debugging; reproduce with test; isolate root cause before fix. |
| **FEATURE / BUILD** | "build", "create", "implement", "add endpoint", "new feature" | Socratic + Plan | Pass Socratic Gate (ask 3 strategic questions); bite-sized plan; TDD RED-GREEN-REFACTOR. |
| **UI / DESIGN** | "design", "UI", "UX", "component", "styling", "layout", "dashboard" | Specialist Tier | Deep Design Thinking; Purple Ban; contrast check; modern typography & micro-interactions. |
| **REFACTOR / CLEAN** | "refactor", "clean code", "simplify", "remove dead code", "consolidate" | Surgical Quality | Test baseline before/after; zero behavior regression; reduce cyclomatic complexity. |
| **AUDIT / SECURITY** | "security audit", "vulnerability", "OWASP", "penetration test", "review" | Security Tier | Threat model; attack surface mapping; strict input validation; DLP check; verification proof. |
| **SLASH COMMAND** | `/brainstorm`, `/create`, `/debug`, `/plan`, `/test`, `/ui-ux-pro-max`, `/mobile-test` | Workflow Command | Execute designated workflow markdown procedure from `.agent/workflows/`. |

---

## 3. Comprehensive 95-Agent Prompt Trigger Matrix

Match the user's intent and prompt keywords to the designated specialist agent(s) and core skills:

### Domain 1: Frontend, UI & Accessibility
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `frontend-specialist` | "frontend", "react", "next.js", "component", "ui", "ux", "css", "tailwind", "responsive layout", "modern dashboard" | `clean-code`, `react-best-practices`, `web-design-guidelines`, `tailwind-patterns`, `frontend-design` |
| `react-reviewer` | "react hooks", "useEffect loop", "memoization", "re-render", "jsx patterns", "zustand/redux state", "nextjs server components" | `react-patterns`, `react-performance`, `react-testing` |
| `react-build-resolver` | "react build fail", "vite build error", "next build error", "webpack compilation", "missing module in react", "turbopack error" | `nextjs-turbopack`, `vite-patterns`, `systematic-debugging` |
| `vue-reviewer` | "vue", "vue 3", "composition api", "pinia", "nuxt", "nuxt4", "vue template", "v-model", "ref/reactive" | `vue-patterns`, `nuxt4-patterns`, `ui-to-vue` |
| `a11y-architect` | "accessibility", "a11y", "wcag", "screen reader", "aria", "color contrast", "keyboard navigation", "focus trap" | `accessibility`, `frontend-a11y`, `web-design-guidelines` |

### Domain 2: Mobile & Cross-Platform
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `mobile-developer` | "mobile app", "react native", "expo", "ios", "android", "mobile navigation", "mobile offline", "mobile ui" | `clean-code`, `mobile-design`, `react-native-patterns` |
| `mobile-automation-engineer` | "mobile automation", "appium", "webdriverio mobile", "mobile test", "mobile e2e", "screen object", "uiautomator2", "xcuitest", "mobile locator", "mobile gestures", "mobile test flakiness" | `clean-code`, `testing-patterns`, `mobile-automation`, `appium-skill`, `tdd-workflow` |
| `flutter-reviewer` | "flutter", "dart", "flutter widget", "bloc", "riverpod", "flutter state", "buildcontext", "flutter layout" | `dart-flutter-patterns`, `flutter-dart-code-review` |
| `dart-build-resolver` | "flutter build error", "pubspec error", "cocoapods pod install", "android gradle flutter", "dart compile error" | `dart-flutter-patterns`, `systematic-debugging` |
| `swift-reviewer` | "swift", "swiftui", "uikit", "combine", "swift concurrency", "actor persistence", "async/await swift" | `swiftui-patterns`, `swift-actor-persistence`, `swift-concurrency-6-2` |
| `swift-build-resolver` | "xcode build failed", "swift compiler error", "spm dependency resolution", "cocoapods swift mismatch" | `swift-protocol-di-testing`, `systematic-debugging` |
| `harmonyos-app-resolver` | "harmonyos", "arkts", "arkui", "huawei dev", "harmony build" | `mobile-design` |

### Domain 3: Backend & Language Specialists
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `backend-specialist` | "backend", "api", "rest api", "graphql", "trpc", "server", "middleware", "express", "hono", "backend auth" | `clean-code`, `nodejs-best-practices`, `python-patterns`, `api-patterns`, `database-design` |
| `python-reviewer` | "python", "pythonic", "pep8", "type hints", "pydantic", "asyncio", "python performance", "generator" | `python-patterns`, `python-testing`, `clean-code` |
| `fastapi-reviewer` | "fastapi", "pydantic v2", "fastapi router", "fastapi dependency", "uvicorn", "async def endpoint" | `fastapi-patterns`, `api-patterns`, `python-patterns` |
| `django-reviewer` | "django", "drf", "django rest framework", "django orm", "django serializer", "django viewset", "django celery" | `django-patterns`, `django-celery`, `django-tdd` |
| `django-build-resolver` | "django migration conflict", "django makemigrations error", "pip dependency conflict", "django settings error" | `django-verification`, `django-security`, `systematic-debugging` |
| `go-reviewer` | "golang", "go code", "goroutine", "go channel", "go interface", "go error handling", "go struct" | `golang-patterns`, `golang-testing` |
| `go-build-resolver` | "go build error", "go vet failure", "go mod tidy error", "undefined go package", "cgo error" | `golang-patterns`, `systematic-debugging` |
| `rust-reviewer` | "rust", "borrow checker", "lifetime", "trait", "ownership", "tokio", "cargo", "result/option rust" | `rust-patterns`, `rust-pro`, `rust-testing` |
| `rust-build-resolver` | "rustc error", "cargo build failed", "borrow checker error", "cannot borrow as mutable", "mismatched types rust" | `rust-patterns`, `systematic-debugging` |
| `java-reviewer` | "java", "spring boot", "quarkus", "jpa/hibernate", "maven", "gradle", "google java style", "spring security" | `java-coding-standards`, `springboot-patterns`, `springboot-tdd` |
| `java-build-resolver` | "maven build failure", "gradle build error", "javac compilation", "circular dependency java", "jar missing" | `springboot-verification`, `quarkus-verification`, `systematic-debugging` |
| `kotlin-reviewer` | "kotlin", "coroutines", "flow", "kmp", "ktor", "kotlin android", "kotlin exposed" | `kotlin-patterns`, `kotlin-coroutines-flows`, `kotlin-ktor-patterns` |
| `kotlin-build-resolver` | "kotlin compiler error", "gradle kts build failed", "kapt/ksp error", "unresolved reference kotlin" | `kotlin-testing`, `systematic-debugging` |
| `typescript-reviewer` | "typescript", "ts error", "generics", "conditional types", "type narrow", "ts-ignore", "strict null" | `typescript-patterns`, `clean-code` |
| `csharp-reviewer` | "c#", ".net", "dotnet", "csharp", "asp.net core", "entity framework", "linq", "xunit" | `dotnet-patterns`, `csharp-testing` |
| `fsharp-reviewer` | "f#", "fsharp", "functional .net", "discriminated unions", "fsunit" | `fsharp-testing` |
| `cpp-reviewer` | "c++", "cpp", "modern c++", "raii", "smart pointers", "templates", "std::vector", "memory safety c++" | `cpp-coding-standards`, `cpp-testing` |
| `cpp-build-resolver` | "cmake error", "gcc/clang error", "undefined reference vtable", "linker error cpp", "make build error" | `cpp-testing`, `systematic-debugging` |
| `php-reviewer` | "php", "laravel", "artisan", "eloquent", "blade", "psr-12", "composer php" | `laravel-patterns`, `laravel-tdd`, `laravel-security` |
| `ruby-reviewer` | "ruby", "rails", "ruby on rails", "activerecord", "rspec", "gemfile", "rubocop" | `rails-patterns` |

### Domain 4: Database & Storage
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `database-architect` | "database schema", "schema design", "migration strategy", "sql vs nosql", "prisma schema", "table indexing", "foreign keys", "er diagram", "erd" | `clean-code`, `database-design`, `prisma-patterns`, `archify` |
| `database-reviewer` | "slow query", "explain analyze", "n+1 query", "postgres optimization", "mysql index", "locking", "transaction deadlock" | `postgres-patterns`, `mysql-patterns`, `database-migrations` |

### Domain 5: DevOps, Cloud, Network & Infrastructure
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `devops-engineer` | "docker", "dockerfile", "docker-compose", "kubernetes", "k8s", "ci/cd", "github actions", "deploy", "nginx", "pm2", "cloudflare" | `deployment-procedures`, `docker-patterns`, `kubernetes-patterns`, `server-management` |
| `network-architect` | "network architecture", "subnetting", "vpn", "bgp routing", "topology", "firewall architecture" | `network-config-validation`, `network-bgp-diagnostics` |
| `network-config-reviewer` | "cisco config", "switch config", "router acl", "juniper", "vlan configuration", "ssh automation" | `cisco-ios-patterns`, `netmiko-ssh-automation` |
| `network-troubleshooter` | "packet loss", "network latency", "dns resolution fail", "ping fail", "interface down", "network connectivity" | `network-interface-health`, `systematic-debugging` |
| `homelab-architect` | "homelab", "pi-hole", "wireguard vpn", "proxmox", "truenas", "vlan segmentation", "home server" | `homelab-network-readiness`, `homelab-pihole-dns`, `homelab-wireguard-vpn` |

### Domain 6: Cybersecurity & Penetration Testing
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `security-auditor` | "security audit", "owasp", "threat model", "vulnerability scan", "hardcoded secrets", "rate limiting", "dlp", "security check" | `vulnerability-scanner`, `red-team-tactics`, `security-review`, `defense-in-depth` |
| `security-reviewer` | "sql injection", "xss", "csrf", "idor", "auth bypass", "sanitization", "jwt validation", "security code review" | `security-scan`, `security-bounty-hunter`, `clean-code` |
| `penetration-tester` | "penetration test", "exploit", "red team", "privilege escalation", "attack payload", "defi exploit" | `red-team-tactics`, `defi-amm-security` |

### Domain 7: Testing, QA, Debugging & Verification
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `test-engineer` | "write test", "unit test", "integration test", "mock", "vitest", "jest", "pytest", "test coverage" | `clean-code`, `testing-patterns`, `tdd-workflow`, `test-driven-development` |
| `debugger` | "debug", "crash", "exception", "traceback", "reproduce bug", "why is this failing", "root cause" | `systematic-debugging`, `root-cause-tracing` |
| `tdd-guide` | "tdd", "test driven development", "red green refactor", "failing test first", "test first" | `test-driven-development`, `tdd-workflow` |
| `qa-automation-engineer` | "e2e test", "playwright", "cypress", "browser automation", "ui automated test", "test suite ci" | `webapp-testing`, `e2e-testing`, `windows-desktop-e2e` |
| `mobile-automation-engineer` | "mobile test", "mobile automation", "appium", "webdriverio mobile", "screen object", "mobile gestures" | `clean-code`, `testing-patterns`, `mobile-automation`, `appium-skill`, `tdd-workflow` |
| `e2e-runner` | "run e2e", "visual regression test", "browser run", "playwright runner" | `browser-qa`, `webapp-testing` |
| `build-error-resolver` | "build error", "compilation failed", "syntax error", "dependency error", "bundle error" | `systematic-debugging` |
| `silent-failure-hunter` | "silent failure", "swallowed exception", "empty catch block", "unhandled rejection", "missing error log" | `error-handling`, `condition-based-waiting` |
| `pr-test-analyzer` | "pr tests", "test gap", "flaky test", "missing assertion", "test quality review" | `testing-anti-patterns`, `conventional-commit-review` |
| `verify` | "verify all", "prove it works", "validation check", "check evidence", "son kontrolleri yap" | `verification-before-completion` |

### Domain 8: Architecture, Quality & Refactoring
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `architect` | "system architecture", "high level architecture", "draw architecture", "archify", "process flow diagram", "flow chart diagram", "sequence diagram", "hexagonal architecture", "adr" | `archify`, `architecture`, `architecture-decision-records`, `hexagonal-architecture` |
| `code-architect` | "oop design", "solid principles", "design patterns", "dependency inversion", "class structure", "draw class diagram" | `archify`, `clean-code`, `architecture` |
| `code-reviewer` | "code review", "review this PR", "review code", "peer review", "lint feedback", "code standards" | `code-review-checklist`, `requesting-code-review`, `receiving-code-review` |
| `code-simplifier` | "simplify code", "too complex", "overcomplicated", "reduce lines", "clean up function" | `clean-code`, `karpathy-guidelines` |
| `refactor-cleaner` | "clean dead code", "remove unused imports", "orphan functions", "consolidate duplicated code" | `clean-code`, `refactor-cleaner` |
| `code-archaeologist` | "legacy code", "understand old codebase", "reverse engineer", "undocumented system", "technical debt" | `brownfield-retrospective`, `codebase-onboarding` |
| `type-design-analyzer` | "type design", "domain invariants", "strong typing", "type modeling" | `clean-code`, `typescript-patterns` |
| `commit-reviewer` | "git commit", "conventional commits", "commit message review", "git history" | `conventional-commit-review`, `git-workflow` |
| `comment-analyzer` | "code comments", "comment quality", "remove emojis from code", "docstring review" | `clean-code` |
| `spec-miner` | "behavioral spec", "contract extraction", "openspec", "system invariant" | `contract-first` |

### Domain 9: Exploration, Documentation & Planning
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `explore` / `explorer-agent` | "explore codebase", "understand architecture", "map dependencies", "find where X is defined" | `repo-scan`, `code-tour`, `codebase-onboarding` |
| `code-explorer` | "trace function caller", "call hierarchy", "find usage across repo", "subsystem search" | `codebase-onboarding` |
| `doc-updater` | "update docs", "sync readme", "update api docs", "codemap update" | `docs-governance`, `living-docs-governance` |
| `docs-lookup` | "lookup docs", "how to use library", "api documentation", "official docs syntax" | `documentation-lookup` |
| `documentation-writer` | "write manual", "technical guide", "architecture document", "user guide" | `documentation-templates` |
| `conversation-analyzer` | "summarize session", "extract takeaways", "session learnings", "knowledge synthesis" | `knowledge-ops` |
| `orchestrator` | "full stack app", "multi-domain project", "build SaaS", "coordinate work", "orchestrate" | `parallel-agents`, `behavioral-modes`, `brainstorming`, `writing-plans` |
| `project-planner` | "plan project", "breakdown tasks", "implementation plan", "socratic planning", "roadmap" | `brainstorming`, `plan-writing`, `writing-plans` |
| `product-manager` / `product-owner` | "user stories", "acceptance criteria", "mvp scope", "product requirements", "backlog" | `plan-writing`, `brainstorming`, `product-lens` |
| `chief-of-staff` / `loop-operator` | "manage agent loop", "operator checkpoint", "intervention policy", "harness loop" | `continuous-agent-loop`, `operator-approval-loop` |

### Domain 10: Specialized Domains & Data Intelligence
| Agent | Trigger Keywords & Intent | Core Skills Auto-Loaded |
| :--- | :--- | :--- |
| `game-developer` | "game", "game development", "phaser", "godot", "unity", "game mechanics", "game loop", "sprites" | `game-development` |
| `seo-specialist` | "seo", "search ranking", "meta tags", "sitemap", "core web vitals", "schema.org", "json-ld", "geo" | `seo-fundamentals`, `geo-fundamentals`, `implementing-schema-org` |
| `performance-optimizer` | "profile performance", "memory leak", "slow execution", "cpu spike", "optimize rendering" | `performance-profiling`, `memory-leak-debugging` |
| `mle-reviewer` | "ml pipeline", "machine learning engineering", "training loop", "dataset contract", "model eval" | `mle-workflow`, `eval-harness` |
| `pytorch-build-resolver` | "pytorch error", "cuda out of memory", "tensor mismatch", "dataloader crash", "torchscript" | `pytorch-patterns`, `systematic-debugging` |
| `rag-pipeline-reviewer` | "rag", "retrieval augmented generation", "vector db", "chunking", "embeddings", "hallucination" | `ai-first-engineering`, `cost-aware-llm-pipeline` |
| `marketing-agent` | "marketing copy", "landing page conversion", "audience research", "marketing campaign" | `marketing-campaign`, `brand-voice` |
| `healthcare-reviewer` | "hipaa", "phi", "healthcare data", "clinical cdss", "emr integration" | `hipaa-compliance`, `healthcare-phi-compliance` |
| `bengali-reviewer` | "bengali", "bangla text", "bengali nlp", "unicode normalization bangla" | `bengali-nlp` |
| `general` | General inquiries not matching specialized domains | `using-superpowers`, `clean-code` |

---

## 4. Multi-Domain Auto-Orchestration Rules

When a prompt contains triggers from **two or more distinct domains** (e.g., "Build a secure REST API with React frontend and PostgreSQL database"):
1. **Auto-Invoke Master Agent**: `orchestrator` + domain specialists (`frontend-specialist`, `backend-specialist`, `database-architect`, `security-auditor`).
2. **Execute Socratic Gate**: Present 2-3 strategic architectural trade-offs to the user before generating code.
3. **Execute Task Decomposition**: Decompose the implementation into bite-sized tasks using `writing-plans`.
4. **Enforce Verification Gate**: Before declaring done, run verification via `verify_all.py` or `checklist.py`.

---

## 5. Global & Multi-Project Portability Specification

To enable this system to operate seamlessly in any repository or global setting:
1. **Relative & Fallback Path Resolution**:
   - Primary: Look in local workspace `.agent/agents/{agent}.md` and `.agent/skills/{skill}/SKILL.md`.
   - Global Fallback: Look in user's global config `~/.gemini/config/agents/{agent}.md` and `~/.gemini/config/skills/{skill}/SKILL.md` or `global-rules/{skill}/SKILL.md`.
2. **Standardized Trigger Syntax**: Users can trigger agents either implicitly through natural prompt keywords OR explicitly with `@agent-name` or `/workflow` commands.
3. **Zero Configuration**: Any project containing this rule setup automatically inherits full automatic agent selection and skill enforcement.

