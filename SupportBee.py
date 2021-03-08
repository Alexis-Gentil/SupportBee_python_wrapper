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


class UserRoles:
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

    def _prepare_url(self, endpoint, **kwargs):
        url = self.api.BASE_URL.format(url=endpoint)
        for key, value in kwargs.items():
            if value is not None:
                url += "&" + key + "=" + str(value)
        return url

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _get(self, endpoint, **kwargs):
        url = self._prepare_url(endpoint, **kwargs)
        print("GET", url)
        return requests.get(url, headers=self._get_headers()).json()

    def _post(self, endpoint, data=None, files=None, **kwargs):
        url = self._prepare_url(endpoint, **kwargs)
        print("POST", url)
        headers = self._get_headers()
        if files is not None: 
            headers.pop("Content-Type")
        response = requests.post(url, headers=headers, json=data, files=files)
        # print(response)
        # print(response.text)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.text

    def _put(self, endpoint, data=None, **kwargs):
        url = self._prepare_url(endpoint, **kwargs)
        print("PUT", url)
        return requests.put(url, headers=self._get_headers(), json=data).json()

    def _delete(self, endpoint, **kwargs):
        url = self._prepare_url(endpoint, **kwargs)
        print("DELETE", url)
        return requests.delete(url, headers=self._get_headers()).json()


# =======================================================
# Tickets
# =======================================================
class Tickets(Resource):
    def fetch(self,
              per_page:         int                        = 100,
              page:             int                        = 1,
              archived:         BasicOptions               = None,  # Default = BasicOptions.FALSE,
              spam:             bool                       = None,  # Default = False,
              trash:            bool                       = None,  # Default = False,
              replies:          bool                       = None,
              max_replies:      int                        = None,
              assigned_user:    int or AssignedUserOptions = None,
              assigned_team:    int or AssignedTeamOptions = None,
              starred:          bool                       = None,
              label:            str                        = None,
              since:            str                        = None,
              until:            str                        = None,
              sort_by:          SortByOptions              = None,  # Default = SortByOptions.LAST_ACTIVITY,
              requester_emails: str                        = None,
              total_only:       bool                       = None   # Default = False
              ):
        return self._get("/tickets",
                         per_page=per_page,
                         page=page,
                         archived=archived,
                         spam=spam,
                         trash=trash,
                         replies=replies,
                         max_replies=max_replies,
                         assigned_user=assigned_user,
                         assigned_team=assigned_team,
                         starred=starred,
                         label=label,
                         since=since,
                         until=until,
                         sort_by=sort_by,
                         requester_emails=requester_emails,
                         total_only=total_only)

    def search(self,
               query:    str,
               per_page: int  = 100,
               page:     int  = 1,
               spam:     bool = False,
               trash:    bool = False):
        return self._get("/tickets/search",
                         query=query,
                         per_page=per_page,
                         page=page,
                         spam=spam,
                         trash=trash)

    def create(self,
               subject:          str,
               requester_name:   str,
               requester_email:  str,
               content:          str,
               cc:               str  = None,
               bcc:              str  = None,
               notify_requester: bool = False,
               attachment_ids:   list = None,
               content_as_html:  bool = False):
        ticket = {
            "subject": subject,
            "requester_name": requester_name,
            "requester_email": requester_email,
            "content": {
                "html" if content_as_html else "text": content,
            },
            "notify_requester": notify_requester
        }

        if cc is not None:
            ticket["cc"] = cc
        if bcc is not None:
            ticket["bcc"] = bcc
        if attachment_ids is not None:
            ticket["content"]["attachment_ids"] = ",".join(attachment_ids)

        return self._post("/tickets", data={"ticket": ticket})

    def get(self,
            ticket_id: int):
        return self._get("/tickets/{ticket_id}".format(ticket_id=ticket_id))

    def delete(self,
               ticket_id: int):
        return self._delete("/tickets/{ticket_id}".format(ticket_id=ticket_id))

    def archive(self,
                ticket_id: int):
        return self._post("/tickets/{ticket_id}/archive".format(ticket_id=ticket_id))

    def unarchive(self,
                  ticket_id: int):
        return self._delete("/tickets/{ticket_id}/archive".format(ticket_id=ticket_id))

    def markAsAnswered(self,
                       ticket_id: int):
        return self._post("/tickets/{ticket_id}/answered".format(ticket_id=ticket_id))

    def markAsUnanswered(self,
                         ticket_id: int):
        return self._delete("/tickets/{ticket_id}/answered".format(ticket_id=ticket_id))

    def assignUser(self,
                   ticket_id: int,
                   user_id: int):
        user_assignment = {
            "user_id": user_id
        }
        return self._post("/tickets/{ticket_id}/user_assignment".format(ticket_id=ticket_id),
                          data={"user_assignment": user_assignment})

    def unassignUser(self,
                     ticket_id: int):
        return self._delete("/tickets/{ticket_id}/user_assignment".format(ticket_id=ticket_id))

    def assignTeam(self,
                   ticket_id: int,
                   team_id: int):
        team_assignment = {
            "team_id": team_id
        }
        return self._post("/tickets/{ticket_id}/team_assignment".format(ticket_id=ticket_id),
                          data={"team_assignment": team_assignment})

    def unassignTeam(self,
                     ticket_id: int):
        return self._delete("/tickets/{ticket_id}/team_assignment".format(ticket_id=ticket_id))

    def star(self,
             ticket_id: int):
        return self._post("/tickets/{ticket_id}/star".format(ticket_id=ticket_id))

    def unstar(self,
               ticket_id: int):
        return self._delete("/tickets/{ticket_id}/star".format(ticket_id=ticket_id))

    def markAsSpam(self,
                   ticket_id: int):
        return self._post("/tickets/{ticket_id}/spam".format(ticket_id=ticket_id))

    def unspam(self,
               ticket_id: int):
        return self._delete("/tickets/{ticket_id}/spam".format(ticket_id=ticket_id))

    def markAsTrash(self,
                    ticket_id: int):
        return self._post("/tickets/{ticket_id}/trash".format(ticket_id=ticket_id))

    def untrash(self,
                ticket_id: int):
        return self._delete("/tickets/{ticket_id}/trash".format(ticket_id=ticket_id))


# =======================================================
# Replies
# =======================================================
class Replies(Resource):
    def fetch(self,
              ticket_id: int):
        return self._get("/tickets/{ticket_id}/replies".format(ticket_id=ticket_id))

    def create(self,
               ticket_id:          int,
               content:            str,
               cc:                 str  = None,
               bcc:                str  = None,
               attachment_ids:     str  = None,
               on_behalf_of_id:    str  = None,
               on_behalf_of_email: str  = None,
               notify_requester:   str  = False,
               content_as_html:    bool = False):
        reply = {
            "content": {
                "html" if content_as_html else "text": content,
            },
            "notify_requester": notify_requester
        }

        if cc is not None:
            reply["cc"] = cc
        if bcc is not None:
            reply["bcc"] = bcc
        if attachment_ids is not None:
            reply["content"]["attachment_ids"] = attachment_ids

        if on_behalf_of_id is not None:
            reply["on_behalf_of"] = {"id": on_behalf_of_id}
        elif on_behalf_of_email is not None:
            reply["on_behalf_of"] = {"email": on_behalf_of_email}

        return self._post("/tickets/{ticket_id}/replies".format(ticket_id=ticket_id), data={"reply": reply})

    def get(self,
            ticket_id: int,
            reply_id:  int):
        return self._get("/tickets/{ticket_id}/replies/{reply_id}".format(ticket_id=ticket_id, reply_id=reply_id))


# =======================================================
# Comments
# =======================================================
class Comments(Resource):
    def fetch(self,
              ticket_id: int):
        return self._get("/tickets/{ticket_id}/comments".format(ticket_id=ticket_id))

    def create(self,
               ticket_id:       str,
               content:         str,
               attachment_ids:  list = None,
               content_as_html: bool = False):
        comment = {
            "content": {
                "html" if content_as_html else "text": content,
            }
        }

        if attachment_ids is not None:
            comment["attachment_ids"] = ",".join(attachment_ids)

        self._post("/tickets/{ticket_id}/comments".format(ticket_id=ticket_id), data={"comment": comment})


# =======================================================
# Teams
# =======================================================
class Teams(Resource):
    def fetch(self,
              only_with_users: bool = False,
              only_mine:       bool = False):
        user = "me" if only_mine else ""
        return self._get("/teams", with_users=only_with_users, user=user)


# =======================================================
# Users
# =======================================================
class Users(Resource):
    def fetch(self,
              with_invited: bool = False,
              with_roles:   list = (UserRoles.ADMIN, UserRoles.AGENT, UserRoles.COLLABORATOR)):
        roles = ",".join([role[0] for role in with_roles])
        return self._get("/users", with_invited=with_invited, with_roles=roles, type="user")

    def get(self,
            user_id:     bool,
            max_tickets: False or int = 5  # False = all tickets
            ):
        return self._get("/users/{user_id}".format(user_id=user_id), max_tickets=max_tickets)

    def create(self,
               email:    str,
               name:     str,
               role:     UserRoles = None,
               team_ids: list      = None):
        user = {
            "email": email,
            "name": name,
            "type": "user"
        }
        if role is not None:
            user["role"] = role[1]
        if team_ids is not None:
            user["team_ids"] = ",".join(team_ids)
        return self._post("/users", data={"user": user})

    def update(self,
               user_id:    int,
               email:      str       = None,
               first_name: str       = None,
               last_name:  str       = None,
               role:       UserRoles = None,
               team_ids:   list      = None):
        user = {
            "type": "user"
        }

        if email is not None:
            user["email"] = email
        if first_name is not None:
            user["first_name"] = first_name
        if last_name is not None:
            user["last_name"] = last_name
        if role is not None:
            user["role"] = role[1]
        if team_ids is not None:
            user["team_ids"] = ",".join(team_ids)

        if len(user.keys()) == 1:
            return  # No update called

        return self._post("/users/{user_id}".format(user_id=user_id), data={"user": user})


# =======================================================
# Customer Groups
# =======================================================
class CustomerGroups(Resource):
    def fetch(self,
              with_invited: bool = False,
              with_roles:   list = (UserRoles.ADMIN, UserRoles.AGENT, UserRoles.COLLABORATOR)):
        roles = ",".join([role[0] for role in with_roles])
        return self._get("/users", with_invited=with_invited, with_roles=roles, type="customer_group")

    def create(self,
               name:                             str,
               role:                             UserRoles = None,
               team_ids:                         list      = None,
               can_members_access_group_tickets: bool      = None,
               email_domains:                    list      = None):
        customer_group = {
            "name": name,
            "type": "customer_group"
        }
        if role is not None:
            customer_group["role"] = role[1]
        if team_ids is not None:
            customer_group["team_ids"] = ",".join(team_ids)
        if can_members_access_group_tickets is not None:
            customer_group["can_members_access_group_tickets"] = can_members_access_group_tickets
        if email_domains is not None:
            customer_group["email_domains"] = ",".join(email_domains)
        return self._post("/users", data={"user": customer_group})

    def update(self,
               group_id:                         int,
               first_name:                       str       = None,
               last_name:                        str       = None,
               role:                             UserRoles = None,
               team_ids:                         list      = None,
               can_members_access_group_tickets: bool      = None,
               email_domains:                    list      = None):
        customer_group = {
            "type": "customer_group"
        }

        if first_name is not None:
            customer_group["first_name"] = first_name
        if last_name is not None:
            customer_group["last_name"] = last_name
        if role is not None:
            customer_group["role"] = role[1]
        if team_ids is not None:
            customer_group["team_ids"] = ",".join(team_ids)
        if can_members_access_group_tickets is not None:
            customer_group["can_members_access_group_tickets"] = can_members_access_group_tickets
        if email_domains is not None:
            customer_group["email_domains"] = ",".join(email_domains)

        if len(customer_group.keys()) == 1:
            return  # No update called

        return self._post("/users/{user_id}".format(user_id=group_id), data={"user": customer_group})

    def fetchMembers(self,
                     group_id: int):
        return self._get("/users/{group_id}/members".format(group_id=group_id))

    def addMember(self,
                  group_id: int,
                  member_id: int):
        member = {
            "id": member_id
        }
        return self._post("/users/{group_id}/members".format(group_id=group_id), data={"member": member})


# =======================================================
# Attachment
# =======================================================
class Attachments(Resource):
    def create(self,
               filename: str,
               file: bytes):
        files = {
            "files[]": (filename, file, "multipart/form-data")
        }
        return self._post("/attachments", files=files)


# =======================================================
# Labels
# =======================================================
class Labels(Resource):
    def fetch(self):
        return self._get("/labels")

    def create(self,  # Not in doc
               name: str,
               color: str):
        label = {
            "name": name,
            "color": color
        }
        return self._post("/labels", data={"custom_label": label})

    def addLabel(self,
                 ticket_id: str,
                 label_name: str):
        return self._post("/tickets/{ticket_id}/labels/{label_name}".format(ticket_id=ticket_id, label_name=label_name))

    def removeLabel(self,
                    ticket_id: str,
                    label_name: str):
        return self._delete("/tickets/{ticket_id}/labels/{label_name}".format(ticket_id=ticket_id,
                                                                              label_name=label_name))


# =======================================================
# Emails
# =======================================================
class Emails(Resource):
    def fetch(self):
        return self._get("/emails")

    def create(self,
               email:          str,
               name:           str  = None,
               filter_spam:    bool = None,
               use_agent_name: str  = None):
        forwarding_address = {
            "email": email
        }

        if name is not None:
            forwarding_address["name"] = name
        if filter_spam is not None:
            forwarding_address["filter_spam"] = filter_spam
        if use_agent_name is not None:
            forwarding_address["use_agent_name"] = use_agent_name

        return self._post("/emails", data={"forwarding_address": forwarding_address})


# =======================================================
# Filters
# =======================================================
class Filters(Resource):
    def createRule(self,
                   requester_email: str = None,
                   delivered_to:    str = None,
                   subject:         str = None,
                   body:            str = None):
        rule = {}

        if requester_email is not None:
            rule["requester_email"] = requester_email
        if delivered_to is not None:
            rule["delivered_to"] = delivered_to
        if subject is not None:
            rule["subject"] = subject
        if body is not None:
            rule["body"] = body

        if len(rule.keys()) == 0:
            return

        return self._post("/rules", data={"rule": rule})

    def createConsequence(self,
                          archive:     str = None,
                          spam:        str = None,
                          trash:       str = None,
                          label:       str = None,
                          assign_user: int = None,
                          assign_team: int = None):
        consequence = {}

        if archive is not None:
            consequence["archive"] = archive
        if spam is not None:
            consequence["spam"] = spam
        if trash is not None:
            consequence["trash"] = trash
        if label is not None:
            consequence["label"] = label
        if assign_user is not None:
            consequence["assign_user"] = assign_user
        if assign_team is not None:
            consequence["assign_team"] = assign_team

        if len(consequence.keys()) == 0:
            return

        return self._post("/consequences", data={"consequence": consequence})

    def create(self,
               consequence_id: int,
               rule_id:        int):
        _filter = {
            "consequence_id": consequence_id,
            "rule_id": rule_id
        }
        return self._post("/filters", data={"filter": _filter})


# =======================================================
# Snippets
# =======================================================
class Snippets(Resource):
    def fetch(self):
        return self._get("/snippets")

    def create(self,
               name:            str,
               content:         str  = None,
               tags:            list = None,
               content_as_html: bool = False):
        snippet = {
            "name": name,
        }

        if content is not None:
            snippet["content"] = {
                "html" if content_as_html else "text": content,
            }
        if tags is not None:
            snippet["tags"] = ",".join(tags)

        return self._post("/snippets", data={"snippet": snippet})

    def update(self,
               snippet_id:      str,
               name:            str  = None,
               content:         str  = None,
               tags:            list = None,
               content_as_html: bool = False):

        snippet = {}

        if name is not None:
            snippet["name"] = name
        if content is not None:
            snippet["content"] = {
                "html" if content_as_html else "text": content,
            }
        if tags is not None:
            snippet["tags"] = ",".join(tags)

        if len(snippet.keys()) == 0:
            return

        return self._put("/snippets/{snippet_id}".format(snippet_id=snippet_id), data={"snippet": snippet})

    def delete(self,
               snippet_id: str):
        return self._delete("/snippets/{snippet_id}".format(snippet_id=snippet_id))


# =======================================================
# Reports
# =======================================================
class Reports(Resource):
    def get(self,
            data_points_type: DataPointType,
            user:             str           = None,
            team:             str           = None,
            label:            str           = None,
            since:            str           = None,
            until:            str           = None):
        return self._get("/reports/{data_points_type}".format(data_points_type=data_points_type),
                         user=user,
                         team=team,
                         label=label,
                         since=since,
                         until=until)


class SupportBee:
    def __init__(self, token, company_url):
        self.BASE_URL = company_url + "{url}?auth_token=" + token

    @property
    def tickets(self):
        return Tickets(self)

    @property
    def replies(self):
        return Replies(self)

    @property
    def comments(self):
        return Comments(self)

    @property
    def teams(self):
        return Teams(self)

    @property
    def users(self):
        return Users(self)

    @property
    def customers_groups(self):
        return CustomerGroups(self)

    @property
    def attachments(self):
        return Attachments(self)

    @property
    def labels(self):
        return Labels(self)

    @property
    def emails(self):
        return Emails(self)

    @property
    def filters(self):
        return Filters(self)

    @property
    def snippets(self):
        return Snippets(self)

    @property
    def reports(self):
        return Reports(self)
