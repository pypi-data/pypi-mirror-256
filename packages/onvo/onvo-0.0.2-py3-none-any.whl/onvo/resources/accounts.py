from . import Resource


class Accounts(Resource):
    def list(self):
        self.get("/accounts")

    def get(self, id):
        self.get("/accounts/{id}".format(id=id))
