""" Utility functions. """

# Standard library
import re


SPECIAL_RE = re.compile('<(.*?)>')

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
