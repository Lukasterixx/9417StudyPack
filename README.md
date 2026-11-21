# COMP9417 study pack

Study notes and an exam-style multiple-choice question bank for UNSW COMP9417 (Machine Learning, 2026 T3). Notes are written for a visual learner: plain-language explanations, signposting for where each idea sits, and a short "Exam toolkit" for calculator-style questions.

## Contents

| Folder | What is in it |
|---|---|
| `notes/` | One Markdown file per week (W1-W10, R2), a concept map (`MAP.md`) and the exam toolkit (`EX.md`). Figures are in `notes/figs/`. |
| `symbols/` | Per-week glossaries (variable meanings) used for tap-an-equation labels in the app. |
| `exam_style/questions/` | Exam-style question banks in a plain-text format (`=== Q`, options `--- A`..`--- E`, `*` marks correct, `>>` explains each option). |
| `COMP9417_Exam_Drill.html` | The quiz app as one offline file (open it in any browser, including iPad). 880 questions; the 24 questions copied from the released practice exam are left out. |
| `exam_style/tools/` | `qbank.py` (parser and linter), `blind.py` (blind-audit helper), `check_app.py`, `assemble.py` (builds the single-file quiz app). |

## Not included

The UNSW slides, tutorials, the released practice exam and its transcription, and the 24 questions copied from it are left out because they are course-owned material. `assemble.py` needs inputs that are not in the repo, so it will not run from a fresh clone.

## Question format

```
=== Q
topic: ...
kind: calc | concept
diff: ...
--- stem
Question text
--- A
Option text
>> why this option is right or wrong
* --- C
...
--- explain
Overall explanation
```

Check a bank with `python exam_style/tools/qbank.py lint exam_style/questions/EX_bayes.txt`.
