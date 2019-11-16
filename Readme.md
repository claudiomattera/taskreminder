Task Reminder
===========

An application that sends reminders from Taskwarrior over email or [Gotify].

https://gitlab.com/claudiomattera/taskreminder/

[Gotify]: https://gotify.net/

Copyright Claudio Mattera 2019

You are free to copy, modify, and distribute Task Reminder with attribution under the terms of the MIT license. See the `License.txt` file for details.


Installation
----

The application is available as three different packages:

-   Debian package, usable on Debian/Ubuntu and derivatives (anything that uses `apt`/`apt-get`).
    Install it with the following command (possibly prepended with `sudo`).

        dpkg -i /path/to/python3-taskreminder_1.0.0-1_all.deb

-   Python wheel package, usable on Windows and almost every system with a Python 3 distribution.
    Install it with the following command (possibly prepended with `sudo`, or passing the `--user` option).

        pip3 install /path/to/taskreminder-1.0.0-py3-none-any.whl

-   Tarball source package.
    It can be used by maintainers to generate a custom package.


Usage
----

This application can be used from command line.
Different commands are available.

~~~~text
usage: task-reminder [-h] [-v] [--ca-cert CA_CERT] {send-gotify,send-email} ...

Sends reminders for tasks from Taskwarrior

positional arguments:
  {send-gotify,send-email}
                        Commands
    send-gotify         sends notifications over Gotify
    send-email          sends notifications over email

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output
  --ca-cert CA_CERT     custom certification authority certificate
~~~~


Sending a reminder through a [Gotify] notification

~~~~text
usage: task-reminder send-gotify [-h] --gotify-host GOTIFY_HOST
                                 [--gotify-token GOTIFY_TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  --gotify-host GOTIFY_HOST
                        Gotify host
  --gotify-token GOTIFY_TOKEN
                        Gotify token

If Gotify token is missing, it is taken from environment variable GOTIFY_TOKEN
~~~~


Sending a reminder through an email.

~~~~text
usage: task-reminder send-email [-h] --smtp-hostname SMTP_HOSTNAME
                                --smtp-username SMTP_USERNAME --email-sender
                                EMAIL_SENDER --email-recipient EMAIL_RECIPIENT

optional arguments:
  -h, --help            show this help message and exit
  --smtp-hostname SMTP_HOSTNAME
                        SMTP hostname
  --smtp-username SMTP_USERNAME
                        SMTP username
  --email-sender EMAIL_SENDER
                        email sender address
  --email-recipient EMAIL_RECIPIENT
                        email recipient address

SMTP password is read from environment variable SMTP_PASSWORD
~~~~
