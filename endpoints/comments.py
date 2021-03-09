from .base import Resource


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
