#!/usr/bin/env python3

# Copyright Claudio Mattera 2019.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT


import argparse
import logging
import typing
import sys
import os

from .gotify import send_message as send_gotify_message
from .email import EmailAddress, send_email
from . import get_reminder


def main() -> None:
    arguments = parse_arguments()
    setup_logging(arguments.verbose)
    logger = logging.getLogger(__name__)

    message = get_reminder()

    if arguments.command == "send-gotify":
        send_over_gotify(arguments, message)
    elif arguments.command == "send-gotify":
        send_over_email(arguments, message)
    else:
        print(message)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sends reminders for tasks from Taskwarrior",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="count",
        help="increase output",
    )
    parser.add_argument(
        "--ca-cert",
        type=str,
        help="custom certification authority certificate",
    )

    subparsers = parser.add_subparsers(
        help="Commands",
        dest="command",
        # required=True,  # Only available from Python 3.7 onward
    )
    send_gotify_parser = subparsers.add_parser(
        "send-gotify",
        help="sends notifications over Gotify",
        epilog="If Gotify token is missing, it is taken from environment variable GOTIFY_TOKEN",
    )
    send_email_parser = subparsers.add_parser(
        "send-email",
        help="sends notifications over email",
        epilog="SMTP password is read from environment variable SMTP_PASSWORD",
    )

    send_gotify_parser.add_argument(
        "--gotify-host",
        type=str,
        required=True,
        help="Gotify host",
    )
    send_gotify_parser.add_argument(
        "--gotify-token",
        type=str,
        help="Gotify token",
    )

    send_email_parser.add_argument(
        "--smtp-hostname",
        type=str,
        required=True,
        help="SMTP hostname",
    )
    send_email_parser.add_argument(
        "--smtp-username",
        type=str,
        required=True,
        help="SMTP username",
    )
    send_email_parser.add_argument(
        "--email-sender",
        type=str,
        required=True,
        help="email sender address",
    )
    send_email_parser.add_argument(
        "--email-recipient",
        type=str,
        required=True,
        help="email recipient address",
    )

    arguments = parser.parse_args()
    return arguments


def setup_logging(verbose: typing.Optional[int]) -> None:
    if verbose is None or verbose <= 0:
        level = logging.WARN
    elif verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logging.basicConfig(
        format="%(levelname)s:%(message)s",
        level=level,
    )


def send_over_gotify(arguments: argparse.Namespace, message: typing.Text) -> None:
    logger = logging.getLogger(__name__)

    if arguments.gotify_token is None:
        logger.debug("Taking Gotify token from environment variable GOTIFY_TOKEN")
        token = os.environ["GOTIFY_TOKEN"]
        logger.debug("Removing Gotify token from environment")
        del os.environ["GOTIFY_TOKEN"]
    else:
        token = arguments.gotify_token

    send_gotify_message(
        arguments.gotify_host,
        token,
        arguments.ca_cert,
        message,
    )


def send_over_email(arguments: argparse.Namespace, message: typing.Text) -> None:
    logger = logging.getLogger(__name__)

    password = os.environ["SMTP_PASSWORD"]
    logger.debug("Removing password from environment")
    del os.environ["SMTP_PASSWORD"]

    sender = EmailAddress("", arguments.email_sender)
    recipient = EmailAddress("", arguments.email_recipient)
    subject = "Task reminder"
    hostname = arguments.smpt_hostname
    username = arguments.smpt_username

    send_email(sender, recipient, subject, message, hostname, username, password)


if __name__ == "__main__":
    main()
