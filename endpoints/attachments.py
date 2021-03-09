from .base import Resource


# =======================================================
# Attachments
# =======================================================
class Attachments(Resource):
    def create(self,
               filename: str,
               file: bytes):
        files = {
            "files[]": (filename, file, "multipart/form-data")
        }
        return self._post("/attachments", files=files)
