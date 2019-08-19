# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # File: test_towerlib.py
# #
# # Copyright 2018 Ilija Matoski
# #
# # Permission is hereby granted, free of charge, to any person obtaining a copy
# #  of this software and associated documentation files (the "Software"), to
# #  deal in the Software without restriction, including without limitation the
# #  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# #  sell copies of the Software, and to permit persons to whom the Software is
# #  furnished to do so, subject to the following conditions:
# #
# # The above copyright notice and this permission notice shall be included in
# #  all copies or substantial portions of the Software.
# #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# #  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# #  DEALINGS IN THE SOFTWARE.
# #
#
# """
# test_towerlib_configuration
# ----------------------------------
# Tests for `towerlib` module.
#
# .. _Google Python Style Guide:
#    http://google.github.io/styleguide/pyguide.html
#
# """
#
# from . import IntegrationTest
# from towerlib import InvalidUser, InvalidValue
#
# __author__ = '''Ilija Matoski <imatoski@schubergphilis.com>'''
# __docformat__ = '''google'''
# __date__ = '''2018-05-25'''
# __copyright__ = '''Copyright 2018, Ilija Matoski'''
# __credits__ = ["Ilija Matoski"]
# __license__ = '''MIT'''
# __maintainer__ = '''Ilija Matoski'''
# __email__ = '''<imatoski@schubergphilis.com>'''
# __status__ = '''Development'''  # "Prototype", "Development", "Production".
#
# TOWER_VERSION = '6.1.0.0'
# TOWER_NAME = 'tower'
#
#
# class TestTowerlibUser(IntegrationTest):
#
#     def test_user_create_delete(self):
#         with self.recorder:
#             username = "test_user"
#             self.assertIsNotNone(self.tower.create_user(username, "password"))
#             self.assertTrue(self.tower.delete_user(username))
#             with self.assertRaises(InvalidUser) as context:
#                 self.tower.delete_user(username)
#             self.assertRaises(Exception, context.exception)
#
#     def test_users_full_rundown(self):
#         with self.recorder:
#             username = "test_user"
#             user = self.tower.create_user(username, "password")
#             self.assertIsNotNone(user)
#             self.assertFalse(user.is_system_auditor)
#             self.assertFalse(user.is_superuser)
#             self.assertIsNotNone(user.created_at)
#             self.assertIsNone(user.modified_at)
#             self.assertIsNotNone(user.password)
#             self.assertEqual(user.first_name, '')
#             self.assertEqual(user.last_name, '')
#             self.assertEqual(user.email, '')
#             self.assertEqual(user.ldap_dn, '')
#             self.assertEqual(user.email, '')
#             self.assertEqual(user.auth, [])
#             self.assertIsNone(user.external_account)
#             self.assertEquals(list(user.teams), [])
#             self.assertEquals(list(user.projects), [])
#             self.assertEquals(list(user.roles), [])
#             self.assertEquals(list(user.credentials), [])
#             self.assertEquals(list(user.organizations), [])
#
#             # Update now
#             user.is_superuser = True
#             user.is_system_auditor = True
#
#             with self.assertRaises(InvalidValue) as context:
#                 user.first_name = "?" * 40
#             self.assertRaises(Exception, context.exception)
#             user.first_name = "First Name"
#
#             with self.assertRaises(InvalidValue) as context:
#                 user.last_name = "?" * 40
#             self.assertRaises(Exception, context.exception)
#             user.last_name = "Last Name"
#
#             with self.assertRaises(InvalidValue) as context:
#                 user.email = "?" * 400
#             self.assertRaises(Exception, context.exception)
#             user.email = "email@email.com"
#
#             user.password = "password2"
#
#             with self.assertRaises(InvalidValue) as context:
#                 user.username = "?" * 400
#             self.assertRaises(Exception, context.exception)
#             user.username = "test_user_renamed"
#
#             self.assertIsNone(user.last_login)
#
#             self.assertIsNotNone(self.tower.get_user_by_id(user.id))
#             self.assertTrue(self.tower.delete_user(user.username))
#             with self.assertRaises(InvalidUser) as context:
#                 self.tower.delete_user(user.username)
#             self.assertRaises(Exception, context.exception)
#             self.assertFalse(user.delete())
#             self.assertIsNone(self.tower.get_user_by_id(user.id))
#             self.assertIsNone(self.tower.get_user_by_username(user.username))
