from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

TARGET = 65.0
DATA = Path(__file__).parent / 'data' / 'dashboard_summary.csv'
df = pd.read_csv(DATA, parse_dates=['month'])
national = df[df.scope == 'national'].sort_values('month')
regions = df[df.scope == 'region_latest'].sort_values('digital_adoption_pct')
latest_month = regions.month.max()

MEASURES = {
    'digital_adoption_pct': ('Digital adoption', '%'),
    'cost_per_txn_sar': ('Cost per transaction', ' SAR'),
    'csat': ('CSAT', ''),
    'completion_time_min': ('Completion time', ' min'),
}

app = Dash(__name__)
server = app.server
card = {'padding':'14px','border':'1px solid #ddd','borderRadius':'10px','background':'white'}
app.layout = html.Div([
    html.H1('Tayseer Executive Dashboard | لوحة تيسير التنفيذية'),
    html.P('Decision: where should the next SAR 40M be focused to close the 65% adoption gap?'),
    html.Div([
        html.Div([html.B('National adoption'), html.H2(f"{national.iloc[-1].digital_adoption_pct:.1f}%")], style=card),
        html.Div([html.B('Regions below 65%'), html.H2(str(int((regions.digital_adoption_pct < TARGET).sum())))], style=card),
        html.Div([html.B('Latest month'), html.H2(latest_month.strftime('%b %Y'))], style=card),
        html.Div([html.B('Priority signal'), html.H2('Najran · Al Jouf · Hail')], style=card),
    ], style={'display':'grid','gridTemplateColumns':'repeat(4,1fr)','gap':'10px'}),
    html.Hr(),
    html.Label('Measure / المؤشر'),
    dcc.Dropdown(id='measure', value='digital_adoption_pct', clearable=False,
                 options=[{'label':v[0], 'value':k} for k,v in MEASURES.items()]),
    html.Div(id='filter-state', style={'margin':'10px 0','fontWeight':'bold'}),
    dcc.Graph(id='region-bar'),
    dcc.Graph(id='trend'),
    html.H3('SAR 40M decision support'),
    html.P('Use the regional ranking to focus investigation on the largest adoption gaps. The dashboard does not claim that spending causes a specific adoption lift; allocation is a scenario for executive discussion with a 90-day checkpoint.'),
], style={'maxWidth':'1150px','margin':'auto','fontFamily':'Arial','padding':'20px','background':'#fafafa'})

@app.callback(Output('region-bar','figure'), Output('trend','figure'), Output('filter-state','children'),
              Input('measure','value'), Input('region-bar','clickData'))
def update(measure, click):
    label, suffix = MEASURES[measure]
    r = regions.sort_values(measure)
    colors = ['#D55E00' if (measure == 'digital_adoption_pct' and v < TARGET) else '#B8B8B8' for v in r[measure]]
    bar = px.bar(r, x=measure, y='region', orientation='h', text=measure,
                 title=f'{label} by region — {latest_month:%B %Y}')
    bar.update_traces(marker_color=colors, texttemplate='%{text:.1f}', textposition='outside')
    bar.update_layout(showlegend=False, plot_bgcolor='white', yaxis_title='')
    bar.update_xaxes(rangemode='tozero', title=f'{label}{suffix}')
    if measure == 'digital_adoption_pct':
        bar.add_vline(x=TARGET, line_dash='dash', annotation_text='65% target')

    selected = None
    if click and click.get('points'):
        selected = click['points'][0].get('y')
    if measure == 'digital_adoption_pct':
        trend = px.line(national, x='month', y='digital_adoption_pct', markers=True,
                        title='National digital adoption trend — weighted by unique users')
        trend.add_hline(y=TARGET, line_dash='dash', annotation_text='65% target')
        trend.update_yaxes(title='Digital adoption (%)')
    else:
        trend = px.line(national, x='month', y=measure, markers=True,
                        title=f'National {label.lower()} trend')
        trend.update_yaxes(title=f'{label}{suffix}')
    trend.update_layout(plot_bgcolor='white')
    state = f"Active measure: {label}. " + (f"Selected region: {selected}." if selected else 'Click a regional bar to make the selected state visible.')
    return bar, trend, state

if __name__ == '__main__':
    app.run(debug=False)
