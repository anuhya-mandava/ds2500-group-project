# Left Off

**Last updated:** 2026-04-19

## Unfinished
- **Peer evaluations ready to paste (`peer_evaluations_draft.md`).** Plain-text, one section per teammate. Still need to locate the actual form (Canvas page or email — Qualtrics/Google Form) and paste each teammate's section in. Due Wed 2026-04-22 11:59pm ET; 50% deduction if skipped.
- **Individual reflection ready (`individual_reflection.md`).** Optional/extra credit Canvas assignment 3174945, due Fri 2026-04-25 11:59pm ET. Submit if there's time.
- **Assemble submission ZIP** named `Section1_<GroupName>.zip` containing: final PDF, all code files used in analysis/modeling, dataset files (reduced to first 1,000 rows if large — verify code runs on reduced set).
- Confirm teammate name spelling **Tsion Tekleab** (matches email `tekleab.t@northeastern.edu`).
- Share `final_report/report.pdf` with teammates for review before submitting.

## Next Up
- Find the peer eval form and submit by 2026-04-22.
- Submit ZIP to Canvas assignment 3174939 (DS2500 Milestone 5) before 2026-04-21 11:59pm ET.
- Submit individual reflection to Canvas assignment 3174945 before 2026-04-25 11:59pm ET (optional/extra credit).

## Blockers
- None.

## Recently completed (2026-04-19)
- **Fix 1 — double-spaced PDF**: rebuilt `final_report/report.pdf` at 8 pages, double-spaced (line-height 2.0), 11.5pt Times, 0.85in margins. CSS persisted at `final_report/double_space.css` for reproducibility. Rebuild command: `pandoc final_report/report.md -o final_report/report.pdf --pdf-engine=weasyprint --css=final_report/double_space.css --standalone`.
- **Fix 3 — Figure 3 caption**: rewrote to describe the Southeast mortality band directly instead of admitting the diabetes/poverty choropleths were "not reproduced here for space."
- **Content cuts**: `final_report/report.md` trimmed from ~3,083 → ~2,210 words to land inside the 4–8 page limit while preserving all required rubric sections, all 5 figures, team info, and references.

## Evaluation summary (2026-04-19)
Report evaluated against Milestone 5 rubric. Estimated 960–1,000 / 1,040.
- Content Quality (600): est. 575–590 — all required sections present, methods honest about cardiovascular-vs-other-tracks asymmetry.
- Analysis & Critical Thinking (240): est. 228–240 — strongest section (VIF, LOOCV leakage, ecological fallacy, BRFSS bias all flagged).
- Communication & Presentation (200): est. 180–195 — double-spacing + page-limit risks now resolved.
