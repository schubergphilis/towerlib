#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: organization.py
#
# Copyright 2019 Ilija Matoski
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

"""
Main code for notification.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import logging

from .core import Entity, EntityManager

__author__ = '''Ilija Matoski <imatoski@schubergphilis.com>'''
__docformat__ = '''google'''
__date__ = '''2018-01-03'''
__copyright__ = '''Copyright 2019, Ilija Matoski'''
__credits__ = ["Ilija Matoski"]
__license__ = '''MIT'''
__maintainer__ = '''Ilija Matoski'''
__email__ = '''<imatoski@schubergphilis.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''notification'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class NotificationTemplate(Entity):
    """Models the notification template of Ansible Tower/AWX."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def name(self):
        """The name of the notification template.

        Returns:
            string: The name of the notification template

        """
        return self._data.get('name')

    @property
    def description(self):
        """The description of the notification template.

        Returns:
            string: The description of the notification template

        """
        return self._data.get('description')

    @property
    def organization(self):
        """The Organization object that this project is part of.

        Returns:
            Organization: The Organization object that this project is part of

        """
        return self._tower.get_organization_by_id(self._data.get('organization'))

    @property
    def notification_type(self):
        """Notification type for the template.

        Returns:
            string: Notification type for the template

        """
        return self._data.get('notification_type')

    @property
    def notification_configuration(self):
        """Gets the notification configuration.

        Returns:
            dict: The configuration for the notification

        """
        data = self._data.get('notification_configuration')
        notification_types = {
            "email": NotificationEmail,
            "slack": NotificationSlack,
            "twilio": NotificationTwilio,
            "pagerduty": NotificationPagerDuty,
            "grafana": NotificationGrafana,
            "hipchat": NotificationHipChat,
            "webhook": NotificationWebHook,
            "mattermost": NotificationMatterMost,
            "rocketchat": NotificationRocketChat,
            "irc": NotificationIRC,
        }

        class_name = notification_types.get(self.notification_type, None)
        if class_name is None:
            raise ValueError(f'Invalid notification type: "{self.notification_type}".')

        return class_name(data)

    @property
    def recent_notifications(self):
        """The groups configured in Tower/AWX.

        Returns:
            EntityManager: The manager object for groups

        """
        url = self._data.get('related', {}).get('notifications')
        return EntityManager(self._tower,
                             entity_object='Notification',
                             primary_match_field='subject',
                             url=url)


class Notification(Entity):
    """Models the notifications of Ansible Tower/AWX."""

    def __init__(self, tower_instance, data):
        Entity.__init__(self, tower_instance, data)

    @property
    def error(self):
        """The error status for the notification.

        Returns:
            string: The error

        """
        return self._data.get('error')

    @property
    def status(self):
        """The status of the notification.

        Returns:
            string: The status of the application can be pending,successful,failed

        """
        return self._data.get('status')

    @property
    def notifications_sent(self):
        """How many notifications have been sent.

        Returns:
            int: Total notifications sent

        """
        return self._data.get('notifications_sent', 0)

    @property
    def notification_type(self):
        """The notification type for which the notification has been sent.

        Returns:
            string: The notification type

        """
        return self._data.get('notification_type')

    @property
    def subject(self):
        """The subject of the notification.

        Returns:
            string: The subject of the notification

        """
        return self._data.get('subject')

    @property
    def recipients(self):
        """The recipients to whom the notification has been sent.

        Returns:
            []string: List of recipients

        """
        return self._data.get('recipients', [])


class NotificationEmail:
    """Notification type configuration for email."""

    def __init__(self, data):
        self._data = data

    @property
    def host(self):
        """
        Host to where we send the email.

        Returns:
            string: Host to where we send the email

        """
        return self._data.get('email')

    @property
    def port(self):
        """
        The port to where to send the email.

        Returns:
            int: Port

        """
        return self._data.get('port')

    @property
    def username(self):
        """
        The username to use.

        Returns:
            string: Username

        """
        return self._data.get('username')

    @property
    def password(self):
        """
        The password to use.

        Returns:
            string: Password

        """
        return self._data.get('password')

    @property
    def use_ssl(self):
        """
        Use SSL for the connection?

        Returns:
            bool: Use SSL for the connection

        """
        return self._data.get('use_ssl')

    @property
    def use_tls(self):
        """
        Use TLS for the connection?

        Returns:
            bool: Use TLS for the connection

        """
        return self._data.get('use_tls')

    @property
    def sender(self):
        """
        Sender email.

        Returns:
            string: Sender Email

        """
        return self._data.get('sender')

    @property
    def recipients(self):
        """
        Recipient list.

        Returns:
            []string: Recipient list

        """
        return self._data.get('recipients')

    @property
    def timeout(self):
        """
        Timeout.

        Returns:
            int: The timeout (defaults to 30)

        """
        return self._data.get('timeout', 30)


class NotificationTwilio:
    """Notification type configuration for twilio."""

    def __init__(self, data):
        self._data = data

    @property
    def account_sid(self):
        """
        The account sid.

        Returns:
            string: Account SID

        """
        return self._data.get('account_sid')

    @property
    def account_token(self):
        """
        Account Token.

        Returns:
            string: Account Token

        """
        return self._data.get('account_token')

    @property
    def from_number(self):
        """
        Source phone number.

        Returns:
            string: The source phone number

        """
        return self._data.get('from_number')

    @property
    def to_numbers(self):
        """
        Destination SMS numbers.

        Returns:
            []string: Destination SMS numbers

        """
        return self._data.get('to_numbers', [])


class NotificationPagerDuty:
    """Notification type configuration for pagerduty."""

    def __init__(self, data):
        self._data = data

    @property
    def subdomain(self):
        """
        Gets the pagerduty subdomain.

        Returns:
            string: Pagerduty subdomain

        """
        return self._data.get('subdomain')

    @property
    def token(self):
        """
        The token for the PagerDuty.

        Returns:
            string: The token for PagerDuty

        """
        return self._data.get('token')

    @property
    def service_key(self):
        """
        The service key for the PagerDuty.

        Returns:
            string: The service key for PagerDuty

        """
        return self._data.get('service_key')

    @property
    def client_name(self):
        """
        The client name for the PagerDuty.

        Returns:
            string: The client name for PagerDuty

        """
        return self._data.get('client_name')


class NotificationGrafana:
    """Notification type configuration for WebHook."""

    def __init__(self, data):
        self._data = data

    @property
    def grafana_url(self):
        """
        The URL to call for the notification.

        Returns:
            string: The URL to call for a notification

        """
        return self._data.get('grafana_url')

    @property
    def grafana_key(self):
        """
        Get the grafana key.

        Returns:
            string: The grafana key

        """
        return self._data.get('grafana_key')


class NotificationHipChat:
    """Notification type configuration for HipChat."""

    def __init__(self, data):
        self._data = data

    @property
    def token(self):
        """
        The token.

        Returns:
            string: token

        """
        return self._data.get('token')

    @property
    def rooms(self):
        """
        Destination Rooms.

        Returns:
            []string: Destination Rooms

        """
        return self._data.get('rooms', [])

    @property
    def color(self):
        """
        Notification color.

        Returns:
            string: Notification color

        """
        return self._data.get('color')

    @property
    def api_url(self):
        """
        API Url (e.g: https://mycompany.hipchat.com).

        Returns:
            string: API Url

        """
        return self._data.get('api_url')

    @property
    def notify(self):
        """
        Notify room.

        Returns:
            bool: Notify room?

        """
        return self._data.get('notify')

    @property
    def message_from(self):
        """
        Label to be shown with notification.

        Returns:
            string: Label to be shown with notification

        """
        return self._data.get('message_from')


class NotificationWebHook:
    """Notification type configuration for WebHook."""

    def __init__(self, data):
        self._data = data

    @property
    def url(self):
        """
        The URL to call for the notification.

        Returns:
            string: The URL to call for a notification

        """
        return self._data.get('url')

    @property
    def disable_ssl_verification(self):
        """
        Disable SSL verification.

        Returns:
            bool: Do we verify SSL?

        """
        return self._data.get('disable_ssl_verification')


class NotificationMatterMost:
    """Notification type configuration for MatterMost."""

    def __init__(self, data):
        self._data = data

    @property
    def mattermost_url(self):
        """
        The URL to call for the notification.

        Returns:
            string: The URL to call for a notification

        """
        return self._data.get('mattermost_url')

    @property
    def mattermost_no_verify_ssl(self):
        """
        Do not verify SSL on MatterMost.

        Returns:
            bool: Do we verify SSL?

        """
        return self._data.get('mattermost_no_verify_ssl')


class NotificationIRC:
    """Notification type configuration for IRC."""

    def __init__(self, data):
        self._data = data

    @property
    def server(self):
        """
        IRC Server Address.

        Returns:
            string: The irc server address

        """
        return self._data.get('server')

    @property
    def port(self):
        """
        The IRC Server Port.

        Returns:
            int: IRC Server Port

        """
        return self._data.get('port')

    @property
    def nickname(self):
        """
        IRC Nick.

        Returns:
            string: The irc nick

        """
        return self._data.get('nickname')

    @property
    def password(self):
        """
        The IRC Server Password.

        Returns:
            string: IRC Server Password

        """
        return self._data.get('password')

    @property
    def use_ssl(self):
        """
        Use SSL for the connection?

        Returns:
            bool: Use SSL for the connection

        """
        return self._data.get('use_ssl')

    @property
    def targets(self):
        """
        Destination channels or users.

        Returns:
            []string: Destination channels or users

        """
        return self._data.get('targets', [])


class NotificationRocketChat:
    """Notification type configuration for Rocket.Chat."""

    def __init__(self, data):
        self._data = data

    @property
    def rocketchat_url(self):
        """
        The URL to call for the notification.

        Returns:
            string: The URL to call for a notification

        """
        return self._data.get('rocketchat_url')

    @property
    def rocketchat_no_verify_ssl(self):
        """
        Do not verify SSL on Rocket.Chat.

        Returns:
            bool: Do we verify SSL?

        """
        return self._data.get('rocketchat_no_verify_ssl')


class NotificationSlack:
    """Notification type configuration for slack."""

    def __init__(self, data):
        self._data = data

    @property
    def channels(self):
        """
        The channels to where we send the notification to.

        Returns:
            []string: List of channels to notify

        """
        return self._data.get('channels', [])

    @property
    def token(self):
        """
        Token required to make an API call.

        Returns:
            string: The token for the API call

        """
        return self._data.get('token')
