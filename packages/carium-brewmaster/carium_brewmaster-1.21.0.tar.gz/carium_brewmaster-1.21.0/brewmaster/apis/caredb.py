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
from cariutils.typing import JsonDict


class Article(Endpoint):
    def get_by_name(self, article_name: str) -> Response:
        """Get article details, search by article name

        Args:
            article_name: article name string
        Returns:
            HTTP API response
        """
        params = {"filter[article-name]": article_name, "filter[organization-id]": self.organization_id}

        return self.api.get("caredb/v1/articles/", params=params)

    def assign(
        self,
        article: str,
        individual_id: Optional[str] = None,
        group_id: Optional[str] = None,
        send_notification: Optional[bool] = True,
    ) -> Response:
        """Assign an article to an individual or a group

        Both individual_id and group_id can be specified

        Args:
            article: article-id or article-name
            individual_id: target individual to be assigned
            group_id: target group to be assigned
            send_notification: send with notification
        Returns:
            HTTP API responses, one for individual assignment, and one for group assignment
        """
        params: JsonDict = {"send_notification": send_notification}

        if not self.barrel.utils.is_valid_uuid(article):
            r = self.barrel.caredb.article.get_by_name(article)
            data = r.json()["data"]
            if not data:
                raise ValueError(f"Invalid article name: {article}")

            article = data[0]["id"]

        if individual_id is not None:
            params["individual-id"] = individual_id

        if group_id is not None:
            params["individual-group-id"] = group_id

        result = self.api.post(f"caredb/v1/articles/{article}/assign-content/", json=params)
        return result

    def unassign(
        self,
        article_id: str,
        individual_id: str,
    ) -> Response:
        """Unassign an article from an individual

        Args:
            article_id: article-id or article-name
            individual_id: target individual to be unassigned from
        Returns:
            HTTP API response
        """
        params = {}
        if self.barrel.utils.is_valid_uuid(article_id):
            path = f"caredb/v1/articles/{article_id}/unassign-content/"
        else:
            params["organization-id"] = self.organization_id
            path = f"caredb/v1/article-names/{article_id}/unassign-content/"

        return self.api.post(
            path,
            json={
                **params,
                "individual-id": individual_id,
            },
        )


class Todo(Endpoint):
    def create(
        self,
        text: str,
        notes: str,
        group_id: Optional[str] = None,
        ref_individual_id: Optional[str] = None,
        with_notification: bool = True,
        todo_due: Optional[str] = None,
    ) -> Response:
        """Create a todo-list item

        Args:
            text: todo text
            notes: todo notes
            group_id: group-id in which this todo is assigned to
            ref_individual_id: optional individual-id associated with this todo
            with_notification: if True, will send notification message
            todo_due: optional, sets due date for todo

        Returns:
            HTTP API response
        """
        params = {
            "notes": notes,
            "organization-id": self.organization_id,
            "text": text,
            "with-notification": with_notification,
        }
        if ref_individual_id is not None:
            params["references"] = [{"type": "individual", "id": ref_individual_id}]

        if group_id is not None:
            params["individual-group-id"] = group_id

        if todo_due is not None:
            params["due-time"] = todo_due

        return self.api.post("caredb/v1/todo-entries/", json={"data": {"type": "todo-entries", "attributes": params}})
