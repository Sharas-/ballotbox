import falcon
from repos import ballotboxrepo as repo


def _read_voterid(req):
    auth_token = req.auth
    if auth_token is None:
        raise falcon.HTTPUnauthorized('Auth token required', 'Voter id must be provided in a form of authorization token', ['Basic'])
    return auth_token

def _read_option(req):
    if not req.content_length:
        raise falcon.HTTPBadRequest(description='Request body has to have a ballot option')
    if req.content_type and falcon.MEDIA_JSON in req.content_type:
        option_key = 'option'
        option = req.media.get(option_key, None)
        if not option:
            raise falcon.HTTPBadRequest(description="JSON request has to have property named {} initialized with ballot option".format(option_key))
        return option
    req_string = req.stream.read().decode('utf-8')
    return req_string.strip() 

class Resource(object):

    def on_get(self, req, resp):
        """
        Returns: Ballot results.
        """
        ballotbox = repo.get_ballotbox()
        resp.media = ballotbox.results()
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """
        Cast a vote in this ballot with a single ballot option in request body and voter id in Authorization header
        """ 
        voterid = _read_voterid(req)
        option = _read_option(req)
        bbox = repo.get_ballotbox()
        try:
            bbox.cast_vote(voterid, option)
        except ValueError as e:
            raise falcon.HTTPBadRequest(description=str(e))
        repo.save_ballotbox(bbox)
        resp.status = falcon.HTTP_200
