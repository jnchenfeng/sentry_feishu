# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_feishu
from .forms import FeiShuOptionsForm

FeiShuTalk_API = "https://open.feishu.cn/open-apis/bot/v2/hook/{token}"


class FeiShuPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to FeiShu.
    """
    author = 'feng.chen'
    author_url = 'https://github.com/jnchenfeng/sentry_feishu'
    version = sentry_feishu.VERSION
    description = 'Send error counts to FeiShu.'
    resource_links = [
        ('Source', 'https://github.com/jnchenfeng/sentry_feishu'),
        ('Bug Tracker', 'https://github.com/jnchenfeng/sentry_feishu/issues'),
        ('README', 'https://github.com/jnchenfeng/sentry_feishu/blob/master/README.md'),
    ]

    slug = 'FeiShu'
    title = 'FeiShu'
    conf_key = slug
    conf_title = title
    project_conf_form = FeiShuOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option('access_token', group.project)
        send_url = FeiShuTalk_API.format(token=access_token)
        project = event.group.project
        title = u"New alert from {}".format(project.slug)

        data = {"title": title, "msg_type": "text",
                "content": {"text": "#### {title} \n > {message} [href]({url})".format(
                    title=title,
                    message=event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
                )}}
        requests.post(
            send_url,
            json=data
        )
