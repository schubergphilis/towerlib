from towerlib import Tower


def sanitize_record(interaction, current_cassette):
    pass


def get_tower(session, user='admin', password='password'):
    return Tower('localhost:8052', user, password, secure=False, session=session)
