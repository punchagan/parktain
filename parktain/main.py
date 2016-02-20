#!/usr/bin/env python

from os.path import abspath, dirname, join
from gendo import Gendo

HERE = dirname(abspath(__file__))
config_path = join(HERE, 'config.yaml')
bot = Gendo.config_from_yaml(config_path)


@bot.listen_for('morning')
def morning(user, message):
    # make sure message is "morning" and doesn't just contain it.
    if message.strip() == "morning":
        return "mornin' @{user.username}"

def main():
    bot.run()

if __name__ == '__main__':
    main()
