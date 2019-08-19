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
# from towerlib import InvalidOrganization
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
# class TestTowerlibCommon(IntegrationTest):
#
#     def test_configuration(self):
#         with self.recorder:
#             data = self.tower.configuration
#             self.assertEqual(data.version, TOWER_VERSION)
#
#     def test_cluster_endpoint(self):
#         with self.recorder:
#             data = self.tower.cluster
#             self.assertEqual(data.version, TOWER_VERSION)
#             self.assertEqual(data.name, TOWER_NAME)
#             self.assertIsNotNone(data.active_node)
#             self.assertEqual(data.capacity, 8)
#             instances = list(data.instances)
#             self.assertEqual(len(instances), 1)
#             instance_group = list(self.tower.instance_groups)[0]
#             self.assertIsNotNone(instance_group.id)
#             self.assertIsNotNone(instance_group.created_at)
#             self.assertIsNotNone(instance_group.modified_at)
#
#     def test_local_users(self):
#         with self.recorder:
#             local_users = list(self.tower.local_users)
#             self.assertIs(len(local_users), 1)
#             users_byusername = self.tower.get_user_by_username("admin")
#             self.assertIsNotNone(users_byusername)
#             users_byid = self.tower.get_user_by_id(users_byusername.id)
#             self.assertIsNotNone(users_byid)
#             self.assertEquals(users_byid.username, "admin")
#
#     def test_cluster(self):
#         with self.recorder:
#             local_users = list(self.tower.external_users)
#             self.assertIs(len(local_users), 0)
#
#     def test_organization_user(self):
#         with self.recorder:
#             self.assertIsNotNone(self.tower)
#             org = self.tower.get_organization_by_name("Default")
#             self.assertIsNotNone(org)
#             self.assertFalse("admin" in org.users)
#
#     def test_get_projects(self):
#         with self.recorder:
#             self.assertIsNone(self.tower.get_project_by_id(9999))
#             projects = self.tower.get_projects_by_name("Demo Project")
#             self.assertTrue(len(list(projects)), 1)
#             demo_project = self.tower.get_organization_project_by_name("Default", "Demo Project")
#             self.assertIsNotNone(demo_project)
#             with self.assertRaises(InvalidOrganization):
#                 self.tower.get_organization_project_by_name("Unknown-Organization", "Demo Project")
#
#     def test_get_teams(self):
#         with self.recorder:
#             self.assertEqual(len(list(self.tower.teams)), 0)
#             self.assertIsNone(self.tower.get_team_by_id(99999))
#             self.assertEqual(len(list(self.tower.get_teams_by_name("Unknown Team"))), 0)
#             with self.assertRaises(InvalidOrganization):
#                 self.tower.get_organization_team_by_name("Unknown Organization", "Team")
