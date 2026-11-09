---
trigger: always_on
---

# MULTI-AGENT SYSTEM PROTOCOL: RUNTIME COMPLEXITY ESCALATION, CONTEXT & MEMORY ENGINEERING

> **UNIVERSAL WORKSPACE INVARIANT:** This rule is always active across all agents and sessions. It governs how specialist agents detect runtime complexity, self-escalate to Superpower skills, communicate with peer agents, share context without token bloat, and maintain cognitive memory.

---

## 1. DYNAMIC RUNTIME COMPLEXITY ESCALATION PROTOCOL

Whenever ANY agent (whether single assistant, specialist, or subagent) encounters execution complexity, it is an **IRON RULE** that the agent must immediately suspend ad-hoc actions and invoke the designated Superpower skill via `read_file`:

| Runtime Complexity Trigger | Observable Threshold | Target Superpower Skill | Mandatory Action |
| :--- | :--- | :--- | :--- |
| **Design Ambiguity & Trade-offs** | Multiple architectural approaches, unclear requirements, or user trade-offs. | `brainstorming` (`.agent/skills/brainstorming/SKILL.md`) | Stop code generation. Propose 2-3 concrete options with pros/cons; get user alignment before proceeding. |
| **Multi-Step / Multi-File Work** | Implementation spans > 2 files or requires > 3 distinct steps. | `writing-plans` & `executing-plans` | Produce bite-sized implementation plan with explicit checkpoints; execute one step at a time. |
| **Runtime Crash / Failing Test / Bug** | Any uncaught exception, build error, or failing test assertion. | `systematic-debugging` & `root-cause-tracing` | Isolate minimal reproduction. Trace root cause with evidence before modifying any code. |
| **New Production Logic Implementation** | Authoring core services, controllers, algorithms, or API endpoints. | `test-driven-development` | Write failing automated test first (RED), implement minimal code to pass (GREEN), then refactor. |
| **Cross-Domain Task Delegation** | Independent work streams (e.g., UI frontend + API backend). | `subagent-driven-development` | Spawn specialized subagents with isolated context and bounded scopes. |
| **Pre-Completion Claim** | Agent is about to declare the task complete or create a PR. | `verification-before-completion` | Run automated test suites and verify observable evidence before claiming completion. |

---

## 2. INTER-AGENT COMMUNICATION & CONTEXT SHARING (BLACKBOARD PROTOCOL)

Agents operating in a multi-agent workflow must coordinate and share context to eliminate redundant computation and prevent contradictory edits:

### 2.1 Communication Channels
1. **Hierarchical Dispatch:** Primary agent launches subagent via `invoke_subagent`.
2. **Peer Messaging:** Active agents message peers via `send_message(Recipient, Message)` for consultations and code reviews.
3. **Shared Blackboard:** All active agents read from and write to `.agent/context/BLACKBOARD.md`.

### 2.2 Standard Context Handoff Payload (CHP)
When handing off between agents, the sending agent must supply:
1. **Task Objective:** Clear definition of success.
2. **Discovered Invariants:** Key codebase patterns, routes, and schemas discovered.
3. **Active Constraints:** Rate limits, zero-emoji policy, error handling standards.
4. **Handoff Artifacts:** Exact file paths to modified files, diffs, and tests.

---

## 3. AGENT CONTEXT ENGINEERING SYSTEM

Context is a finite, scarce resource. Agents must adhere to strict context engineering:

1. **Attention Curve Optimization:**
   - Place critical system constraints and objective at the **Head** of the prompt.
   - Place exact output schemas, deliverables, and validation criteria at the **Tail**.
2. **Subagent Context Boundary Insulation:**
   - Heavy reconnaissance (scanning hundreds of files, reading compiler logs, AST extraction) must occur inside subagents.
   - Subagents must return condensed conclusions (under 300 words) with file references, never dumping raw logs or large file bodies into parent context.
3. **Progressive Disclosure:**
   - Agents read `SKILL.md` first. Never read all files in a skill directory unless specifically required.

---

## 4. AGENT MEMORY ENGINEERING SYSTEM

Every agent operates within a dual-tier cognitive memory model:

1. **Layer 1: Ephemeral Session Memory (`SESSION_FAILURES.md`):**
   - Maintained in the current working directory.
   - Records every failed approach, incorrect assumption, and invalid path immediately upon occurrence.
   - **Rule:** Before retrying any failed command or editing an alternative file, the agent must check `SESSION_FAILURES.md` to avoid repeating errors.
2. **Layer 2: Persistent Architectural Memory (`.agent/memory/ARCHITECTURE_MEMORY.md`):**
   - Records permanent project conventions, technology stack boundaries, and established patterns.
   - **Rule:** Before proposing architectural refactoring or schema alterations, the agent must consult this memory.

---

## 5. PROMPT-TRIGGER MULTI-AGENT ORCHESTRATION MODES

Based on user prompt intent, Antigravity selects the execution topology:

- **Single Specialist Mode:** Single-domain prompts -> Direct specialist activation (e.g. `fastapi-reviewer` or `unslop`).
- **Dynamic Escalation Mode:** Starts with a single specialist; if runtime complexity is encountered, self-escalates to Superpower skills.
- **Multi-Agent Swarm Mode:** Complex multi-domain prompts (e.g. "Build SaaS with React frontend, Go backend, and Postgres") -> `orchestrator` coordinates `frontend-specialist`, `go-reviewer`, `database-architect`, and `test-engineer` via the shared blackboard.

---

## 6. WORKFLOW AUTOMATION & STRUCTURED ANSWER PROTOCOL (PYTHON & NODE.JS)

All 108 agents are equipped with the Workflow Automation Engine to standardize complex task execution and formulate structured, reproducible answers:

### 6.1 Available Workflows Catalog (`.agent/workflows/`)
- `/plan`: Sequential project planning with milestone checklists.
- `/orchestrate`: Multi-agent orchestration requiring minimum 3 agents.
- `/test`: Automated test generation, execution, and coverage analysis.
- `/mobile-test`: Mobile automation auditing, screen objects, and locators.
- `/debug`: 4-phase systematic root-cause investigation.
- `/review`: Structured pull request, code smell, and security review.
- `/audit`: Security, accessibility (WCAG), performance, and dependency audit.
- `/reverse-engineer`: Reference application feature extraction and contract synthesis.
- `/unslop`: Visual modernization and anti-slop design token enforcement.
- `/understand`: Codebase onboarding, AST scanning, and architecture tours.
- `/deploy`: Production deployment verification and infrastructure staging.
- `/enhance`: Iterative feature enhancement and non-breaking refactoring.
- `/create`: Green-field application scaffolding and feature implementation.
- `/brainstorm`: Structured architectural trade-off exploration.
- `/preview`: Local development server lifecycle management.
- `/status`: Real-time agent status tracking and progress reporting.
- `/ui-ux-pro-max`: Design system planning and high-fidelity UI implementation.

### 6.2 Programmatic Automation Execution
Any agent can trigger or inspect workflows programmatically using either Python or Node.js scripts:
- **Python Workflow Runner:**
  ```bash
  python .agent/scripts/workflow_engine.py run <workflow> --args "<scope>" --agent <agent_name>
  ```
- **Node.js Workflow Runner:**
  ```bash
  node .agent/scripts/workflow-engine.js run <workflow> --args "<scope>" --agent <agent_name>
  ```
- **Automated Workflow Answers:**
  ```bash
  python .agent/scripts/workflow_engine.py answer "<user query>"
  ```

### 6.3 Standard Workflow Answer Structure
When providing answers to complex user requests, agents must follow the structured workflow pattern:
1. **Target Agent & Skill Assignment:** Explicitly state the primary specialist and injected skills.
2. **Matching Workflow & Objective:** Reference the relevant workflow from `.agent/workflows/`.
3. **Sub-Commands & Capabilities:** Display the actionable sub-commands.
4. **Step-by-Step Implementation Sequence:** Provide numbered, verifiable milestones.
5. **Automation Script Invocations:** Provide exact Python and Node.js commands to execute or dry-run.
6. **Blackboard Coordination:** Automatically log task start, checkpoints, and completion to `.agent/context/BLACKBOARD.md`.

---

## 7. MANDATORY ZERO-ASSUMPTION & USER CLARIFICATION INVARIANT (ALL AGENTS)

> **IRON RULE FOR ALL AGENTS:** If ANY agent (primary specialist, subagent, reviewer, or orchestrator) has ANY doubt, ambiguity, missing context, or uncertainty to make the correct decision, the agent MUST NOT ASSUME AND CONTINUE WORK.

1. **Zero Speculation:**
   - Guessing user intent, API contracts, architectural boundaries, or business logic is strictly prohibited.
   - Proceeding on unverified assumptions is treated as a critical system violation.

2. **Immediate Pause & Inquire Protocol:**
   - Whenever an agent reaches an ambiguous branch or lacks decisive clarity, the agent must immediately pause execution.
   - Formulate clear, concise questions detailing the exact decision point, why it matters, and 2-3 concrete options with trade-offs.
   - Present the questions directly to the user (via `ask_question` or direct text).
   - Only resume work after explicit user confirmation is received.

3. **Multi-Agent Coordination & Blackboard Integration:**
   - If an agent is blocked awaiting user clarification during multi-agent orchestration, it must update `.agent/context/BLACKBOARD.md` marking the work item as `BLOCKED (Awaiting User Clarification)`.
   - Peer agents must not overwrite or assume the blocked agent's scope.



