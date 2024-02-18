"""
#
# Overlord API
#
# Copyright(c) 2021-, Carium, Inc. All rights reserved.
#
"""
from typing import List, Optional

from requests.models import Response

from brewmaster.apis.base import Endpoint


class InterviewProfile(Endpoint):
    def get(self, profile_id: str) -> Response:
        """Get interview profile details

        Args:
            profile_id: interview profile id
        Returns:
            HTTP API response
        """
        return self.api.get(f"overlord/v1/interview-profiles/{profile_id}/")


class Interview(Endpoint):
    def bulk_send(
        self,
        profile: str,
        individual_ids: Optional[List[str]] = None,
        individual_group_ids: Optional[List[str]] = None,
        auto_start: bool = True,
    ) -> Response:
        """Bulk sends a survey to to a list of individual-ids, or individual-group-ids

        Args:
            profile: interview profile-id or profile-name
            individual_ids: list of individual-ids
            individual_group_ids: list of individual-group-ids
            auto_start: auto-start option for interview, default True
        Returns:
            HTTP API response
        """
        if self.barrel.utils.is_valid_uuid(profile):
            r = self.barrel.overlord.interview_profile.get(profile)
            if not r.ok:
                raise ValueError(f"Invalid profile id: {profile}")

            profile = r.json()["data"]["attributes"]["name"]

        if not individual_ids:
            individual_ids = []
        if not individual_group_ids:
            individual_group_ids = []

        payload = {
            "individual-ids": individual_ids,
            "individual-group-ids": individual_group_ids,
            "organization-id": self.organization_id,
            "profile-name": profile,
            "auto-start": auto_start,
        }

        return self.api.post("overlord/v1/bulk-interviews/", json=payload)

    def send(self, individual_id: str, profile: str, notify_user: bool = True) -> Response:
        """Sends a survey to an individual

        Args:
            individual_id: target individual-id
            profile: interview profile-id or profile-name
            notify_user: send notification to user, defaults to True
        Returns:
            HTTP API response
        """
        if self.barrel.utils.is_valid_uuid(profile):
            r = self.barrel.overlord.interview_profile.get(profile)
            if not r.ok:
                raise ValueError(f"Invalid profile id: {profile}")

            profile = r.json()["data"]["attributes"]["name"]

        payload = {
            "data": {
                "type": "interviews",
                "attributes": {
                    "auto-start": True,
                    "individual-id": individual_id,
                    "notify-user": notify_user,
                    "organization-id": self.organization_id,
                    "profile-name": profile,
                },
            }
        }

        return self.api.post("overlord/v1/interviews/", json=payload)
