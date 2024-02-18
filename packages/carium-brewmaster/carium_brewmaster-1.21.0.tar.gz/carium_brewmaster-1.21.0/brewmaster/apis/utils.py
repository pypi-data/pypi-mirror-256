"""
#
# Utilities
#
# Copyright(c) 2020-, Carium, Inc. All rights reserved.
#
"""

import uuid
from datetime import date, datetime, time

import dateutil.parser
from django.utils import timezone

from brewmaster.apis.base import Endpoint


class DateUtils(Endpoint):
    DATE_FORMAT = "%Y-%m-%d"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    TIME_FORMAT = "%H:%M:%S"

    def from_date(self, _date: date) -> str:
        """Convert date to string representation.

        Args:
            _date: date to be converted
        Returns:
            formatted date string
        """
        return _date.strftime(self.DATE_FORMAT)

    def from_datetime(self, _datetime: datetime) -> str:
        """Convert datetime to string representation.

        Args:
            _datetime: datetime to be converted
        Returns:
            formatted datetime string
        """
        if timezone.is_aware(_datetime):
            _datetime = _datetime.astimezone(timezone.utc)

        return _datetime.strftime(self.DATETIME_FORMAT)

    def from_time(self, _time: time) -> str:
        """Convert time to string representation.

        Args:
            _time: time to be converted
        Returns:
            formatted time string
        """
        return _time.strftime(self.TIME_FORMAT)

    def to_date(self, date_s: str) -> date:
        """Convert date-string to date.

        Args:
            date_s: date-string to be converted
        Returns:
            date representation of date_s
        """
        return datetime.strptime(date_s, self.DATE_FORMAT).date()

    def to_datetime(self, datetime_s: str) -> datetime:
        """Convert date-string to datetime in UTC timezone.

        Args:
            datetime_s: string to be converted
        Returns:
            datetime representation of datetime_s
        """
        # timezone-aware format
        if "T" in datetime_s:
            return dateutil.parser.isoparse(datetime_s).astimezone(timezone.utc)

        # non-tz format
        return datetime.strptime(datetime_s, self.DATETIME_FORMAT).replace(tzinfo=timezone.utc)

    def to_time(self, time_s: str) -> time:
        """Convert time-string to time.

        Args:
            time_s: string to be converted
        Returns:
            time representation of time_s
        """
        return datetime.strptime(time_s, self.TIME_FORMAT).time()


class Utils(Endpoint):
    def is_valid_uuid(self, uuid_s: str) -> bool:
        """Verify if a string is valid UUID

        Args:
            uuid_s: UUID string to be verified
        Returns:
            True if uuid_s is valid UUID string, False otherwise
        """
        try:
            uuid.UUID(uuid_s)
            return True
        except Exception:
            return False
