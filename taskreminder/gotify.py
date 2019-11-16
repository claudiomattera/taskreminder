#!/usr/bin/env python3

# Copyright Claudio Mattera 2019.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT


import logging
import typing

import requests


def send_message(
            host: typing.Text,
            token: typing.Text,
            ca_cert: typing.Text,
            message: typing.Text,
        ) -> None:
    logger = logging.getLogger(__name__)

    payload = {
        "extras": {
            "client::display": {
                "contentType": "text/markdown"
            }
        },
        "message": message,
        # "priority": 2,
        "title": "Daily tasks reminder"
    }

    url = "{}/message?token={}".format(host, token)

    logger.info("Sending message through Gotify host %s", host)

    response = requests.post(
        url,
        json=payload,
        verify=ca_cert,
    )
