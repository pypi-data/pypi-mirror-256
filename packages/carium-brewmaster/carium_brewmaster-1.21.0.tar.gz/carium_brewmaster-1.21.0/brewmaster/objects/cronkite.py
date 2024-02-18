"""
#
# Cronkite models
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

from io import BytesIO
from typing import Optional

import requests

from brewmaster.objects.base import ApiObject
from cariutils.typing import JsonDict


class CustomJobDashboard(ApiObject):
    base_path = "/cronkite/v1/customjob-dashboards"


class CustomJobReport(ApiObject):
    base_path = "/cronkite/v1/customjob-reports"


class CustomJobRepository(ApiObject):
    base_path = "/cronkite/v1/customjob-repositories"


class CustomJobRun(ApiObject):
    base_path = "/cronkite/v1/customjob-runs"

    @classmethod
    def get_output(cls, run_id: str, attributes: Optional[JsonDict] = None) -> BytesIO:
        return BytesIO(
            requests.get(cls(run_id).call("get-output", attributes=attributes, http_method="get")["url"]).content
        )


class CustomJobSpec(ApiObject):
    base_path = "/cronkite/v1/customjob-specs"


class CustomJobTable(ApiObject):
    base_path = "/cronkite/v1/customjob-tables"


class CustomJobWidget(ApiObject):
    base_path = "/cronkite/v1/customjob-widgets"


class CustomJobWidgetLog(ApiObject):
    base_path = "/cronkite/v1/customjob-widgetlogs"


class CustomJobWidgetOutput(ApiObject):
    base_path = "/cronkite/v1/customjob-widget-outputs"


class CustomJobWidgetSpec(ApiObject):
    base_path = "/cronkite/v1/customjob-widgetspecs"


class DbmCluster(ApiObject):
    base_path = "/cronkite/v1/dbm-clusters"


class DbmDatabase(ApiObject):
    base_path = "/cronkite/v1/dbm-databases"


class DbtProject(ApiObject):
    base_path = "/cronkite/v1/dbt-projects"


class DbtRun(ApiObject):
    base_path = "/cronkite/v1/dbt-runs"
