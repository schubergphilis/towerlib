#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: schedule.py
#
# Copyright 2020 Ilija Matoski
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
Main code for Schedule.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from .core import Entity


class Schedule(Entity):
    """Models the schedule entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def rrule(self):
        """The rrule of the schedule.

        Returns:
            string: The rrule of the schedule.

        """
        return self._data.get('rrule')

    @property
    def name(self):
        """The name of the schedule.

        Returns:
            string: The name of the schedule.

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the schedule.

        Returns:
            string: The description of the schedule.

        """
        return self._data.get('description')

    @property
    def extra_data(self):
        """The extra data of the schedule.

        Returns:
            dict: The extra data of the schedule.

        """
        return self._data.get('extra_data')

    @property
    def inventory(self):
        """The inventory this schedule belongs to.

        Returns:
            Inventory: The inventory this schedule belongs to.

        """
        return self._data.get('inventory')

    @property
    def scm_branch(self):
        """The scm_branch of the schedule.

        Returns:
            string: The scm_branch of the schedule.

        """
        return self._data.get('scm_branch')

    @property
    def job_type(self):
        """The job_type of the schedule.

        Returns:
            string: The job_type of the schedule.

        """
        return self._data.get('job_type')

    @property
    def job_tags(self):
        """The job tags of the schedule.

        Returns:
            string: The job tags of the schedule.

        """
        return self._data.get('job_tags')

    @property
    def skip_tags(self):
        """The tags to skip of the schedule.

        Returns:
            string: The tags to skip of the schedule.

        """
        return self._data.get('job_tags')

    @property
    def limit(self):
        """The limit of the schedule.

        Returns:
            string: The limit of the schedule.

        """
        return self._data.get('limit')

    @property
    def diff_mode(self):
        """Display mode for the execution the schedule.

        Returns:
            boolean: Are we displaying diff mode for the run?

        """
        return self._data.get('diff_mode')

    @property
    def verbosity(self):
        """Verbosity of the run.

        Returns:
            string: Verbosity of the run .

        """
        return self._data.get('verbosity')

    @property
    def unified_job_template(self):
        """Unified job template.

        Returns:
            string: Unified job template .

        """
        return self._data.get('unified_job_template')

    @property
    def enabled(self):
        """Enables processing of this schedule.

        Returns:
            bool: Enables processing of this schedule.

        """
        return self._data.get('enabled')

    @property
    def dtstart(self):
        """The first occurrence of the schedule occurs on or after this time.

        Returns:
            datetime: The first occurrence of the schedule occurs on or after this time.

        """
        return self._data.get('dtstart')

    @property
    def dtend(self):
        """The last occurrence of the schedule occurs before this time, aftewards the schedule expires.

        Returns:
            datetime: The last occurrence of the schedule occurs before this time, aftewards the schedule expires.

        """
        return self._data.get('dtend')

    @property
    def next_run(self):
        """The next time that the scheduled action will run.

        Returns:
            datetime: The next time that the scheduled action will run.

        """
        return self._data.get('next_run')

    @property
    def timezone(self):
        """The timezone of the schedule.

        Returns:
            string: The timezone of the schedule.

        """
        return self._data.get('timezone')

    @property
    def until(self):
        """Until when does the schedule run?

        Returns:
            datetime: Until when does the schedule run?

        """
        return self._data.get('until')

# @TODO: Editable
#
# rrule
# name
# description
# extra_data
# inventory
# scm_branch
# job_type (Choice list)
# job_tags
# skip_tags
# limit
# diff_mode (Boolean)
# verbosity (Choice list)
# unified_job_template
# enabled
