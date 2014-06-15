#!/usr/bin/env python

"""Create static html files from original pages.

Output to ./app/build directory.
"""

from flask_frozen import Freezer
from app import app


freezer = Freezer(app)


@freezer.register_generator
def pages_generator():
    # URLs as strings
    yield '/research/'
    yield '/publications/'
    yield '/members/'
    yield '/alumni/'
    yield '/photos/'
    yield '/links/'


if __name__ == '__main__':
    freezer.freeze()
