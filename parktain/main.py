#!/usr/bin/env python

# Standard library
from datetime import datetime
from os.path import abspath, dirname, join
import re

# 3rd party library
from gendo import Gendo


class Parktain(Gendo):
    """Overridden to add simple additional functionality."""

    @property
    def id(self):
        """Get id of the bot."""

        if not hasattr(self, '_id',):
            self._id = self.client.server.login_data['self']['id']
        return self._id

    @property
    def username(self):
        """Get username of the bot."""

        if not hasattr(self, '_username',):
            self._username = self.client.server.username
        return self.username



HERE = dirname(abspath(__file__))
config_path = join(HERE, 'config.yaml')
bot = Parktain.config_from_yaml(config_path)

def is_mention(f):
    """Decorator to check if bot is mentioned."""

    def wrapped(name, message):
        BOT_ID_RE = re.compile('<@{}>'.format(bot.id))
        mention = BOT_ID_RE.search(message) is not None
        if mention:
            return f(name, message)

    return wrapped


#### Bot Functions ############################################################

@bot.listen_for('where do you live')
@is_mention
def source_code(user, message):
    repo_url = 'https://github.com/punchagan/parktain'
    message = 'Well, I live in your hearts...\nYou can change me from here {}, though.'
    return message.format(repo_url)


@bot.cron('0 5 * * *')
def checkins_reminder():
    date = datetime.now().strftime('%d %B, %Y')
    bot.speak('Morning! What are you doing on {}!'.format(date), "#checkins")


def main():
    bot.run()

if __name__ == '__main__':
    main()
