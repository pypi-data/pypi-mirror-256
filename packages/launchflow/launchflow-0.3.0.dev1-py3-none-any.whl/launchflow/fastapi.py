try:
    from sqlalchemy.orm import Session, sessionmaker
except ImportError:
    Session = None
    sessionmaker = None


class _SQLAlchemyDep:
    def __init__(
        self,
        engine,
        expire_on_commit: bool,
        autoflush: bool,
    ):
        self.engine = engine
        self._SessionLocal = sessionmaker(
            expire_on_commit=expire_on_commit, autoflush=autoflush, bind=engine
        )

    def __call__(self):
        with self._SessionLocal() as db:
            yield db


def sqlalchemy(engine, expire_on_commit: bool = False, autoflush: bool = False):
    if Session is None or sessionmaker is None:
        raise ImportError(
            "Requires `sqlalchemy` library, which is not installed. Install with `pip install sqlalchemy`."
        )
    return _SQLAlchemyDep(
        engine, expire_on_commit=expire_on_commit, autoflush=autoflush
    )
