---
name: n8n-week6-automation
description: "Helps complete the Week 6 Automation & Orchestration with n8n curriculum (instructor Abdullah Barghash), a 5-day plan covering n8n basics, API integration, AI Agent chaining, error handling/human-in-the-loop, and an end-to-end build. Use this skill whenever the user mentions n8n, this Week 6 curriculum, or any of its daily tasks (scheduled workflow, connecting two APIs in n8n, chaining LLM/AI Agent steps, adding error handling or an approval/checkpoint step to a workflow, or building an end-to-end document-summarize-file-notify automation). Trigger even if the user just says 'help me with today's n8n task' or names a day number (e.g. 'Day 3 task') without saying n8n explicitly, since this curriculum is the likely context. Use for step-by-step guidance, generating ready-to-import n8n workflow JSON, reviewing/debugging a workflow the user built, and tracking which of the 5 days are complete."
---

# n8n Week 6 Automation & Orchestration Curriculum Helper

Supports a learner working through a 5-day n8n curriculum. Each day has one required **Task** (graded deliverable) plus supporting Activity/Skills/Tools/Outcomes context. This skill helps in three modes — **teach**, **build**, **review** — and maintains a progress checklist.

## The curriculum

| Day | Focus | Task (what must be delivered) |
|---|---|---|
| 1 | Automation foundations & intro to n8n | Build an n8n workflow that runs automatically on a schedule and performs at least two connected actions. |
| 2 | Connecting tools & APIs in n8n | Connect two external APIs inside n8n and exchange data between them successfully. |
| 3 | AI workflows & chaining agents | Create an AI workflow where multiple LLM steps process data sequentially before producing a final output. |
| 4 | Error handling & human-in-the-loop | Add error handling and a human approval step to an existing workflow, then test both success and failure scenarios. |
| 5 | Build an automation | Build an end-to-end automation that receives a document, summarizes it using AI, stores the result, and sends a notification. |

Full day-by-day detail (activities, skills, tools, outcomes) is in `references/curriculum.md` — read it when you need the fuller framing for a specific day, not just the task line above.

## Figure out what the user needs

Ask (or infer from their message) two things if not already clear:
1. **Which day** are they working on? (1–5)
2. **Which mode** do they want:
   - **Teach** — walk through the day's task step by step, explaining n8n concepts as they go (nodes, triggers, credentials, expressions).
   - **Build** — generate a ready-to-import n8n workflow JSON that satisfies that day's Task.
   - **Review** — the user has a workflow already (pasted JSON, screenshot, or description); debug it against that day's Task requirements and point out gaps.

Don't block on asking if the user's message already makes this obvious (e.g. they pasted workflow JSON and asked "why isn't this working" → Review mode, day inferred from the workflow's shape).

## Teach mode

For the given day, walk through:
1. The concept in plain language (what a trigger/node/credential/expression is, if this is early in the week).
2. A concrete build sequence: which nodes to add, in what order, and why.
3. What "done" looks like — restate that day's Task line as the acceptance test.
4. A common pitfall specific to that day (see `references/curriculum.md` for day-specific gotchas).

Keep it hands-on — the user is building in the actual n8n editor, not reading a lecture. Prefer short numbered steps over long paragraphs.

## Build mode — generating workflow JSON

When asked to generate a workflow, produce valid n8n workflow JSON (importable via n8n's "Import from File/URL" or paste-to-canvas). Rules:

- Structure: top-level `nodes` array and `connections` object, matching n8n's export format. Each node needs `id`, `name`, `type` (e.g. `n8n-nodes-base.scheduleTrigger`, `n8n-nodes-base.httpRequest`, `n8n-nodes-base.set`, `@n8n/n8n-nodes-langchain.agent`), `typeVersion`, `position`, and `parameters`.
- Never invent real API keys/credentials — use n8n's credential reference placeholders (e.g. `"credentials": {"httpBasicAuth": {"id": "PLACEHOLDER", "name": "Replace with your credential"}}`) and call this out explicitly to the user.
- For Day 1 (schedule + 2 actions): `scheduleTrigger` → two downstream connected nodes (e.g. an HTTP Request and a Set/spreadsheet write) — pick reasonable stand-in actions if the user hasn't specified real services, and say so.
- For Day 2 (two APIs): two `httpRequest` nodes (or one httpRequest + one native-service node) with a mapping step between them showing data actually flows from API A's output into API B's input.
- For Day 3 (chained AI): use `@n8n/n8n-nodes-langchain.agent` or `@n8n/n8n-nodes-langchain.chainLlm` nodes in sequence, each consuming the prior step's output — not three independent calls to the same prompt.
- For Day 4 (error handling + HITL): add an `errorTrigger` or per-node "Continue On Fail" + error branch, and a human checkpoint (e.g. `n8n-nodes-base.wait` for manual resume, a Slack/email "approve?" node, or n8n's built-in Form/Approval node). Include a note on how to test both the success path and a forced-failure path.
- For Day 5 (end-to-end): trigger (webhook or schedule) → document intake → AI summarization step → storage node (e.g. Google Drive/database) → notification node (email/Slack). This is the week's capstone — treat it as chaining the earlier days' patterns together.

After generating JSON, save it as a `.json` file for the user via the file tools rather than only pasting inline, and briefly explain what each node does and what they need to fill in (credentials, real endpoint URLs) before it will run.

## Review mode

When the user shares a workflow (JSON, screenshot, or description):
1. Identify which day's Task it's meant to satisfy (ask if ambiguous).
2. Check it against that day's Task line as a literal checklist — e.g. for Day 2, confirm there really are *two* external APIs and that data is passed between them, not just two independent calls.
3. Flag concrete bugs: broken node connections, missing credential references, expressions referencing the wrong node (`{{$node["X"].json[...]}}` pointing at a non-existent node), missing error handling.
4. Suggest the minimal fix, not a rewrite, unless the user asks for one.

## Progress tracking

Maintain `assets/progress-checklist.md` (copy it into the user's own workspace/outputs on first use if it isn't already there) with one line per day:

```
- [ ] Day 1 — Automation foundations & intro to n8n
- [ ] Day 2 — Connecting tools & APIs in n8n
- [ ] Day 3 — AI workflows & chaining agents
- [ ] Day 4 — Error handling & human-in-the-loop
- [ ] Day 5 — Build an automation
```

Mark a day `[x]` when the user confirms they've completed and tested that day's Task (don't mark it done just because Claude generated a workflow for it — completion means the user has it working). When the user asks "where am I" or "what's left," read this file back rather than guessing. Update it after any turn where a day is completed.
