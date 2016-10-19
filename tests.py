#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import json

import dbmodels
import app


class AddUserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
#        dbmodels.db.init_app(app)
#        with app.app_context():
        dbmodels.create_tables()

        # create test structures
        g = {'name': 'schwingers'}
        self.app.post('/groups', data=json.dumps(g),
                      headers={'content-type': 'application/json'})
        g = {'name': 'hammers'}
        self.app.post('/groups', data=json.dumps(g),
                      headers={'content-type': 'application/json'})
        u = {'first_name': 'IP', 'last_name': 'freely',
             'userid': 'dobby', 'groups': []}
        self.app.post('/users', data=json.dumps(u),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
#        with app.app_context():
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_add_user_empty_groups(self):
        u = {'first_name': 'john', 'last_name': 'schwinghammer',
             'userid': 'jschwing', 'groups': []}
        r = self.app.post('/users', data=json.dumps(u),
                          headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/users/jschwing')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), u)

    def test_add_user_to_nonexistent_group(self):
        u = {'first_name': 'john', 'last_name': 'schwinghammer',
             'userid': 'jschwing', 'groups': ['philanderers']}
        r = self.app.post('/users', data=json.dumps(u),
                          headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 400)
        r = self.app.get('/users/jschwing')
        self.assertEqual(r.status_code, 404)

    def test_add_user_with_existing_groups(self):
        # create user in those groups
        u = {'first_name': 'john', 'last_name': 'schwinghammer',
             'userid': 'jschwing', 'groups': ['schwingers', 'hammers']}
        r = self.app.post('/users', data=json.dumps(u),
                          headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/users/jschwing')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), u)

    def test_add_duplicate_user(self):
        u = {'first_name': 'asdf', 'last_name': 'qwerty',
             'userid': 'dobby', 'groups': []}
        r = self.app.post('/users', data=json.dumps(u),
                          headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 418)


class GetUserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
        dbmodels.create_tables()

        # add test user
        self.test_user = {'first_name': 'john', 'last_name': 'schwinghammer',
                          'userid': 'jschwing', 'groups': []}
        self.app.post('/users', data=json.dumps(self.test_user),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_get_nonexistent_user(self):
        r = self.app.get('/users/baduserid')
        self.assertEqual(r.status_code, 404)

    def test_get_existing_user(self):
        r = self.app.get('/users/jschwing')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), self.test_user)


class DeleteUserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
        dbmodels.create_tables()

        # add test user
        self.test_user = {'first_name': 'john', 'last_name': 'schwinghammer',
                          'userid': 'jschwing', 'groups': []}
        self.app.post('/users', data=json.dumps(self.test_user),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_delete_nonexistent_user(self):
        r = self.app.delete('/users/baduserid')
        self.assertEqual(r.status_code, 404)

    def test_delete_existing_user(self):
        r = self.app.delete('/users/jschwing')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, '')


class PutUserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
        dbmodels.create_tables()

        # create test structures
        self.test_group1 = {'name': 'schwingers'}
        self.app.post('/groups', data=json.dumps(self.test_group1),
                      headers={'content-type': 'application/json'})
        self.test_group2 = {'name': 'hammers'}
        self.app.post('/groups', data=json.dumps(self.test_group2),
                      headers={'content-type': 'application/json'})
        self.test_user1 = {'first_name': 'IP', 'last_name': 'freely',
                           'userid': 'dobby', 'groups': ['schwingers',
                                                         'hammers']}
        self.app.post('/users', data=json.dumps(self.test_user1),
                      headers={'content-type': 'application/json'})
        self.test_user2 = {'first_name': 'john', 'last_name': 'schwinghammer',
                           'userid': 'jschwing', 'groups': ['schwingers',
                                                            'hammers']}
        self.app.post('/users', data=json.dumps(self.test_user2),
                      headers={'content-type': 'application/json'})
        self.test_user3 = {'first_name': 'jenny', 'last_name': 'says',
                           'userid': 'jdizzy', 'groups': []}
        self.app.post('/users', data=json.dumps(self.test_user3),
                      headers={'content-type': 'application/json'})
        self.test_user4 = {'first_name': 'brad', 'last_name': 'lawton',
                           'userid': 'wiggles', 'groups': []}
        self.app.post('/users', data=json.dumps(self.test_user4),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_put_user_add_group(self):
        r = self.app.get('/users/%s' % self.test_user3['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 0)
        user = self.test_user3.copy()
        user['groups'] = [self.test_group1['name'], self.test_group2['name']]
        r = self.app.put('/users/%s' % user['userid'], data=json.dumps(user),
                         headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)

        # test groups were added
        r = self.app.get('/users/%s' % user['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 2)

        # test user was added to groups
        r = self.app.get('/groups/%s' % self.test_group1['name'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['users']), 3)

    def test_put_user_remove_group(self):
        r = self.app.get('/users/%s' % self.test_user1['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 2)
        user = self.test_user1.copy()
        user['groups'] = [self.test_group2['name']]
        r = self.app.put('/users/%s' % user['userid'], data=json.dumps(user),
                         headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)

        # test groups were removed
        r = self.app.get('/users/%s' % user['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 1)

        # test user was removed from group
        r = self.app.get('/groups/%s' % self.test_group1['name'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['users']), 1)

    def test_put_user_nonexistent_group(self):
        r = self.app.get('/users/%s' % self.test_user1['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 2)
        user = self.test_user1.copy()
        user['groups'].append('blimey')
        r = self.app.put('/users/%s' % user['userid'], data=json.dumps(user),
                         headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 400)

        # test no groups were removed
        r = self.app.get('/users/%s' % user['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 2)

    def test_put_user_change_name(self):
        user = self.test_user4.copy()
        user['last_name'] = 'goober'
        r = self.app.put('/users/%s' % user['userid'], data=json.dumps(user),
                         headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)

        # see if last name updated
        r = self.app.get('/users/%s' % user['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data)['last_name'], 'goober')


class AddDeleteGroupTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
        dbmodels.create_tables()

        # create test group
        g = {'name': 'schwingers'}
        self.app.post('/groups', data=json.dumps(g),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_add_group(self):
        g = {'name': 'hammers'}
        r = self.app.post('/groups', data=json.dumps(g),
                          headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/groups/hammers')
        self.assertEqual(r.status_code, 200)
        g['users'] = []
        self.assertEqual(json.loads(r.data), g)

    def test_add_duplicate_group(self):
        g = {'name': 'schwingers'}
        r = self.app.post('/groups', data=json.dumps(g),
                          headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 418)


class GetGroupTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
        dbmodels.create_tables()

        # create test group
        self.test_group = {'name': 'schwingers'}
        self.app.post('/groups', data=json.dumps(self.test_group),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_get_nonexistent_group(self):
        r = self.app.get('/groups/bingsucks')
        self.assertEqual(r.status_code, 404)

    def test_get_existing_group(self):
        r = self.app.get('/groups/schwingers')
        expected_data = self.test_group.copy()
        expected_data['users'] = []

        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), expected_data)


class DeleteGroupTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
        dbmodels.create_tables()

        # create test group
        self.test_group = {'name': 'schwingers'}
        self.app.post('/groups', data=json.dumps(self.test_group),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_delete_nonexistent_group(self):
        r = self.app.delete('/groups/flibbertigibbet')
        self.assertEqual(r.status_code, 404)

    def test_delete_existing_user(self):
        r = self.app.delete('/groups/schwingers')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, '')


class PutGroupTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
        dbmodels.create_tables()

        # create test structures
        self.test_group1 = {'name': 'schwingers'}
        self.app.post('/groups', data=json.dumps(self.test_group1),
                      headers={'content-type': 'application/json'})
        self.test_group2 = {'name': 'hammers'}
        self.app.post('/groups', data=json.dumps(self.test_group2),
                      headers={'content-type': 'application/json'})
        self.test_user1 = {'first_name': 'IP', 'last_name': 'freely',
                           'userid': 'dobby', 'groups': ['schwingers',
                                                         'hammers']}
        self.app.post('/users', data=json.dumps(self.test_user1),
                      headers={'content-type': 'application/json'})
        self.test_user2 = {'first_name': 'john', 'last_name': 'schwinghammer',
                           'userid': 'jschwing', 'groups': ['schwingers',
                                                            'hammers']}
        self.app.post('/users', data=json.dumps(self.test_user2),
                      headers={'content-type': 'application/json'})
        self.test_user3 = {'first_name': 'jenny', 'last_name': 'says',
                           'userid': 'jdizzy', 'groups': []}
        self.app.post('/users', data=json.dumps(self.test_user3),
                      headers={'content-type': 'application/json'})
        self.test_user4 = {'first_name': 'brad', 'last_name': 'lawton',
                           'userid': 'wiggles', 'groups': []}
        self.app.post('/users', data=json.dumps(self.test_user4),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_put_group_add_users(self):
        r = self.app.get('/groups/%s' % self.test_group2['name'])
        rd = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(rd['users']), 2)
        group = rd
        group['users'] = [self.test_user1['userid'],
                          self.test_user2['userid'],
                          self.test_user3['userid'],
                          self.test_user4['userid']]
        r = self.app.put('/groups/%s' % group['name'], data=json.dumps(group),
                         headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)

        # test users were added
        r = self.app.get('/groups/%s' % group['name'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['users']), 4)

        # test group was added to users
        r = self.app.get('/users/%s' % self.test_user4['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 1)

    def test_put_group_remove_users(self):
        r = self.app.get('/groups/%s' % self.test_group2['name'])
        rd = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(rd['users']), 2)
        group = rd
        group['users'] = [self.test_user1['userid']]
        r = self.app.put('/groups/%s' % group['name'], data=json.dumps(group),
                         headers={'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)

        # test users were removed
        r = self.app.get('/groups/%s' % group['name'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['users']), 1)

        # test group was removed from users
        r = self.app.get('/users/%s' % self.test_user2['userid'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 1)

    def test_put_group_nonexistent_user(self):
        r = self.app.get('/groups/%s' % self.test_group2['name'])
        rd = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(rd['users']), 2)
        group = rd
        group['users'].append(u'strongbad')
        r = self.app.put('/groups/%s' % group['name'], data=json.dumps(group),
                         headers={'content-type': 'application/json'})

        # test no users were removed
        r = self.app.get('/groups/%s' % group['name'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['users']), 2)


class TestUserGroupAssociation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app.config['TESTING'] = True

    def setUp(self):
        self.app = app.app.test_client()
        dbmodels.create_tables()

        # create test structures
        self.test_group1 = {'name': 'schwingers'}
        self.app.post('/groups', data=json.dumps(self.test_group1),
                      headers={'content-type': 'application/json'})
        self.test_group2 = {'name': 'hammers'}
        self.app.post('/groups', data=json.dumps(self.test_group2),
                      headers={'content-type': 'application/json'})
        self.test_user1 = {'first_name': 'IP', 'last_name': 'freely',
                           'userid': 'dobby', 'groups': ['schwingers',
                                                         'hammers']}
        self.app.post('/users', data=json.dumps(self.test_user1),
                      headers={'content-type': 'application/json'})
        self.test_user2 = {'first_name': 'john', 'last_name': 'schwinghammer',
                           'userid': 'jschwing', 'groups': ['schwingers',
                                                            'hammers']}
        self.app.post('/users', data=json.dumps(self.test_user2),
                      headers={'content-type': 'application/json'})

    def tearDown(self):
        dbmodels.destroy_tables()
        dbmodels.db.session.remove()

    def test_adding_users_to_groups(self):
        r = self.app.get('/groups/schwingers')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['users']), 2)

        r = self.app.get('/users/dobby')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 2)

    def test_deleting_group_from_user(self):
        r = self.app.delete('/groups/schwingers')
        self.assertEqual(r.status_code, 200)

        r = self.app.get('/users/dobby')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['groups']), 1)

    def test_deleting_user_from_group(self):
        r = self.app.delete('/users/jschwing')
        self.assertEqual(r.status_code, 200)

        r = self.app.get('/groups/hammers')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(json.loads(r.data)['users']), 1)


if __name__ == '__main__':
    unittest.main()
