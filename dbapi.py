#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbmodels import db
from dbmodels import User
from dbmodels import Group


##################>> users <<##################################################
def create_user(first_name, last_name, userid, groups=None):
    user = User(first_name, last_name, userid)
    db.session.add(user)
    db.session.commit()
    return user


def delete_user(userid):
    user = get_user(userid)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    return user


def get_user(userid):
    return User.query.filter_by(userid=userid).first()


def user_exists(userid):
    if get_user(userid) is not None:
        return True
    return False


##################>> groups <<#################################################
def create_group(name):
    group = Group(name)
    db.session.add(group)
    db.session.commit()
    return group


def delete_group(name):
    group = get_group(name)
    if group is not None:
        db.session.delete(group)
        db.session.commit()
    return group


def get_group(name):
    return Group.query.filter_by(name=name).first()
