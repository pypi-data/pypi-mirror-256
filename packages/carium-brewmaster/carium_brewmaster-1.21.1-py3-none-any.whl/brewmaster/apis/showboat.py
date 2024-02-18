"""
#
# Showboat API
#
# Copyright(c) 2021-, Carium, Inc. All rights reserved.
#
"""
from typing import List, Optional, Union

from requests.models import Response

from brewmaster.apis.base import Endpoint
from cariutils.typing import JsonDict


class Banner(Endpoint):
    def get_by_survey_name(self, individual_id: str, survey_name: str) -> List[JsonDict]:
        """Returns a list of data responses from a search by survey name, for individual_id

        Args:
            individual_id: individual-id
            survey_name: match by survey name

        Returns:
            list of banner JSON structure
        """
        params = {"individual-id": individual_id, "organization-id": str(self.organization_id)}

        result = self.api.get("showboat/v1/banners/", params=params)
        data = result.json()["data"]
        return [
            each
            for each in data
            if each["attributes"]["args"]["name"] == survey_name and each["attributes"]["type"] == "survey"
        ]

    def create_individual_survey(
        self, individual_id: str, messages: Union[str, dict], survey_name: str, banner_name: Optional[str] = None
    ) -> Response:
        """Adds an individual banner for individual_id

        Args:
            individual_id: target individual-id
            messages: banner messages
            survey_name: survey name
            banner_name: banner name, optional
        Returns:
            HTTP API response
        """
        params = {
            "type": "survey",
            "args": {"name": survey_name},
            "name": f"{individual_id}_{survey_name}",
            "organization-id": self.organization_id,
            "individual-id": individual_id,
        }

        if banner_name is not None:
            params["name"] = banner_name

        params["messages"] = {"en_US": messages} if isinstance(messages, str) else messages

        return self.api.post("showboat/v1/banners/", json={"data": {"type": "banners", "attributes": params}})

    def delete_individual_survey(self, individual_id: str, survey_name: str, raised_on_fail: bool = True) -> None:
        """Deletes an individual_id survey banner for survey_name, if banner exists

        Args:
            individual_id: target individual-id
            survey_name: survey name
            raised_on_fail: raises ValueError if banner doesn't exist for individual_id, default True
        Returns:
            None
        """
        banner_data = self.barrel.showboat.banner.get_by_survey_name(individual_id, survey_name)
        if banner_data:
            banner_id = banner_data[0]["id"]
            response = self.api.delete(f"showboat/v1/banners/{banner_id}/")
            if not response.ok:
                raise ValueError(f"Delete banners error: {response.content.decode()}")
        else:
            if raised_on_fail:
                raise ValueError(f"Unknown survey banner for individual: {survey_name}")
