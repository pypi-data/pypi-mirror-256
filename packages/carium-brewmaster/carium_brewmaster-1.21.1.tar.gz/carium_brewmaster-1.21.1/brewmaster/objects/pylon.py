"""
#
# Pylon models
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

from brewmaster.objects.base import ApiObject


class CustomJobExecutor(ApiObject):
    base_path = "/pylon/v1/customjob-executors"


class CustomJobLog(ApiObject):
    base_path = "/pylon/v1/customjob-logs"


class CustomJobModule(ApiObject):
    base_path = "/pylon/v1/customjob-modules"


class CustomJobQueue(ApiObject):
    base_path = "/pylon/v1/customjob-queues"


class CustomJobQueueEntry(ApiObject):
    base_path = "/pylon/v1/customjob-queue-entries"


class CustomJobRepository(ApiObject):
    base_path = "/pylon/v1/customjob-repositories"


class CustomJobSpec(ApiObject):
    base_path = "/pylon/v1/customjob-specs"


class CustomJobSpecModule(ApiObject):
    base_path = "/pylon/v1/customjob-spec-modules"


class CustomJobSpecVcs(ApiObject):
    base_path = "/pylon/v1/customjob-spec-vcses"


class CustomJobSetting(ApiObject):
    base_path = "/pylon/v1/customjob-settings"


class CustomJobStorage(ApiObject):
    base_path = "/pylon/v1/customjob-storages"


class Organization(ApiObject):
    base_path = "/pylon/v1/organizations"


class SftpFile(ApiObject):
    base_path = "/pylon/v1/sftp-files"


class SftpUser(ApiObject):
    base_path = "/pylon/v1/sftp-users"
