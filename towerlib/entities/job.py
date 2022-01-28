#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: jobs.py
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
# pylint: disable=too-many-lines
"""
Main code for jobs.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging
import datetime

from bs4 import BeautifulSoup as Bfs
from dateutil.parser import parse
from towerlib.entities.core import Label

from towerlib.towerlibexceptions import InvalidCredential, InvalidValue, InvalidInventory, InvalidProject
from .core import Entity, EntityManager, validate_max_length


__author__ = '''Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-03'''
__copyright__ = '''Copyright 2018, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<ctyfoxylos@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging.
LOGGER_BASENAME = '''jobs'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())
JOB_TYPE_ACCEPTED_VALUES = ['run', 'check']


class Job:  # pylint: disable=too-few-public-methods
    """Job factory to handle the different job types returned."""

    def __new__(cls, tower_instance, data):
        entity_type = data.get('type')
        if entity_type == 'job':
            obj = JobRun(tower_instance, data)
        elif entity_type == 'workflow_job':
            obj = WorkflowJobRun(tower_instance, data)
        elif entity_type == 'project_update':
            obj = ProjectUpdateJob(tower_instance, data)
        elif entity_type == 'system_job':
            obj = SystemJob(tower_instance, data)
        elif entity_type == 'ad_hoc_command':
            obj = AdHocCommandJob(tower_instance, data)
        else:
            LOGGER.error('Unknown entity type %s', entity_type)
            LOGGER.debug(data)
            return None
        return obj


class JobEvent(Entity):  # pylint: disable=too-many-public-methods
    """Models the job event entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def job(self):
        """The job this event belongs to.

        Returns:
            Job: The job this event belongs to.

        """
        url = self._data.get('related', {}).get('job')
        return self._tower._get_object_by_url('Job', url)  # pylint: disable=protected-access

    @property
    def event(self):
        """The name of the host.

        Returns:
            string: The name of the event.

        """
        return self._data.get('event')

    @property
    def created_at(self):
        """The created date of the event.

        Returns:
            date_time (string): The string formatted datetime of the event creation.

        """
        return self._data.get('created')

    @property
    def modified_at(self):
        """The modified date of the event.

        Returns:
            basestring: The string formatted datetime of the event's last modification.

        """
        return self._data.get('modified')

    @property
    def counter(self):
        """The counter of the event.

        Returns:
            integer: The counter of the event.

        """
        return self._data.get('counter')

    @property
    def event_display(self):
        """The display of the event.

        Returns:
            basestring: The display of the event.

        """
        return self._data.get('event_display')

    @property
    def event_data(self):
        """The data of the event.

        Returns:
            basestring: The data of the event.

        """
        return self._data.get('event_data')

    @property
    def event_level(self):
        """The level of the event.

        Returns:
            integer: The level of the event.

        """
        return self._data.get('event_level')

    @property
    def is_failed(self):
        """Whether the event is failed.

        Returns:
            bool: Whether the event is failed.

        """
        return self._data.get('failed')

    @property
    def is_changed(self):
        """Whether the event is changed.

        Returns:
            bool: Whether the event is changed.

        """
        return self._data.get('changed')

    @property
    def uuid(self):
        """The uuid of the event.

        Returns:
            basestring: The uuid of the event.

        """
        return self._data.get('uuid')

    @property
    def parent_uuid(self):
        """The parent uuid of the event.

        Returns:
            basestring: The parent uuid of the event.

        """
        return self._data.get('parent_uuid')

    @property
    def host(self):
        """The host of the event.

        Returns:
            basestring: The host of the event.

        """
        return self._data.get('host')

    @property
    def host_name(self):
        """The hostname of the event.

        Returns:
            basestring: The hostname of the event.

        """
        return self._data.get('host_name')

    @property
    def parent(self):
        """The parent of the event.

        Returns:
            basestring: The parent of the event.

        """
        return self._data.get('parent')

    @property
    def playbook(self):
        """The playbook of the event.

        Returns:
            basestring: The playbook of the event.

        """
        return self._data.get('playbook')

    @property
    def play(self):
        """The play of the event.

        Returns:
            basestring: The play of the event.

        """
        return self._data.get('play')

    @property
    def task(self):
        """The task of the event.

        Returns:
            basestring: The task of the event.

        """
        return self._data.get('task')

    @property
    def role(self):
        """The role of the event.

        Returns:
            basestring: The role of the event.

        """
        return self._data.get('role')

    @property
    def stdout(self):
        """The stdout of the event.

        Returns:
            basestring: The stdout of the event.

        """
        return self._data.get('stdout')

    @property
    def start_line(self):
        """The start line of the event.

        Returns:
            integer: The start line of the event.

        """
        return self._data.get('start_line')

    @property
    def end_line(self):
        """The end line of the event.

        Returns:
            integer: The end line of the event.

        """
        return self._data.get('end_line')

    @property
    def verbosity(self):
        """The verbosity of the event.

        Returns:
            integer: The verbosity of the event.

        """
        return self._data.get('verbosity')


class JobSummary(Entity):
    """Models the Job entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def summary_fields(self):
        """The summary_fields of this job summary.

        Returns:
            dict: The summary_fields of this job summary.

        """
        return self._data.get('summary_fields')

    @property
    def host(self):
        """The host of the job summary.

        Returns:
            basestring: The host of the job summary.

        """
        return self._data.get('host')

    @property
    def host_name(self):
        """The host name of the job summary.

        Returns:
            basestring: The host name of the job summary.

        """
        return self._data.get('host_name')

    @property
    def is_changed(self):
        """Whether the job had been changed.

        Returns:
            integer: Whether the job had been changed.

        """
        return self._data.get('changed')

    @property
    def is_dark(self):
        """Whether the job is dark.

        Returns:
            integer: Whether the job is dark.

        """
        return self._data.get('dark')

    @property
    def failures_count(self):
        """The number of job failures.

        Returns:
            integer: The number of job failures.

        """
        return self._data.get('failures')

    @property
    def is_ok(self):
        """Whether the job is dark.

        Returns:
            integer: Whether the job is dark.

        """
        return self._data.get('ok')

    @property
    def processed_count(self):
        """The number of time the job was processed.

        Returns:
            integer: The number of time the job was processed.

        """
        return self._data.get('processed')

    @property
    def skipped_count(self):
        """The number of time the job was skipped.

        Returns:
            integer: The number of time the job was skipped.

        """
        return self._data.get('skipped')

    @property
    def failed(self):
        """Whether the job is failed or not.

        Returns:
            bool: Whether the job is failed or not.

        """
        return self._data.get('failed')


class JobRun(Entity):  # pylint: disable=too-many-public-methods
    """Models the Job entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def created_by(self):
        """The User that created the job.

        Returns:
            User: The user that created the job in tower.

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    # TOFIX add labels, model them and implement them here

    def _get_dynamic_value(self, variable):
        url = f'{self._tower.api}/jobs/{self.id}'
        response = self._tower.session.get(url)
        return response.json().get(variable) if response.ok else None

    def cancel(self):
        """Cancels the running or pending job.

        Returns:
            True on success, False otherwise.

        """
        url = f'{self._tower.api}/jobs/{self.id}/cancel/'
        response = self._tower.session.post(url)
        return response.ok

    @property
    def extra_vars(self):
        """The extra_vars of the job.

        Returns:
            extra_vars: The extra_vars of the job

        """
        return self._get_dynamic_value('extra_vars')

    @property
    def modified_at(self):
        """The modification datetime of the job.

        Returns:
            modification_datetime: The datetime of the modification.

        """
        return self._get_dynamic_value('modified')

    @property
    def finished(self):
        """The finished datetime of the job.

        Returns:
            finished_datetime: The datetime of the end of the job.

        """
        return self._get_dynamic_value('finished')

    @property
    def elapsed_time(self):
        """The elpsed time of the job.

        Returns:
            elapsed: The seconds elapsed since the start of the job.

        """
        return self._get_dynamic_value('elapsed')

    @property
    def status(self):
        """The status of the job.

        Returns:
            status: The status of the job.

        """
        return self._get_dynamic_value('status')

    @property
    def result_stdout(self):
        """The result stdout of the job.

        Returns:
            result_stdout: The result stdout of the job.

        """
        return self._get_dynamic_value('result_stdout')

    @property
    def result_traceback(self):
        """The result traceback of the job.

        Returns:
            result_traceback: The result traceback of the job.

        """
        return self._get_dynamic_value('result_traceback')

    @property
    def inventory(self):
        """The inventory this job belongs to.

        Returns:
            Inventory: The inventory this job belongs to.

        """
        url = self._data.get('related', {}).get('inventory')
        return self._tower._get_object_by_url('Inventory', url)  # pylint: disable=protected-access

    @property
    def project(self):
        """The project this job belongs to.

        Returns:
            Project: The project this job belongs to.

        """
        url = self._data.get('related', {}).get('project')
        return self._tower._get_object_by_url('Project', url)  # pylint: disable=protected-access

    @property
    def credentials(self):
        """The credentials of this job.

        Returns:
            Credentials: The credentials this job has.

        """
        url = self._data.get('related', {}).get('credentials')
        return EntityManager(self._tower,
                             entity_object='Credential',
                             primary_match_field='name',
                             url=url)

    @property
    def extra_credentials(self):
        """The extra credentials of the job.

        Returns:
            EntityManager: EntityManager of the extra credentials.

        """
        url = self._data.get('related', {}).get('extra_credentials')
        return EntityManager(self._tower,
                             entity_object='Credential',
                             primary_match_field='name',
                             url=url)

    @property
    def unified_job_template(self):
        """The job template this job belongs to.

        Returns:
            JobTemplate: The job template this job belongs to.

        """
        url = self._data.get('related', {}).get('unified_job_template')
        return self._tower._get_object_by_url('JobTemplate', url)  # pylint: disable=protected-access

    @property
    def stdout(self):
        """The stdout of the job execution.

        Returns:
            basestring: The stdout of the job execution.

        """
        url = f"{self._tower.host}{self._data.get('related', {}).get('stdout')}"
        response = self._tower.session.get(url)
        soup = Bfs(response.text, 'html.parser')
        # get stdout div tag
        div = soup.find('div', {'class': 'nocode ansi_fore ansi_back'})
        # remove style tag
        div.find('style').extract()
        return div.text

    # TOFIX use, model and implement notifications.

    @property
    def host(self):
        """The host of the credential.

        Returns:
            dictionary: The host structure of the credential.

        """
        return self._data.get('summary_fields', {}).get('host')

    @property
    def job_host_summaries(self):
        """The job summaries of the runs of this job.

        Returns:
            EntityManager: EntityManager of the job host summaries.

        """
        url = self._data.get('related', {}).get('job_host_summaries')
        return EntityManager(self._tower,
                             entity_object='JobSummary',
                             primary_match_field='name',
                             url=url)

    @property
    def job_events(self):
        """The job events of the runs of this job.

        Returns:
            EntityManager: EntityManager of the job events.

        """
        url = self._data.get('related', {}).get('job_events')
        return EntityManager(self._tower,
                             entity_object='JobEvent',
                             primary_match_field='name',
                             url=url)

    # TOFIX model activity streams and implement them here.

    @property
    def job_template(self):
        """The job template of this job.

        Returns:
            JobTemplate: The job template of this job.

        """
        url = self._data.get('related', {}).get('job_template')
        return self._tower._get_object_by_url('JobTemplate', url)  # pylint: disable=protected-access

    # TOFIX model cancel event and implement it here.

    # TOFIX model relaunch event and implement it here.

    @property
    def summary_fields(self):
        """The summary fields of the job.

        Returns:
            dict: The summary fields of the job.

        """
        return self._data.get('summary_fields')

    @property
    def name(self):
        """The name of the job.

        Returns:
            string: The name of the job.

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the job.

        Returns:
            string: The description of the job.

        """
        return self._data.get('description')

    @property
    def job_type(self):
        """The type of the job.

        Returns:
            string: The type of the job.

        """
        return self._data.get('job_type')


class WorkflowJobRun(JobRun):
    """Models the Workflow Job Run entity of ansible tower."""

    def _get_dynamic_value(self, variable):
        url = f'{self._tower.api}/workflow_jobs/{self.id}'
        response = self._tower.session.get(url)
        return response.json().get(variable) if response.ok else None

    def cancel(self):
        """Cancels the running or pending job.

        Returns:
            True on success, False otherwise.

        """
        url = f'{self._tower.api}/workflow_jobs/{self.id}/cancel/'
        response = self._tower.session.post(url)
        return response.ok


class JobTemplate(Entity):  # pylint: disable=too-many-public-methods
    """Models the Job Template entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)
        self._object_roles = None

    @property
    def name(self):
        """The name of the job template.

        Returns:
            string: The name of the job template.

        """
        return self._data.get('name')

    @name.setter
    def name(self, value):
        """Update the name of the template."""
        max_characters = 512
        conditions = [validate_max_length(value, max_characters)]
        if all(conditions):
            self._update_values('name', value)
        else:
            raise InvalidValue(f'{value} is invalid. Condition max_characters must be less than or equal to '
                               f'{max_characters}')

    @property
    def description(self):
        """The description of the job template.

        Returns:
            string: The description of the job template.

        """
        return self._data.get('description')

    @property
    def created_by(self):
        """The User that created the job template.

        Returns:
            User: The user that created the job template in tower.

        """
        url = self._data.get('related', {}).get('created_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def modified_by(self):
        """The User that modified the job template last.

        Returns:
            User: The user that modified the job template in tower last.

        """
        url = self._data.get('related', {}).get('modified_by')
        return self._tower._get_object_by_url('User', url)  # pylint: disable=protected-access

    @property
    def job_type(self):
        """The job_type of the job template.

        Returns:
            string: The job_type of the job template.

        """
        return self._data.get('job_type')

    @job_type.setter
    def job_type(self, value):
        """Update the job_type of the template."""
        if value not in JOB_TYPE_ACCEPTED_VALUES:
            raise InvalidValue(f'{value} is invalid. Given value must be one of these: {JOB_TYPE_ACCEPTED_VALUES}')
        self._update_values('job_type', value)

    @property
    def inventory(self):
        """The inventory that the job template is part of.

        Returns:
            Inventory: The inventory that the job template is part of.

        """
        url = self._data.get('related', {}).get('inventory')
        return self._tower._get_object_by_url('Inventory', url)  # pylint: disable=protected-access

    @property
    def project(self):
        """The project that the job template is part of.

        Returns:
            Inventory: The project that the job template is part of.

        """
        url = self._data.get('related', {}).get('project')
        if not url:
            return None
        return self._tower._get_object_by_url('Project', url)  # pylint: disable=protected-access

    @project.setter
    def project(self, value):
        """Update the project of the job template by project id.

        Args:
            value: The new project id, to which the project will be updated.

        """
        project = self._tower.get_project_by_id(value)
        if not project:
            raise InvalidProject(value)
        self._update_values('project', value)

    @property
    def playbook(self):
        """The playbook of the job template.

        Returns:
            string: The playbook of the job template.

        """
        return self._data.get('playbook')

    @property
    def credentials(self):
        """The credentials that the job template uses.

        Returns:
            Credentials: The credentials that the job template uses.

        """
        url = self._data.get('related', {}).get('credentials')
        return EntityManager(self._tower,
                             entity_object='Credential',
                             primary_match_field='name',
                             url=url)

    @property
    def labels(self):
        """The labels of the job template.

        Returns:
            labels (list): The job template labels (only id and name can be retrieved).

        """
        return [Label(**data) for data in self._data.get('summary_fields', {}).get('labels', {}).get('results', [])]

    @property
    def extra_credentials(self):
        """The extra_credentials that the job template uses.

        Returns:
            EntityManager: EntityManager of the extra credentials.

        """
        url = self._data.get('related', {}).get('extra_credentials')
        return EntityManager(self._tower,
                             entity_object='Credential',
                             primary_match_field='name',
                             url=url)

    def add_credential(self, credential, credential_type='Machine'):
        """Adds credential by name.

        Args:
            credential (str): A single string of a credential.
            credential_type (int): The type of the credential.

        """
        extra_credential = self.inventory.organization.get_credential_by_name(credential,
                                                                              credential_type)
        if not extra_credential:
            raise InvalidCredential(credential)
        return self._add_credential_by_id(extra_credential.id, f'Failed to add credential {credential}')

    def add_credential_by_id(self, credential_id):
        """Adds credential by id.

        Args:
            credential_id (int): The id of the credential.

        """
        return self._add_credential_by_id(credential_id, f'Failed to add credential id {credential_id}')

    def _add_credential_by_id(self, credential_id, error_message):
        """Adds credential helper function.

        Args:
            credential_id (int): The id of the credential.
            error_message (str): The message if no credential is added.

        """
        payload = {'id': credential_id}
        url = f'{self._tower.api}/job_templates/{self.id}/credentials/'
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error(error_message)
        return response.ok

    @property
    def schedules(self):
        """The schedules that the job template uses.

        Returns:
            EntityManager: EntityManager of the schedules.

        """
        url = self._data.get('related', {}).get('schedules')
        return EntityManager(self._tower,
                             entity_object='Schedule',
                             primary_match_field='name',
                             url=url)

    def add_schedule(self,  # pylint: disable=too-many-arguments
                     name,
                     start_date,
                     start_time,
                     limit='',
                     description='',
                     time_zone='Europe/Berlin',
                     repeat_frequency='DAILY',
                     interval=1):
        """Adds a schedule to a job template.

        Args:
            name (str): A name of the schedule.
            start_date (datetime.date): The start date of the schedule
            start_time (datetime.time): Start time of the schedule
            limit (str): Limit of the schedule
            description (str): Description of the schedule
            time_zone (str): The time zone assigned to the schedule
            repeat_frequency (str): How frequently the job will be run
            interval (int): Interval of the Job

        """
        if not isinstance(start_date, datetime.date):
            raise InvalidValue
        if not isinstance(start_time, datetime.time):
            raise InvalidValue
        schedule_datetime = f"20{datetime.datetime.combine(start_date,start_time).strftime('%y%m%dT%H%M%S')}"
        payload = {
            'description': description,
            'limit': limit,
            'name': name,
            'rrule': f'DTSTART;TZID={time_zone}:{schedule_datetime} RRULE:FREQ={repeat_frequency};INTERVAL={interval}'
        }
        url = f'{self._tower.api}/job_templates/{self.id}/schedules/'
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Failed to add schedule %s. Error: %s', name, response.json())
        return response.ok

    @property
    def object_roles(self):
        """The object roles.

        Returns:
            ObjectRole: The object roles supported.

        """
        if not self._object_roles:
            url = self._data.get('related', {}).get('object_roles')
            self._object_roles = EntityManager(self._tower,
                                               entity_object='ObjectRole',
                                               primary_match_field='name',
                                               url=url)
        return self._object_roles

    @property
    def vault_credential(self):
        """The vault credential of the job template.

        Returns:
            string: The vault credential of the job template.

        """
        return self._data.get('vault_credential')

    @property
    def forks_count(self):
        """The number of forks of the job template.

        Returns:
            string: The number of forks of the job template.

        """
        return self._data.get('forks')

    @property
    def limit(self):
        """The limit of the job template.

        Returns:
            string: The limit of the job template.

        """
        return self._data.get('limit')

    @property
    def verbosity(self):
        """The verbosity level of the job template.

        Returns:
            string: The verbosity level of the job template.

        """
        return self._data.get('verbosity')

    @property
    def extra_vars(self):
        """The extra vars of the job template.

        Returns:
            string: The extra vars of the job template.

        """
        return self._data.get('extra_vars')

    @property
    def job_tags(self):
        """The job tags of the job template.

        Returns:
            string: The job tags of the job template.

        """
        return self._data.get('job_tags')

    @property
    def force_handlers(self):
        """Flag about whether the handlers are forced.

        Returns:
            bool: True if the handlers are forced, False otherwise.

        """
        return self._data.get('force_handlers')

    @property
    def skip_tags(self):
        """The tags to skip for the job template.

        Returns:
            string: The tags to skip for the job template.

        """
        return self._data.get('skip_tags')

    @property
    def start_at_task(self):
        """Not really sure what this is.

        Returns:
            string:

        """
        return self._data.get('start_at_task')

    @property
    def timeout(self):
        """The timeout setting of the job template.

        Returns:
            integer: The timeout setting of the job template.

        """
        return self._data.get('timeout')

    @property
    def use_fact_cache(self):
        """Flag about whether the fact cache should be used.

        Returns:
            bool: True if the fact cache should be used, False otherwise.

        """
        return self._data.get('use_fact_cache')

    @use_fact_cache.setter
    def use_fact_cache(self, value):
        """Set or unset the "user fact cache flag".

        Args:
            value: bool value of the flag: use_fact_cache for the job_template.

        Returns:
            None.

        """
        self._update_values('use_fact_cache', value)

    @property
    def last_job_run_at(self):
        """Date and time that the last job template job was run.

        Returns:
            datetime: The datetime of the last job execution.

        """
        return self._to_datetime(self._data.get('last_job_run'))

    @property
    def is_last_job_failed(self):
        """Flag about whether the last job failed.

        Returns:
            bool: True if last run job failed, False otherwise.

        """
        return self._data.get('last_job_failed')

    @property
    def next_job_run_at(self):
        """Date and time when the next job template job will run.

        Returns:
            datetime: The datetime of the next job execution.

        """
        return self._to_datetime(self._data.get('next_job_run'))

    @property
    def recent_jobs(self):
        """The most recent jobs on the template.

        Returns:
            list if dict: The most recent jobs run on the template.

        """
        return self._data.get('summary_fields', {}).get('recent_jobs')

    @property
    def last_job_run_id(self):
        """The id of most recent job run on the template.

        Returns:
            int/None: The id of the most recent job run on the template

        """
        recent_jobs = self._data.get('summary_fields', {}).get('recent_jobs')
        ids = [v for job in recent_jobs for k, v in job.items() if k == 'id']
        ids.sort()
        return ids[-1]

    @property
    def status(self):
        """The status of the job template.

        Returns:
            string: The status of the job template.

        """
        return self._data.get('status')

    @property
    def host_config_key(self):
        """Not really sure what this is.

        Returns:
            string:

        """
        return self._data.get('host_config_key')

    @property
    def ask_diff_mode_on_launch(self):
        """Flag about whether to ask for diff mode on launch.

        Returns:
            bool: True if set to ask for diff mode on launch, False otherwise.

        """
        return self._data.get('ask_diff_mode_on_launch')

    @property
    def ask_variables_on_launch(self):
        """Flag about whether to ask for variables on launch.

        Returns:
            bool: True if set to ask for variables on launch, False otherwise.

        """
        return self._data.get('ask_variables_on_launch')

    @property
    def ask_limit_on_launch(self):
        """Flag about whether to ask for limit on launch.

        Returns:
            bool: True if set to ask for limit on launch, False otherwise.

        """
        return self._data.get('ask_limit_on_launch')

    @property
    def ask_tags_on_launch(self):
        """Flag about whether to ask for tags on launch.

        Returns:
            bool: True if set to ask for tags on launch, False otherwise.

        """
        return self._data.get('ask_tags_on_launch')

    @property
    def ask_skip_tags_on_launch(self):
        """Flag about whether to ask to skip tags on launch.

        Returns:
            bool: True if set to ask to skip tags on launch, False otherwise.

        """
        return self._data.get('ask_skip_tags_on_launch')

    @property
    def ask_job_type_on_launch(self):
        """Flag about whether to ask for job type on launch.

        Returns:
            bool: True if set to ask for job type on launch, False otherwise.

        """
        return self._data.get('ask_job_type_on_launch')

    @property
    def ask_verbosity_on_launch(self):
        """Flag about whether to ask for verbosity on launch.

        Returns:
            bool: True if set to ask for verbosity on launch, False otherwise.

        """
        return self._data.get('ask_verbosity_on_launch')

    @property
    def ask_inventory_on_launch(self):
        """Flag about whether to ask for inventory on launch.

        Returns:
            bool: True if set to ask for inventory on launch, False otherwise.

        """
        return self._data.get('ask_inventory_on_launch')

    @property
    def ask_credential_on_launch(self):
        """Flag about whether to ask for credential on launch.

        Returns:
            bool: True if set to ask for credential on launch, False otherwise.

        """
        return self._data.get('ask_credential_on_launch')

    @property
    def survey_enabled(self):
        """Flag about whether the survey mode is enabled.

        Returns:
            bool: True if survey mode is enabled, False otherwise.

        """
        return self._data.get('survey_enabled')

    @property
    def survey_spec(self):
        """Survey specification.

        Returns:
            dict: Dict that contains info about the linked survey if exists

        """
        if not self.survey_enabled:
            return {}
        response = self._tower.session.get(f'{self.url}survey_spec/')
        if not response.ok:
            return {}
        return response.json()

    @property
    def become_enabled(self):
        """Not really sure what this is.

        Returns:
            bool:

        """
        return self._data.get('become_enabled')

    @property
    def diff_mode(self):
        """Flag about whether the diff mode is enabled.

        Returns:
            bool: True if diff mode is enabled, False otherwise.

        """
        return self._data.get('diff_mode')

    @property
    def allow_simultaneous(self):
        """Flag about whether to allow simultaneous executions.

        Returns:
            bool: True if set to allow simultaneous executions , False otherwise.

        """
        return self._data.get('allow_simultaneous')

    # pylint: disable=unused-argument,too-many-arguments
    def launch(self,
               extra_vars=None,
               job_tags=None,
               limit=None,
               inventory=None,
               credential=None,
               credentials=None,
               scm_branch=None):
        """Launches the job template.

        https://docs.ansible.com/ansible-tower/latest/html/towerapi/launch_jobtemplate.html.

        Returns:
            Job: Job object of the running job on success, None otherwise.

        """
        if all([isinstance(credentials, list),
                bool(credentials),
                credential is None]):
            credential = credentials[0]
        payload = {key: value for key, value in locals().items() if value and key != 'self'}
        url = f'{self.url}launch/'
        response = self._tower.session.post(url, json=payload)
        if not response.ok:
            self._logger.error('Error launching job %s, response was :%s', self.name, response.text)
            return None
        return Job(self._tower, response.json())

    def set_inventory(self, organization, name):
        """Inventory from specified organization applied as a prompt, assuming job template prompts for inventory.

        Args:
            organization (str): The organization name the inventory belongs to
            name (str): The inventory name to set. To reset the inventory set it to empty string.

        Returns:
            None.

        """
        value = ''
        if name:
            inventory = self._tower.get_organization_inventory_by_name(organization, name)
            if not inventory:
                raise InvalidInventory(name)
            value = inventory.id
        self._update_values('inventory', value)
        self._refresh_state()


class SystemJob(Entity):
    """Models the Job entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    # TOFIX use, model and implement cancel.

    # TOFIX use, model and implement notifications.

    # TOFIX use, model and implement system_job_template.

    # TOFIX use, model and implement unified_job_template.

    @property
    def started_at(self):
        """The date and time the job was started.

        Returns:_
            datetime: The datetime object of the date and time of the start of the job.
            None: If there is no entry for the start.

        """
        return self._to_datetime(self._data.get('start'))

    @property
    def finished_at(self):
        """The date and time the job was finished.

        Returns:_
            datetime: The datetime object of the date and time of the end of the job.
            None: If there is no entry for the finish.

        """
        return self._to_datetime(self._data.get('finished'))

    @property
    def summary_fields(self):
        """The summary fields of the job.

        Returns:
            dict: The summary fields of the job.

        """
        return self._data.get('summary_fields')

    @property
    def name(self):
        """The name of the job.

        Returns:
            string: The name of the job.

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the job.

        Returns:
            string: The description of the job.

        """
        return self._data.get('description')

    @property
    def job_type(self):
        """The type of the job.

        Returns:
            string: The type of the job.

        """
        return self._data.get('job_type')

    @property
    def elapsed(self):
        """The time elapsed during the run.

        Returns:
            float: The time elapsed during the run.

        """
        return self._data.get('elapsed')

    @property
    def job_args(self):
        """The arguments passed to the execution of the job.

        Returns:
            basestring: The arguments passed to the execution of the job.

        """
        return self._data.get('job_args')

    @property
    def job_cwd(self):
        """The current working directory of the execution of the job.

        Returns:
            basestring: The current working directory of the execution of the job.

        """
        return self._data.get('job_cwd')

    @property
    def job_env(self):
        """The environment of the execution of the job.

        Returns:
            dict: The environment of the execution of the job.

        """
        return self._data.get('job_env')

    @property
    def job_explanation(self):
        """The explanation of the job.

        Returns:
            basestring: The explanation of the job.

        """
        return self._data.get('job_explanation')

    @property
    def result_stdout(self):
        """The stdout of the result of the job.

        Returns:
            basestring: The stdout of the result of the job.

        """
        return self._data.get('result_stdout')

    @property
    def execution_node(self):
        """The node the job got executed on.

        Returns:
            basestring: The node the job got executed on.

        """
        return self._data.get('execution_node')

    @property
    def result_traceback(self):
        """The traceback of the result.

        Returns:
            basestring: The traceback of the result.

        """
        return self._data.get('result_traceback')

    @property
    def launch_type(self):
        """The type of launching for the update.

        Returns:
            basestring: The type of launching for the update.

        """
        return self._data.get('launch_type')

    @property
    def is_failed(self):
        """The status of the update.

        Returns:
            bool: The status of the update.

        """
        return self._data.get('failed')

    @property
    def status(self):
        """The status of the update.

        Returns:
            basestring: The status of the update.

        """
        return self._data.get('status')

    @property
    def extra_vars(self):
        """The extra vars of the job template.

        Returns:
            string: The extra vars of the job template.

        """
        return self._data.get('extra_vars')


class ProjectUpdateJob(Entity):  # pylint: disable=too-many-public-methods
    """Models the project update entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def credentials(self):
        """The credentials of the project.

        Returns:
            Credentials: The credentials of the project.

        """
        url = self._data.get('related', {}).get('credentials')
        return EntityManager(self._tower,
                             entity_object='Credential',
                             primary_match_field='name',
                             url=url)

    @property
    def stdout(self):
        """The stdout of the project update.

        Returns:
            basestring: The stdout of the project update.

        """
        stdout_url = self._data.get('related', {}).get('stdout')
        url = f'{self._tower.host}{stdout_url}'
        response = self._tower.session.get(url)
        soup = Bfs(response.text, 'html.parser')
        # get stdout div tag
        div = soup.find('div', {'class': 'nocode ansi_fore ansi_back'})
        # remove style tag
        div.find('style').extract()
        return div.text

    # TOFIX model and use cancel.

    # TOFIX use, model and implement notifications.

    # TOFIX use, model and implement scm_inventory_updates.

    @property
    def project(self):
        """The project of the ProjectUpdateJob.

        Returns:
            Project: The Project that this project_update belongs to.

        """
        url = self._data.get('related', {}).get('project')
        return self._tower._get_object_by_url('Project', url)  # pylint: disable=protected-access

    @property
    def summary_fields(self):
        """The summary fields of the job.

        Returns:
            dict: The summary fields of the job.

        """
        return self._data.get('summary_fields')

    @property
    def name(self):
        """The name of the project for the update.

        Returns:
            basestring: The name of the project for the update.

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the project for the update.

        Returns:
            basestring: The description of the project for the update.

        """
        return self._data.get('description')

    @property
    def local_path(self):
        """The local path of the project for the update.

        Returns:
            basestring: The local path of the project for the update.

        """
        return self._data.get('local_path')

    @property
    def scm_type(self):
        """The scm type of the project for the update.

        Returns:
            basestring: The scm type of the project for the update.

        """
        return self._data.get('scm_type')

    @property
    def scm_url(self):
        """The scm url of the project for the update.

        Returns:
            basestring: The scm url of the project for the update.

        """
        return self._data.get('scm_url')

    @property
    def scm_branch(self):
        """The scm branch of the project for the update.

        Returns:
            basestring: The scm branch of the project for the update.

        """
        return self._data.get('scm_branch')

    @property
    def scm_clean(self):
        """Whether the scm clean flag is set on the project.

        Returns:
            bool: Whether the scm clean flag is set on the project.

        """
        return self._data.get('scm_clean')

    @property
    def scm_delete_on_update(self):
        """Whether the scm delete on update flag is set on the project.

        Returns:
            bool: Whether the scm delete on update flag is set on the project.

        """
        return self._data.get('scm_delete_on_update')

    @property
    def timeout(self):
        """Timeout setting of the project.

        Returns:
            integer: Timeout setting of the project.

        """
        return self._data.get('timeout')

    @property
    def launch_type(self):
        """The type of launching for the update.

        Returns:
            basestring: The type of launching for the update.

        """
        return self._data.get('launch_type')

    @property
    def status(self):
        """The status of the update.

        Returns:
            basestring: The status of the update.

        """
        return self._data.get('status')

    @property
    def is_failed(self):
        """The status of the update.

        Returns:
            bool: The status of the update.

        """
        return self._data.get('failed')

    @property
    def started_at(self):
        """The date and time the update was started.

        Returns:
            datetime: The date and time the update was started.
            None: If there is no entry for the start time.

        """
        try:
            date_ = parse(self._data.get('started'))
        except (ValueError, TypeError):
            date_ = None
        return date_

    @property
    def finished_at(self):
        """The date and time the update was finished.

        Returns:
            datetime: The date and time the update was finished.
            None: If there is no entry for the finish time.

        """
        try:
            date_ = parse(self._data.get('finished'))
        except (ValueError, TypeError):
            date_ = None
        return date_

    @property
    def elapsed(self):
        """The time elapsed during the run.

        Returns:
            float: The time elapsed during the run.

        """
        return self._data.get('elapsed')

    @property
    def job_args(self):
        """The arguments passed to the execution of the job.

        Returns:
            basestring: The arguments passed to the execution of the job.

        """
        return self._data.get('job_args')

    @property
    def job_cwd(self):
        """The current working directory of the execution of the job.

        Returns:
            basestring: The current working directory of the execution of the job.

        """
        return self._data.get('job_cwd')

    @property
    def job_env(self):
        """The environment of the execution of the job.

        Returns:
            dict: The environment of the execution of the job.

        """
        return self._data.get('job_env')

    @property
    def job_explanation(self):
        """The explanation of the job.

        Returns:
            basestring: The explanation of the job.

        """
        return self._data.get('job_explanation')

    @property
    def result_stdout(self):
        """The stdout of the result of the job.

        Returns:
            basestring: The stdout of the result of the job.

        """
        return self._data.get('result_stdout')

    @property
    def execution_node(self):
        """The node the job got executed on.

        Returns:
            basestring: The node the job got executed on.

        """
        return self._data.get('execution_node')

    @property
    def result_traceback(self):
        """The traceback of the result.

        Returns:
            basestring: The traceback of the result.

        """
        return self._data.get('result_traceback')

    @property
    def job_type(self):
        """The type of the job executed on the update.

        Returns:
            basestring: The type of the job executed on the update.

        """
        return self._data.get('job_type')


class AdHocCommandJob(SystemJob):
    """Models the project update entity of ansible tower."""

    def __init__(self, tower_instance, data):
        SystemJob.__init__(self, tower_instance, data)

    @property
    def become_enabled(self):
        """Boolean on whether the job has become enabled.

        Returns:
            bool: Boolean on whether the job has become enabled.

        """
        return self._data.get('become_enabled')

    @property
    def credential(self):
        """The credential of the job.

        Returns:
            Credential: The credential of the job.

        """
        return self._tower.get_credential_by_id(self._data.get('credential'))

    @property
    def inventory(self):
        """The inventory of the job.

        Returns:
            Inventory: The inventory of the job.

        """
        return self._tower.get_inventory_by_id(self._data.get('inventory'))

    @property
    def diff_mode(self):
        """Boolean on whether the job has diff mode enabled.

        Returns:
            bool: Boolean on whether the job has diff mode enabled.

        """
        return self._data.get('diff_mode')

    @property
    def forks_count(self):
        """Number of forks supported by the job.

        Returns:
            integer: Number of forks supported by the job.

        """
        return self._data.get('forks')

    @property
    def module_args(self):
        """The arguments passed to the module.

        Returns:
            basestring: The arguments passed to the module.

        """
        return self._data.get('module_args')

    @property
    def module_name(self):
        """The name of the module executed.

        Returns:
            basestring: The name of the module executed.

        """
        return self._data.get('module_name')

#
# u'related': {u'activity_stream': u'/api/v2/ad_hoc_commands/4979/activity_stream/',
#              u'cancel': u'/api/v2/ad_hoc_commands/4979/cancel/',
#              u'created_by': u'/api/v2/users/69/',
#              u'credential': u'/api/v2/credentials/25/',
#              u'events': u'/api/v2/ad_hoc_commands/4979/events/',
#              u'inventory': u'/api/v2/inventories/17/',
#              u'notifications': u'/api/v2/ad_hoc_commands/4979/notifications/',
#              u'relaunch': u'/api/v2/ad_hoc_commands/4979/relaunch/',
#              u'stdout': u'/api/v2/ad_hoc_commands/4979/stdout/'},
