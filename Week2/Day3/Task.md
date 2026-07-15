Continuing this week's task

I let the AI read the codebase and mention 5 improvements that will be implemented tomorrow:

Here are 5 ideas — a mix of a real bug fix, features, and extensions — each anchored to the current code:

**1. Fix the no-op `--staged` flag + add diff-range selection (bug fix → extension)**
Right now `cli.py:78` declares `--staged` as `is_flag=True, default=True`, so it can never be turned off and does literally nothing — and `LocalGitSource` only ever runs `git diff --cached`. That's misleading. Fix it into a real source selector: `aicr review` (staged, default), `aicr review --unstaged` (working tree), and `aicr review --range main..HEAD` (review a branch/PR locally before pushing). *Touches:* `cli.py`, `diff/source.py`. High value, ~half day, and it makes the tool useful outside the pre-commit moment.

**2. `aicr init` scaffolding command (feature)**
There's no way to generate config today — users hand-write `.aicr.yaml` and `.env`. Add `aicr init` that writes a commented `.aicr.yaml`, a `.env` (gitignored) with the key prompt, and optionally runs `enable`. Closes the onboarding gap between "install" and "first review." *Touches:* new `cli.py` command + a template. Small, high polish-per-effort.

**3. Hunk-level caching (extension — roadmap §10)**
The `CHANGELOG`/plan already reserve `cache.py` for this. Hash each file's changed-line content; on re-runs (amended commits, re-staging, tweaking a message) skip files whose reviewable content is unchanged and replay cached comments. Cuts cost and latency on the common "commit, fix, recommit" loop. *Touches:* new `cache.py`, wired into `engine.py`. Medium effort; needs a cache-invalidation test.

**4. `--strict` blocking mode + `severity_block_threshold` (extension — roadmap)**
v1 is deliberately warn-only (`cli.py` always `exit 0`). Add an **opt-in** `--strict` flag / config key that returns a non-zero exit when a comment at/above a threshold (e.g. `critical`) is found — turning aicr into a real gate for teams that want it, without changing the safe default. *Touches:* `config.py`, `engine.py`, `cli.py`. Small-medium; mostly careful exit-code plumbing + tests.

**5. Token & cost tracking (extension — roadmap)**
OpenRouter returns `usage` in its response, which we currently discard in `openrouter.py`. Capture prompt/completion tokens, surface "~1.2k tokens · ~$0.003" in the summary line, and optionally append to a local `.aicr/usage.log`. Useful once this runs on every commit. *Touches:* `providers/openrouter.py`, `models.py` (`ReviewResult`), `report/`. Small-medium.

**Two strong alternates if you'd swap one out:**
- **Local/offline provider (Ollama)** — directly answers the README's "your code goes to a third party" privacy caveat by allowing fully-local review. Proves the `LLMProvider` adapter with a second impl. *Touches:* new `providers/ollama.py` + `registry.py`.
- **`severity_display_threshold` validation bug** — it's typed as a bare `str` in `config.py:45` with no validation, so a typo silently shows/hides nothing predictably. Small hardening fix.

My recommendation for the best mix of impact and demo value: **#1 (fixes a real bug + big usability win)**, **#2 (onboarding)**, and **#5 or the Ollama provider (shows the adapter pattern paying off)**.

Which of these do you want to move forward with? Once you've picked, toggle to **Act mode** and I'll implement them with tests and doc updates.