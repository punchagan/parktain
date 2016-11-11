#!/usr/bin/env python
from os.path import abspath, dirname, join
HERE = dirname(abspath(__file__))

archive = join(HERE, '..', '..', 'slack-export.zip')
debug = False

from slackviewer.app import app
from slackviewer.main import configure_app
configure_app(app, archive, debug)
