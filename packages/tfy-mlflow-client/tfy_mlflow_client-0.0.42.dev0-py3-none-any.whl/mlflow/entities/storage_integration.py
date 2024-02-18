import re
from enum import Enum
from typing import Any, Dict, Optional, TypeVar, Union

from typing_extensions import Annotated, Literal

from mlflow.exceptions import MlflowException
from mlflow.pydantic_v1 import BaseModel, Field, parse_obj_as, root_validator


class IntegrationType(str, Enum):
    STORAGE_INTEGRATION = "STORAGE_INTEGRATION"


class IntegrationProvider(str, Enum):
    AWS_S3 = "aws-s3"
    GCP_GCS = "gcp-gcs"
    AZURE_BLOB = "azure-blob"


class StorageIntegrationMetadata(BaseModel):
    storageRoot: str


class BaseCredentials(BaseModel):
    class Config:
        extra = "allow"


class GCSCredentials(BaseCredentials):
    keyFileContent: Dict[str, Any]


class AWSS3Credentials(BaseCredentials):
    awsAccessKeyId: Optional[str] = None
    awsSecretAccessKey: Optional[str] = None
    region: Optional[str] = None
    assumedRoleArn: Optional[str] = None


class AzureBlobCredentials(BaseCredentials):
    connectionString: str


class BaseStorageIntegration(BaseModel):
    id: str
    name: str
    fqn: str
    tenantName: str
    type: IntegrationType
    integrationProvider: IntegrationProvider
    metaData: StorageIntegrationMetadata
    authData: Optional[BaseCredentials] = None

    @root_validator(pre=True)
    def check_empty_auth_data(cls, values):
        if not values.get("authData"):
            values["authData"] = None
        return values

    def get_storage_root(self) -> str:
        if self.integrationProvider == IntegrationProvider.AZURE_BLOB:
            storageRoot = (
                self.metaData.storageRoot
                if self.metaData.storageRoot.endswith("/")
                else self.metaData.storageRoot + "/"
            )
            match = re.match(
                r"https://(?P<storage_account>[^.]+)\.blob\.core\.windows\.net/(?P<container_name>[^/]+)/(?P<path>.*)",
                storageRoot,
            )
            if not match:
                raise MlflowException(
                    "Invalid Azure Blob Storage URI: {}, for storage integration: {}".format(
                        storageRoot, self.fqn
                    )
                )
            container_name = match.group("container_name")
            storage_account_name = match.group("storage_account")
            path = match.group("path") or ""
            return f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/{path}"
        return self.metaData.storageRoot


class AWSStorageIntegration(BaseStorageIntegration):
    integrationProvider: Literal[IntegrationProvider.AWS_S3] = IntegrationProvider.AWS_S3
    authData: Optional[AWSS3Credentials] = None


class GCSStorageIntegration(BaseStorageIntegration):
    integrationProvider: Literal[IntegrationProvider.GCP_GCS] = IntegrationProvider.GCP_GCS
    authData: Optional[GCSCredentials] = None


class AzureBlobStorageIntegration(BaseStorageIntegration):
    integrationProvider: Literal[IntegrationProvider.AZURE_BLOB] = IntegrationProvider.AZURE_BLOB
    authData: Optional[AzureBlobCredentials] = None


_StorageIntegration = Annotated[
    Union[AWSStorageIntegration, GCSStorageIntegration, AzureBlobStorageIntegration],
    Field(..., discriminator="integrationProvider"),
]

StorageIntegration = TypeVar("StorageIntegration", bound=BaseStorageIntegration)


def storage_integration_from_dict(dct: Dict[str, Any]) -> StorageIntegration:
    return parse_obj_as(_StorageIntegration, dct)
