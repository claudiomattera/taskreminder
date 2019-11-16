#!/usr/bin/env python3

# Copyright Claudio Mattera 2019.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT


import logging
import typing
from datetime import datetime, timedelta
from io import StringIO
from operator import itemgetter

from dateutil.tz import tzlocal

import taskw


ONE_DAY = timedelta(days=1)
TWO_DAY = timedelta(days=2)
ONE_WEEK = timedelta(days=7)


def get_reminder() -> typing.Text:
    logger = logging.getLogger(__name__)

    today = datetime.now(tzlocal()).replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + ONE_DAY
    overmorrow = today + TWO_DAY

    next_monday = _get_next_monday(today)
    two_mondays_from_now = _get_two_mondays_from_now(today)

    logger.debug("Today is {}".format(today))
    logger.debug("Tomorrow is {}".format(tomorrow))
    logger.debug("Overmorrow is {}".format(overmorrow))
    logger.debug("Next Monday is {}".format(next_monday))
    logger.debug("Two Mondays from now is {}".format(two_mondays_from_now))
    task_warrior = taskw.TaskWarrior(marshal=True)
    all_tasks = task_warrior.load_tasks()

    buffer = StringIO()

    tasks: typing.Dict[typing.Text, typing.List[typing.Any]] = {
        "no_deadline": [],
        "due_today": [],
        "due_tomorrow": [],
        "due_this_week": [],
        "due_next_week": [],
        "future": [],
    }

    for task in all_tasks["pending"]:
        if "wait" in task and task["wait"] is not None and task["wait"] > today:
            continue

        if "due" not in task:
            logger.debug("This task does not have a due date")
            logger.debug("  {}".format(task["description"]))
            tasks["no_deadline"].append(task)

        elif today < task["due"] <= tomorrow:
            logger.debug("This task is due today")
            logger.debug("  {}: {}".format(task["due"], task["description"]))
            tasks["due_today"].append(task)

        elif tomorrow < task["due"] <= overmorrow:
            logger.debug("This task is due tomorrow")
            logger.debug("  {}: {}".format(task["due"], task["description"]))
            tasks["due_tomorrow"].append(task)

        elif overmorrow < task["due"] <= next_monday:
            logger.debug("This task is due this week")
            logger.debug("  {}: {}".format(task["due"], task["description"]))
            tasks["due_this_week"].append(task)

        elif next_monday < task["due"] <= two_mondays_from_now:
            logger.debug("This task is due next week")
            logger.debug("  {}: {}".format(task["due"], task["description"]))
            tasks["due_next_week"].append(task)

        else:
            logger.debug("This task is due sometime in the future")
            logger.debug("  {}: {}".format(task["due"], task["description"]))
            tasks["future"].append(task)

    labels = {
        "no_deadline": "Without deadline",
        "due_today": "Due today",
        "due_tomorrow": "Due tomorrow",
        "due_this_week": "Due this week",
        "due_next_week": "Due next week",
        "future": "In future",
    }

    show_date = {
        "no_deadline": False,
        "due_today": False,
        "due_tomorrow": False,
        "due_this_week": True,
        "due_next_week": True,
        "future": True,
    }

    for key, label in labels.items():
        if len(tasks[key]) > 0:
            print("## {}\n".format(label), file=buffer)
            for task in sorted(tasks[key], key=itemgetter("urgency"), reverse=True):
                print("-  {}".format(task["description"]), file=buffer, end="")
                if show_date[key]:
                    print(", due on ", file=buffer, end="")
                    if task["due"].year == today.year:
                        print(task["due"].strftime("%A %-d %B"), file=buffer, end="")
                    else:
                        print(task["due"].strftime("%A %-d %B %Y"), file=buffer, end="")
                print("", file=buffer)
            print("", file=buffer)

    return buffer.getvalue()


def _get_next_monday(date: datetime) -> datetime:
    while date.date().weekday() != 0:
        date += ONE_DAY
    return date


def _get_two_mondays_from_now(date: datetime) -> datetime:
    date = _get_next_monday(date)
    date += ONE_WEEK
    return date
