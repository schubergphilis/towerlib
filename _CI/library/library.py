#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import json
import logging
import os
import shlex
import shutil
import sys
from collections import namedtuple
from subprocess import Popen, PIPE

from pipenv.project import Project
from configuration import LOGGERS_TO_DISABLE, ENVIRONMENT_VARIABLES, LOGGING_LEVEL

logging_level = os.environ.get('LOGGING_LEVEL', '').upper() or LOGGING_LEVEL
if logging_level == 'DEBUG':
    print('Current executing python version is {}'.format(sys.version_info))

# needed to support alternate .venv path if PIPENV_PIPFILE is set
for name, value in ENVIRONMENT_VARIABLES.items():
    if name.startswith('PIPENV_'):
        if logging_level == 'DEBUG':
            print('Loading PIPENV related variable {} : {} '.format(name, value))
        os.environ[name] = value

# Provides possible python2.7 compatibility
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI.library'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

Package = namedtuple('Package', ['name', 'version'])

REQUIREMENTS_HEADER = """# 
# Please do not manually update this file since the requirements are managed
# by pipenv through Pipfile and Pipfile.lock . 
#
# This file is created and managed automatically by the template and it is left
# here only for backwards compatibility reasons with python's ecosystem.
#
# Please use Pipfile to update the requirements.
#
"""


# The sequence here is important because it makes sure
# that the virtual environment is loaded as soon as possible
def is_venv_created():
    dev_null = open(os.devnull, 'w')
    venv = Popen(['pipenv', '--venv'], stdout=PIPE, stderr=dev_null).stdout.read().strip()
    return True if venv else False


def is_venv_active():
    return hasattr(sys, 'real_prefix')


def get_project_root_path():
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_file_path, '..', '..'))


def get_venv_parent_path():
    alternate_pipefile_location = os.environ.get('PIPENV_PIPFILE', None)
    if alternate_pipefile_location:
        venv_parent = os.path.abspath(os.path.dirname(alternate_pipefile_location))
    else:
        venv_parent = os.path.abspath('.')
    return venv_parent


def activate_virtual_environment():
    os.chdir(get_project_root_path())
    activation_script_directory = 'Scripts' if sys.platform == 'win32' else 'bin'
    venv_parent = get_venv_parent_path()
    activation_file = os.path.join(venv_parent, '.venv', activation_script_directory, 'activate_this.py')
    if is_venv_created():
        if sys.version_info[0] == 3:
            with open(activation_file) as f:
                exec(f.read(), {'__file__': activation_file})
        elif sys.version_info[0] == 2:
            execfile(activation_file, dict(__file__=activation_file))

# After this everything is executed inside a virtual environment
if not is_venv_active():
    activate_virtual_environment()

try:
    import coloredlogs
    colored_logs = True
except ImportError:
    colored_logs = False


if is_venv_active():
    import semver


def get_emojize():
    from emoji import emojize
    return emojize


def setup_logging(level):
    if colored_logs:
        coloredlogs.install(level=level.upper())
    else:
        LOGGER = logging.getLogger()
        handler = logging.StreamHandler()
        handler.setLevel(level.upper())
        formatter = logging.Formatter(('%(asctime)s - '
                                       '%(name)s - '
                                       '%(levelname)s - '
                                       '%(message)s'))
        handler.setFormatter(formatter)
        LOGGER.addHandler(handler)
        LOGGER.setLevel(level.upper())
    for logger in LOGGERS_TO_DISABLE:
        logging.getLogger(logger).disabled = True


# TODO extend debug logging in the following methods

def load_environment_variables(environment_variables):
    LOGGER.debug('Loading environment variables')
    for name, value in environment_variables.items():
        if name in os.environ.keys():
            LOGGER.debug('Environment variable "%s" already loaded, not overriding', name)
        else:
            LOGGER.debug('Loading environment variable "%s" with value "%s"', name, value)
            os.environ[name] = value


def load_dot_env_file():
    if os.path.isfile('.env'):
        LOGGER.info('Loading environment variables from .env file')
        variables = {}
        for line in open('.env', 'r').read().splitlines():
            if line.strip().startswith('export '):
                line = line.replace('export ', '')
            key, value = line.strip().split('=', 1)
            variables[key.strip()] = value.strip()
        load_environment_variables(variables)


def get_binary_path(executable):
    """Gets the software name and returns the path of the binary."""
    if sys.platform == 'win32':
        if executable == 'start':
            return executable
        executable = executable + '.exe'
        if executable in os.listdir('.'):
            binary = os.path.join(os.getcwd(), executable)
        else:
            binary = next((os.path.join(path, executable)
                           for path in os.environ['PATH'].split(os.pathsep)
                           if os.path.isfile(os.path.join(path, executable))), None)
    else:
        binary = Popen(['which', executable], stdout=PIPE).stdout.read().strip().decode('utf-8')
    return binary if binary else None


def validate_binary_prerequisites(software_list):
    LOGGER.debug('Trying to validate binary prerequisites')
    success = True
    for executable in software_list:
        if not get_binary_path(executable):
            success = False
            LOGGER.error('Executable "%s" not found', executable)
        else:
            LOGGER.debug('Executable "%s" found in the path!', executable)
    return success


def validate_environment_variable_prerequisites(variable_list):
    LOGGER.debug('Trying to validate prerequisites')
    success = True
    for variable in variable_list:
        if not os.environ.get(variable):
            success = False
            LOGGER.error('Environment variable "%s" not found', variable)
        else:
            LOGGER.debug('Environment variable "%s" found in the path!', variable)
    return success


def execute_command(command):
    LOGGER.debug('Executing command "%s"', command)
    if sys.platform == 'win32':
        process = Popen(command, shell=True,  bufsize=1)
    else:
        command = shlex.split(command)
        LOGGER.debug('Command split to %s for posix shell', command)
        process = Popen(command, bufsize=1)
    process.communicate()
    return process.returncode


def open_file(path):
    open_programs = {'darwin': 'open',
                     'linux': 'xdg-open',
                     'win32': 'start'}
    executable = get_binary_path(open_programs.get(sys.platform))
    command = '{} {}'.format(executable, path)
    return execute_command(command)


def clean_up(items):
    if not isinstance(items, (list, tuple)):
        items = [items]
    for item in items:
        if os.path.isdir(item):
            LOGGER.debug('Trying to remove directory "%s"', item)
            shutil.rmtree(item)
        elif os.path.isfile(item):
            LOGGER.debug('Trying to remove file "%s"', item)
            os.unlink(item)
        else:
            LOGGER.warning('Unable to remove file or directory "%s"', item)


def get_top_level_dependencies():
    packages = Project().parsed_pipfile.get('packages', {}).keys()
    dev_packages = Project().parsed_pipfile.get('dev-packages', {}).keys()
    return packages, dev_packages


def get_all_packages():
    try:
        venv_parent = get_venv_parent_path()
        lock_file = os.path.join(venv_parent, 'Pipfile.lock')
        all_packages = json.loads(open(lock_file, 'r').read())
    except FileNotFoundError:
        LOGGER.error('Could not open Pipfile.lock, so cannot get dependencies, exiting...')
        raise SystemExit(1)
    packages = [Package(package_name, data.get('version'))
                for package_name, data in all_packages.get('default').items()]
    dev_packages = [Package(package_name, data.get('version'))
                    for package_name, data in all_packages.get('develop').items()]
    return packages, dev_packages


def save_requirements():
    top_level_packages, top_level_dev_packages = get_top_level_dependencies()
    all_packages, all_dev_packages = get_all_packages()
    packages = [package for package in all_packages
                if package.name in top_level_packages]
    dev_packages = [package for package in all_dev_packages
                    if package.name in top_level_dev_packages]
    venv_parent = get_venv_parent_path()
    requirements_file = os.path.join(venv_parent, 'requirements.txt')
    with open(requirements_file, 'w') as f:
        requirements = '\n'.join(['{}{}'.format(package.name, package.version.replace('==', '~='))
                                  for package in sorted(packages, key=lambda x: x.name)])
        f.write(REQUIREMENTS_HEADER + requirements)
    dev_requirements_file = os.path.join(venv_parent, 'dev-requirements.txt')
    with open(dev_requirements_file, 'w') as f:
        dev_requirements = '\n'.join(['{}{}'.format(package.name, package.version.replace('==', '~='))
                                      for package in sorted(dev_packages, key=lambda x: x.name)])
        f.write(REQUIREMENTS_HEADER + dev_requirements)


def get_version_file_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..',
                                        '..',
                                        '.VERSION'))


def bump(segment=None):
    version_file = get_version_file_path()
    try:
        version_text = open(version_file).read().strip()
        _ = semver.parse(version_text)
    except FileNotFoundError:
        LOGGER.error('Could not find .VERSION file')
        raise SystemExit(1)
    except ValueError:
        LOGGER.error('Invalid version found in .VERSION file "%s"', version_text)
        raise SystemExit(1)
    if segment:
        if segment not in ('major', 'minor', 'patch'):
            LOGGER.error('Invalid segment "%s" was provided for semantic versioning, exiting...')
            raise SystemExit(1)
        new_version = getattr(semver, 'bump_{}'.format(segment))(version_text)
        with open(version_file, 'w') as vfile:
            vfile.write(new_version)
            return new_version
    else:
        print(version_text)
        return version_text
