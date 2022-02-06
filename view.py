import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from sqlalchemy import desc

from assets.database import db_session
from assets.models import MatchInfoData
from assets.models import MatchStatsData
from assets.models import PlayerStatsData

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


data = db_session.query(PlayerStatsData.player_name, PlayerStatsData.passes, PlayerStatsData.pass_succeeds).all()

player_name = []
passes = []
pass_succeeds = []

for datum in data:
    player_name.append(datum.player_name)
    passes.append(datum.passes)
    pass_succeeds.append(datum.pass_succeeds)


match_id = db_session.query(MatchInfoData.match_id).all()

# ドロップダウン
cnt = 1
drop_down_options = []
for datum in match_id:

    drop_down_options.append({'label': f'match_{cnt}', 'value': datum.match_id})
    cnt += 1

drop_down_normalize = [{'label': '原系列', 'value': '原系列', 
                        'title': 'もとの株価を表示します.'},
                       {'label': '開始時点を100にする', 'value': '基準化', 
                        'title': '開始時点を100とて比較しやすくします.'},
                       {'label': '正規化', 'value': '正規化', 
                        'disabled': True,
                        'title': '今は使用できません.'}]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# servre = app.server

app.layout = html.Div(children = [

    html.H2(children = 'PythonによるWebスクレイピング〜アプリケーション編〜', style={'textAlign': 'center'}),

    html.Div([html.Div(dcc.Dropdown(id='match_id',
                                              options=drop_down_options,
                                              multi=False,
                                              placeholder='試合'
                                              ),
                                          style={'width': '15%', 'display': 'inline-block',
                                          'margin-right': 10}),
                                 html.Div(dcc.Dropdown(id='player_stats',
                                                       options=drop_down_options,
                                                       multi=False,
                                                       placeholder='選手'),
                                          style={'width': '15%', 'display': 'inline-block',
                                                 'margin-right': 10}),
                                 html.Div(dcc.Dropdown(id='stock_chart_dropdown_normalize',
                                                       options=drop_down_normalize,
                                                       multi=False,
                                                       clearable=False,
                                                       value='原系列'),
                                          style={'width': '20%', 'display': 'inline-block'})
                                 ]),


    # グラフ描画部
    html.Div(children=[
        dcc.Graph(
            id = 'passees_graph',
            figure={
                'data': [
                    go.Bar(
                        x=player_name,
                        y=passes,
                        name='passes',
                        opacity=0.7,
                        yaxis='y1'
                    ),
                    go.Bar(
                        x=player_name,
                        y=pass_succeeds,
                        name='pass_succeeds',
                        opacity=0.5,
                        yaxis='y2'
                    )
                ],
                'layout': go.Layout(
                    title='Player Stats',
                    xaxis=dict(title='date'),
                    yaxis=dict(title='受講生総数', side='left', showgrid=False),
                    yaxis2=dict(title='増加人数', side='right', overlaying='y', showgrid=False),
                    margin=dict(l=200, r=200, b=100, t=100)
                )
            }
        ),
    ]),

    html.Div(id='passes_graph')

], style={
    'textAlign': 'center',
    'width': '1200px'
})

def get_player_stats(match_id):
    data = db_session.query(PlayerStatsData.player_name, PlayerStatsData.passes, PlayerStatsData.pass_succeeds).filter(PlayerStatsData.match_id==match_id).order_by(desc(PlayerStatsData.passes)).all()

    player_name = []
    passes = []
    pass_succeeds = []

    for datum in data:
        player_name.append(datum.player_name)
        passes.append(datum.passes)
        pass_succeeds.append(datum.pass_succeeds)

    return player_name, passes, pass_succeeds

def plot_data(fig, player_name, passes, pass_succeeds, is_first):

    fig.add_trace(go.Bar(x=player_name,
                            y=passes,
                            name='passes',
                        opacity=0.5,
                        yaxis='y2')
                    )

@app.callback(
    Output(component_id='passes_graph', component_property='children'),
    [Input(component_id='match_id', component_property='value')]
)
def update_graph(match_id):

    player_name, passes, pass_succeeds = get_player_stats(match_id)
    
    fig = go.Figure()
    plot_data(fig, player_name, passes, pass_succeeds, is_first=True)

    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run_server(debug=True)
