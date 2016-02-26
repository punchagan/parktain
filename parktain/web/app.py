#!/usr/bin/env python

# Standard library.
import datetime
from os.path import abspath, dirname, join

# 3rd party library.
from flask import Flask, redirect, render_template, Response, url_for
from flask_dance.contrib.slack import make_slack_blueprint, slack
import yaml

# Local library
from parktain.main import Message, session, URL_RE

HERE = dirname(abspath(__file__))

def get_app_config():
    path_to_yaml = join(HERE, '..', 'config.yaml')
    with open(path_to_yaml, 'r') as ymlfile:
        web = yaml.load(ymlfile).get('web')

    default = {'client_id': '', 'client_secret': '', 'secret_key': ''}
    return web or default


config = get_app_config()
app = Flask(__name__)
app.secret_key = config['secret_key']
blueprint = make_slack_blueprint(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    scope=["identify", "chat:write:bot"],
)
app.register_blueprint(blueprint, url_prefix="/login")


#### Routes ####

@app.route("/")
def index():
    if not slack.authorized:
        return redirect(url_for("slack.login"))
    return 'Hello, there!'


@app.route("/links")
@app.route("/links/<days>")
def show_links(days=0):
    if not slack.authorized:
        return redirect(url_for("slack.login"))

    day = datetime.datetime.utcnow().date() - datetime.timedelta(days=int(days))
    next_ = day + datetime.timedelta(days=1)
    days_messages = session.query(Message).filter(day < Message.timestamp).filter(Message.timestamp < next_).order_by(Message.timestamp).all()
    links = []

    for message in days_messages:
        for url in URL_RE.findall(message.message):
            if '|' in url:
                url, title = url.split('|', 1)
            else:
                title = url

            link = {
                'url': url,
                'title': title,
                'user': message.user_id,
                'channel': message.channel_id,
                'message': message.message,
                'timestamp': message.timestamp
            }

            links.append(link)

    context = {'links': links, 'date': day}

    return render_template('clickbaits.html', **context)


if __name__ == "__main__":
    # See: http://flask-dance.readthedocs.org/en/latest/quickstarts/slack.html
    # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout web.key -out web.crt
    # NOTE: When running locally, export OAUTHLIB_INSECURE_TRANSPORT=1 if you
    # don't want to create certificates, etc. Comment the context from below.
    ssl_context = (join(HERE, 'keys', 'web.crt'), join(HERE, 'keys', 'web.key'))
    app.run(debug=True, ssl_context=ssl_context)
