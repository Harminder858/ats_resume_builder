# app/dashboard.py

from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import requests

def create_dashboard(app):
    app.layout = html.Div([
        html.H1('ATS Resume Matcher'),
        
        html.Div([
            html.Div([
                html.H3('Job Description'),
                dcc.Textarea(
                    id='jd-input',
                    placeholder='Paste the job description here...',
                    style={'width': '100%', 'height': 300},
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.H3('Resume'),
                dcc.Textarea(
                    id='resume-input',
                    placeholder='Paste the resume here...',
                    style={'width': '100%', 'height': 300},
                ),
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        ]),
        
        html.Button('Match Resume', id='match-button', n_clicks=0),
        
        html.Div(id='match-results'),
        
        dcc.Graph(id='score-chart')
    ])

    @app.callback(
        [Output('match-results', 'children'),
         Output('score-chart', 'figure')],
        [Input('match-button', 'n_clicks')],
        [State('jd-input', 'value'),
         State('resume-input', 'value')]
    )
    def update_match_results(n_clicks, jd, resume):
        if n_clicks > 0 and jd and resume:
            response = requests.post('http://localhost:5000/api/match', json={
                'job_description': jd,
                'resume': resume
            })
            
            if response.status_code == 200:
                result = response.json()
                
                # Create a bar chart of scores
                categories = list(result['scores'].keys())
                scores = list(result['scores'].values())
                
                fig = go.Figure(data=[
                    go.Bar(x=categories, y=scores)
                ])
                
                fig.update_layout(
                    title='ATS Match Scores',
                    yaxis_title='Score',
                    yaxis=dict(range=[0, 10])
                )
                
                suggestions = html.Ul([html.Li(s) for s in result['suggestions']])
                
                return (
                    [
                        html.H3(f"Overall Score: {result['overall_score']:.2f}/10"),
                        html.H4("Suggestions for Improvement:"),
                        suggestions
                    ],
                    fig
                )
            else:
                return "Error in processing request", go.Figure()
        
        return "Please enter both job description and resume, then click 'Match Resume'", go.Figure()

    return app