# Antigravity Kit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit

---

## 📋 Overview

Antigravity Kit is a comprehensive AI engineering system consisting of:

- **108 Specialist Agents** - Role-based AI specialist personas across 10 engineering domains
- **365+ Skills** - Domain-specific patterns, testing frameworks, and knowledge modules
- **11 Workflows** - Slash command guided procedures
- **Intelligent Prompt Trigger Engine** - Automated agent and skill selection based on prompt intent

---

## 🏗️ Directory Structure

```plaintext
.agent/
├── ARCHITECTURE.md          # Architecture overview & catalog
├── PROMPT-TEMPLATE.md       # Prompt practices and trigger guide
├── SKILL.md                 # Gravitas runtime invariants
├── agents/                  # 108 Specialist Agent Personas
├── skills/                  # 365+ Domain Skills
├── workflows/               # 11 Slash Command Workflows
├── rules/                   # Workspace Rules & Trigger Matrix
└── scripts/                 # Validation & Testing Suites
```

---

## 🤖 Specialist Agents (108 Across 10 Domains)

Specialist AI personas equipped with specialized rule sets, frontmatter skills, and prompt triggers:

### 1. Frontend & UI (11 Agents)
`frontend-specialist`, `react-reviewer`, `react-build-resolver`, `vue-reviewer`, `a11y-architect`

### 2. Mobile & Cross-Platform (7 Agents)
`mobile-developer`, `mobile-automation-engineer`, `flutter-reviewer`, `dart-build-resolver`, `swift-reviewer`, `swift-build-resolver`, `harmonyos-app-resolver`

### 3. Backend & Languages (20 Agents)
`backend-specialist`, `python-reviewer`, `fastapi-reviewer`, `django-reviewer`, `django-build-resolver`, `go-reviewer`, `go-build-resolver`, `rust-reviewer`, `rust-build-resolver`, `java-reviewer`, `java-build-resolver`, `kotlin-reviewer`, `kotlin-build-resolver`, `typescript-reviewer`, `csharp-reviewer`, `fsharp-reviewer`, `cpp-reviewer`, `cpp-build-resolver`, `php-reviewer`, `ruby-reviewer`

### 4. Database & Storage (2 Agents)
`database-architect`, `database-reviewer`

### 5. DevOps, Cloud & Network (5 Agents)
`devops-engineer`, `network-architect`, `network-config-reviewer`, `network-troubleshooter`, `homelab-architect`

### 6. Cybersecurity & Penetration Testing (3 Agents)
`security-auditor`, `security-reviewer`, `penetration-tester`

### 7. Testing, QA, Debugging & Verification (9 Agents)
`test-engineer`, `debugger`, `tdd-guide`, `qa-automation-engineer`, `e2e-runner`, `build-error-resolver`, `silent-failure-hunter`, `pr-test-analyzer`, `verify`

### 8. Architecture, Quality & Refactoring (10 Agents)
`architect`, `code-architect`, `code-reviewer`, `code-simplifier`, `refactor-cleaner`, `code-archaeologist`, `type-design-analyzer`, `commit-reviewer`, `comment-analyzer`, `spec-miner`

### 9. Exploration, Documentation & Planning (9 Agents)
`explore`, `explorer-agent`, `code-explorer`, `doc-updater`, `docs-lookup`, `documentation-writer`, `conversation-analyzer`, `project-planner`, `product-manager`, `product-owner`

### 10. Specialized Domains & Data Intelligence (19 Agents)
`game-developer`, `seo-specialist`, `performance-optimizer`, `mle-reviewer`, `pytorch-build-resolver`, `rag-pipeline-reviewer`, `marketing-agent`, `healthcare-reviewer`, `bengali-reviewer`, `orchestrator`, `coordinator`, `plan`, `planner`, `chief-of-staff`, `loop-operator`, `agent-evaluator`, `harness-optimizer`, `general`

---


## 🧩 Skills (36)

Modular knowledge domains that agents can load on-demand. based on task context.

### Frontend & UI

| Skill                   | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `react-best-practices`  | React & Next.js performance optimization (Vercel - 57 rules)          |
| `web-design-guidelines` | Web UI audit - 100+ rules for accessibility, UX, performance (Vercel) |
| `tailwind-patterns`     | Tailwind CSS v4 utilities                                             |
| `frontend-design`       | UI/UX patterns, design systems                                        |
| `ui-ux-pro-max`         | 50 styles, 21 palettes, 50 fonts                                      |

### Backend & API

| Skill                   | Description                    |
| ----------------------- | ------------------------------ |
| `api-patterns`          | REST, GraphQL, tRPC            |
| `nestjs-expert`         | NestJS modules, DI, decorators |
| `nodejs-best-practices` | Node.js async, modules         |
| `python-patterns`       | Python standards, FastAPI      |

### Database

| Skill             | Description                 |
| ----------------- | --------------------------- |
| `database-design` | Schema design, optimization |
| `prisma-expert`   | Prisma ORM, migrations      |

### TypeScript/JavaScript

| Skill               | Description                         |
| ------------------- | ----------------------------------- |
| `typescript-expert` | Type-level programming, performance |

### Cloud & Infrastructure

| Skill                   | Description               |
| ----------------------- | ------------------------- |
| `docker-expert`         | Containerization, Compose |
| `deployment-procedures` | CI/CD, deploy workflows   |
| `server-management`     | Infrastructure management |

### Testing & Quality

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `testing-patterns`      | Jest, Vitest, strategies |
| `webapp-testing`        | E2E, Playwright          |
| `tdd-workflow`          | Test-driven development  |
| `code-review-checklist` | Code review standards    |
| `lint-and-validate`     | Linting, validation      |

### Security

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `vulnerability-scanner` | Security auditing, OWASP |
| `red-team-tactics`      | Offensive security       |

### Architecture & Planning

| Skill           | Description                                                |
| --------------- | ---------------------------------------------------------- |
| `archify`       | Interactive architecture, workflow, ERD, and process flow diagrams |
| `app-builder`   | Full-stack app scaffolding                                 |
| `architecture`  | System design patterns                                     |
| `plan-writing`  | Task planning, breakdown                                   |
| `brainstorming` | Socratic questioning                                       |

### Mobile

| Skill           | Description           |
| --------------- | --------------------- |
| `mobile-design` | Mobile UI/UX patterns |

### Game Development

| Skill              | Description           |
| ------------------ | --------------------- |
| `game-development` | Game logic, mechanics |

### SEO & Growth

| Skill              | Description                   |
| ------------------ | ----------------------------- |
| `seo-fundamentals` | SEO, E-E-A-T, Core Web Vitals |
| `geo-fundamentals` | GenAI optimization            |

### Shell/CLI

| Skill                | Description               |
| -------------------- | ------------------------- |
| `bash-linux`         | Linux commands, scripting |
| `powershell-windows` | Windows PowerShell        |

### Other

| Skill                     | Description               |
| ------------------------- | ------------------------- |
| `clean-code`              | Coding standards (Global) |
| `behavioral-modes`        | Agent personas            |
| `parallel-agents`         | Multi-agent patterns      |
| `mcp-builder`             | Model Context Protocol    |
| `documentation-templates` | Doc formats               |
| `i18n-localization`       | Internationalization      |
| `performance-profiling`   | Web Vitals, optimization  |
| `systematic-debugging`    | Troubleshooting           |

---

## 🔄 Workflows (11)

Slash command procedures. Invoke with `/command`.

| Command          | Description              |
| ---------------- | ------------------------ |
| `/brainstorm`    | Socratic discovery       |
| `/create`        | Create new features      |
| `/debug`         | Debug issues             |
| `/deploy`        | Deploy application       |
| `/enhance`       | Improve existing code    |
| `/orchestrate`   | Multi-agent coordination |
| `/plan`          | Task breakdown           |
| `/preview`       | Preview changes          |
| `/status`        | Check project status     |
| `/test`          | Run tests                |
| `/ui-ux-pro-max` | Design with 50 styles    |

---

## 🎯 Skill Loading Protocol

```plaintext
User Request → Skill Description Match → Load SKILL.md
                                            ↓
                                    Read references/
                                            ↓
                                    Read scripts/
```

### Skill Structure

```plaintext
skill-name/
├── SKILL.md           # (Required) Metadata & instructions
├── scripts/           # (Optional) Python/Bash scripts
├── references/        # (Optional) Templates, docs
└── assets/            # (Optional) Images, logos
```

### Enhanced Skills (with scripts/references)

| Skill               | Files | Coverage                            |
| ------------------- | ----- | ----------------------------------- |
| `ui-ux-pro-max`     | 27    | 50 styles, 21 palettes, 50 fonts    |
| `app-builder`       | 20    | Full-stack scaffolding              |

---

## � Scripts (2)

Master validation scripts that orchestrate skill-level scripts.

### Master Scripts

| Script          | Purpose                                 | When to Use              |
| --------------- | --------------------------------------- | ------------------------ |
| `checklist.py`  | Priority-based validation (Core checks) | Development, pre-commit  |
| `verify_all.py` | Comprehensive verification (All checks) | Pre-deployment, releases |

### Usage

```bash
# Quick validation during development
python .agent/scripts/checklist.py .

# Full verification before deployment
python .agent/scripts/verify_all.py . --url http://localhost:3000
```

### What They Check

**checklist.py** (Core checks):

- Security (vulnerabilities, secrets)
- Code Quality (lint, types)
- Schema Validation
- Test Suite
- UX Audit
- SEO Check

**verify_all.py** (Full suite):

- Everything in checklist.py PLUS:
- Lighthouse (Core Web Vitals)
- Playwright E2E
- Bundle Analysis
- Mobile Audit
- i18n Check

For details, see [scripts/README.md](scripts/README.md)

---

## 📊 Statistics

| Metric              | Value                         |
| ------------------- | ----------------------------- |
| **Total Agents**    | 95                            |
| **Total Skills**    | 350+                          |
| **Total Workflows** | 11                            |
| **Total Scripts**   | 2 (master) + 20+ (test & validation) |
| **Coverage**        | 100% full-stack, mobile, cloud, security & AI |

---

## 🔗 Quick Reference

| Need     | Agent                 | Skills                                |
| -------- | --------------------- | ------------------------------------- |
| Web App  | `frontend-specialist` | react-best-practices, frontend-design |
| API      | `backend-specialist`  | api-patterns, nodejs-best-practices   |
| Mobile   | `mobile-developer`    | mobile-design                         |
| Database | `database-architect`  | database-design, prisma-expert        |
| Security | `security-auditor`    | vulnerability-scanner                 |
| Testing  | `test-engineer`       | testing-patterns, webapp-testing      |
| Debug    | `debugger`            | systematic-debugging                  |
| Plan     | `project-planner`     | brainstorming, plan-writing           |
