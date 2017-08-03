import os
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
            }, verify=self.verification())
            respObj = json.loads(response.content)
            Tokenator.TOKEN = "bearer " + respObj['access_token']
        else:
            print "reusing security token"

    def verification(self):
        # if we have a ca bundle in the current directory, use that as the certificate verification method,
        # otherwise don't do verification.  get your own by curling https://curl.haxx.se/ca/cacert.pem
        certFile = './cacert.pem'

        if not os.path.exists(certFile):
            return False

        return certFile
