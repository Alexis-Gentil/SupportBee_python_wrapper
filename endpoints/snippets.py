from .base import Resource


# =======================================================
# Snippets
# =======================================================
class Snippets(Resource):
    def fetch(self):
        return self._get("/snippets")

    def create(self,
               name:            str,
               content:         str  = None,
               tags:            list = None,
               content_as_html: bool = False):
        snippet = {
            "name": name,
        }

        if content is not None:
            snippet["content"] = {
                "html" if content_as_html else "text": content,
            }
        if tags is not None:
            snippet["tags"] = ",".join(tags)

        return self._post("/snippets", data={"snippet": snippet})

    def update(self,
               snippet_id:      str,
               name:            str  = None,
               content:         str  = None,
               tags:            list = None,
               content_as_html: bool = False):

        snippet = {}

        if name is not None:
            snippet["name"] = name
        if content is not None:
            snippet["content"] = {
                "html" if content_as_html else "text": content,
            }
        if tags is not None:
            snippet["tags"] = ",".join(tags)

        if len(snippet.keys()) == 0:
            return

        return self._put("/snippets/{snippet_id}".format(snippet_id=snippet_id), data={"snippet": snippet})

    def delete(self,
               snippet_id: str):
        return self._delete("/snippets/{snippet_id}".format(snippet_id=snippet_id))
