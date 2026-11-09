---
name: agentic-frameworks
description: Production multi-agent systems, state graph design, human-in-the-loop workflows, supervisor-worker topologies, and automation orchestration using LangGraph, CrewAI, AutoGen, and n8n/Make.
---

# Agentic Frameworks & Multi-Agent Orchestration

Production-grade agentic frameworks move beyond simple prompting and sequential chains to stateful, cyclic, resilient multi-agent systems.

---

## 1. Core Framework Architectures

### 1.1 LangGraph State Machine Architecture

LangGraph implements agents as cyclic state machines where computation nodes mutate a shared state and conditional edges direct control flow.

```text
                  +-----------------------+
                  |      User Input       |
                  +-----------------------+
                              |
                              v
                   +---------------------+
                   |   Supervisor /      |
                   |   Router Node       |
                   +---------------------+
                              |
              +---------------+---------------+
              |                               |
              v                               v
    +-------------------+           +-------------------+
    | Research Specialist|          | Coding Specialist  |
    | (Worker Node A)   |           | (Worker Node B)   |
    +-------------------+           +-------------------+
              |                               |
              +---------------+---------------+
                              |
                              v
                   +---------------------+
                   | State Checkpoint    |
                   | (Human-in-the-Loop) |
                   +---------------------+
                              |
                              v
                   +---------------------+
                   | Verification Gate   |
                   +---------------------+
```

#### Production LangGraph Implementation
```python
from typing import Annotated, Dict, List, Literal, TypedDict
from pydantic import BaseModel, Field
import operator
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. Strongly Typed State Schema
class AgentState(TypedDict):
    task: str
    plan: List[str]
    current_step: int
    worker_outputs: Annotated[List[Dict[str, str]], operator.add]
    error_count: int
    status: Literal["PLANNING", "EXECUTING", "REVIEW", "DONE", "BLOCKED"]

# 2. Worker Nodes
def plan_node(state: AgentState) -> Dict:
    task = state["task"]
    # Decompose into sequential milestones
    milestones = [f"Phase 1: Analyze {task}", f"Phase 2: Implement {task}", "Phase 3: Verify"]
    return {
        "plan": milestones,
        "current_step": 0,
        "status": "EXECUTING"
    }

def worker_node(state: AgentState) -> Dict:
    step_idx = state["current_step"]
    plan = state["plan"]
    if step_idx >= len(plan):
        return {"status": "REVIEW"}
    
    current_action = plan[step_idx]
    # Execute atomic action
    output = {"step": current_action, "result": f"Executed {current_action}"}
    return {
        "worker_outputs": [output],
        "current_step": step_idx + 1,
        "status": "EXECUTING" if step_idx + 1 < len(plan) else "REVIEW"
    }

def human_approval_node(state: AgentState) -> Dict:
    # State checkpoint for human-in-the-loop validation
    return {"status": "DONE"}

# 3. Conditional Router
def route_next_step(state: AgentState) -> str:
    if state["error_count"] > 3:
        return "blocked"
    if state["status"] == "EXECUTING":
        return "worker"
    if state["status"] == "REVIEW":
        return "human_approval"
    return "end"

# 4. Graph Assembly & Checkpointing
def build_agent_graph():
    memory = SqliteSaver.from_conn_string(":memory:")
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", plan_node)
    workflow.add_node("worker", worker_node)
    workflow.add_node("human_approval", human_approval_node)
    
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "worker")
    workflow.add_conditional_edges(
        "worker",
        route_next_step,
        {
            "worker": "worker",
            "human_approval": "human_approval",
            "blocked": END,
            "end": END
        }
    )
    workflow.add_edge("human_approval", END)
    
    return workflow.compile(checkpointer=memory, interrupt_before=["human_approval"])
```

---

## 2. Supervisor-Worker & Swarm Topologies (CrewAI & AutoGen)

### 2.1 Context Isolation Principle
- **Root Coordinator Context:** Never dump raw tool outputs or multi-file ASTs into the supervisor context.
- **Worker Isolation:** Each worker runs in an independent context window with specialized tools.
- **Structured Handoff Payload:**
  ```json
  {
    "task_id": "TASK-104",
    "assigned_worker": "security-reviewer",
    "objective": "Audit authentication middleware for token expiration bypass",
    "inputs": {
      "target_file": "app/auth/middleware.py",
      "relevant_lines": "45-92"
    },
    "constraints": ["Do not modify database schema", "Zero emojis"]
  }
  ```

### 2.2 CrewAI Enterprise Pattern
```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import DirectoryReadTool, FileReadTool

# Strict tool binding to prevent tool pollution
file_reader = FileReadTool()
dir_reader = DirectoryReadTool()

planner = Agent(
    role="Principal System Architect",
    goal="Design decoupled service contracts and validation schemas",
    backstory="15-year distributed systems architect specializing in micro-frontends and APIs",
    tools=[dir_reader, file_reader],
    verbose=True,
    allow_delegation=False
)

developer = Agent(
    role="Senior Backend Engineer",
    goal="Implement clean, strongly-typed endpoints conforming to architecture plan",
    backstory="Expert backend software engineer adhering strictly to SOLID and test-driven development",
    tools=[file_reader],
    verbose=True,
    allow_delegation=False
)

plan_task = Task(
    description="Analyze repository layout and define schema for User Authentication API",
    expected_output="Architecture specification markdown with data contracts",
    agent=planner
)

code_task = Task(
    description="Implement endpoint handlers based on the approved architecture plan",
    expected_output="Production Python code with comprehensive error handling",
    agent=developer
)

crew = Crew(
    agents=[planner, developer],
    tasks=[plan_task, code_task],
    process=Process.sequential,
    memory=True
)
```

---

## 3. Workflow Automation Platforms (n8n, Make.com)

### 3.1 Idempotent Webhook Receiver Pattern
When integrating AI agents into n8n or Make.com workflows:
1. **Deduplication:** Compute hash of incoming payload `hash = sha256(event_id + timestamp)`. Reject duplicate events within 600s.
2. **Asynchronous Dispatch:** Return HTTP `202 Accepted` with a `job_id` immediately. Do not hold HTTP connections open during multi-turn LLM reasoning loops.
3. **Webhook Polling & Callback:** Post completion status back to n8n webhook URL via signed HMAC-SHA256 headers.

---

## 4. Mandatory Quality Gates & Anti-Patterns

### Anti-Patterns to Strictly Avoid
- **Unbounded Cyclical Execution:** Never connect a worker node back to itself without an incrementing counter or strict exit condition.
- **Shared Mutable Global State:** Never allow subagents to write directly to shared variables; all state transitions must occur via explicit reducer functions.
- **Implicit Tool Delegation:** Never allow an agent to pick from 40+ generic tools without pre-filtering. Bind only the exact 2-3 tools required for the assigned milestone.

### Mandatory Verification Checklist
1. Is the state schema strongly typed with Pydantic or TypedDict?
2. Is there an explicit `recursion_limit` configured on graph compilation?
3. Are high-risk actions (file deletion, git push, production database mutations) gated behind human approval checkpoints (`interrupt_before`)?
4. Is all inter-agent telemetry logged with structured timestamps and status codes?
