#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# This file is placed into the public domain.

# Calculates the current version number.  If possible, this is the
# output of “git describe”, modified to conform to the versioning
# scheme that setuptools uses.  If “git describe” returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the RELEASE-VERSION file.
#
# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import *
#
# setup(
#     version=get_git_version(),
#     .
#     .
#     .
# )
#
#
# This will automatically update the RELEASE-VERSION file, if
# necessary.  Note that the RELEASE-VERSION file should *not* be
# checked into git; please add it to your top-level .gitignore file.
#
# You'll probably want to distribute the RELEASE-VERSION file in your
# sdist tarballs; to do this, just create a MANIFEST.in file that
# contains the following line:
#
#   include RELEASE-VERSION

__all__ = ("get_git_version")

from subprocess import Popen, PIPE


def get_version_from_upstream():
    """Read version from upstream .VERSION file.

    Returns:
        str: version on success, else None.
    """
    try:
        f = open(".VERSION", "r")

        try:
            version = f.readlines()[0]
            return version.strip()

        finally:
            f.close()

    except:
        return None


def call_git_describe(abbrev):
    """Get git tag number.

    Args:
        abbrev:

    Returns:
        bytes: git tag on success, else None.

    """
    try:
        p = Popen(['git', 'describe', '--abbrev=%d' % abbrev],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        return line.strip()

    except:
        return None


def is_dirty():
    """Check if current git repo has uncommitted files.

    Returns:
        bool: True if dirty, else False.
    """
    try:
        p = Popen(["git", "diff-index", "--name-only", "HEAD"],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        lines = p.stdout.readlines()
        return len(lines) > 0
    except:
        return False


def read_release_version():
    """Read release_version from given file.

    Returns:
        str: release_version on success, else None.
    """
    try:
        f = open("RELEASE-VERSION", "r")

        try:
            version = f.readlines()[0]
            return version.strip()

        finally:
            f.close()

    except:
        return None


def write_release_version(version):
    """Write the release_version back into the given file.

    Args:
        version: version number

    """
    f = open("RELEASE-VERSION", "w")
    f.write("%s\n" % version)
    f.close()


def get_git_version(abbrev=7):
    """Get git version with the help of other files.

    Args:
        abbrev: given abbrev=7

    Returns:
        str: git version as string.
    """

    # Read in the version that's currently in RELEASE-VERSION.
    release_version = read_release_version()
    upstream_version = get_version_from_upstream()
    if upstream_version:
        if upstream_version != release_version:
            write_release_version(upstream_version)
        return upstream_version
    else:
        # Try to get the current version using “git describe”.
        version = call_git_describe(abbrev)
        if version is not None:
            try:
                version = version.decode('UTF-8')
                if is_dirty():
                    version += "-dirty"
            except (UnicodeDecodeError, AttributeError):
                pass
        # If that doesn't work, fall back on the value that's in
        # RELEASE-VERSION.
        else:
            version = release_version
        # If we still don't have anything, that's an error.
        if version is None:
            raise ValueError("Cannot find the version number!")
        # If the current version is different from what's in the
        # RELEASE-VERSION file, update the file to be current.
        if version != release_version:
            write_release_version(version)
        # Finally, return the current version.
        return version


if __name__ == "__main__":
    print(get_git_version())
