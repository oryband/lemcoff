#!/usr/bin/env python

import os
import sys

from flask.ext.script import Manager, Server

from app import app, DEBUG


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=DEBUG,
    use_reloader=DEBUG,
    host='0.0.0.0')
)

if __name__ == "__main__":
    manager.run()
