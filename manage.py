#!/usr/bin/env python

import os
import os.path as op
import sys

from flask.ext.script import Manager, Server, Command, Option
from werkzeug.security import generate_password_hash

from app import app, DEBUG


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Password(Command):
    """Changes admin password, and saves it (hashed + salted) to
    'app/password.txt'
    """
    password_path = op.join(op.dirname(__file__), 'app/password.txt')

    option_list = (
        Option('--password', '-p', dest='password'),
    )

    def set_password(self, password):
        return generate_password_hash(password)

    def run(self, password):
        if not password:
            print 'Please provide a --password <password> argument.'
            return

        with open(self.password_path, 'wb') as f:
            f.write(generate_password_hash(password))

        print 'Password saved.'


manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=DEBUG,
    use_reloader=DEBUG,
    host='0.0.0.0')
)

manager.add_command('change', Password())

if __name__ == "__main__":
    manager.run()
