# Copyright (c) 2014, Patrick Uiterwijk <patrick@puiterwijk.org>
# All rights reserved.
#
# This file is part of Foobar.
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import flask
import jinja2

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
        return flask.render_template('loggedin.html',
                                     success='false',
                                     error=error)
    else:
        immediate = False
        if flask.request.args.get('immediate', None) == 'true':
            immediate = True
        return oid.try_login('http://localhost:5050/', ask_for=['email', 'nickname'],
                                     ask_for_optional=['fullname'],
                                     immediate=immediate)


@oid.after_login
def create_or_login(resp):
    flask.session['loggedin'] = True
    flask.session['user'] = {'nickname': resp.nickname,
                             'fullname': resp.fullname,
                             'email': resp.email}
    return flask.redirect('/')



APP.debug = True
APP.run(port=6060,debug=True)
