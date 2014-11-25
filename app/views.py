from flask import render_template
from sqlalchemy import desc

from app import app
from app.models import RunInfo, Platform

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/platform/<platform_name>")
def show_runinfo(platform_name):
    platform = Platform.query.filter(Platform.name == platform_name).first_or_404()
    runs = platform.runs.order_by(desc(RunInfo.run_start_date)).all()
    return render_template('runinfo.html', platform=platform, runs=runs)
