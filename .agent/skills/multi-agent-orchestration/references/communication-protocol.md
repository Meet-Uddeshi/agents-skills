# Inter-Agent Communication Protocol

This document specifies the communication contracts, context handoff schemas, and message exchange mechanisms used between agents in Antigravity.

## Communication Channels

1. **Direct Subagent Dispatch:** Invoked via `invoke_subagent` for hierarchical, isolated execution.
2. **Peer Messaging:** Exchanged via `send_message(Recipient, Message)` for peer-to-peer reviews and inquiries.
3. **Blackboard Coordination:** Shared file state via `.agent/context/BLACKBOARD.md` for multi-agent swarm awareness.

## Standard Context Handoff Payload (CHP)

When Agent A hands off a task to Agent B, it delivers this structured JSON or Markdown contract:

```json
{
  "sender": "understand-anything",
  "recipient": "backend-specialist",
  "taskObjective": "Implement user authentication endpoint",
  "discoveredInvariants": [
    "Express router mounted at /api/v1/auth",
    "Prisma client singleton in src/lib/db.ts",
    "Password hashing uses bcrypt with 12 rounds"
  ],
  "constraints": [
    "No emojis in errors or logs",
    "Enforce rate limiting middleware",
    "Strict TypeScript types without any"
  ],
  "handoffArtifacts": [
    "src/routes/auth.ts",
    "tests/auth.test.ts"
  ],
  "actionRequired": "Add POST /login route with tests"
}
```

## Peer Query Contract (Review & Consult)

When an implementer agent needs validation from a specialist:
1. **Query:**
   - Implementer sends: *"Review proposed SQL index on `orders(user_id, created_at)` for query latency."*
2. **Specialist Review:**
   - Specialist (`database-reviewer`) inspects query plan and returns:
     - Verdict: `APPROVED` | `REJECTED` | `AMENDMENT_REQUIRED`
     - Concrete adjustment (e.g., *"Include status column to cover dashboard query filter"*).
3. **Execution:**
   - Implementer applies the adjustment with zero debate.

