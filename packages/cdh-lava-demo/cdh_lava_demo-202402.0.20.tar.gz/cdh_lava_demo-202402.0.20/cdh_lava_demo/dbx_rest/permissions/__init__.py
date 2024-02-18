from cdh_lava_demo.dbx_rest import ApiContainer, ApiClient

__all__ = ["Permissions"]


class Permissions(ApiContainer):
    def __init__(self, client: ApiClient):
        self.client = client

        from cdh_lava_demo.rest.permissions.clusters import Clusters

        self.clusters = Clusters(client)

        from cdh_lava_demo.rest.permissions.directories import Directories

        self.directories = Directories(client)

        from cdh_lava_demo.rest.permissions.jobs import Jobs

        self.jobs = Jobs(client)

        from cdh_lava_demo.rest.permissions.pools import Pools

        self.pools = Pools(client)

        from cdh_lava_demo.rest.permissions.sql import Sql

        self.sql = Sql(client)

        from cdh_lava_demo.rest.permissions.cluster_policies import ClusterPolicies

        self.cluster_policies = ClusterPolicies(client)

        from cdh_lava_demo.rest.permissions.warehouses import Warehouses

        self.warehouses = Warehouses(client)

        class Authorization:
            def __init__(self):
                from cdh_lava_demo.rest.permissions.authorization_tokens import Tokens

                self.tokens = Tokens(client)

        self.authorizations = Authorization()
