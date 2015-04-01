# Written in 2014-2015, Patrick Uiterwijk <patrick@puiterwijk.org>
# Written in 2015, Pierre-Yves Chibon <pingou@pingoured.fr>
#
# This file is part of JSAutoLogin Example Code.
# This example code is licensed under the CC0 license.
#
# To the extent possible under law, the authors
# have waived all copyright and related or neighboring
# rights to JSAutoLogin Example Code.
# This work is published from: the Netherlands, France.

OPENID_ENDPOINT = 'http://localhost:5050/'

import flask

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info('Testing')

APP = flask.Flask(__name__)
APP.secret_key = 'setme1'

from flask.ext.openid import OpenID
oid = OpenID(APP, safe_roots=[])


@APP.route('/')
def home():
    userdata = None
    if 'loggedin' in flask.session:
        userdata = flask.session['user']
    return flask.render_template('index.html',
                                 userdata=userdata)


@APP.route('/logout')
def logout():
    flask.session = {}
    return flask.redirect('/')


@APP.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    error = oid.fetch_error()
    if error:
        flask.flash(error)
        return flask.render_template('login_error.html',
                                     error=error)
    else:
        immediate = False
        if flask.request.args.get('immediate', None) == 'true':
            immediate = True
        return oid.try_login(OPENID_ENDPOINT,
                             ask_for=['email', 'nickname'],
                             ask_for_optional=['fullname'],
                             immediate=immediate)


@oid.after_login
def after_login(resp):
    flask.session['loggedin'] = True
    flask.session['user'] = {'nickname': resp.nickname,
                             'fullname': resp.fullname,
                             'email': resp.email}
    return flask.redirect('/')


APP.debug = True
APP.run(port=6060, debug=True)
