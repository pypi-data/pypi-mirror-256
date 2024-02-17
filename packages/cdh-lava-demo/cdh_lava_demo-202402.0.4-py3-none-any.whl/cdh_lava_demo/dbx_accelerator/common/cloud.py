__all__ = ["Cloud"]

from enum import Enum


from enum import Enum


class Cloud(Enum):
    """
    Represents the cloud provider for the current workspace.
    """

    AWS = "AWS"
    MSA = "MSA"
    GCP = "GCP"
    UNKNOWN = "UNKNOWN"

    @property
    def is_aws(self) -> bool:
        """
        Checks if the cloud provider is AWS.
        :return: True if the cloud provider is AWS, False otherwise.
        """
        return self == Cloud.AWS

    @property
    def is_msa(self) -> bool:
        """
        Checks if the cloud provider is MSA.
        :return: True if the cloud provider is MSA, False otherwise.
        """
        return self == Cloud.MSA

    @property
    def is_gcp(self) -> bool:
        """
        Checks if the cloud provider is GCP.
        :return: True if the cloud provider is GCP, False otherwise.
        """
        return self == Cloud.GCP

    @staticmethod
    def current_cloud() -> "Cloud":
        """
        Indicates which cloud the current workspace is deployed into.
        :return: One of GCP, AWS, MSA, or UNKNOWN if the current cloud cannot be auto-determined.
        """
        import os

        config_path = "/databricks/common/conf/deploy.conf"
        if not os.path.exists(config_path):
            return Cloud.UNKNOWN

        with open(config_path) as f:
            for line in f:
                if (
                    "databricks.instance.metadata.cloudProvider" in line
                    and '"GCP"' in line
                ):
                    return Cloud.GCP
                elif (
                    "databricks.instance.metadata.cloudProvider" in line
                    and '"AWS"' in line
                ):
                    return Cloud.AWS
                elif (
                    "databricks.instance.metadata.cloudProvider" in line
                    and '"Azure"' in line
                ):
                    return Cloud.MSA

        return Cloud.UNKNOWN
