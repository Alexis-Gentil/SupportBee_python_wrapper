from .base import Resource, BasicOptions, AssignedUserOptions, AssignedTeamOptions, SortByOptions


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
