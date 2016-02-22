#!/usr/bin/env python

# Standard library
from datetime import datetime
from os.path import abspath, dirname, join
import re

# 3rd party library
from gendo import Gendo
from sqlalchemy.orm import sessionmaker

# Local library
from parktain.models import Base, engine, Message

Session = sessionmaker(bind=engine)
session = Session()

HERE = dirname(abspath(__file__))
config_path = join(HERE, 'config.yaml')
bot = Gendo.config_from_yaml(config_path)

def is_mention(f):
    """Decorator to check if bot is mentioned."""

    def wrapped(user, channel, message):
        BOT_ID_RE = re.compile('<@{}>'.format(bot.id))
        mention = BOT_ID_RE.search(message) is not None
        if mention:
            return f(user, channel, message)

    return wrapped


def all_messages(user, channel, message):
    return True

URL_RE = re.compile('<(https{0,1}://.*?)>')

def message_has_url(user, channel, message):
    return URL_RE.search(message) is not None

#### Bot Functions ############################################################

@bot.listen_for('where do you live')
@is_mention
def source_code(user, channel, message):
    repo_url = 'https://github.com/punchagan/parktain'
    message = 'Well, I live in your hearts...\nYou can change me from here {}, though.'
    return message.format(repo_url)

@bot.cron('0 0 * * *')
def checkins_reminder():
    date = datetime.now().strftime('%d %B, %Y')
    bot.speak('Morning! What are you doing on {}!'.format(date), "#checkins")

@bot.listen_for(all_messages)
def logger(user, channel, message):
    message_log = Message(user_id=user, channel_id=channel, message=message, timestamp=datetime.now())
    session.add(message_log)
    session.commit()

@bot.listen_for(message_has_url, target_channel='clickbaits', ignore_channels=['clickbaits'])
def link_repost(user, channel, message):
    """Repost links in any channel to target_channel."""
    return '@{user.username} shared "%s"' % message

def main():
    Base.metadata.create_all(engine)
    bot.run()

if __name__ == '__main__':
    main()
