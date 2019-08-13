from betamax.cassette import cassette
from pprint import pprint


def sanitize_record(interaction, current_cassette):
    sanitize_token(interaction, current_cassette)


def sanitize_token(interaction, current_cassette):
    if interaction.data['response']['status']['code'] != 200:
        return

    headers = interaction.data['response']['headers']
    token = headers.get('Authorization')

    # If there was no token header in the response, exit
    if token is None:
        return

    current_cassette.placeholders.append(
        cassette.Placeholder(placeholder='<AUTH_TOKEN>', replace=token)
    )

