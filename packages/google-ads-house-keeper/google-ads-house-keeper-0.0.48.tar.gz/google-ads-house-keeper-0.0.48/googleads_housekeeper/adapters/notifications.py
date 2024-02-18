# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from dataclasses import dataclass
import abc

import os
from typing import Any, Dict, Optional, Union
from gaarf.report import GaarfReport
from google.appengine.api import mail


@dataclass
class MessagePayload:
    task_name: str
    placements_excluded_sample: GaarfReport
    total_placement_excluded: int
    recipient: str


class BaseNotifications(abc.ABC):

    @abc.abstractmethod
    def send(self, payload: MessagePayload) -> None:
        ...


class GoogleCloudAppEngineEmailNotifications(BaseNotifications):

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    def send(self, payload: MessagePayload, **kwargs: str):
        if task_name := payload.task_name:
            task_prefix = f"_{task_name}"
        else:
            task_prefix = ""
        sender = f"exclusions{task_prefix}@{self.project_id}.appspotmail.com"
        if placements_excluded := payload.placements_excluded_sample:
            subject = f"{payload.total_placement_excluded} placements were excluded"
            body = "\n".join([p.name for p in placements_excluded["name"].to_list()])
        else:
            subject = "No placements were excluded"
            body = ""
        recipient = payload.recipient.split(",")
        message = mail.EmailMessage(sender=sender,
                                    to=recipient,
                                    subject=subject,
                                    body=body)
        message.send()


class SlackNotifications(BaseNotifications):

    def __init__(self, bot_token: str, channel: str) -> None:
        from slack import WebClient
        self.client = WebClient(token=bot_token)
        self.channel = channel

    def send(self, payload: MessagePayload, **kwargs: str) -> None:

        file = payload.placements_excluded_sample["name"].to_pandas().to_csv(index=False,
                                                              sep="\t")
        task_name = payload.task_name
        self.client.files_upload(
            channels=self.channel,
            initial_comment=
            f"{task_name}: {payload.total_placement_excluded} placements_excluded",
            filename=f"{task_name}.tsv" if task_name else "cpr.tsv",
            content=file)


class ConsoleNotifications(BaseNotifications):

    def send(self, payload: MessagePayload, **kwargs):
        print(payload)


class NullNofication(BaseNotifications):

    def __init__(self, notification_type: str, **kwargs):
        raise ValueError(f"{notification_type} is unknown writer type!")


class NotificationFactory:
    types: Dict[str, Dict[str, Union[BaseNotifications, Dict[str, Any]]]] = {}

    def __init__(self):
        self.load_types()

    def load_types(self):
        self.types["email"] = {
            "type": GoogleCloudAppEngineEmailNotifications,
            "args": {}
        }
        self.types["slack"] = {
            "type": SlackNotifications,
            "args": {
                "bot_token": os.environ.get("CPR_SLACK_BOT_TOKEN"),
                "channel": os.environ.get("CPR_SLACK_CHANNEL")
            }
        }
        self.types["console"] = {"type": ConsoleNotifications, "args": {}}

    def create_nofication_service(self, notification_type: str):
        if notification_type in self.types:
            if args := self.types[notification_type].get("args"):
                return self.types[notification_type].get("type")(**args)
            else:
                return self.types[notification_type].get("type")()
        else:
            return NullNotifications(notification_type)
