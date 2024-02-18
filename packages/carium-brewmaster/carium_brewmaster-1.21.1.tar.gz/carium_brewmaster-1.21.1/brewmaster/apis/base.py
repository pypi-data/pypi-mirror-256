"""
#
# API base
#
# Copyright(c) 2020-, Carium, Inc. All rights reserved.
#
"""

from brewmaster.barrel import Barrel


class Endpoint:
    def __init__(self, barrel: Barrel):
        self.barrel = barrel
        self.api = barrel.api
        self.organization_id = barrel.organization_id
