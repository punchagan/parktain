#!/usr/bin/env python

# Standard library.
from os.path import abspath, dirname, join

# 3rd party library.
from flask import Flask, redirect, url_for
from flask_dance.contrib.slack import make_slack_blueprint, slack
import yaml

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

@app.route("/")
def index():
    if not slack.authorized:
        return redirect(url_for("slack.login"))
    return 'Hello, there!'



if __name__ == "__main__":
    # See: http://flask-dance.readthedocs.org/en/latest/quickstarts/slack.html
    # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout web.key -out web.crt
    # NOTE: When running locally, export OAUTHLIB_INSECURE_TRANSPORT=1 if you
    # don't want to create certificates, etc. Comment the context from below.
    context = (join(HERE, 'keys', 'web.crt'), join(HERE, 'keys', 'web.key'))
    app.run(debug=True, ssl_context=context)
