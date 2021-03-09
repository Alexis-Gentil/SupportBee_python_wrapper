from .base import Resource


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
