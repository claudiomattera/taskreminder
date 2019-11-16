#!/usr/bin/env python

# Copyright Claudio Mattera 2019.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT

import sys

from setuptools import setup

setup(
    name="task-reminder",
    version="0.1.0",
    description="Sends reminders for tasks from Taskwarrior",
    long_description=open("Readme.md").read(),
    author="Claudio Giovanni Mattera",
    author_email="claudio@mattera.it",
    url="https://gitlab.com/claudiomattera/task-reminder/",
    license="MIT",
    packages=[
        "taskreminder",
    ],
    include_package_data=True,
    entry_points={
        "gui_scripts": [
            "task-reminder = taskreminder.__main__:main",
        ],
    },
    install_requires=[
        "python-dateutil",
        "taskw",
        "requests",
        "markdown",
        "gnupg",
    ],
)
