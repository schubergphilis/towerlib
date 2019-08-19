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
# from towerlib import InvalidValue, InvalidOrganization
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
# class TestTowerlibOrganization(IntegrationTest):
#
#     def test_organization(self):
#         with self.recorder:
#             data = list(self.tower.organizations)
#             assert len(data) == 1
#             assert data[0].name == "Default"
#
#     def test_organization_generic(self):
#         with self.recorder:
#             org_name = "Lorem Ipsum"
#             org_description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt " \
#                               "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation " \
#                               "ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " \
#                               "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
#                               "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia " \
#                               "deserunt mollit anim id est laborum."
#
#             org_create = self.tower.create_organization(org_name, org_description)
#             self.assertIsNotNone(org_create)
#             self.assertEqual(org_create.name, org_name)
#             self.assertEqual(org_create.description, org_description)
#             self.assertIsNotNone(org_create.created_by)
#             self.assertIsNotNone(org_create.modified_by)
#
#             with self.assertRaises(InvalidValue) as context:
#                 org_create.name = "*" * 600
#
#             org_create.name = "Lorem Ipsum 2"
#             org_create.description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor"
#             self.assertIsNone(org_create.custom_virtualenv)
#
#             with self.assertRaises(InvalidValue) as context:
#                 org_create.custom_virtualenv = "*" * 600
#
#             org_create.custom_virtualenv = "/var/lib/awx/test"
#             self.assertTrue(len(org_create.object_role_names) > 0)
#
#             self.assertEqual(org_create.users_count, 0)
#             self.assertEqual(org_create.admins_count, 0)
#             self.assertEqual(org_create.inventories_count, 0)
#             self.assertEqual(org_create.job_templates_count, 0)
#             self.assertEqual(org_create.projects_count, 0)
#             self.assertEqual(org_create.teams_count, 0)
#
#             self.assertEqual(len(list(org_create.projects)), org_create.projects_count)
#             self.assertEqual(len(list(org_create.users)), org_create.users_count)
#             self.assertEqual(len(list(org_create.teams)), org_create.teams_count)
#             self.assertEqual(len(list(org_create.inventories)), org_create.inventories_count)
#
#             org_byid = self.tower.get_organization_by_id(org_create.id)
#             org_byname = self.tower.get_organization_by_name(org_create.name)
#             self.assertEqual(org_byid.name, org_byname.name)
#             self.assertEqual(org_byid.description, org_byname.description)
#             self.assertTrue(self.tower.delete_organization(org_byname.name))
#             self.assertIsNone(self.tower.get_organization_by_id(org_create.id))
#             self.assertDictEqual(org_byid._data, org_byname._data)
#
#             with self.assertRaises(InvalidOrganization):
#                 self.tower.delete_organization("Invalid Organization")
#
#     def test_organization_user(self):
#         with self.recorder:
#             username = "test_user_default_organization"
#             org = self.tower.create_organization("Test Organization", "Description")
#             self.assertIsNotNone(org)
#             user = self.tower.create_user_in_organization(org.name,
#                                                           "first_name", "last_name", "example@example.com",
#                                                           username, "password")
#             self.assertIsNotNone(user)
#
#             # unknown invalid roles/organization
#             with self.assertRaises(InvalidOrganization) as context:
#                 self.tower.create_user_in_organization("unknown-organization-does-not-exist",
#                                                        "first_name1", "last_name1", "example1@example.com",
#                                                        username, "password")
#
#             with self.assertRaises(Exception):
#                 user.associate_organization_role(org, 'Non Existing Role')
#
#             with self.assertRaises(Exception):
#                 user.disassociate_organization_role(org, 'Non Existing Role')
#
#             # valid roles
#             self.assertTrue(user.associate_organization_role(org, 'Admin'))
#
#             # make sure we have a user associated with the account
#             org_1 = self.tower.get_organization_by_name('Test Organization')
#             self.assertIsNotNone(org_1)
#             self.assertEqual(org_1.users_count, 1)
#
#             self.assertTrue(user.disassociate_organization_role(org, 'Admin'))
#             self.assertTrue(user.disassociate_organization_role(org, 'Member'))
#
#             # make sure that the user has been disassociated
#             org_2 = self.tower.get_organization_by_name('Test Organization')
#             self.assertIsNotNone(org_2)
#             self.assertEqual(org_2.users_count, 0)
#
#             # Cleanup
#             self.assertTrue(user.delete())
#             self.assertTrue(org_1.delete())
#             self.assertFalse(org_2.delete())
#             self.assertFalse(org.delete())
