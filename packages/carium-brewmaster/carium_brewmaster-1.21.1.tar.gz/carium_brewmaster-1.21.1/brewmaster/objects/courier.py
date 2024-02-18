"""
#
# Courier models
#
# Copyright(c) 2023-, Carium, Inc. All rights reserved.
#
"""

from brewmaster.objects.base import ApiObject


class Announcer(ApiObject):
    base_path = "/courier/v1/announcers"


class Individual(ApiObject):
    base_path = "/courier/v1/individuals"


class MessagingChannel(ApiObject):
    base_path = "/courier/v1/messaging-channels"


class MessagingMessage(ApiObject):
    base_path = "/courier/v1/messaging-messages"


class MessagingPlugin(ApiObject):
    base_path = "/courier/v1/messaging-plugins"


class MessagingResponder(ApiObject):
    base_path = "/courier/v1/messaging-responders"


class Text(ApiObject):
    base_path = "/courier/v1/texts"


class TextAccount(ApiObject):
    base_path = "/courier/v1/text-accounts"


class TextAccountNumber(ApiObject):
    base_path = "/courier/v1/text-account-numbers"


class TextNumberLog(ApiObject):
    base_path = "/courier/v1/text-number-logs"


class UserDevice(ApiObject):
    base_path = "/courier/v1/user-devices"


class UserEmailAttachment(ApiObject):
    base_path = "/courier/v1/user-email-attachments"


class UserEmail(ApiObject):
    base_path = "/courier/v1/user-emails"


class UserNotification(ApiObject):
    base_path = "/courier/v1/user-notifications"


class VideoChannel(ApiObject):
    base_path = "/courier/v1/video-channels"


class VideoComposition(ApiObject):
    base_path = "/courier/v1/video-compositions"


class VideoParticipant(ApiObject):
    base_path = "/courier/v1/video-participants"


class VoiceSetting(ApiObject):
    base_path = "/courier/v1/voice-settings"
