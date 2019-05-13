from domain.ballotbox import BallotBox
from pickle import Pickler, Unpickler

_STATE_FILE = 'ballot_box.pickle'

def init(options):
    save_ballotbox(BallotBox(options))

def get_ballotbox():
    with open(_STATE_FILE, 'rb') as file:
        return Unpickler(file).load()

def save_ballotbox(ballotbox):
    with open(_STATE_FILE, 'wb+') as file:
        return Pickler(file).dump(ballotbox)
