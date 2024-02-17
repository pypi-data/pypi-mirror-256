from cdh_lava_demo.dbx_db_rest import cdh_lava_demoRestClient
from cdh_lava_demo.dbx_rest import ApiContainer


class SqlClient(ApiContainer):
    def __init__(self, client: cdh_lava_demoRestClient):
        self.client = client  # Client API exposing other operations to this class

        from cdh_lava_demo.dbx_db_rest.sql.config import SqlConfigClient

        self.config = SqlConfigClient(self.client)

        from cdh_lava_demo.dbx_db_rest.sql.endpoints import SqlEndpointsClient

        self.endpoints = SqlEndpointsClient(self.client)

        from cdh_lava_demo.dbx_db_rest.sql.queries import SqlQueriesClient

        self.queries = SqlQueriesClient(self.client)

        self.permissions = client.permissions.sql
