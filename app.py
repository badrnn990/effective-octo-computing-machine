from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

DATA_PATH = Path(__file__).parent / "data" / "tayseer_services.csv"
TARGET = 65.0
REQUIRED = {
    "month",
    "region",
    "digital_adoption_pct",
    "unique_users",
    "cost_per_txn_sar",
    "csat",
    "completion_time_min",
}


def load_data(path=DATA_PATH):
    if not path.exists():
        raise FileNotFoundError(
            "Official dataset not found. Place tayseer_services.csv in the data/ folder."
        )
    df = pd.read_csv(path)
    missing = REQUIRED.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    df = df.copy()
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    for col in REQUIRED - {"month", "region"}:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["month", "region", "digital_adoption_pct", "unique_users"])


def weighted_adoption(frame):
    valid = frame.dropna(subset=["digital_adoption_pct", "unique_users"])
    weights = valid["unique_users"].clip(lower=0)
    if valid.empty or weights.sum() == 0:
        return np.nan
    return np.average(valid["digital_adoption_pct"], weights=weights)


def region_summary(frame):
    rows = []
    for region, group in frame.groupby("region", observed=True):
        adoption = weighted_adoption(group)
        rows.append(
            {
                "region": region,
                "digital_adoption_pct": adoption,
                "gap_to_target": max(TARGET - adoption, 0) if pd.notna(adoption) else np.nan,
                "unique_users": group["unique_users"].sum(),
                "cost_per_txn_sar": np.average(
                    group["cost_per_txn_sar"].fillna(0),
                    weights=group["unique_users"].clip(lower=0),
                ) if group["unique_users"].clip(lower=0).sum() else np.nan,
                "csat": np.average(
                    group["csat"].fillna(0),
                    weights=group["unique_users"].clip(lower=0),
                ) if group["unique_users"].clip(lower=0).sum() else np.nan,
                "completion_time_min": np.average(
                    group["completion_time_min"].fillna(0),
                    weights=group["unique_users"].clip(lower=0),
                ) if group["unique_users"].clip(lower=0).sum() else np.nan,
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty:
        out["priority_signal"] = out["gap_to_target"] * out["unique_users"]
    return out


df = load_data()
regions = sorted(df["region"].dropna().astype(str).unique())

MEASURES = {
    "digital_adoption_pct": "Digital adoption (%)",
    "csat": "Customer satisfaction (CSAT)",
    "cost_per_txn_sar": "Cost per transaction (SAR)",
    "completion_time_min": "Completion time (min)",
}

app = Dash(__name__)
app.title = "Tayseer Executive Dashboard"

CARD = {
    "padding": "14px 18px",
    "border": "1px solid #ddd",
    "borderRadius": "10px",
    "minWidth": "180px",
    "flex": "1",
}

app.layout = html.Div(
    [
        html.H1("Tayseer Digital Services — Executive Dashboard"),
        html.P(
            "Decision question: Where should the next SAR 40M be focused to help lagging regions reach 65% digital adoption by December?"
        ),
        html.Div(
            [
                html.Div([html.Small("National adoption"), html.H2(id="kpi-adoption")], style=CARD),
                html.Div([html.Small("Regions below 65%"), html.H2(id="kpi-below")], style=CARD),
                html.Div([html.Small("Unique users"), html.H2(id="kpi-users")], style=CARD),
                html.Div([html.Small("Gap vs target"), html.H2(id="kpi-gap")], style=CARD),
            ],
            style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Region filter"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[{"label": r, "value": r} for r in regions],
                            multi=True,
                            placeholder="All regions (national view)",
                        ),
                    ],
                    style={"flex": "2", "minWidth": "280px"},
                ),
                html.Div(
                    [
                        html.Label("Measure"),
                        dcc.Dropdown(
                            id="measure",
                            options=[{"label": label, "value": key} for key, label in MEASURES.items()],
                            value="digital_adoption_pct",
                            clearable=False,
                        ),
                    ],
                    style={"flex": "1", "minWidth": "240px"},
                ),
            ],
            style={"display": "flex", "gap": "18px", "flexWrap": "wrap"},
        ),
        html.P(id="filter-state", style={"fontWeight": "600"}),
        dcc.Graph(id="region-bar"),
        dcc.Graph(id="trend"),
        html.H2("Prioritisation evidence"),
        html.P(
            "Priority signal = positive adoption gap × unique users. It is a transparent decision-support signal, not a causal ROI forecast."
        ),
        dcc.Graph(id="priority"),
        html.P(
            "Use the dashboard with docs/STORYBOARD.md for the seven-minute executive briefing."
        ),
    ],
    style={"maxWidth": "1180px", "margin": "0 auto", "padding": "24px", "fontFamily": "Arial, sans-serif"},
)


@app.callback(
    Output("kpi-adoption", "children"),
    Output("kpi-below", "children"),
    Output("kpi-users", "children"),
    Output("kpi-gap", "children"),
    Output("filter-state", "children"),
    Output("region-bar", "figure"),
    Output("trend", "figure"),
    Output("priority", "figure"),
    Input("region-filter", "value"),
    Input("measure", "value"),
)
def update_dashboard(selected_regions, measure):
    frame = df if not selected_regions else df[df["region"].isin(selected_regions)]
    adoption = weighted_adoption(frame)
    summary = region_summary(frame)
    below = int((summary["digital_adoption_pct"] < TARGET).sum()) if not summary.empty else 0
    users = frame["unique_users"].sum()
    gap = adoption - TARGET if pd.notna(adoption) else np.nan

    state = "Scope: National — all regions" if not selected_regions else "Scope: " + ", ".join(selected_regions)
    state += f" | Measure: {MEASURES[measure]}"

    plot = summary.sort_values(measure, ascending=True)
    bar = px.bar(
        plot,
        x=measure,
        y="region",
        orientation="h",
        hover_data=["digital_adoption_pct", "unique_users", "gap_to_target"],
        title=f"Regional comparison — {MEASURES[measure]}",
        labels={measure: MEASURES[measure], "region": "Region"},
    )
    if measure == "digital_adoption_pct":
        bar.add_vline(x=TARGET, line_dash="dash", annotation_text="65% target")
    bar.update_layout(yaxis={"categoryorder": "total ascending"}, margin={"l": 120, "r": 30, "t": 70, "b": 50})

    trend_rows = []
    for month, group in frame.groupby("month"):
        if measure == "digital_adoption_pct":
            value = weighted_adoption(group)
        else:
            w = group["unique_users"].clip(lower=0)
            value = np.average(group[measure].fillna(0), weights=w) if w.sum() else np.nan
        trend_rows.append({"month": month, "value": value})
    trend_df = pd.DataFrame(trend_rows).sort_values("month")
    trend = px.line(
        trend_df,
        x="month",
        y="value",
        markers=True,
        title=f"Monthly trend — {MEASURES[measure]} ({'national' if not selected_regions else 'selected scope'})",
        labels={"month": "Month", "value": MEASURES[measure]},
    )
    if measure == "digital_adoption_pct":
        trend.add_hline(y=TARGET, line_dash="dash", annotation_text="65% target")

    priority_df = summary[summary["gap_to_target"] > 0].sort_values("priority_signal", ascending=True)
    priority = px.bar(
        priority_df,
        x="priority_signal",
        y="region",
        orientation="h",
        title="Below-target regions — material gap signal (gap × users)",
        labels={"priority_signal": "Gap × unique users", "region": "Region"},
        hover_data=["digital_adoption_pct", "gap_to_target", "unique_users", "csat", "cost_per_txn_sar", "completion_time_min"],
    )
    priority.update_layout(margin={"l": 120, "r": 30, "t": 70, "b": 50})

    return (
        f"{adoption:.1f}%" if pd.notna(adoption) else "N/A",
        str(below),
        f"{users:,.0f}",
        f"{gap:+.1f} pp" if pd.notna(gap) else "N/A",
        state,
        bar,
        trend,
        priority,
    )


if __name__ == "__main__":
    app.run(debug=True)
