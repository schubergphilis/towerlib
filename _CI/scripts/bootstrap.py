#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: bootstrap.py
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


import os
import sys
import logging

current_file_path = os.path.dirname(os.path.abspath(__file__))
ci_path = os.path.abspath(os.path.join(current_file_path, '..'))
if ci_path not in sys.path:
    sys.path.append(ci_path)

from configuration import LOGGING_LEVEL, ENVIRONMENT_VARIABLES, PREREQUISITES
from library import (setup_logging,
                     get_project_root_path,
                     validate_binary_prerequisites,
                     validate_environment_variable_prerequisites,
                     is_venv_created,
                     execute_command,
                     load_environment_variables,
                     load_dot_env_file,
                     activate_virtual_environment,
                     get_emojize)

# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI.bootstrap'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def bootstrap():
    setup_logging(os.environ.get("LOGGING_LEVEL") or LOGGING_LEVEL)
    load_environment_variables(ENVIRONMENT_VARIABLES)
    load_dot_env_file()
    if not validate_binary_prerequisites(PREREQUISITES.get('executables', [])):
        LOGGER.error('Prerequisite binary missing, cannot continue.')
        raise SystemExit(1)
    if not validate_environment_variable_prerequisites(PREREQUISITES.get('environment_variables', [])):
        LOGGER.error('Prerequisite environment variable missing, cannot continue.')
        raise SystemExit(1)
    if not is_venv_created():
        LOGGER.debug('Trying to create virtual environment.')
        skip_lock = '--skip-lock' if os.environ.get('PIPENV_SKIP_LOCK') else ''
        exit_code = execute_command(f'pipenv install --dev --ignore-pipfile {skip_lock}')
        success = not exit_code
        if success:
            activate_virtual_environment()
            emojize = get_emojize()
            LOGGER.info('%s Successfully created virtual environment and loaded it! %s',
                        emojize(':white_heavy_check_mark:'),
                        emojize(':thumbs_up:'))
        else:
            LOGGER.error('Creation of virtual environment failed, cannot continue, '
                         'please clean up .venv directory and try again...')
            raise SystemExit(1)
    return get_emojize()


if __name__ == '__main__':
    bootstrap()
