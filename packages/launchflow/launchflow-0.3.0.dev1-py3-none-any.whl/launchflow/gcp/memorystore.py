# Handling imports and missing dependencies
try:
    import redis
except ImportError:
    redis = None

from pydantic import BaseModel

from launchflow.resource import Resource


class MemorystoreRedisConnectionInfo(BaseModel):
    host: str
    port: int
    password: str


class MemorystoreRedis(Resource[MemorystoreRedisConnectionInfo]):

    def __init__(self, name: str, *, memory_size_gb: int = 1) -> None:
        super().__init__(
            name=name,
            provider_product_type="gcp_memorystore_redis",
            create_args={
                "memory_size_gb": memory_size_gb,
                # TODO: Determine the right place for the "preview" bit to live.
                # Should this be on the environment?
                # In this specific case, the preview version doesnt use memorystore, so
                # maybe it should only be on the generic Redis type?
                "preview": True,
            },
        )
        self._connection_info = self._load_connection(
            MemorystoreRedisConnectionInfo.model_validate
        )

        if redis is None:
            raise ImportError(
                "redis library is not installed. Please install it with `pip install redis`."
            )

        self._async_pool = None
        self._sync_client = None

    def redis(self):
        if self._sync_client is None:
            self._sync_client = redis.Redis(
                host=self._connection_info.host,
                port=self._connection_info.port,
                password=self._connection_info.password,
                decode_responses=True,
            )
        return self._sync_client

    async def redis_async(self):
        if self._async_pool is None:
            self._async_pool = await redis.asyncio.from_url(
                f"redis://{self._connection_info.host}:{self._connection_info.port}",
                password=self._connection_info.password,
                decode_responses=True,
            )
        return self._async_pool
