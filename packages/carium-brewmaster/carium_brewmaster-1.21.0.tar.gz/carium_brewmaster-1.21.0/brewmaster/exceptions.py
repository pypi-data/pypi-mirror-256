"""
#
# Collection of brewmaster exceptions
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

from typing import Optional

from cariutils.typing import JsonDict


class BrewmasterError(Exception):
    pass


class SettingError(BrewmasterError):
    pass


class WaitError(BrewmasterError):
    pass


class ApiError(BrewmasterError):
    def __init__(self, error: Optional[JsonDict] = None, message: str = "", path: str = "", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

        self._msg = message
        self.error = error or {}
        self.path = path

    def __str__(self):
        return self._msg or str(self.error)


class CallError(ApiError):
    pass


class DeleteError(ApiError):
    pass


class GetError(ApiError):
    pass


class GetMultipleError(ApiError):
    pass


class PatchError(ApiError):
    pass


class PostError(ApiError):
    pass


class ResourceNotFound(ApiError):
    pass
