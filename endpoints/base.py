import json
import requests
from enum import Enum


# =======================================================
# Parameter enums
# =======================================================
class BasicOptions(Enum):
    TRUE  = "true"
    FALSE = "false"
    ANY   = "any"


class AssignedUserOptions(Enum):
    ME   = "me"
    ANY  = "any"
    NONE = "none"


class AssignedTeamOptions(Enum):
    MINE = "mine"
    NONE = "none"


class SortByOptions(Enum):
    LAST_ACTIVITY = "last_activity"
    CREATION_TIME = "creation_time"


class UserRoles(Enum):
    ADMIN        = ("admin",        20)
    AGENT        = ("agent",        10)
    COLLABORATOR = ("collaborator", 9)
    CUSTOMER     = ("customer",     None)


class DataPointType(Enum):
    AVG_FIRST_RESPONSE_TIME = "avg_first_response_time"
    TICKETS_COUNT = "tickets_count"
    REPLIES_COUNT = "replies_count"


# =======================================================
# Resource - Base class with default requests
# =======================================================
class Resource:
    def __init__(self, api):
        self.api = api
        self.default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _prepare_url(self, endpoint, **kwargs):
        url = self.api.BASE_URL.format(url=endpoint)
        for key, value in kwargs.items():
            if value is not None:
                url += "&" + key + "=" + str(value)
        return url

    def _get(self, endpoint, **kwargs):
        url = self._prepare_url(endpoint, **kwargs)
        return requests.get(url, headers=self.default_headers).json()

    def _post(self, endpoint, data=None, files=None, **kwargs):
        url = self._prepare_url(endpoint, **kwargs)
        headers = self.default_headers
        if files is not None:
            headers.pop("Content-Type")
        response = requests.post(url, headers=headers, json=data, files=files)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.text

    def _put(self, endpoint, data=None, **kwargs):
        url = self._prepare_url(endpoint, **kwargs)
        return requests.put(url, headers=self.default_headers, json=data).json()

    def _delete(self, endpoint, **kwargs):
        url = self._prepare_url(endpoint, **kwargs)
        return requests.delete(url, headers=self.default_headers).json()
