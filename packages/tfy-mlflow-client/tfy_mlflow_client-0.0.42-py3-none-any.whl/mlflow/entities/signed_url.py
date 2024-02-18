from mlflow.protos import mlfoundry_artifacts_pb2 as mlfa_pb2
from mlflow.pydantic_v1 import BaseModel


class SignedURL(BaseModel):
    path: str
    url: str

    @classmethod
    def from_proto(cls, message: mlfa_pb2.SignedURL) -> "SignedURL":
        return cls(path=message.path, url=message.signed_url)

    def to_proto(self):
        return mlfa_pb2.SignedURL(path=self.path, signed_url=self.url)
