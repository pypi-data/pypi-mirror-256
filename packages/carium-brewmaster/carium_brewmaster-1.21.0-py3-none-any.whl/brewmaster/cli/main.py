"""
#
# Overlord CLI entry point
#
# Copyright(c) 2018, Carium, Inc. All rights reserved.
#
"""

import logging
from typing import List, NoReturn, Optional

from cariutils.cli import Cli


class BrewCli(Cli):
    django_settings_module = "brewmaster.settings.test"

    commands = ("brewmaster.cli.docs.GenCmd",)

    @classmethod
    def main(cls, argv: Optional[List[str]] = None) -> NoReturn:
        # Disable the annoying readiness probe
        log = logging.getLogger("cariumlib.runtime.probes.readiness")
        log.setLevel(logging.ERROR)

        super().main(argv)
