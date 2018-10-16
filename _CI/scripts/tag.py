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


import argparse
import logging
from bootstrap import bootstrap
from gitwrapperlib import Git
from library import bump
from configuration import BRANCHES_SUPPORTED_FOR_TAG

# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI.tag'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def check_branch():
    git = Git()
    if git.get_current_branch() not in BRANCHES_SUPPORTED_FOR_TAG:
        accepted_branches = ', '.join(BRANCHES_SUPPORTED_FOR_TAG)
        print("Tagging is only supported on {} "
              "you should not tag any other branch, exiting!".format(accepted_branches))
        raise SystemExit(1)


def push():
    git = Git()
    with open('.VERSION', 'r') as version_file:
        current_version = version_file.read()
        version_file.close()
    git.commit('Set version to {}'.format(current_version), '.VERSION')
    git.tag(current_version)
    git.push()
    git.push('origin', current_version)


def get_arguments():
    parser = argparse.ArgumentParser(description='Handles bumping of the artifact version')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--major', help='Bump the major version', action='store_true')
    group.add_argument('--minor', help='Bump the minor version', action='store_true')
    group.add_argument('--patch', help='Bump the patch version', action='store_true')
    args = parser.parse_args()
    return args


def tag():
    emojize = bootstrap()
    args = get_arguments()
    check_branch()
    if args.major:
        bump('major')
    elif args.minor:
        bump('minor')
    elif args.patch:
        bump('patch')
    else:
        bump()
        raise SystemExit(0)
    push()


if __name__ == '__main__':
    tag()
