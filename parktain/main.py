#!/usr/bin/env python

# Standard library
from datetime import datetime
from os.path import abspath, dirname, join
import re
from datetime import datetime
from urllib.parse import urlparse

# 3rd party library
from gendo import Gendo

# sqlalchemey stuff
from models import Base, engine, Message
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

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

    def wrapped(user, channel, message):
        BOT_ID_RE = re.compile('<@{}>'.format(bot.id))
        mention = BOT_ID_RE.search(message) is not None
        if mention:
            return f(user, channel, message)

    return wrapped


#### Bot Functions ############################################################

@bot.listen_for('where do you live')
@is_mention
def source_code(user, channel, message):
    repo_url = 'https://github.com/punchagan/parktain'
    message = 'Well, I live in your hearts...\nYou can change me from here {}, though.'
    return message.format(repo_url)

@bot.cron('0 5 * * *')
def checkins_reminder():
    date = datetime.now().strftime('%d %B, %Y')
    bot.speak('Morning! What are you doing on {}!'.format(date), "#checkins")

@bot.listen_for(lambda user, channel, message: True)
def logger(user, channel, message):
    message = Message(user_id=user, channel_id=channel, message=message, timestamp=datetime.now())
    session.add(message)
    session.commit()

def main():
    Base.metadata.create_all(engine)
    bot.run()

if __name__ == '__main__':
    main()
