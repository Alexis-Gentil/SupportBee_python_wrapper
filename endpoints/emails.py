from .base import Resource


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
