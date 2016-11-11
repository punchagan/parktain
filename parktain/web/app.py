#!/usr/bin/env python

# Standard library.
import datetime

# 3rd party library.
from flask import Flask, jsonify, redirect, render_template, url_for
from flask_dance.contrib.slack import slack
from sqlalchemy.sql import extract, func

# Local library
from parktain.main import session, URL_RE
from parktain.models import Base, Channel, engine, Message, User
from parktain.web.utils import format_slack_message, get_id_name_mapping_from_db, configure_slack_auth, slack_authorized

app = Flask(__name__)
configure_slack_auth(app)


# Routes ####

@app.route("/")
@slack_authorized
def index():
    context = {}
    return render_template('index.html', **context)


@app.route("/random_link/")
@slack_authorized
def random_link():
    url = None
    while url is None:
        messages = session.query(Message).order_by(func.random()).limit(10).all()
        for message in messages:
            for url_ in URL_RE.findall(message.message):
                url = url_.split('|', 1)[0] if '|' in url_ else url_
                break
            if url is not None:
                break

    return redirect(url)


@app.route("/links/")
@app.route("/links/<days>/")
@slack_authorized
def show_links(days=0):
    days = int(days)
    day = datetime.datetime.utcnow().date() - datetime.timedelta(days=days)
    days_messages = _get_days_messages(day)
    links = []

    channels = get_id_name_mapping_from_db(session, Channel)
    users = get_id_name_mapping_from_db(session, User)

    for message in days_messages:
        for url in URL_RE.findall(message.message):
            if '|' in url:
                url, title = url.split('|', 1)
            else:
                title = url

            link = {
                'url': url,
                'title': title,
                'user': users.get(message.user_id, '<deleted-user>'),
                'channel': channels.get(message.channel_id, '<deleted-channel>'),
                'message': format_slack_message(message.message, channels, users),
                'timestamp': message.timestamp,
            }

            links.append(link)

    context = {
        'links': links,
        'date': day,
        'previous': days + 1,
        'next': days - 1 if days > 0 else None,
    }

    return render_template('clickbaits.html', **context)


@app.route("/stats/")
@slack_authorized
def show_stats():
    dow = extract('dow', Message.timestamp)
    stats = {
        i: session.query(Message).filter(dow == i).count() for i in range(7)
    }

    return render_template('stats.html')


@app.route("/stats/yearly/")
@slack_authorized
def yearly_stats():
    day = datetime.datetime.utcnow().date()
    # FIXME: Use dateutil.relativedelta or something
    last_year = day + datetime.timedelta(-365)

    doy = extract('doy', Message.timestamp)
    messages = session.query(Message.timestamp, func.count(doy))\
                      .filter(last_year < Message.timestamp).group_by(doy)

    response = {date.strftime('%Y-%m-%d'): count for date, count in messages.all()}
    return jsonify(response)


# Helpers ####

def _get_days_messages(day):
    """Return all messages sent on given day."""

    next_ = day + datetime.timedelta(days=1)
    days_messages = session.query(Message)\
                           .filter(day < Message.timestamp)\
                           .filter(Message.timestamp < next_)\
                           .order_by(Message.timestamp).all()

    return days_messages


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # See: http://flask-dance.readthedocs.org/en/latest/quickstarts/slack.html
    # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout web.key -out web.crt
    # NOTE: When running locally, export OAUTHLIB_INSECURE_TRANSPORT=1 if you
    # don't want to create certificates, etc. Comment the context from below.
    app.run(host='0.0.0.0', debug=True)
