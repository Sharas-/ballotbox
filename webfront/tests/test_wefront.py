import requests
import subprocess

BALLOT_URL = 'http://localhost/ballotapi'
OPTIONS = ['Chilli Pica', 'Delano', 'Gusto Blynai', 'Iki Mishraines']

def setup_module():
    import os, time
    env_vars = dict(os.environ, BALLOT_OPTIONS = ','.join(OPTIONS))
    subprocess.run(['docker-compose', 'up', '--detach', '--build'], check=True, env=env_vars)
    time.sleep(1) # give time for web server in the container to start

def test_can_get_voting_results_without_authentication():
    r = requests.get(BALLOT_URL)
    assert r.status_code == 200

def test_cannot_vote_without_authentication():
    vote = {'option': OPTIONS[0]}
    r = requests.post(BALLOT_URL, json = vote) 
    assert r.status_code == 401

def test_cannot_vote_with_non_existent_user():
    user_auth = ('non existent user', 'some password')
    vote = {'option': OPTIONS[0]}
    r = requests.post(BALLOT_URL, json = vote, auth=user_auth) 
    assert r.status_code == 401

def teardown_module():
    subprocess.run(['docker-compose', 'down'])
