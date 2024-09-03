# app/main.py

from flask import Flask, render_template, jsonify, request
from dash import Dash
from .dashboard import create_dashboard
from .ats_matcher.matcher import match_resume_to_jd

app = Flask(__name__)

# Initialize Dash app
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')
create_dashboard(dash_app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/match', methods=['POST'])
def match_resume():
    data = request.json
    jd = data.get('job_description')
    resume = data.get('resume')
    
    if not jd or not resume:
        return jsonify({'error': 'Both job description and resume are required'}), 400
    
    match_result = match_resume_to_jd(jd, resume)
    return jsonify(match_result)

server = app.server

if __name__ == '__main__':
    app.run(debug=True)
