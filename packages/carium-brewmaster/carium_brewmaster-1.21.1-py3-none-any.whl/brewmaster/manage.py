#!/usr/bin/env python
#
# Copyright(c) 2020-, Carium, Inc. All rights reserved.
#

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bremaster.settings.test")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":  # pragma: no cover
    main()
