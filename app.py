#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import logging

import dbapi as db
import dbmodels

app = Flask('aviato')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
LOG = logging.getLogger(__name__)
LOG = app.logger


@app.route('/users/<userid>')
def get_user(userid):
    user = db.get_user(userid)
    if user is not None:
        return user.to_json()
    return 'user %s not found' % userid, 404


@app.route('/users', methods=('post',))
def add_user():
    if ('first_name' not in request.json or
            'last_name' not in request.json or
            'userid' not in request.json):
        return 'first_name, last_name, and userid are required', 400

    if db.get_user(request.json['userid']):
        return 'user already exists', 418
    user = db.create_user(request.json['first_name'],
                          request.json['last_name'],
                          request.json['userid'],
                          request.json['groups'])
    LOG.debug('added user: %s', user)

    return user.to_json()


@app.route('/users/<userid>', methods=('delete',))
def delete_user(userid):
    if db.delete_user(userid):
        return ''
    return 'User(%s) not found' % userid, 404


@app.route('/groups/<name>')
def get_group(name):
    group = db.get_group(name)
    if group is not None:
        return group.to_json()
    return 'group %s not found' % name, 404


@app.route('/groups', methods=('post',))
def add_group():
    if db.get_group(request.json['name']):
        return 'group already exists', 418
    group = db.create_group(request.json['name'])
    LOG.debug('added group: %s', group)

    return group.to_json()


@app.route('/groups/<name>', methods=('delete',))
def delete_group(name):
    if db.delete_group(name):
        return ''
    return 'Group(%s) not found' % name, 404


@app.route('/')
def hello_there():
    return 'hello world'


if __name__ == '__main__':
    dbmodels.create_tables()
    app.run(debug=True, host='127.0.0.1', port=5000)
