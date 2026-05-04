"""
Storage adapters with pluggable backends: local filesystem, S3, Azure Blob.
Selected at startup via STORAGE_BACKEND env variable.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import shutil

from app.config import settings
from app.logging_config import logger


class StorageAdapter(ABC):
    @abstractmethod
    def put_file(self, local_path: str, object_key: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_signed_url(self, object_key: str, expires_in: int = 3600) -> str:
        raise NotImplementedError

    @abstractmethod
    def exists(self, object_key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, object_key: str) -> None:
        raise NotImplementedError


# ── Local filesystem ──────────────────────────────────────────────────────────

class LocalStorageAdapter(StorageAdapter):
    def __init__(self, base_dir: str) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def put_file(self, local_path: str, object_key: str) -> str:
        destination = self.base_dir / object_key
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(local_path, destination)
        logger.info("storage.put_file", object_key=object_key, backend="local")
        return str(destination)

    def get_signed_url(self, object_key: str, expires_in: int = 3600) -> str:
        return f"/artifacts/{object_key}"

    def exists(self, object_key: str) -> bool:
        return (self.base_dir / object_key).exists()

    def delete(self, object_key: str) -> None:
        path = self.base_dir / object_key
        if path.exists():
            path.unlink()


# ── S3 ────────────────────────────────────────────────────────────────────────

class S3StorageAdapter(StorageAdapter):
    def __init__(self) -> None:
        import boto3
        self._client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self._bucket = settings.s3_bucket

    def put_file(self, local_path: str, object_key: str) -> str:
        self._client.upload_file(local_path, self._bucket, object_key)
        logger.info("storage.put_file", object_key=object_key, backend="s3")
        return object_key

    def get_signed_url(self, object_key: str, expires_in: int = 3600) -> str:
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": object_key},
            ExpiresIn=expires_in,
        )

    def exists(self, object_key: str) -> bool:
        from botocore.exceptions import ClientError
        try:
            self._client.head_object(Bucket=self._bucket, Key=object_key)
            return True
        except ClientError:
            return False

    def delete(self, object_key: str) -> None:
        self._client.delete_object(Bucket=self._bucket, Key=object_key)


# ── Azure Blob ────────────────────────────────────────────────────────────────

class AzureBlobStorageAdapter(StorageAdapter):
    def __init__(self) -> None:
        from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
        from datetime import timedelta
        self._service = BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )
        self._container = settings.azure_container_name
        self._BlobSasPermissions = BlobSasPermissions
        self._generate_blob_sas = generate_blob_sas
        self._timedelta = timedelta

    def put_file(self, local_path: str, object_key: str) -> str:
        blob = self._service.get_blob_client(container=self._container, blob=object_key)
        with open(local_path, "rb") as data:
            blob.upload_blob(data, overwrite=True)
        logger.info("storage.put_file", object_key=object_key, backend="azure")
        return object_key

    def get_signed_url(self, object_key: str, expires_in: int = 3600) -> str:
        from datetime import datetime, timezone
        account = self._service.account_name
        account_key = self._service.credential.account_key
        sas = self._generate_blob_sas(
            account_name=account,
            container_name=self._container,
            blob_name=object_key,
            account_key=account_key,
            permission=self._BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + self._timedelta(seconds=expires_in),
        )
        return f"https://{account}.blob.core.windows.net/{self._container}/{object_key}?{sas}"

    def exists(self, object_key: str) -> bool:
        blob = self._service.get_blob_client(container=self._container, blob=object_key)
        return blob.exists()

    def delete(self, object_key: str) -> None:
        blob = self._service.get_blob_client(container=self._container, blob=object_key)
        blob.delete_blob()


# ── Factory ───────────────────────────────────────────────────────────────────

def _build_storage() -> StorageAdapter:
    backend = settings.storage_backend.lower()
    if backend == "s3":
        return S3StorageAdapter()
    if backend == "azure":
        return AzureBlobStorageAdapter()
    return LocalStorageAdapter(settings.local_storage_dir)


storage: StorageAdapter = _build_storage()
