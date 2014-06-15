# [Lemcoff Group website][lemcoff]

## Dependencies:

 - Python 2.7.6
     - pip
 - Node.js 0.10.25
     - npm

See [pip.txt][pip] and [package.json][package] for package info & versions.

## Installation

 1. `git clone --recursive https://github.com/oryband/lemcoff.git`
 2. `pip install --requirement pip.txt`
 3. `npm install`
 4. `./stylus.sh` in order to generate CSS from Stylus files.
 5. Set/Reset password: `python manage.py change --password <password>`
 6. In order to run development (NOT production apache) server: `python manage runserver`

## Guides

See [app/static/humans.txt][humans.txt] for all the apps & tools used in this website.


[lemcoff]: http://www.bgu.ac.il/~lemcoff
[pip]: pip.txt
[package]: package.json
[humans.txt]: app/static/humans.txt
