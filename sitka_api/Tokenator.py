import json

import requests


class Tokenator:
    """

    """
    TOKEN = None

    def __init__(self, keystone_url, client_id, client_secret, user, password):
        if self.TOKEN is None:
            print "Getting security token"
            response = requests.post(keystone_url, data={
                "username": user,
                "password": password,
                "grant_type": "password",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": 'keystone openid profile'
            }, verify=False)
            respObj = json.loads(response.content)
            Tokenator.TOKEN = "bearer " + respObj['access_token']
        else:
            print "reusing security token"