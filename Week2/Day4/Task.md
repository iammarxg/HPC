## Bug Report — AI Code Review Assistant (aicr)

### Bug 1: `aicr init` and `aicr scan` reported different file counts

**Symptom**
Running the setup wizard (`aicr init`) reported a different number of reviewable
files than the actual repository scan (`aicr scan`) later processed — e.g. init
said 12 files, scan reviewed 8.

**Diagnosis**
Both commands share `analyze.py` for file discovery, but only `scan` passed the
`.aicr.yaml` `exclude_paths` globs into the filter. `init`'s `analyze_repo()`
applied the built-in non-source filtering (binaries, heavy dirs) but ignored the
user's configured excludes entirely, so it counted files the scan would later drop.

**Solution**
Added an `exclude_paths` parameter to `analyze_repo()` so it applies the same
effective excludes as `scan`. Also added a `total_excluded_by_config` counter so
the wizard can show a transparent "N tracked · M excluded by your config"
breakdown. Verified with a unit test that a file matching a user glob is counted
as excluded, not reviewable.

---

### Bug 2: The pre-scan token estimate didn't match the files being scanned

**Symptom**
The confirmation prompt before a scan ("About to scan N files, ~X tokens") showed
a token number that didn't correspond to the files actually sent — especially
after `--max-files` capping or excludes trimmed the set.

**Diagnosis**
The CLI displayed the whole-repo token figure from the initial analysis, but the
file list had already been filtered and capped downstream. The number and the
"N files" beside it were computed from two different sets.

**Solution**
Added `estimate_scan_tokens(files)` in `scan.py` that computes the estimate from
the exact `DiffFile` list about to be sent (post-exclude, post-cap), and wired the
CLI to use it. The displayed token count now always matches the files listed.

---

### Bug 3: Token estimates ran ~40% low

**Symptom**
The estimated token usage shown by both `init` and `scan` was consistently far
below actual usage. On one repo the estimate read ~12k tokens while the real run
consumed ~20k.

**Diagnosis**
The estimator counted only file content (≈ characters / 4). But a scan makes one
API call per file, and each call also carries fixed prompt overhead (system
prompt + grounding block + category templates + scaffolding) plus generated
output tokens — none of which were counted. On many small files, that per-call
overhead dominates, producing the large undercount.

**Solution**
Introduced `estimate_total_tokens(chars, file_count)` which adds per-file prompt
overhead and an output allowance on top of the content estimate. After the fix,
the same repo estimates ~19k tokens against ~20k actual. Covered with a unit test
asserting the estimate exceeds the content-only figure and scales with file count.
