#!/usr/bin/env python3

# Copyright Claudio Mattera 2019.
# Distributed under the MIT License.
# See accompanying file License.txt, or online at
# https://opensource.org/licenses/MIT


from collections import namedtuple
import smtplib
import typing

from email.message import EmailMessage, Message
from email.headerregistry import Address
from email.utils import make_msgid
from email.mime.base import MIMEBase

import markdown

import gnupg


EmailAddress = namedtuple("EmailAddress", "name address")


def send_email(
            sender: EmailAddress,
            recipient: EmailAddress,
            subject: typing.Text,
            text: typing.Text,
            hostname: typing.Text,
            username: typing.Text,
            password: typing.Text,
        ) -> None:
    message = prepare_message(sender, recipient, subject, text)
    send_message(message, hostname, username, password)


def encrypt_text(
            identity: typing.Text,
            text: typing.Text,
        ) -> typing.Text:
    gpg = gnupg.GPG()
    encrypted_data = gpg.encrypt(text, identity)
    encrypted_str = str(encrypted_data)
    if not encrypted_data.ok:
        raise RuntimeError("Could not encrypt text for {}".format(identity))
    return encrypted_str


def prepare_message(
            sender_: EmailAddress,
            recipient_: EmailAddress,
            subject: typing.Text,
            text: typing.Text,
        ) -> MIMEBase:

    sender = Address(sender_.name, addr_spec=sender_.address)
    recipient = Address(recipient_.name, addr_spec=recipient_.address)

    html = markdown.markdown(text)

    plaintext_message = EmailMessage()
    plaintext_message["Subject"] = subject
    plaintext_message["From"] = sender
    plaintext_message["To"] = (recipient,)
    plaintext_message.set_content(text)

    plaintext_message.add_alternative(html, subtype="html")

    encrypted_text = encrypt_text(recipient.addr_spec, plaintext_message.as_string())

    encrypted_message = MIMEBase(_maintype="multipart", _subtype="encrypted", protocol="application/pgp-encrypted")
    encrypted_message["Subject"] = subject
    encrypted_message["From"] = str(sender)
    encrypted_message["To"] = str(recipient)

    encrypted_message_part1 = Message()
    encrypted_message_part1.add_header(_name="Content-Type", _value="application/pgp-encrypted")
    encrypted_message_part1.add_header(_name="Content-Description", _value="PGP/MIME version identification")
    encrypted_message_part1.set_payload("Version: 1" + "\n")

    encrypted_message_part2 = Message()
    encrypted_message_part2.add_header(_name="Content-Type", _value="application/octet-stream", name="encrypted.asc")
    encrypted_message_part2.add_header(_name="Content-Description", _value="OpenPGP encrypted message")
    encrypted_message_part2.add_header(_name="Content-Disposition", _value="inline", filename="encrypted.asc")
    encrypted_message_part2.set_payload(encrypted_text)

    encrypted_message.attach(encrypted_message_part1)
    encrypted_message.attach(encrypted_message_part2)

    return encrypted_message


def send_message(
            message: MIMEBase,
            hostname: typing.Text,
            username: typing.Text,
            password: typing.Text,
        ) -> None:
    with smtplib.SMTP_SSL(hostname) as server:
        server.login(username, password)
        server.send_message(message)
