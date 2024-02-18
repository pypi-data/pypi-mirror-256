"""
#
# Caredb models
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

from brewmaster.objects.base import ApiObject


class AggregationIndividual(ApiObject):
    base_path = "/caredb/v1/aggregation-individuals"


class Article(ApiObject):
    base_path = "/caredb/v1/articles"


class ArticleTag(ApiObject):
    base_path = "/caredb/v1/article-tags"


class Challenge(ApiObject):
    base_path = "/caredb/v1/challenges"


class CustomExtEntry(ApiObject):
    base_path = "/caredb/v1/customext-entries"


class CustomExtField(ApiObject):
    base_path = "/caredb/v1/customext-fields"


class CustomExtTable(ApiObject):
    base_path = "/caredb/v1/customext-tables"


class JournalAttachment(ApiObject):
    base_path = "/caredb/v1/journal-attachments"


class JournalEntry(ApiObject):
    base_path = "/caredb/v1/journal-entries"


class LcrContact(ApiObject):
    base_path = "/caredb/v1/lcr-contacts"


class LcrProgramIndividualAssociation(ApiObject):
    base_path = "/caredb/v1/lcr-program-individual-associations"


class LcrProgram(ApiObject):
    base_path = "/caredb/v1/lcr-programs"


class LcrReachableResources(ApiObject):
    base_path = "/caredb/v1/lcr-reachable-resources"


class LcrResourceIndividualAssociation(ApiObject):
    base_path = "/caredb/v1/lcr-resource-individual-associations"


class LcrResourceProgramAssociation(ApiObject):
    base_path = "/caredb/v1/lcr-resource-program-associations"


class LcrResource(ApiObject):
    base_path = "/caredb/v1/lcr-resources"


class OrgAppointment(ApiObject):
    base_path = "/caredb/v1/org-appointments"


class OrgAppointmentStatus(ApiObject):
    base_path = "/caredb/v1/org-appointment-statuses"


class OrgAppointmentType(ApiObject):
    base_path = "/caredb/v1/org-appointment-types"


class OrgCarePlanTag(ApiObject):
    base_path = "/caredb/v1/org-care-plan-tags"


class OrgCarePlanTemplate(ApiObject):
    base_path = "/caredb/v1/org-care-plan-templates"


class OrgCarePlan(ApiObject):
    base_path = "/caredb/v1/org-care-plans"


class OrgCareTeam(ApiObject):
    base_path = "/caredb/v1/org-care-teams"


class OrgCondition(ApiObject):
    base_path = "/caredb/v1/org-conditions"


class OrgContact(ApiObject):
    base_path = "/caredb/v1/org-contacts"


class OrgDiagnosticReport(ApiObject):
    base_path = "/caredb/v1/org-diagnostic-reports"


class OrgDocumentClass(ApiObject):
    base_path = "/caredb/v1/org-document-classes"


class OrgDocumentReference(ApiObject):
    base_path = "/caredb/v1/org-document-references"


class OrgEncounter(ApiObject):
    base_path = "/caredb/v1/org-encounters"


class OrgEncounterReason(ApiObject):
    base_path = "/caredb/v1/org-encounter-reasons"


class OrgEncounterType(ApiObject):
    base_path = "/caredb/v1/org-encounter-types"


class OrgObservation(ApiObject):
    base_path = "/caredb/v1/org-observations"


class OrgObservationTag(ApiObject):
    base_path = "/caredb/v1/org-observation-tags"


class OrgObservationTemplate(ApiObject):
    base_path = "/caredb/v1/org-observation-templates"


class OrgPractitioner(ApiObject):
    base_path = "/caredb/v1/org-practitioners"


class TodoEntry(ApiObject):
    base_path = "/caredb/v1/todo-entries"


class TodoEntryLog(ApiObject):
    base_path = "/caredb/v1/todo-entries-logs"


class TodoEntryStatus(ApiObject):
    base_path = "/caredb/v1/todo-entries-statuses"
