"""
#
# Barrel of APIs
#
# Copyright(c) 2020-, Carium, Inc. All rights reserved.
#
"""

import logging
import sys
from logging import StreamHandler
from typing import cast, List, Optional

from brewmaster.adapter import ApiAdapter
from cariutils.shortcuts import import_class
from cariutils.typing import JsonDict


logger = logging.getLogger(__name__)


class Folder:
    def __init__(self, name: str, hierarchy: dict, **kwargs):
        self.name = name
        self.hierarchy = hierarchy
        self.kwargs = kwargs
        self._endpoints = {}
        self._folders = {}

    def __getattr__(self, name: str):
        value = self.hierarchy.get(name)
        if value is None:
            raise AttributeError(f"Folder {self.name} object has no attribute {name}")

        if isinstance(value, dict):
            # For dictionary, this is an indirect access. Returns the folder object instead

            if name not in self._folders:
                # Cache to avoid regenerating folders
                self._folders[name] = Folder(".".join((self.name, name)), value, **self.kwargs)

            return self._folders[name]

        # Otherwise, this is the endpoint class
        if name not in self._endpoints:
            self._endpoints[name] = value(self.kwargs["barrel"])
        return self._endpoints[name]


class JsonApi:
    """JSON Api wrapper. Simplify JSON-API-based API call."""

    def __init__(self, api: ApiAdapter):
        self.api = api
        self.api.js = self  # pyre-fixme[16]

    @classmethod
    def _tokenize_path(cls, path: str) -> List[str]:
        return [each for each in path.split("/") if each != ""]

    def patch(self, path: str, attributes: JsonDict) -> None:
        tokens = self._tokenize_path(path)
        self.api.patch(path, json={"data": {"attributes": attributes, "id": tokens[-1], "type": tokens[-2]}})

    def post(self, path: str, attributes: JsonDict) -> Optional[str]:
        resp = self.api.post(path, json={"data": {"attributes": attributes, "type": self._tokenize_path(path)[-1]}})
        return resp.json()["data"]["id"] if resp.ok else None


class Barrel(Folder):
    """
    Collection of APIs
    Each object is loaded lazily to reduce the initialization time
    """

    commands = {
        "color.scheme": "brewmaster.apis.themes.ColorScheme",
        "caredb.article": "brewmaster.apis.caredb.Article",
        "caredb.todo": "brewmaster.apis.caredb.Todo",
        "courier.channel": "brewmaster.apis.courier.Channel",
        "courier.message": "brewmaster.apis.courier.Message",
        "courier.notification": "brewmaster.apis.courier.Notification",
        "dateutils": "brewmaster.apis.utils.DateUtils",
        "overlord.interview": "brewmaster.apis.overlord.Interview",
        "overlord.interview_profile": "brewmaster.apis.overlord.InterviewProfile",
        "showboat.banner": "brewmaster.apis.showboat.Banner",
        "utils": "brewmaster.apis.utils.Utils",
    }
    _hierarchy = {}

    @classmethod
    def get_hierarchy(cls) -> dict:
        """Build hierarchy of commands"""
        if len(cls._hierarchy) == 0:
            for k, api in cls.commands.items():
                cwd = cls._hierarchy
                tokens = k.split(".")
                for token in tokens[:-1]:
                    if token not in cwd:
                        cwd[token] = {}
                    cwd = cwd[token]

                cwd[tokens[-1]] = import_class(api)

        return cast(dict, cls._hierarchy)

    @classmethod
    def reset(cls) -> None:
        cls._hierarchy = {}

    def __init__(self, organization_id: str, adapter: ApiAdapter):
        super().__init__("", self.get_hierarchy(), barrel=self)

        self.organization_id = organization_id
        self.api = adapter
        self.js_api = JsonApi(self.api)

    @classmethod
    def _get_stream_handler(cls) -> Optional[StreamHandler]:
        global logger

        current = logger
        while current:
            for handler in current.handlers:
                return handler
            current = current.parent

        return None

    def get_logger(self, level: int, new_line: bool = False):
        global logger

        handler = self._get_stream_handler()
        if handler is None:
            handler = StreamHandler(stream=sys.stdout)
            logger.addHandler(handler)

        handler.setLevel(logging.DEBUG)
        new_line_s = "\n" if new_line else ""
        handler.setFormatter(logging.Formatter(f"%(asctime)s %(levelname)s %(message)s{new_line_s}"))
        logger.setLevel(level)
        return logger
