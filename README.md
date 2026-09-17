# Tayseer Digital Services — Executive Dashboard & Data Story

**SDAIA Academy · SDA-DSC-112 · Data Visualization & Storytelling**

This repository contains the capstone project for SDAIA Academy's **Data Visualization and Storytelling** course. The project turns the Tayseer National Digital Services dataset into a decision-ready executive dashboard and a concise data story.

## Executive decision

**Decision question:** Where should the next **SAR 40 million** be directed to help lagging regions reach the **65% digital-adoption target by December**?

The project is designed for a simulated Steering Committee. It prioritizes decision clarity, honest visual encoding, accessibility, visible filter state, and self-service exploration.

## Project objectives

- Show the national digital-adoption KPI and the 65% target clearly.
- Identify regions below target and quantify their adoption gaps.
- Show the adoption trend over time.
- Allow users to filter and drill into regional performance.
- Recompute percentage metrics correctly under filters rather than using an unsafe average-of-averages.
- Compare lagging regions using decision-relevant measures such as adoption, users, cost per transaction, CSAT, and completion time.
- Translate the analysis into a seven-scene executive narrative with a clear BLUF and decision ask.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── app.py
├── data/
│   └── README.md
├── docs/
│   ├── CAPSTONE_CHECKLIST.md
│   ├── DATA_DICTIONARY.md
│   └── STORYBOARD.md
└── factory_dashboard_colab (1).ipynb   # legacy file; retained temporarily during rebuild
```

## Dashboard design

The default state is intentionally useful before any click. It contains:

1. **Headline KPI** — weighted national digital adoption versus the 65% target.
2. **Regional gap view** — sorted regions with a visible target reference.
3. **Monthly trend** — adoption over time.
4. **Interactive controls** — region and measure selectors with the active state displayed.
5. **Supporting KPIs** — unique users, CSAT, cost per transaction, and completion time.

### Metric correctness

Digital adoption is treated as a non-additive percentage. At national or filtered level it is recomputed as a user-weighted percentage:

`SUM(digital_adoption_pct × unique_users) / SUM(unique_users)`

This avoids the common average-of-averages error.

## Executive story — seven scenes

1. **BLUF** — state the recommendation and decision required.
2. **Situation** — establish current Tayseer adoption.
3. **Complication** — identify regions that remain below 65%.
4. **Evidence** — use one annotated visual to carry the main argument.
5. **Options** — compare possible uses of the SAR 40M.
6. **Recommendation** — focus intervention on the lagging regions using transparent criteria.
7. **Ask** — request approval and propose a 90-day checkpoint.

See [`docs/STORYBOARD.md`](docs/STORYBOARD.md) for the presentation plan.

## Run locally

1. Place the official `tayseer_services.csv` file in `data/tayseer_services.csv`.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the dashboard:

```bash
python app.py
```

4. Open the local Dash URL shown in the terminal.

## Assessment alignment

The repository is structured around the SDAIA course outcomes: honest chart choice, decluttering and annotation, interactive multi-view dashboard design, visible filter/drill state, accessibility, narrative structure, and executive delivery. A detailed evidence checklist is provided in [`docs/CAPSTONE_CHECKLIST.md`](docs/CAPSTONE_CHECKLIST.md).

## Course

- **Course:** Data Visualization and Storytelling / تصور البيانات وسرد القصص
- **Code:** SDA-DSC-112
- **Provider:** SDAIA Academy
- **Capstone:** Tayseer National Digital Services executive dashboard and storytelling briefing

> This repository is being rebuilt from an earlier unrelated prototype so the final submission follows the Tayseer golden thread used throughout SDA-DSC-112.
