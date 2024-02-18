"""
#
# Base class for brewmaster objects
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

import time
from typing import Callable, List, Optional, Protocol, Type, TypeVar, Union

import jq  # pyre-fixme[21]

from brewmaster.exceptions import (
    CallError,
    DeleteError,
    GetError,
    GetMultipleError,
    PatchError,
    PostError,
    ResourceNotFound,
    SettingError,
    WaitError,
)
from cariutils.typing import JsonDict


class ApiProto(Protocol):
    def delete(self, path, *args, **kwargs):
        """delete() operation"""

    def get(self, path, *args, **kwargs):
        """get() operation"""

    def patch(self, path: str, *args, **kwargs):
        """patch() operation"""

    def post(self, path: str, *args, **kwargs):
        """post() operation"""


class Manager:
    _instance = None

    @classmethod
    def instance(cls) -> "Manager":
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self.api = None

    def set_api(self, api: Optional[ApiProto]) -> "Manager":
        self.api = api
        return self


class ContextManager:
    def __init__(self, api: ApiProto):
        self._api = api

    def __enter__(self):
        self._old_api = Manager.instance().api
        Manager.instance().set_api(self._api)

    def __exit__(self, exc_type, exc_val, exc_tb):
        Manager.instance().set_api(self._old_api)


T = TypeVar("T", bound="ApiObject")


class ApiList(List[T]):
    def __init__(self, *args, **kwargs):
        self.meta = kwargs.pop("meta", {})
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if isinstance(key, int):
            # Individual index
            return super().__getitem__(key)

        # Otherwise, returns the slice
        return ApiList(super().__getitem__(key))

    def reversed(self) -> "ApiList[T]":
        return ApiList(super().__reversed__())

    def filter_jq(self, filter: str) -> "ApiList[T]":
        return ApiList(
            (
                ApiObject.from_response(each)
                for each in jq.compile(f".[] | select({filter})").input([each.as_json_dict() for each in self])
            ),
            meta=self.meta,
        )

    def order_by(self, key: Callable) -> "ApiList[T]":
        return ApiList(sorted(self, key=key), meta=self.meta)


class ApiObject:
    manager = Manager.instance()

    DEFAULT_RETRY_COUNT = 60
    DEFAULT_RETRY_SLEEP = 1
    DEFAULT_LIST_COUNT = 100
    DEFAULT_LIST_PAGE_SIZE = 100

    # Configurable properties
    abstract = True
    base_path = ""
    resource = ""

    @classmethod
    def _get_manager_api(cls) -> ApiProto:
        if cls.manager.api is None:
            raise SettingError("Please initialize Manager.api")

        return cls.manager.api

    @classmethod
    def _get_path(cls, id: Optional[str] = None, method: Optional[str] = None) -> str:
        path = f"{cls.base_path}/"
        if id is not None:
            path = f"{path}{id}/"
        if method is not None:
            path = f"{path}{method}/"

        return path

    @classmethod
    def _get_resource_name(cls) -> str:
        return cls.resource or cls.base_path.rsplit("/", 1)[-1]

    @classmethod
    def create(cls: Type[T], attributes: JsonDict, api: Optional[ApiProto] = None) -> "T":
        path = cls._get_path()
        resp = (api or cls._get_manager_api()).post(
            path,
            json={"data": {"attributes": attributes, "type": cls._get_resource_name()}},
        )
        result = resp.json()
        if not resp.ok:
            raise PostError(error=result, path=path)

        return cls.from_response(result["data"], api=api)

    @classmethod
    def from_id(cls: Type[T], id: str, params: Optional[JsonDict] = None, api: Optional[ApiProto] = None) -> "T":
        path = cls._get_path(id=id)
        resp = (api or cls._get_manager_api()).get(path, params=(params or {}))
        result = resp.json()
        if not resp.ok:
            raise ResourceNotFound(error=result, path=path)

        return cls.from_response(result["data"], api=api)

    @classmethod
    def from_response(cls: Type[T], response: JsonDict, api: Optional[ApiProto] = None) -> "T":
        return cls(id=response["id"], attributes=response["attributes"], api=api)

    @classmethod
    def get(cls: Type[T], filters: Optional[JsonDict] = None) -> "T":
        path = cls._get_path()
        results = cls.list(filters)
        if len(results) == 0:
            raise GetMultipleError(message="No result found", path=path)
        if len(results) > 1:
            raise GetMultipleError(message=f"Found multiple results {len(results)}", path=path)

        return results[0]

    @classmethod
    def is_abstract(cls) -> bool:
        return cls.__dict__.get("abstract", False)

    @classmethod
    def list(
        cls: Type[T],
        filters: Optional[JsonDict] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        api: Optional[ApiProto] = None,
    ) -> ApiList[T]:
        filters = filters or {}
        if limit is not None:
            filters["page[limit]"] = limit
        if offset is not None:
            filters["page[offset]"] = offset

        api = api or cls._get_manager_api()
        path = cls._get_path()
        resp = api.get(path, params=filters)
        result = resp.json()
        if not resp.ok:
            raise GetError(error=result, path=path)

        return ApiList((cls.from_response(each, api=api) for each in result["data"]), meta=result.get("meta", {}))

    @classmethod
    def list_all(
        cls: Type[T],
        filters: Optional[JsonDict] = None,
        offset: int = 0,
        count: int = DEFAULT_LIST_COUNT,
        page_size: int = DEFAULT_LIST_PAGE_SIZE,
        api: Optional[ApiProto] = None,
    ) -> ApiList[T]:
        objects = []
        meta = {}
        for _ in range(100):  # Limit to 100 loops
            limit = min(page_size, count - len(objects))
            result = cls.list({**(filters or {}), "page[offset]": offset, "page[limit]": limit}, api=api)
            meta = result.meta
            objects.extend(result)
            offset += page_size
            if (offset >= result.meta["page[total]"]) or (len(objects) >= count):
                break

        return ApiList(objects, meta=meta)

    def __init__(self, id: str = "", attributes: Optional[JsonDict] = None, api: Optional[ApiProto] = None):
        self.api = api or self._get_manager_api()
        self.id = id
        self.attributes = attributes or {}
        self.q = self.get_attribute

    def __contains__(self, key: str) -> bool:
        return key in self.attributes

    def __getitem__(self, key: str):
        return self.attributes[key]

    def as_json_dict(self) -> JsonDict:
        return {
            "attributes": self.attributes,
            "id": self.id,
            "type": self._get_resource_name(),
        }

    def call(self, method: str, attributes: Optional[JsonDict] = None, http_method: str = "post", **kwargs) -> JsonDict:
        path = self._get_path(id=self.id, method=method)

        if attributes is not None:
            arg_name = "params" if http_method in ("delete", "get") else "json"
            kwargs[arg_name] = attributes

        resp = getattr(self.api, http_method)(path, **kwargs)
        result = resp.json()
        if not resp.ok:
            raise CallError(error=result, path=path)

        return result

    def delete(self: T) -> T:
        path = self._get_path(id=self.id)
        resp = self.api.delete(path)
        if not resp.ok:
            raise DeleteError(error=resp.json(), path=path)

        return self

    def get_attribute(self, key: str, default=None):
        """Retrieve specific attribute. Use `/` for nested keys"""
        cwd = self.attributes
        for path in key.split("/"):
            if path not in cwd:
                return default
            cwd = cwd[path]

        return cwd

    def patch(self: T, attributes: Union[JsonDict, List[JsonDict]], with_id: bool = True) -> T:
        kwargs = {}
        if with_id:
            # By default, we always include `id` in the PATCH body. But some APIs don't have it.
            kwargs["id"] = self.id

        path = self._get_path(id=self.id)
        resp = self.api.patch(
            path,
            json={"data": {"attributes": attributes, "type": self._get_resource_name(), **kwargs}},
        )
        result = resp.json()
        if not resp.ok:
            raise PatchError(error=result, path=path)

        self.attributes = result["data"]["attributes"]
        return self

    def refresh(self: T) -> T:
        result = self.from_id(self.id, api=self.api)
        self.attributes = result.attributes
        return self

    def wait_until(self: T, fn: Callable[[T], bool], retry_count: int = DEFAULT_RETRY_COUNT) -> T:
        for _ in range(retry_count):
            if fn(self):
                break
            time.sleep(self.DEFAULT_RETRY_SLEEP)
            self.refresh()
        else:
            raise WaitError(f"Timeout waiting for {self.id}")

        return self
