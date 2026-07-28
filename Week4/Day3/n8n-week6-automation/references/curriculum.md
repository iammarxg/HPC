# Week 6 — Automation & Orchestration with n8n (Eng: Abdullah Barghash)

Full detail per day. Use alongside the task checklist in SKILL.md.

## Day 1 — Automation foundations & intro to n8n
- **Activity**: Automating multi-step workflows; n8n basics — nodes, triggers, scheduling.
- **Skills**: Workflow design.
- **Tools**: n8n, Schedulers/triggers.
- **Outcome**: A first n8n workflow running on a schedule.
- **Task**: Build an n8n workflow that runs automatically on a schedule and performs at least two connected actions.
- **Pitfall**: Learners often add a Schedule Trigger with only one downstream node, or two nodes that aren't actually connected to each other in sequence. "Connected actions" means node A's output feeds node B — not two parallel unconnected branches.

## Day 2 — Connecting tools & APIs in n8n
- **Activity**: Wire external services into a workflow using n8n nodes and HTTP/API calls.
- **Skills**: API integration, node-based automation.
- **Tools**: n8n, External APIs.
- **Outcome**: A workflow that connects 2+ external services.
- **Task**: Connect two external APIs inside n8n and exchange data between them successfully.
- **Pitfall**: "Exchange data" is the key requirement — calling two APIs independently doesn't satisfy this. Output of API A must be mapped (via expressions or a Set node) into the request body/params of API B.

## Day 3 — AI workflows & chaining agents
- **Activity**: Use the n8n AI Agent node; chain LLM steps and agents to pass work along.
- **Skills**: Orchestration, AI workflows.
- **Tools**: n8n, LLM API.
- **Outcome**: An AI-powered, chained n8n workflow.
- **Task**: Create an AI workflow where multiple LLM steps process data sequentially before producing a final output.
- **Pitfall**: "Sequentially" means step 2's prompt should consume step 1's output (e.g. extract → summarize → format), not three independent LLM calls on the same input that get concatenated at the end.

## Day 4 — Error handling & human-in-the-loop
- **Activity**: n8n error workflows; approval/checkpoint steps; recovering from failures.
- **Skills**: Error handling, HITL (human-in-the-loop) design.
- **Tools**: n8n.
- **Outcome**: A resilient workflow with a human checkpoint.
- **Task**: Add error handling and a human approval step to an existing workflow, then test both success and failure scenarios.
- **Pitfall**: This builds on an *existing* workflow (from an earlier day), not a new one. Two things are required, not one: (1) error handling — e.g. a dedicated Error Trigger workflow, or "Continue On Fail" plus a branch that reports the failure; and (2) a human checkpoint — e.g. a Wait node paired with a manual resume, or an approval message via Slack/email/Form that pauses the flow until a human responds. Both success and failure paths must actually be run and shown working, not just built.

## Day 5 — Build an automation (capstone)
- **Activity**: End-to-end n8n build: summarize incoming docs, file them, then notify.
- **Skills**: End-to-end automation.
- **Tools**: n8n, APIs, LLM API.
- **Outcome**: A working end-to-end n8n automation.
- **Task**: Build an end-to-end automation that receives a document, summarizes it using AI, stores the result, and sends a notification.
- **Pitfall**: All four stages must be present and connected: (1) document intake (webhook, form trigger, or watched folder/email), (2) AI summarization, (3) storage of the *result* (not just the original doc — the summary needs to be saved somewhere retrievable), (4) a notification step that fires after storage succeeds. This is meant to combine patterns from Days 1–4 (scheduling/triggers, API/service integration, AI chaining, and ideally error handling).
