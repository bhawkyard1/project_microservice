import functools
import os
import sys
import traceback

from flask import Flask, request
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import project

import logging

logging.basicConfig(level=logging.DEBUG)


def handle_uncaught_exception(type, value, tb):
    """ Log uncaught exceptions, then raise as normal.
    """
    logging.error("Unhandled Exception: %s", "".join(traceback.format_exception(type, value, tb)))
    sys.__excepthook__(type, value, tb)


sys.excepthook = handle_uncaught_exception

logging.info("Creating sqlalchemy engine...")
engine = create_engine("sqlite:///test.db", echo=True, future=True)

logging.info("Setting up tables...")
project.Base.metadata.create_all(engine)

logging.info("Starting app %s...", __name__)
app = Flask(__name__)
logging.info("App running...")


def _log_call(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        logging.info("Calling %s with args %s and kwargs %s", fn, args, kwargs)
        logging.info("Request data is %s", request.get_data())
        result = fn(*args, **kwargs)
        logging.info("%s returns %s", fn, result)
        return result

    return inner


@app.route("/", methods=["GET"])
@_log_call
def main():
    return "Hello World!"


@_log_call
def _add_project():
    session = Session(engine)
    data = request.get_json()
    logging.info("Adding a new project %s", data)
    kwargs = {
        "name": data["name"],
        "path": data["path"]
    }
    proj = project.Project(**kwargs)
    session.add(proj)
    session.commit()
    return f"New project {project} created successfully!"


@_log_call
def _get_projects():
    session = Session(engine)
    params = {k: request.args[k] for k in ("name", "path") if k in request.args}
    matches = session.query(project.Project).filter_by(**params)
    return [p.as_dict() for p in matches]


@app.route("/project", methods=["GET", "POST"])
@_log_call
def project_endpoint():
    if request.method == "GET":
        return _get_projects()
    elif request.method == "POST":
        return _add_project()
