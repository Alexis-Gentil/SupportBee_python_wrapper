from .base import Resource


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
