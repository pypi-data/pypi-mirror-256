"""
#
# Overlord models
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

from brewmaster.objects.base import ApiObject


class FormInstance(ApiObject):
    base_path = "/overlord/v1/form-instances"


class FormSpec(ApiObject):
    base_path = "/overlord/v1/form-specs"


class FormSpecVersion(ApiObject):
    base_path = "/overlord/v1/form-spec-versions"


class Interaction(ApiObject):
    base_path = "/overlord/v1/interactions"


class InteractionInvocation(ApiObject):
    base_path = "/overlord/v1/interaction-invocations"


class InteractionProfile(ApiObject):
    base_path = "/overlord/v1/interaction-profiles"


class Interview(ApiObject):
    base_path = "/overlord/v1/interviews"


class InterviewProfile(ApiObject):
    base_path = "/overlord/v1/interview-profiles"


class InterviewQuestion(ApiObject):
    base_path = "/overlord/v1/interview-questions"


class LnpProgram(ApiObject):
    base_path = "/overlord/v1/lnp-programs"


class LnpRun(ApiObject):
    base_path = "/overlord/v1/lnp-runs"


class LnpRunBlock(ApiObject):
    base_path = "/overlord/v1/lnp-run-blocks"


class LnpRunLog(ApiObject):
    base_path = "/overlord/v1/lnp-run-logs"


class LnpVersionBlock(ApiObject):
    base_path = "/overlord/v1/lnp-version-blocks"


class LnpVersionLink(ApiObject):
    base_path = "/overlord/v1/lnp-version-links"


class PathwayInstance(ApiObject):
    base_path = "/overlord/v1/pathway-instances"


class PathwayInstanceForm(ApiObject):
    base_path = "/overlord/v1/pathway-instance-forms"


class PathwayInstanceLog(ApiObject):
    base_path = "/overlord/v1/pathway-instance-logs"


class PathwayInstanceNote(ApiObject):
    base_path = "/overlord/v1/pathway-instance-notes"


class PathwayInstanceReminder(ApiObject):
    base_path = "/overlord/v1/pathway-instance-reminders"


class PathwayInstanceStage(ApiObject):
    base_path = "/overlord/v1/pathway-instance-stages"


class PathwayInstanceStep(ApiObject):
    base_path = "/overlord/v1/pathway-instance-steps"


class PathwayInstanceStore(ApiObject):
    base_path = "/overlord/v1/pathway-instance-stores"


class PathwayInstanceTodo(ApiObject):
    base_path = "/overlord/v1/pathway-instance-todos"


class PathwaySpec(ApiObject):
    base_path = "/overlord/v1/pathway-specs"


class PathwaySpecForm(ApiObject):
    base_path = "/overlord/v1/pathway-spec-forms"


class PathwaySpecGroup(ApiObject):
    base_path = "/overlord/v1/pathway-spec-groups"


class PathwaySpecStage(ApiObject):
    base_path = "/overlord/v1/pathway-spec-stages"


class PathwaySpecStep(ApiObject):
    base_path = "/overlord/v1/pathway-spec-steps"


class PathwaySpecVersion(ApiObject):
    base_path = "/overlord/v1/pathway-spec-versions"


class PathwaySpecVersionLoader(ApiObject):
    base_path = "/overlord/v1/pathway-spec-version-loaders"


class PathwayTask(ApiObject):
    base_path = "/overlord/v1/pathway-tasks"


class PlaygroundDesign(ApiObject):
    base_path = "/overlord/v1/playground-designs"


class PlaygroundRealm(ApiObject):
    base_path = "/overlord/v1/playground-realms"


class PlaygroundSimulation(ApiObject):
    base_path = "/overlord/v1/playground-simulations"


class PlaygroundSimObject(ApiObject):
    base_path = "/overlord/v1/playground-simobjects"


class PlaygroundTxInteraction(ApiObject):
    base_path = "/overlord/v1/playground-tx-interactions"


class PlaygroundWfEvent(ApiObject):
    base_path = "/overlord/v1/playground-wf-events"


class PlaygroundWfState(ApiObject):
    base_path = "/overlord/v1/playground-wf-states"


class Program(ApiObject):
    base_path = "/overlord/v1/programs"


class ProgramArgsHistory(ApiObject):
    base_path = "/overlord/v1/program-args-histories"


class ProgramConfig(ApiObject):
    base_path = "/overlord/v1/program-configs"


class ProgramLog(ApiObject):
    base_path = "/overlord/v1/program-logs"


class ProgramStat(ApiObject):
    base_path = "/overlord/v1/program-stats"


class Workflow(ApiObject):
    base_path = "/overlord/v1/workflows"


class WorkflowType(ApiObject):
    base_path = "/overlord/v1/workflow-types"
