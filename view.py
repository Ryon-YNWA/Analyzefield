import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from assets.database import db_session
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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# servre = app.server

app.layout = html.Div(children = [

    html.H2(children = 'PythonによるWebスクレイピング〜アプリケーション編〜', style={'textAlign': 'center'}),
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
    ])
], style={
    'textAlign': 'center',
    'width': '1200px'
})


if __name__ == '__main__':
    app.run_server(debug=True)
