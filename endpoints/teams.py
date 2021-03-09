from .base import Resource


# =======================================================
# Teams
# =======================================================
class Teams(Resource):
    def fetch(self,
              only_with_users: bool = False,
              only_mine:       bool = False):
        user = "me" if only_mine else ""
        return self._get("/teams", with_users=only_with_users, user=user)
