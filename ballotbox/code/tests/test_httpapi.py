import requests
import subprocess
from domain.ballotbox import *

BALLOT_URL = 'http://localhost:9393/ballot'
OPTIONS = ['Chilli Pica', 'Delano', 'Gusto Blynai', 'Iki Mishraines']

def setup_module():
    import os, time
    env_vars = dict(os.environ, BALLOT_OPTIONS = ','.join(OPTIONS))
    result = subprocess.run(['docker-compose', '-f', 'tests/startweb-docker-compose.yml', 'up', '--detach', '--build'], check=True, env=env_vars)
    time.sleep(1) # give time for web server in the container to start

def test_ballot_results_are_all_zeros_initially():
    bbox = BallotBox(OPTIONS)
    r = requests.get(BALLOT_URL)
    assert r.status_code == 200
    assert r.json() == bbox.results()

def test_voter_can_vote_only_once():
    user_auth = ('user1', 'pass1') 
    vote = {'option': OPTIONS[0]} 
    r = requests.post(BALLOT_URL, json = vote, auth = user_auth) 
    assert r.status_code == 200
    r = requests.post(BALLOT_URL, json = vote, auth = user_auth) 
    assert r.status_code == 400
    assert 'already voted' in r.json()['description']

def test_cannot_vote_on_nonexistent_ballot_option():
    user_auth = ('user2', 'pass2')
    vote = {'option': 'non existent option'}
    r = requests.post(BALLOT_URL, json = vote, auth = user_auth) 
    assert r.status_code == 400
    assert 'no option' in r.json()['description']

def test_vote_counts_are_aggregated():
    user1_auth = ('user2', 'pass2')
    user2_auth = ('user3', 'pass3')
    option = OPTIONS[1]
    vote_json = {'option': option}
    r = requests.post(BALLOT_URL, json = vote_json, auth = user1_auth) 
    assert r.status_code == 200
    r = requests.post(BALLOT_URL, json = vote_json, auth = user2_auth) 
    assert r.status_code == 200
    r = requests.get(BALLOT_URL)
    assert r.status_code == 200
    assert r.json()[option] == 2
    
def test_can_get_voting_results_without_authentication():
    r = requests.get(BALLOT_URL)
    assert r.status_code == 200

def test_cannot_vote_without_authentication():
    vote = {'option': OPTIONS[0]}
    r = requests.post(BALLOT_URL, json = vote) 
    assert r.status_code == 401

def teardown_module():
    subprocess.run(['docker-compose', '-f', 'tests/startweb-docker-compose.yml', 'down'])

