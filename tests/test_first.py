from wayback_discover_diff import Discover
from flask import json
import os
import yaml
from celery import Celery

with open(os.environ['WAYBACK_DISCOVER_DIFF_CONF'], 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

app = Discover(cfg)

# Initialize Celery and register Discover task.
celery = Celery(__name__, broker='redis://'+str(cfg['redis']['host'])+':'+str(cfg['redis']['port']))
celery.conf.update(
    CELERY_BROKER_URL='redis://'+str(cfg['redis']['host'])+':'+str(cfg['redis']['port']),
    CELERY_RESULT_BACKEND='redis://'+str(cfg['redis']['host'])+':'+str(cfg['redis']['port'])
)
celery.register_task(app)


def test_no_url():
    url = None
    timestamp = '20141115130953'
    result = app.simhash(url, timestamp)
    assert json.dumps({'error': 'URL is required.'}) == result


def test_no_timestamp():
    url = 'iskme.org'
    timestamp = None
    result = app.simhash(url, timestamp)
    assert json.dumps({'error': 'Timestamp is required.'}) == result


def test_no_entry():
    url = 'nonexistingdomain.org'
    timestamp = '20180000000000'
    result = app.simhash(url, timestamp)
    assert json.dumps({'simhash': 'None'}) == result


def test_start_task():
    url = 'iskme.org'
    year = '2018'
    job_id = celery.tasks['Discover'].apply_async(args=[url, year])
    assert job_id is not None


def test_task_no_url():
    url = None
    year = '2018'
    job = celery.tasks['Discover'].apply(args=[url, year])
    assert job.get() == json.dumps({'status':'error', 'info': 'URL is required.'})


def test_task_no_year():
    url = 'nonexistingdomain.org'
    year = None
    job = celery.tasks['Discover'].apply(args=[url, year])
    assert job.get() == json.dumps({'status':'error', 'info': 'Year is required.'})