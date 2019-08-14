from towerlib import Tower as TowerOriginal
from requests import Session
import os
from pprint import pprint


class Tower(TowerOriginal):  # pylint: disable=too-many-public-methods
    """Models the api of ansible tower."""

    def __init__(self, host, username, password, secure=False, ssl_verify=True, session=None):  # pylint: disable=too-many-arguments
        super(host, username, password, secure, ssl_verify)
        self.session = self._setup_session(secure, ssl_verify, session)

    def _setup_session(self, secure, ssl_verify, session=None):
        session = Session() if not session else session
        if secure:
            session.verify = ssl_verify
        session.get(self.host)
        session.auth = (self.username, self.password)
        session.headers.update({'content-type': 'application/json'})
        url = '{api}/me/'.format(api=self.api)
        response = session.get(url)
        if response.status_code == 401:
            raise AuthFailed(response.content)
        return session



def sanitize_record(interaction, current_cassette):
    pass


def get_tower(user='admin', password='password'):
    return Tower('localhost:8052', user, password, secure=False)
