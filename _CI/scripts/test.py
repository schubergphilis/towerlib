#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test.py
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

import logging
import os
from time import sleep

# this sets up everything and MUST be included before any third party module in every step
import _initialize_template

from emoji import emojize
from bootstrap import bootstrap
from library import (open_file,
                     clean_up,
                     execute_command,
                     save_requirements)

# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI.test'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def test():
    bootstrap()
    clean_up('test-output')
    os.mkdir('test-output')
    save_requirements()
    success = execute_command('tox4')
    try:
        open_file(os.path.join('test-output', 'coverage', 'index.html'))
        sleep(0.5)
        open_file(os.path.join('test-output', 'nosetests.html'))
    except Exception:
        LOGGER.warning('Could not execute UI portion. Maybe running headless?')
    if success:
        LOGGER.info('%s No testing errors found! %s',
                    emojize(':check_mark_button:'),
                    emojize(':thumbs_up:'))
    else:
        LOGGER.error('%s Testing errors found! %s',
                     emojize(':cross_mark:'),
                     emojize(':crying_face:'))
    raise SystemExit(0 if success else 1)


if __name__ == '__main__':
    test()
