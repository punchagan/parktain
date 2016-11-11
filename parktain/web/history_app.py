#!/usr/bin/env python
from os.path import abspath, dirname, join
from slackviewer.main import configure_app
from parktain.web.utils import configure_slack_auth, slack_authorized

HERE = dirname(abspath(__file__))

from slackviewer.app import app
archive = join(HERE, '..', '..', 'slack-export.zip')
debug = False

configure_app(app, archive, debug)
configure_slack_auth(app)
for name, func in app.view_functions.items():
    if name.startswith('slack') or name == 'static':
        continue
    app.view_functions[name] = slack_authorized(func)
