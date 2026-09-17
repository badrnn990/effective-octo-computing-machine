# Tayseer Digital Services — Executive Dashboard & Data Story

**SDAIA Academy · SDA-DSC-112 · Data Visualization & Storytelling**

Decision-ready capstone built around the Tayseer golden thread.

## Executive decision
**Question:** Where should the next **SAR 40 million** be focused to help lagging regions close the **65% digital-adoption target**?

Using the official course dataset (Jan 2024–Dec 2025), the user-weighted national adoption rate reaches **66.1% in Dec 2025**, while **9 of 13 regions remain below 65%**. The three lowest latest-month regions are **Najran 50.0%**, **Al Jouf 55.8%**, and **Hail 58.1%**. These facts motivate investigation and scenario planning; they do **not** prove that a specific spend causes a specific adoption lift.

## Repository structure
```text
.
├── README.md
├── requirements.txt
├── app.py
├── data/
│   ├── dashboard_summary.csv
│   └── README.md
├── notebooks/
│   └── lab1_solution.ipynb
└── docs/
    ├── CAPSTONE_CHECKLIST.md
    ├── DATA_DICTIONARY.md
    └── STORYBOARD.md
```

## Dashboard
The default view answers the core question before any click: headline KPI, count below target, sorted regional comparison, 65% reference line, national trend, and a priority signal. A measure toggle exposes adoption, cost per transaction, CSAT and completion time. Clicking a regional bar makes the selected state visible.

### Correct metric logic
Digital adoption is non-additive and is recomputed with `unique_users` as weights:

`SUM(digital_adoption_pct × unique_users) / SUM(unique_users)`

The committed `data/dashboard_summary.csv` is a reproducible dashboard-ready extract calculated from the official supplied Tayseer CSV using that logic. It keeps the application lightweight and runnable directly from the repository.

## Run
```bash
pip install -r requirements.txt
python app.py
```
Then open the local Dash URL printed in the terminal.

## Seven-scene executive story
1. BLUF / decision ask.
2. Situation — national progress.
3. Complication — regional gap remains.
4. Evidence — sorted regional comparison and target.
5. Options — compare transparent SAR 40M allocation scenarios.
6. Recommendation — focus investigation/intervention on the largest gaps, with assumptions stated.
7. Ask — approve the chosen scenario and review at a 90-day checkpoint.

See `docs/STORYBOARD.md` for speaker flow and `docs/CAPSTONE_CHECKLIST.md` for submission checks.

## Lab evidence
`notebooks/lab1_solution.ipynb` implements the required five encodings, decoding-accuracy ranking, bad-dashboard audit, and corrected one-highlight chart.

## Course
- **Course:** Data Visualization and Storytelling / تصور البيانات وسرد القصص
- **Code:** SDA-DSC-112
- **Provider:** SDAIA Academy
- **Capstone:** Tayseer executive dashboard + 7-minute data story
