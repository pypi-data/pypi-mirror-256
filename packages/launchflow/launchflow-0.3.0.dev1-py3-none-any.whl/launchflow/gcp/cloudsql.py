# Handling imports and missing dependencies
try:
    from google.cloud.sql.connector import Connector, IPTypes, create_async_connector
except ImportError:
    Connector = None
    IPTypes = None
    create_async_connector = None

try:
    import asyncpg
except ImportError:
    asyncpg = None

try:
    import pg8000
except ImportError:
    pg8000 = None

try:
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
except ImportError:
    async_sessionmaker = None
    create_async_engine = None

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import DeclarativeBase, sessionmaker
except ImportError:
    create_engine = None
    DeclarativeBase = None
    sessionmaker = None

# Importing the required modules

from pydantic import BaseModel

from launchflow.resource import Resource


# Connection information model
class CloudSQLPostgresConnectionInfo(BaseModel):
    connection_name: str
    user: str
    password: str
    database: str


class CloudSQLPostgres(Resource[CloudSQLPostgresConnectionInfo]):

    # TODO: Add postgres version as an argument
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            provider_product_type="gcp_sql_postgres",
            create_args={
                # TODO: move this to EnvironmentConfig
                "preview": True,
            },
        )
        # load connection_info
        self._connection_info = self._load_connection(
            CloudSQLPostgresConnectionInfo.model_validate
        )

    def sqlalchemy_engine(self, *, ip_type=IPTypes.PUBLIC, **engine_kwargs):
        if create_engine is None:
            raise ImportError(
                "SQLAlchemy is not installed. Please install it with "
                "`pip install sqlalchemy`."
            )
        if Connector is None or IPTypes is None or create_async_connector is None:
            raise ImportError(
                "google-cloud-sql-connector not installed. Please install it with "
                "`pip install launchflow[gcp]`."
            )
        if pg8000 is None:
            raise ImportError(
                "pg8000 is not installed. Please install it with `pip install pg8000`."
            )
        connector = Connector(ip_type)

        # initialize Connector object for connections to Cloud SQL
        def getconn():
            conn = connector.connect(
                instance_connection_string=self._connection_info.connection_name,
                driver="pg8000",
                user=self._connection_info.user,
                password=self._connection_info.password,
                db=self._connection_info.database,
            )
            return conn

        return create_engine("postgresql+pg8000://", creator=getconn, **engine_kwargs)

    async def sqlalchemy_async_engine(self, *, ip_type=IPTypes.PUBLIC, **engine_kwargs):
        if create_async_engine is None:
            raise ImportError(
                "SQLAlchemy asyncio extension is not installed. "
                "Please install it with `pip install sqlalchemy[asyncio]`."
            )
        if Connector is None or IPTypes is None or create_async_connector is None:
            raise ImportError(
                "google-cloud-sql-connector not installed. Please install it with "
                "`pip install launchflow[gcp]`."
            )
        if asyncpg is None:
            raise ImportError(
                "asyncpg is not installed. Please install it with `pip install asyncpg`."
            )
        connector = await create_async_connector()

        # initialize Connector object for connections to Cloud SQL
        async def getconn():
            conn = await connector.connect_async(
                instance_connection_string=self._connection_info.connection_name,
                driver="asyncpg",
                user=self._connection_info.user,
                password=self._connection_info.password,
                db=self._connection_info.database,
                ip_type=ip_type,
            )
            return conn

        return create_async_engine(
            "postgresql+asyncpg://", async_creator=getconn, **engine_kwargs
        )
