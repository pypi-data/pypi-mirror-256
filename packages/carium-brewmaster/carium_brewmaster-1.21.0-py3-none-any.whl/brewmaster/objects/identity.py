"""
#
# Identity models
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

from brewmaster.objects.base import ApiObject


class AnonymousAccess(ApiObject):
    base_path = "/identity/v1/anonymous-accesses"


class ArchiveRequest(ApiObject):
    base_path = "/identity/v1/archive-requests"


class DeletionRequest(ApiObject):
    base_path = "/identity/v1/deletion-requests"


class Feature(ApiObject):
    base_path = "/identity/v1/features"


class IndividualGroup(ApiObject):
    base_path = "/identity/v1/individual-groups"


class IndividualGroupTag(ApiObject):
    base_path = "/identity/v1/individual-group-tags"


class OnboardingRequest(ApiObject):
    base_path = "/identity/v1/onboarding-requests"


class Organization(ApiObject):
    base_path = "/identity/v1/organizations"


class OrganizationCode(ApiObject):
    base_path = "/identity/v1/organization-codes"


class OrganizationEmailTemplate(ApiObject):
    base_path = "/identity/v1/organization-email-templates"


class OrganizationFeature(ApiObject):
    base_path = "/identity/v1/organization-features"


class OrganizationGeneralMessage(ApiObject):
    base_path = "/identity/v1/organization-general-messages"


class OrganizationSmsTemplate(ApiObject):
    base_path = "/identity/v1/organization-sms-templates"


class OrganizationTheme(ApiObject):
    base_path = "/identity/v1/organization-themes"


class Task(ApiObject):
    base_path = "/identity/v1/tasks"


class UrlShortener(ApiObject):
    base_path = "/identity/v1/url-shorteners"


class User(ApiObject):
    base_path = "/identity/v1/users"


class UserFeature(ApiObject):
    base_path = "/identity/v1/user-features"
