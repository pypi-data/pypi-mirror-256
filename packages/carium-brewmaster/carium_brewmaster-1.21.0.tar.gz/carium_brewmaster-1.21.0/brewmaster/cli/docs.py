"""
#
# Documentation CLI
#
# Copyright(c) 2019, Carium, Inc. All rights reserved.
#
"""

import inspect
import os
from argparse import ArgumentParser
from typing import Callable, cast

import docstring_parser
from django.conf import settings
from docstring_parser.common import Docstring
from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment

from brewmaster.barrel import Barrel
from cariutils.cli import Command
from cariutils.shortcuts import import_class


class DocParser:
    @classmethod
    def get_annotation_name(cls, _type) -> str:
        if str(_type).startswith("typing."):
            # Typing annotation
            result = str(_type).replace("typing.", "")
        else:
            if hasattr(_type, "__name__"):
                # Regular class
                result = _type.__name__
            else:
                result = str(_type)

        return result

    def parse(self, class_name: str, fn: Callable) -> Docstring:
        """Parse docstring, based on https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html"""
        result = docstring_parser.parse(fn.__doc__)

        # Fix types
        signature = inspect.signature(fn)
        for param in result.params:
            param_signature = signature.parameters[param.arg_name]
            param.type_name = self.get_annotation_name(param_signature.annotation)

        assert result.returns is not None, f"Missing returns {class_name}.{fn.__name__}"
        result.returns.type_name = self.get_annotation_name(signature.return_annotation)  # pyre-ignore[16]
        return result


class GenCmd(Command):
    name = "doc-gen"
    BASE_DIR = os.path.join(settings.BASE_DIR, "..", "docs", "commands")

    @classmethod
    def init_args(cls, subparser: ArgumentParser) -> None:
        subparser.add_argument("--command")

    @classmethod
    def generate_command(cls, command: str) -> str:
        context = {"command": command, "functions": []}
        parser = DocParser()
        api_cls = import_class(Barrel.commands[command])
        for obj in api_cls.__dict__.values():
            # We only care about function, and the name is not started with `_`
            if not inspect.isfunction(obj) or obj.__name__.startswith("_"):  # pragma: nocover
                continue

            functions = cast(list, context["functions"])
            functions.append({"name": obj.__name__, "docs": parser.parse(api_cls.__name__, obj)})

        env = SandboxedEnvironment(loader=FileSystemLoader(os.path.join(settings.BASE_DIR, "templates")))
        template = env.get_template("module.md")
        return template.render(**context)

    def execute(self) -> int:
        if self.args.command is not None:
            print(self.generate_command(self.args.command))
            return 0

        for command in Barrel.commands.keys():
            with open(os.path.join(self.BASE_DIR, f"{command}.md"), "w") as fout:
                fout.write(self.generate_command(command))

        return 0
