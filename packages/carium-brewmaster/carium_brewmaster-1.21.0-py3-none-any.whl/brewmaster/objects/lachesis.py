"""
#
# Lachesis models
#
# Copyright(c) 2024-, Carium, Inc. All rights reserved.
#
"""

from brewmaster.objects.base import ApiObject


class SeriesMetaData(ApiObject):
    base_path = "/lachesis/v1/metadata"


class SourceSummary(ApiObject):
    base_path = "/lachesis/v2/source-summaries"
