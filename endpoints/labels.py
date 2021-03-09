from .base import Resource


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
