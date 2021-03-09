from endpoints import base
from endpoints.tickets import Tickets
from endpoints.replies import Replies
from endpoints.comments import Comments
from endpoints.teams import Teams
from endpoints.users import Users
from endpoints.customer_groups import CustomerGroups
from endpoints.attachments import Attachments
from endpoints.labels import Labels
from endpoints.emails import Emails
from endpoints.filters import Filters
from endpoints.snippets import Snippets
from endpoints.reports import Reports

# Enums
BasicOptions        = base.BasicOptions
AssignedUserOptions = base.AssignedUserOptions
AssignedTeamOptions = base.AssignedTeamOptions
SortByOptions       = base.SortByOptions
UserRoles           = base.UserRoles
DataPointType       = base.DataPointType


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
