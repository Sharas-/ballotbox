import falcon
import os
from http_api import ballot
from repos import ballotboxrepo

ENV_BALLOT_OPTIONS = "BALLOT_OPTIONS"

def init_ballot_box_app():
    options_csv = os.environ.get(ENV_BALLOT_OPTIONS, None)
    if not options_csv:
        raise Exception("environment variable {0} is not found or its value is empty".format(ENV_BALLOT_OPTIONS))
    ballot_options = [o.strip() for o in options_csv.split(',') if o]
    ballotboxrepo.init(ballot_options)
    return falcon.API()

api = application = init_ballot_box_app()
api.add_route('/ballot', ballot.Resource())
