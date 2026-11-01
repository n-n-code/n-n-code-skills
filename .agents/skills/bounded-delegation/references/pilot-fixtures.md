# Paired pilot fixtures

`../scripts/pilot_cases.py` prepares four small, runnable evaluation tasks using
only Python's standard library. Each case has byte-identical `baseline` and
`candidate` inputs and a raw `task.txt` that describes work without choosing a
model or delegation strategy. Give each worker only its own directory and task;
apply the routing policy outside that task. Keep the grader script outside the
worker's permitted context.

```console
python .agents/skills/bounded-delegation/scripts/pilot_cases.py prepare --dest ABSENT_ABSOLUTE_DIRECTORY
python .agents/skills/bounded-delegation/scripts/pilot_cases.py grader --root SAME_ABSOLUTE_DIRECTORY
```

Use task-artifact storage or a temporary location outside the checkout. Preparation
refuses an existing destination and never deletes it. It creates `manifest.json`
and `p1` through `p4`, each containing `baseline/` and `candidate/`. No expected
answers or grader are copied into those worker directories. The unique run ID is
identical between paired arms and must appear in their outputs; a fresh preparation
therefore rejects outputs copied unchanged from an earlier run.

| Pilot | Worker input | Required worker output | Independent check |
| --- | --- | --- | --- |
| P1: factual extraction | Large synthetic operating ledger; five requested active facts | `answer.json` with run ID, values, relative paths, exact quotes, and 1-based lines | Exact requested records plus source locations and quotations |
| P2: bounded inventory | Python source tree with executable, dynamic, commented, and excluded matches | `answer.json` with run ID and matching call paths, lines, enclosing functions | Complete inventory within the stated path and syntax boundaries |
| P3: predictable tests | Real normalization function, explicit behavior contract, representative unittest style | `generated/test_labels.py`, including run constant | At least five discovered tests pass the correct implementation without skips; the same suite detects every independent behavior mutant |
| P4: config/type scaffold | Reference dataclass and exact field/profile specification | `generated/mirror_config.py` and `generated/profiles.json`, including run identifiers | Real dataclass field types, defaults, immutability, construction, and exact JSON schema/values |

The grader reconstructs original inputs from its own definitions and fails any
worker whose supplied inputs were removed or changed. It rejects missing outputs,
wrong run identifiers, malformed JSON, duplicate JSON keys, incorrect evidence,
empty or failing suites, skipped/expected-failure tests, surviving mutants, and
invalid scaffolds. Unexpected output files and symlinks fail. Python `.pyc` files
inside `__pycache__` directories are tolerated and listed in `ignored_bytecode_files`;
grading executes fresh source copies without those caches. P3 mutations independently challenge whitespace trimming,
Unicode case folding, deduplication, empty segments, first-seen order, truncation,
boolean limits, both numeric bounds, and value-type validation. They are not
available in worker inputs. All must be detected; this fixture uses no partial
credit threshold to turn a weak test suite into a pass.

Grading emits a single JSON result to stdout. Exit status is 0 when all eight arms
pass, 1 for a failed arm, and 2 for an invalid invocation state. Inspect per-arm
results even when the overall result fails because another worker is unfinished.
Validation subprocess output is captured and never mixed with the JSON report.
Only fixed Python invocations are used; no submitted shell commands are executed.

P3 and P4 execute generated Python in fresh interpreter processes with a timeout.
Import checks constrain the task contract but are **not a security sandbox**;
grade trusted, reviewed agent output only. P3 and P4 run against temporary copies
and do not replace worker source files. Timeout, discovery failure,
or invalid runner output cannot count as a successful result. Temporary grading
directories are removed by Python's temporary-directory context manager.

These fixtures grade output correctness, not elapsed time, tokens, cost, or model
identity. Record those separately for both arms using the same task, context, and
completion boundary. Do not expose the oracle to workers, let one arm read the
other, reuse completed output directories, or report a faster incorrect result as
a delegation win. Keep individual results and transcripts outside this repository.
