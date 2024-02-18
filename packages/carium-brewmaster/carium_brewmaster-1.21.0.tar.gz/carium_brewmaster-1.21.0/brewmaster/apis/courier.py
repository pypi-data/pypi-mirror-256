"""
#
# CareDB API
#
# Copyright(c) 2020-, Carium, Inc. All rights reserved.
#
"""

from typing import Optional

from requests.models import Response

from brewmaster.apis.base import Endpoint


class Channel(Endpoint):
    def create(
        self,
        group_id: str,
        individual_id: Optional[str],
        label: str,
        name: str,
        subscription_type: str = "single",
        individual_ids: Optional[list] = None,
    ) -> Optional[str]:
        """Create a new messaging channel to specific individual

        Args:
            group_id: care-team group-id
            individual_id: target participant's individual-id, or None
            label: channel label
            name: channel name
            subscription_type: subscription type, default 'single'
            individual_ids: target list of individual-ids
        Returns:
            If the channel already exists, it will return the existing channel-id.
        """
        if not individual_ids:
            individual_ids = []

        if individual_id:
            individual_ids.append(individual_id)

        attrs = {
            "floating": True,
            "individual-group-id": group_id,
            "label": label,
            "name": name,
            "organization-id": str(self.organization_id),
            "subscription-type": subscription_type,
            "individual-ids": individual_ids,
        }

        result = self.api.post(
            "courier/v1/messaging-channels/", json={"data": {"type": "messaging-channels", "attributes": attrs}}
        )
        if result.ok:
            channel_id = result.json()["data"]["id"]
        else:
            # If channel exists then use it.
            error = result.json()["errors"][0]
            if error.get("code", "") != "DuplicateChannel":
                return None
            channel_id = error["meta"]["id"]

        return channel_id


class Message(Endpoint):
    def send(
        self,
        channel_id: str,
        sender_id: str,
        message: str,
    ) -> Response:
        """Send a message to specific individual

        Args:
            channel_id: message channel id
            sender_id: individual-id of the sender
            message: message content
        Returns:
            HTTP API response
        """
        params = {
            "data": {
                "type": "messaging-messages",
                "attributes": {
                    "channel-id": channel_id,
                    "individual-id": sender_id,
                    "message": message,
                },
            }
        }
        return self.api.post("courier/v1/messaging-messages/", json=params)


class Notification(Endpoint):
    def send(
        self,
        individual_id: str,
        title: str,
        message: str,
    ) -> Response:
        """Send a notification to specific individual

        Args:
            individual_id: individual-id of the sender
            title: notification title
            message: notification message
        Returns:
            HTTP API response
        """

        payload = {
            "organization-id": self.organization_id,
            "template-id": "courier.account.multicast.NotificationTemplate",
            "template-data": {"title": title, "message": message},
        }
        return self.api.post(f"courier/v1/individuals/{individual_id}/multicast/", json=payload)
