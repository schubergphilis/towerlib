#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: workflow_node.py

"""
Main code for workflow_nodes.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from .core import (Entity)

# This is the main prefix used for logging
LOGGER_BASENAME = '''workflow_nodes'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class WorkflowNodes(Entity):
    """Models the user entity of ansible tower."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def count(self):
        """The job this event belongs to.

        Returns:
            Job: The job this event belongs to.

        """
        return self._data.get('count')

    @property
    def next(self):
        """The job this event belongs to.

        Returns:
            Job: The job this event belongs to.

        """
        return self._data.get('next')

    @property
    def previous(self):
        """The job this event belongs to.

        Returns:
            Job: The job this event belongs to.

        """
        return self._data.get('previous')

    @property
    def results(self):
        """The job this event belongs to.

        Returns:
            Job: The job this event belongs to.

        """
        return self._data.get('results')
