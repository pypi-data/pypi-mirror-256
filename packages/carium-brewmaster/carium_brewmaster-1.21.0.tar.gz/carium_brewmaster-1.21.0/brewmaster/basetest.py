"""
#
# Brewmaster base test
#
# Copyright(c) 2020-, Carium, Inc. All rights reserved.
#
"""

import json
import uuid
from unittest import mock
from urllib import parse

import requests
from django.test import TestCase as DjangoTestCase
from responses import BaseResponse, RequestsMock

from brewmaster.adapter import ApiAdapter
from brewmaster.barrel import Barrel


class MockManager:
    def __init__(self):
        self._patches = {}
        self.fakes = {}  # return values of starting each patch

    def patch(self, target, **kwargs):
        _patch = mock.patch(target, **kwargs)
        return self.add(_patch, name=target)

    def add(self, patch, name=None):
        """Start a patch and make it managed by the MockManager"""
        name = name or id(patch)
        assert name not in self._patches, f"{name} already patched!"  # we don't support a double patch
        self._patches[name] = patch
        self.fakes[name] = patch.start()
        return self.fakes[name]

    def cleanup(self):
        for _patch in self._patches.values():
            _patch.stop()

    def remove(self, name):
        """remove and stop the patch if exists"""
        patch = self._patches.pop(name, None)
        if patch:
            patch.stop()


class MockApi(ApiAdapter):
    def _common(self, method, path, *args, **kwargs):
        service = path.split("/", 1)[0]
        path = f"http://{service}/{path}"
        return getattr(requests, method)(path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self._common("delete", path, *args, **kwargs)

    def get(self, path, *args, **kwargs):
        return self._common("get", path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return self._common("patch", path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self._common("post", path, *args, **kwargs)


class TestCase(DjangoTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.organization_id = str(uuid.uuid4())
        self.mock = MockManager()
        self.api = MockApi()
        self.barrel = Barrel(self.organization_id, self.api)

        self.responses = RequestsMock()
        self.responses.start()

    def tearDown(self) -> None:
        self.responses.reset()
        self.responses.stop()
        self.mock.cleanup()
        super().tearDown()

    def assert_qs(self, request: requests.PreparedRequest, expected: dict) -> None:
        """Assert the query-string dictionary from the given request"""
        self.assertEqual(parse.parse_qs(parse.urlparse(request.url).query), expected)  # pyre-ignore[6]

    def _add_callback(self, method: str, path: str, fn) -> BaseResponse:
        def _trampoline(request):
            _response.requests.append(request)
            return fn(request)

        self.responses.add_callback(method, path, _trampoline)
        _response = self.responses._registry._responses[-1]
        _response.requests = []  # pyre-ignore[16]
        return _response

    def _add_response(self, method: str, path: str, json_dict: dict) -> BaseResponse:
        status_code_map = {
            "DELETE": 204,
            "GET": 200,
            "POST": 201,
            "PATCH": 200,
        }

        def _trampoline(request):
            # requests will raise exception if a delete response has any content length
            # https://github.com/getsentry/responses/pull/655
            # https://github.com/psf/requests/issues/3794
            body = "" if method == "DELETE" else json.dumps(json_dict)
            return (status_code_map[method], {}, body)

        return self._add_callback(method, path, _trampoline)
