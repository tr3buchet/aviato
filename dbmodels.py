#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
import json

from app import app

db = SQLAlchemy(app)


user_group_association = db.Table(
    'usersgroups', db.Model.metadata,
    db.Column('userid', db.String(35), db.ForeignKey('users.userid')),
    db.Column('groupname', db.Integer, db.ForeignKey('groups.name')))


class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.String(35), primary_key=True)
    first_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))

    groups = db.relationship('Group', secondary=user_group_association,
                             backref='users')

    def __init__(self, first_name, last_name, userid, groups=None):
        self.first_name = first_name
        self.last_name = last_name
        self.userid = userid
        self.groups = groups or []

    def __repr__(self):
        return 'User(%s)' % self.userid

    def to_json(self):
        return json.dumps({'first_name': self.first_name,
                           'last_name': self.last_name,
                           'userid': self.userid,
                           'groups': [g.name for g in self.groups]})

    def __str__(self):
        msg = ('first_name; %s\n'
               'last_name: %s\n'
               'userid: %s\n'
               'groups: %s')
        return msg % (self.first_name, self.last_name,
                      self.userid, self.groups)


class Group(db.Model):
    __tablename__ = 'groups'
    name = db.Column(db.String(50), primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Group(%s)' % self.name

    def to_json(self):
        return json.dumps({'name': self.name,
                           'users': [u.userid for u in self.users]})


def create_tables():
    db.create_all()
