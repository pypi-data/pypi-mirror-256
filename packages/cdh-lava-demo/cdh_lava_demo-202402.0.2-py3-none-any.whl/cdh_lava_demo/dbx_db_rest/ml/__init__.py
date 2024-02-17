from cdh_lava_demo.dbx_db_rest import cdh_lava_demoRestClient
from cdh_lava_demo.dbx_rest import ApiContainer


class MlClient(ApiContainer):
    def __init__(self, client: cdh_lava_demoRestClient):
        self.client = client  # Client API exposing other operations to this class

        from cdh_lava_demo.dbx_db_rest.ml.feature_store import FeatureStoreClient

        self.feature_store = FeatureStoreClient(self.client)

        from cdh_lava_demo.dbx_db_rest.ml.mlflow import MLflowClient

        self.mlflow = MLflowClient(self.client)
