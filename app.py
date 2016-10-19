#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import logging

import dbapi as db
import dbmodels

app = Flask('aviato')
LOG = app.logger



@app.route('/users/<userid>')
def get_user(userid):
    user = db.get_user(userid)
    LOG.info('found user %r for userid |%s|', user, userid)
    if user is not None:
        return user.to_json()
    return 'User(%s) not found' % userid, 404


@app.route('/users', methods=('post',))
def add_user():
    if ('first_name' not in request.get_json() or
            'last_name' not in request.get_json() or
            'userid' not in request.get_json() or
            'groups' not in request.get_json()):
        return 'first_name, last_name, userid, and groups are required', 400

    if db.get_user(request.get_json()['userid']):
        return 'User(%s) already exists' % request.get_json()['userid'], 418

    try:
        user = db.create_user(request.get_json()['first_name'],
                              request.get_json()['last_name'],
                              request.get_json()['userid'],
                              request.get_json()['groups'])
    except db.UserGroupDoesNotExist as e:
        return 'cannot create user, %s' % e, 400
    LOG.info('added %r', user)

    return user.to_json()


@app.route('/users/<userid>', methods=('put',))
def update_user(userid):
    if ('first_name' not in request.get_json() or
            'last_name' not in request.get_json() or
            'userid' not in request.get_json() or
            'groups' not in request.get_json()):
        return 'first_name, last_name, userid, and groups are required', 400

    if not db.get_user(userid):
        return 'User(%s) does not exist' % userid, 404
    try:
        user = db.update_user(request.get_json()['first_name'],
                              request.get_json()['last_name'],
                              userid,
                              request.get_json()['groups'])
    except db.UserGroupDoesNotExist as e:
        return 'cannot update user, %s' % e, 400
    LOG.info('updated %r', user)

    return user.to_json()


@app.route('/users/<userid>', methods=('delete',))
def delete_user(userid):
    if db.delete_user(userid):
        LOG.info('deleted User(%s)', userid)
        return ''
    return 'User(%s) not found' % userid, 404


@app.route('/groups/<name>')
def get_group(name):
    group = db.get_group(name)
    LOG.info('found group %r for name |%s|', group, name)
    if group is not None:
        return group.to_json()
    return 'Group(%s) not found' % name, 404


@app.route('/groups', methods=('post',))
def add_group():
    if db.get_group(request.get_json()['name']):
        return 'Group(%s) already exists' % request.get_json()['name'], 418
    group = db.create_group(request.get_json()['name'])
    LOG.info('added %r', group)

    return group.to_json()


@app.route('/groups/<name>', methods=('put',))
def update_group(name):
    if 'name' not in request.get_json() or 'users' not in request.get_json():
        return 'first_name, last_name, userid, and groups are required', 401

    if not db.get_group(name):
        return 'Group(%) does not exist' % name, 404

    try:
        user = db.update_group(name,
                               request.get_json()['users'])
    except db.UserDoesNotExist as e:
        return 'cannot update group, %s' % e, 402
    LOG.info('updated %r', user)

    return user.to_json()

@app.route('/groups/<name>', methods=('delete',))
def delete_group(name):
    if db.delete_group(name):
        LOG.info('deleted Group(%s)', name)
        return ''
    return 'Group(%s) not found' % name, 404


@app.route('/')
def hello_there():
    return 'hello world'


def configure_logging():
    """ i hate python logging so, so much... :/ """
    # disable the stupid werkzeug logger
    l = logging.getLogger('werkzeug')
    l.setLevel(10000)

    # have to completely disable flask's handlers because they can't be
    # removed for some reason
    for h in LOG.handlers:
        h.setLevel(10000)

    # set my own format instead of the awful multiline flask awfulness
    fmt = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} '
                            '%(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(fmt)
    LOG.setLevel(logging.DEBUG)
    LOG.addHandler(sh)


if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    configure_logging()

    #dbmodels.db.init_app(app)
    #with app.app_context():
    dbmodels.create_tables()
    app.run(host='127.0.0.1', port=5000)
