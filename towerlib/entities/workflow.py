#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: inventory source.py
#
# Copyright 2019 Yorick Hoorneman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for inventory_script.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from towerlib.towerlibexceptions import InvalidValue
from .core import (Entity,
                   EntityManager,
                   validate_max_length)

__author__ = '''Yorick Hoorneman <yhoorneman@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2019-11-22'''
__copyright__ = '''Copyright 2019, Yorick Hoorneman'''
__credits__ = ["Yorick Hoorneman"]
__license__ = '''MIT'''
__maintainer__ = '''Yorick Hoorneman'''
__email__ = '''<yhoorneman@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''inventory_script'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Workflow(Entity):  # pylint: disable=too-many-public-methods
    """Models the Job Template entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

# step 1. Create workflow
# step 2. Create Nodes
# step 3. Associate nodes with each other
    # @property
    # def workflow_nodes(self):
    #     """The inventory scripts of the organization.

    #     Returns:
    #         EntityManager: EntityManager of the inventory scripts of the organization.

    #     """
    #     url = '{api}/workflow_job_templates/{id}/workflow_nodes/'.format(api=self._tower.api, id=self.id)
    #     return EntityManager(self._tower,
    #                          entity_object='inventory_scripts',
    #                          primary_match_field='name',
    #                          url=url)

    @property
    def name(self):
        """The name of the workflow.

        Returns:
            string: The name of the workflow.

        """
        return self._data.get('name')

    @property
    def workflow_nodes(self):
        """The nodes of the workflow.

        Returns:
            Workflow: The nodes that the workflow is part of.

        """
        url = self._data.get('related', {}).get('workflow_nodes')
        return self._tower._get_object_by_url('WorkflowNodes', url)  # pylint: disable=protected-access

    def add_workflow_nodes_to_workflow(self,
                                       unified_job_template):
        """Adds workflow nodes to a workflow.

        Args:
            unified_job_template: The ID of the job template.

        Returns:
            Workflow: ??

        """

        payload = {'unified_job_template': unified_job_template}
        url = '{api}/workflow_job_templates/{workflow_template}/workflow_nodes/'.format(api=self._tower.api,
                                                                                        workflow_template=self.id)
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error adding workflow node to job template, response was: "%s"', response.text)
        return WorkflowNodes(self, response.json()) if response.ok else None

    def associate_workflow_job_template_nodes(self,
                                              first_node,
                                              second_node):
        """Associate an existing workflow job template node with this workflow job template node.
        """
        payload = {'associate': True, 'id': second_node}
        url = '{api}/workflow_job_template_nodes/{node}/success_nodes/'.format(api=self._tower.api, node=first_node)
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error adding workflow node to job template, response was: "%s"', response.text)
        return WorkflowNodes(self, response.json()) if response.ok else None

class WorkflowNodes(Entity):  # pylint: disable=too-many-public-methods
    """Models the Job Template entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def unified_job_template(self):
        """The ID of the unified job template.

        Returns:
            integer: The ID of the unified job template.

        """
        return self._data.get('unified_job_template')

    @property
    def workflow_job_template(self):
        """The ID of the workflow job template.

        Returns:
            integer: The ID of the workflow job template.

        """
        return self._data.get('workflow_job_template')

    def add_workflow_job_template_nodes(self,
                                        workflow_template,
                                        unified_job_template):
        """Creates a workflow job template node.
        """
        payload = {'workflow_job_template': workflow_template,
                   'unified_job_template': unified_job_template}
        url = '{api}/workflow_job_template_nodes/'.format(api=self._tower.api)
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error creating a workflow job template node, response was: "%s"', response.text)
        return Workflow(self, response.json()) if response.ok else None