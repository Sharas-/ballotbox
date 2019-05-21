import pytest
import requests
import subprocess
from datetime import date

MANGER_DIR= '../manger'
MANGER_HOST = 'http://localhost:8080'
FLYERS_URL = f"{MANGER_HOST}/flyers"
TODAYS_MENUS_URL = f"{MANGER_HOST}/todays_menus"
BALLOT_URL = 'http://localhost/ballotapi'

TODAY = str(date.today())

MENUS = [(('restaurant1', 'pass1'), {'restaurant_name': "best restaurant 1", 'date' : TODAY, 'menu' : 'kokletai, kompotas'}),
         (('restaurant2', 'pass2'), {'restaurant_name': "best restaurant 2", 'date' : TODAY, 'menu' : 'kokletai, kompotas'}),
         (('restaurant3', 'pass3'), {'restaurant_name': "best restaurant 3", 'date' : TODAY, 'menu' : 'geresni kokletai, kompotas'}),
         (('restaurant4', 'pass4'), {'restaurant_name': "best restaurant 4", 'date' : TODAY, 'menu' : 'geresni kokletai, kompotas'}),
         (('restaurant5', 'pass5'), {'restaurant_name': "best restaurant 5", 'date' : TODAY, 'menu' : 'geresni kokletai, kompotas'})]

VOTES = [(('user1', 'pass1'), {'option': "best restaurant 2"}),
         (('user2', 'pass2'), {'option': "best restaurant 1"}),
         (('user3', 'pass3'), {'option': "best restaurant 2"}),
         (('user4', 'pass4'), {'option': "best restaurant 5"}),
         (('user5', 'pass5'), {'option': "best restaurant 5"})]

EXPECTED_RESULT = {"best restaurant 2": 2,
                   "best restaurant 1": 1,
                   "best restaurant 5": 2,
                   "best restaurant 3": 0,
                   "best restaurant 4": 0}

def populate_menus(menus):
    for item in menus:
        auth, menu = item
        r = requests.put(FLYERS_URL, json = menu, auth=auth) 
        assert r.status_code == 200
        
def cast_votes(votes):
    for item in votes:
        auth, vote = item
        r = requests.post(BALLOT_URL, json = vote, auth=auth) 
        assert r.status_code == 200

def setup_module():
    subprocess.check_call([f"cd {MANGER_DIR} && docker-compose up -d && cd -"], shell=True)
    populate_menus(MENUS)
    todays_menus = requests.get(TODAYS_MENUS_URL).content
    p = subprocess.Popen(["./startballot"], stdin=subprocess.PIPE)
    p.communicate(todays_menus) 

def test_ballot_results_correct():
    cast_votes(VOTES) 
    r = requests.get(BALLOT_URL)
    assert r.json() == EXPECTED_RESULT

def teardown_module():
    subprocess.check_call([f"cd {MANGER_DIR} && docker-compose down && cd - && ./stopballot"], shell=True)
