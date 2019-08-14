from towerlib import Tower
from requests import Session
import os
from pprint import pprint


def sanitize_record(interaction, current_cassette):
    pass


def get_tower(user='admin', password='password', session=None):
    return Tower('localhost:8052', user, password, secure=False, session=session)
