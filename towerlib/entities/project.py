#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: project.py
#
# Copyright 2018 Costas Tyfoxylos
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
Main code for project.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from dateutil.parser import parse

from towerlib.towerlibexceptions import (InvalidValue,
                                         InvalidCredential,
                                         InvalidOrganization)
from .core import (Entity,
                   EntityManager,
                   validate_max_length,
                   validate_range)

__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-03'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''project'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Project(Entity):  # pylint: disable=too-many-public-methods
    """Models the project entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)
        self._object_roles = None

    @property
    def last_job(self):  # TOFIX model the job and return an object instead of dictionary
        """The last job run on the project.

        Returns:
            dict: The last job executed.

        """
        return self._data.get('summary_fields', {}).get('last_job')

    @property
    def last_update(self):  # TOFIX model the job and return an object instead of dictionary
        """The last update of the project.

        Returns:
            dict: The last update.

        """
        return self._data.get('summary_fields', {}).get('last_update')

    @property
    def created_by(self):
        """The person that created the project.

        Returns:
            dict: The person that created the project.

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def playbooks(self):
        """The playbooks of the project.

        Returns:
            list: A list of the project specified playbooks.

        """
        playbook_url = self._data.get('related', {}).get('playbooks')
        url = f'{self._tower.host}{playbook_url}'
        response = self._tower.session.get(url)
        if not response.ok:
            self._logger.error('Error getting playbooks for project "%s", response was :"%s"', self.name,
                               response.text)
        return response.json() if response.ok else None

    @property
    def object_roles(self):
        """The object roles.

        Returns:
            EntityManager: EntityManager of the object roles supported.

        """
        if not self._object_roles:
            url = self._data.get('related', {}).get('object_roles')
            self._object_roles = EntityManager(self._tower,
                                               entity_object='ObjectRole',
                                               primary_match_field='name',
                                               url=url)
        return self._object_roles

    @property
    def object_role_names(self):
        """The names of the object roles.

        Returns:
            list: A list of strings for the object_roles.

        """
        return [object_role.name for object_role in self.object_roles]

    @property
    def name(self):
        """The name of the project.

        Returns:
            string: The name of the project.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the project.

        Returns:
            None:

        """
        max_characters = 512
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('name', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less than or equal to '
                               f'{max_characters}')

    @property
    def description(self):
        """The description of the Project.

        Returns:
            string: The description of the Project.

        """
        return self._data.get('description')

    @description.setter
    def description(self, value):
        """Update the description of the project.

        Returns:
            None:

        """
        self._update_values('description', value)

    @property
    def job_templates(self):
        """The job templates for the project entity.

        Returns:
            job_templates (list): list of all the job templates object for the project.

        """
        return self._tower.job_templates.filter({'project__exact': self.id})

    @property
    def local_path(self):
        """The internal local path of the project.

        Returns:
            string: The internal local path of the project.

        """
        return self._data.get('local_path')

    @property
    def scm_type(self):
        """The type of the scm used.

        Returns:
            string: The type of the scm used.

        """
        return self._data.get('scm_type')

    @property
    def scm_url(self):
        """The url of the scm used.

        Returns:
            string: The url of the scm used.

        """
        return self._data.get('scm_url')

    @scm_url.setter
    def scm_url(self, value):
        """Update the scm_url project.

        Returns:
            None:

        """
        max_characters = 1024
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('scm_url', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less than or equal to '
                               f'{max_characters}')

    @property
    def scm_branch(self):
        """The branch of the scm used.

        Returns:
            string: The branch of the scm used.

        """
        return self._data.get('scm_branch')

    @scm_branch.setter
    def scm_branch(self, value):
        """Update the scm_branch project.

        Returns:
            None:

        """
        max_characters = 256
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('scm_branch', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less than or equal to '
                               f'{max_characters}')

    @property
    def scm_clean(self):
        """A flag to clean the scm or not.

        Returns:
            bool: True if set, False otherwise.

        """
        return self._data.get('scm_clean')

    @scm_clean.setter
    def scm_clean(self, value):
        """Update the scm_clean project.

        Returns:
            None:

        """
        self._update_values('scm_clean', value)

    @property
    def scm_delete_on_update(self):
        """A flag to delete the scm on update.

        Returns:
            bool: True if set, False otherwise.

        """
        return self._data.get('scm_delete_on_update')

    @scm_delete_on_update.setter
    def scm_delete_on_update(self, value):
        """Update the scm_delete_on_update project flag.

        Returns:
            None:

        """
        self._update_values('scm_delete_on_update', value)

    @property
    def credential(self):
        """The Credential object associated with this project.

        Returns:
            Credential: The Credential object of the project.

        """
        return self._tower.get_credential_by_id(self._data.get('credential'))

    @credential.setter
    def credential(self, value):
        """Update the credential attached to the project.

        Returns:
            None:

        """
        credential = self.organization.get_credential_by_name_with_type_id(value,
                                                                           self.credential._data.get('credential_type'))
        if not credential:
            raise InvalidCredential(value)
        self._update_values('credential', credential.id)

    @property
    def timeout(self):
        """The timeout setting of the project.

        Returns:
            integer: The timeout setting of the project.

        """
        return self._data.get('timeout')

    @timeout.setter
    def timeout(self, value):
        """Update the timeout of the project.

        Returns:
            None:

        """
        minimum = -2147483648
        maximum = 2147483647
        conditions = [validate_range(value, minimum, maximum)]
        if all(conditions):
            self._update_values('timeout', value)
        else:
            raise InvalidValue(f'{value} is invalid, must be between {minimum} and {maximum}')

    @property
    def last_job_run(self):
        """The date and time of the last run job.

        Returns:
            datetime: The datetime object of when the last job run.

        """
        try:
            date_ = parse(self._data.get('last_job_run'))
        except (ValueError, TypeError):
            date_ = None
        return date_

    @property
    def is_last_job_failed(self):
        """A flag of whether the last job run failed.

        Returns:
            bool: True if the job failed, False otherwise.

        """
        return self._data.get('last_job_failed')

    @property
    def next_job_run(self):
        """Not sure what this does.

        Returns:
            None.

        """
        return self._data.get('next_job_run')

    @property
    def status(self):
        """The status of the project.

        Returns:
            string: The status of the project.

        """
        self._refresh_state()
        return self._data.get('status')

    @property
    def organization(self):
        """The Organization object that this project is part of.

        Returns:
            Organization: The Organization object that this project is part of.

        """
        return self._tower.get_organization_by_id(self._data.get('organization'))

    @organization.setter
    def organization(self, value):
        """Update the organization attached to the project.

        Returns:
            None:

        """
        organization = self._tower.get_organization_by_name(value)
        if not organization:
            raise InvalidOrganization(value)
        self._update_values('organization', organization.id)

    @property
    def scm_delete_on_next_update(self):
        """A flag on whether to delete the scm on the next update.

        Returns:
            bool: True if set, False otherwise.

        """
        return self._data.get('scm_delete_on_next_update')

    @property
    def scm_update_on_launch(self):
        """A flag on whether to update scm on launch.

        Returns:
            bool: True if set, False otherwise.

        """
        return self._data.get('scm_update_on_launch')

    @scm_update_on_launch.setter
    def scm_update_on_launch(self, value):
        """Update the scm_update_on_launch project.

        Returns:
            None:

        """
        self._update_values('scm_update_on_launch', value)

    @property
    def scm_update_cache_timeout(self):
        """The cache timeout set for the scm.

        Returns:
            integer: The cache time out set.

        """
        return self._data.get('scm_update_cache_timeout')

    @scm_update_cache_timeout.setter
    def scm_update_cache_timeout(self, value):
        """Update the scm_update_cache_timeout of the project.

        Returns:
            None:

        """
        minimum = 0
        maximum = 2147483647
        conditions = [validate_range(value, minimum, maximum)]
        if all(conditions):
            self._update_values('scm_update_cache_timeout', value)
        else:
            raise InvalidValue(f'{value} is invalid, must be between {minimum} and {maximum}')

    @property
    def scm_revision(self):
        """The hash of the scm revision.

        Returns:
            string: The hash of the scm revision.

        """
        return self._data.get('scm_revision')

    @property
    def is_last_update_failed(self):
        """Flag on whether the last update failed or not.

        Returns:
            bool: True if last update has failed, False otherwise.

        """
        return self._data.get('last_update_failed')

    @property
    def last_updated(self):
        """The date and time of the last update.

        Returns:
            datetime: The datetime of the last update, None if not set.

        """
        try:
            date_ = parse(self._data.get('last_updated'))
        except (ValueError, TypeError):
            date_ = None
        return date_

    @property
    def custom_virtualenv(self):
        """The path of the custom virtual environment.

        Returns:
            string: The path of the custom virtual environment.

        """
        return self._data.get('custom_virtualenv')

    @custom_virtualenv.setter
    def custom_virtualenv(self, value):
        """Update the custom_virtualenv of the group.

        Returns:
            None:

        """
        max_characters = 100
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('custom_virtualenv', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less than or equal to '
                               f'{max_characters}')

    def update(self):
        """Send an SCM update request to the project.

        Returns:
            dict: Response of api request as json on success, None otherwise.

        """
        update_url = '{api}/projects/{id}/update/'.format(api=self._tower.api, id=self.id)
        response = self._tower.session.post(update_url)

        if not response.ok:
            self._logger.error(
                "Error updating the project '{}'. response was: {})".format(self.name, response.text))
        return response.json() if response.ok else {}

    @property
    def project_updates(self):
        """Get all the job_events for host.

        Returns:
            list: list of all the job events for the host.

        """
        return self._tower.project_updates.filter({'project': self.id})
