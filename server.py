import time

from flask import Flask, render_template, request
from sqlalchemy import and_
from multiprocessing import Process
from flask.ext.sqlalchemy import SQLAlchemy

from utils import run_test, get_requests_n_ids
from database import db_session


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET', 'POST'])
def modules():
    if request.method == 'GET':
        all_requests, available_ids = get_requests_n_ids(db_session)
    elif request.method == 'POST':
        # start subprocess to run test in request
        p = Process(target=run_test, args=(
            request.form['env'], request.form['template'],
            request.form['path'], db_session, request.form['requester'],))
        p.start()
        # wait for 2 seconds till subprocess commits new request to db
        time.sleep(2)
        all_requests, available_ids = get_requests_n_ids(db_session)
    return render_template('index.html', available_ids=available_ids,
                           all_requests=all_requests)


@app.route('/logs/<int:req_id>')
def get_stacktrace(req_id):
    from models import Request
    req_stacktrace = db_session.query(Request.stacktrace).filter(and_(
        Request.id == str(req_id), Request.status == 'Failed')).first()

    return render_template('stacktrace.html', req_stacktrace=req_stacktrace[0])


if __name__ == '__main__':
    app.run(debug=True)
