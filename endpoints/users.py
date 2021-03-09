from .base import Resource, UserRoles


# =======================================================
# Users
# =======================================================
class Users(Resource):
    def fetch(self,
              with_invited: bool = False,
              with_roles:   list = (UserRoles.ADMIN, UserRoles.AGENT, UserRoles.COLLABORATOR)):
        roles = ",".join([role.value[0] for role in with_roles])
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
            user["role"] = role.value[1]
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
            user["role"] = role.value[1]
        if team_ids is not None:
            user["team_ids"] = ",".join(team_ids)

        if len(user.keys()) == 1:
            return  # No update called

        return self._post("/users/{user_id}".format(user_id=user_id), data={"user": user})
