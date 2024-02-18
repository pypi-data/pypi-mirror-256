"""
#
# Adapter utilities
#
# Copyright(c) 2020-, Carium, Inc. All rights reserved.
#
"""


class ApiAdapter:
    def delete(self, path, *args, **kwargs):
        raise NotImplementedError()

    def get(self, path, *args, **kwargs):
        raise NotImplementedError()

    def patch(self, path, *args, **kwargs):
        raise NotImplementedError()

    def post(self, path, *args, **kwargs):
        raise NotImplementedError()
