#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
import json

from app import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.String(35), primary_key=True)
    first_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))

    def __init__(self, first_name, last_name, userid, groups=None):
        self.first_name = first_name
        self.last_name = last_name
        self.userid = userid

    def __repr__(self):
        return 'User(%s)' % self.userid

    def to_json(self):
        return json.dumps({'first_name': self.first_name,
                           'last_name': self.last_name,
                           'userid': self.userid})


class Group(db.Model):
    __tablename__ = 'groups'
    name = db.Column(db.String(50), primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr(self):
        return 'Group(%s)' % self.name

    def to_json(self):
        return json.dumps({'name': self.name})


def create_tables():
    db.create_all()
