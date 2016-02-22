#!/usr/bin/env python

# Standard library
from datetime import datetime
from os.path import abspath, dirname, join
import re
from urllib.parse import urlparse

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

@bot.listen_for(lambda user, channel, message: True, target_channel='clickbaits')
def logger(user, channel, message):
    message_log = Message(user_id=user, channel_id=channel, message=message, timestamp=datetime.now())
    session.add(message_log)
    session.commit()

    # Check for presence of HyperLink in message
    if user == bot.id:
        return
    for word in message.split():
        try:
            o = urlparse(word[1:-1])
            if o.netloc:
                return '@{user.username} shared "%s"' %message
        except IndexError:
            pass

def main():
    Base.metadata.create_all(engine)
    bot.run()

if __name__ == '__main__':
    main()
