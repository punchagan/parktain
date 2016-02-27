activate_this = '/home/punchagan/.venvs/parktain/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from parktain.main import app as application
