from .base import Resource, DataPointType


# =======================================================
# Reports
# =======================================================
class Reports(Resource):
    def get(self,
            data_points_type: DataPointType,
            user:             str           = None,
            team:             str           = None,
            label:            str           = None,
            since:            str           = None,
            until:            str           = None):
        return self._get("/reports/{data_points_type}".format(data_points_type=data_points_type),
                         user=user,
                         team=team,
                         label=label,
                         since=since,
                         until=until)
