#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbmodels import db
from dbmodels import User
from dbmodels import Group


class UserGroupDoesNotExist(Exception):
    def __init__(self, name):
        msg = 'user group Group(%s) does not exist' % name
        super(UserGroupDoesNotExist, self).__init__(msg)


class UserDoesNotExist(Exception):
    def __init__(self, userid):
        msg = 'user User(%s) does not exist' % userid
        super(UserDoesNotExist, self).__init__(msg)


##################>> users <<##################################################
def get_user(userid):
    return User.query.filter_by(userid=userid).first()


def create_user(first_name, last_name, userid, groups):
    user = User(first_name, last_name, userid)
    for name in groups:
        group = get_group(name)
        if group:
            user.groups.append(group)
        else:
            raise UserGroupDoesNotExist(name)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(first_name, last_name, userid, groups):
    user = get_user(userid)
    user.first_name = first_name
    user.last_name = last_name
    user.groups = []
    for name in groups:
        group = get_group(name)
        if group:
            user.groups.append(group)
        else:
            raise UserGroupDoesNotExist(name)

    db.session.commit()
    return user


def delete_user(userid):
    user = get_user(userid)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    return user


##################>> groups <<#################################################
def get_group(name):
    return Group.query.filter_by(name=name).first()


def create_group(name):
    group = Group(name)
    db.session.add(group)
    db.session.commit()
    return group


def update_group(name, users):
    group = get_group(name)
    group.users = []
    for userid in users:
        user = get_user(userid)
        if user:
            group.users.append(user)
        else:
            raise UserDoesNotExist(userid)

    db.session.commit()
    return group


def delete_group(name):
    group = get_group(name)
    if group is not None:
        db.session.delete(group)
        db.session.commit()
    return group
