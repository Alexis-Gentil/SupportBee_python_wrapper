from .base import Resource, UserRoles


# =======================================================
# Customer Groups
# =======================================================
class CustomerGroups(Resource):
    def fetch(self,
              with_invited: bool = False,
              with_roles:   list = (UserRoles.ADMIN, UserRoles.AGENT, UserRoles.COLLABORATOR)):
        roles = ",".join([role.value[0] for role in with_roles])
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
            customer_group["role"] = role.value[1]
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
            customer_group["role"] = role.value[1]
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
