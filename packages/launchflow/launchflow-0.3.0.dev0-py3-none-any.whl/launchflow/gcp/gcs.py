try:
    from google.cloud import storage
except ImportError:
    storage = None


from pydantic import BaseModel

from launchflow.resource import Resource


class GCSBucketConnectionInfo(BaseModel):
    bucket_name: str


class GCSBucket(Resource[GCSBucketConnectionInfo]):
    """A GCS Bucket resource.

    **Attributes**:
    - `name` (str): The name of the bucket This must be globally unique.
    - `location` (str): The location of the bucket. Defaults to "US".

    Example usage:
    ```python
    import launchflow as lf

    bucket = lf.gcp.GCSBucket("my-bucket")
    lf.bucket().blob("my-file").upload_from_filename("my-file")
    ```
    """

    def __init__(self, name: str, *, location="US") -> None:
        super().__init__(
            name=name,
            provider_product_type="gcp_storage_bucket",
            create_args={"location": location},
        )
        # public metadata
        self.location = location
        # load connection_info
        self._connection_info = self._load_connection(
            GCSBucketConnectionInfo.model_validate
        )
        if storage is None:
            raise ImportError(
                "google-cloud-storage not found. "
                "You can install it with pip install launchflow[gcp]"
            )

    def bucket(self):
        """Get the GCS bucket object returned by the google-cloud-storage library.

        **Returns**:
        - The [GCS bucket object](https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.bucket.Bucket) from the GCS client library.
        """
        if self._connection_info is None:
            raise RuntimeError(f"Connection info not found for {self}.")
        return storage.Client().get_bucket(self._connection_info.bucket_name)
