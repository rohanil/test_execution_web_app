import subprocess
from sqlalchemy import and_
from models import Request


def run_test(env_id, template, path, session, requester):
    # if path is given then use path for test otherwise use template
    if path != "":
        test_path = "autotest/tests/" + path
        template_for_db = 'Custom Path: ' + path
    else:
        test_path = template
        template_for_db = template

    new_request = Request(environment_id=env_id, template=template_for_db,
                          requester=requester, status='Running')
    session.add(new_request)
    session.commit()

    command = ["py.test", "-k " + test_path]
    stacktrace = None
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        status = "Succeded"
    except subprocess.CalledProcessError as e:
        status = "Failed"
        stacktrace = e.output.replace('\n', '<br />')

    req = session.query(Request).filter(and_(
        Request.environment_id == env_id, Request.status == 'Running')).first()
    req.status = status
    if stacktrace:
        req.stacktrace = stacktrace
    session.commit()


def get_requests_n_ids(session):
    all_requests = session.query(Request).all()
    total_ids = range(1, 101)
    busy_ids = [
        i.environment_id for i in all_requests if i.status == 'Running']
    available_ids = [x for x in total_ids if x not in busy_ids]

    return all_requests, available_ids
