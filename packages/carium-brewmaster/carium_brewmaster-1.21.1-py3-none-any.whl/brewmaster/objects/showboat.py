"""
#
# Showboat models
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

from brewmaster.objects.base import ApiObject


class HomefeedLog(ApiObject):
    base_path = "/showboat/v1/homefeed-logs"
