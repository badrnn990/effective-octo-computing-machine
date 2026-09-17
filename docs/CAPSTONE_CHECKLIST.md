# SDA-DSC-112 Capstone Evidence Checklist

This checklist maps repository evidence to the requirements described in the SDAIA instructor training material.

## Dashboard project

- [x] Tayseer dataset is the project golden thread.
- [x] Executive decision question is explicit.
- [x] KPI headline is defined.
- [x] 65% adoption target is visible.
- [x] Regional breakdown is sorted for decision use.
- [x] Monthly trend is included.
- [x] Multi-view interactive dashboard implementation is provided.
- [x] Region filtering is provided.
- [x] Measure toggle is provided.
- [x] Active filter state is displayed.
- [x] Non-additive adoption percentage is recomputed with user weighting.
- [x] Default state is designed to answer the primary question before interaction.
- [x] Supporting metrics include users, CSAT, transaction cost, and completion time.
- [x] Charts use direct titles/reference lines rather than a gauge wall.
- [x] Source code and dependency file are included for reproducibility.

## Visual craft

- [x] Position/length are preferred for regional comparison.
- [x] Colour is used sparingly and does not carry the only meaning.
- [x] Target reference is explicitly labelled.
- [x] Titles communicate the takeaway/question.
- [x] Decorative non-data ink is minimized.
- [x] Dashboard is structured in an inverted-pyramid hierarchy.

## Storytelling

- [x] One Big Idea is documented.
- [x] Seven-scene executive arc is documented.
- [x] BLUF appears first.
- [x] Situation and complication are separated.
- [x] Evidence scene carries the central argument.
- [x] Options for SAR 40M are compared transparently.
- [x] Recommendation is tied to evidence without inventing causal ROI.
- [x] Ask is repeated at the close.
- [x] 90-day checkpoint is included.

## Live presentation items

These require the participant during delivery and cannot be proven by repository code alone:

- [ ] Rehearse the briefing to seven minutes.
- [ ] Deliver BLUF within the first 30 seconds.
- [ ] Use one message per presentation slide/scene.
- [ ] Practice chart explanation and transitions.
- [ ] Prepare concise Steering Committee Q&A responses.
- [ ] Maintain time discipline and presence.

## Pre-submission verification

1. Put the official `tayseer_services.csv` in `data/`.
2. Run `pip install -r requirements.txt`.
3. Run `python app.py`.
4. Confirm headline KPIs render with no filter selected.
5. Test every region filter and measure toggle.
6. Confirm active filter state always matches the view.
7. Rehearse the seven-scene story using `STORYBOARD.md`.
8. Do not present the allocation model as a causal forecast; it is decision support based on available fields.
