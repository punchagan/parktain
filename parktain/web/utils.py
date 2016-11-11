""" Utility functions. """

# Standard library
from functools import wraps
from os.path import abspath, dirname, join
import re

import flask
from flask_dance.contrib.slack import make_slack_blueprint, slack
import yaml

SPECIAL_RE = re.compile('<(.*?)>')
HERE = dirname(abspath(__file__))


def get_id_name_mapping_from_db(session, cls):
    """ Return a mapping of id to name for cls objects in DB."""

    return {obj.id: obj.name for obj in session.query(cls).all()}


# Utilities for templating
def format_slack_message(message, channels, users):
    """Function formats messages into a human readable form.

    Performs the six steps outlined here:
    https://api.slack.com/docs/formatting#how_to_display_formatted_messages

    """

    message_ = message

    # Detect all sequences matching
    for match in SPECIAL_RE.finditer(message):
        match_text = match.groups()[0]
        if '|' in match_text:
            match_text = match_text.rsplit('|', 1)[0]

        # Within those sequences, format content starting with #C as a channel link
        if match_text.startswith('#C'):
            channel_name = '#{}'.format(channels.get(match_text.strip('#'), '<deleted-channel>'))
            message_ = message.replace(message[slice(*match.span())], channel_name)

        # Within those sequences, format content starting with @U as a user link
        elif match_text.startswith('@U'):
            user_name = '@{}'.format(users.get(match_text.strip('@'), '<deleted-user>'))
            message_ = message.replace(message[slice(*match.span())], user_name)

        # Within those sequences, format content starting with ! according to
        # the rules for the special command.
        elif match_text.startswith('!'):
            pass

        else:
            # For remaining sequences, format as a link
            pass

        # Once the format has been determined, check for a pipe - if present,
        # use the text following the pipe as the link label

    return message_


def get_app_config():
    path_to_yaml = join(HERE, '..', 'config.yaml')
    with open(path_to_yaml, 'r') as ymlfile:
        web = yaml.load(ymlfile).get('web')

    default = {'client_id': '', 'client_secret': '', 'secret_key': ''}
    return web or default


def configure_slack_auth(app):
    config = get_app_config()
    app.secret_key = config['secret_key']
    blueprint = make_slack_blueprint(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        scope=["identify", "chat:write:bot"],
    )
    app.register_blueprint(blueprint, url_prefix="/login")


def slack_authorized(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        if not slack.authorized:
            return flask.redirect(flask.url_for('slack.login'))
        return f(*args, **kwargs)
    return _wrapper
