from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from src.photoshare.core.config import settings

# ==========================================
# Database Connection & Session Management
# ==========================================


class DatabaseHelper:
    """
    Manages asynchronous engine lifecycle and constructs execution sessions
    leveraging SQLAlchemy's network pool architecture.
    """

    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        # Configure and spin up the core asynchronous engine
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        # Establish the factory pipeline for issuing detached transactions
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """
        Gracefully tears down underlying database sockets and drops active connections.
        """
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Asynchronous context generator yielding database sessions.
        Ensures proper resource disposal and connection closing upon lifecycle completion.
        Suitable for FastAPI dependency injection.
        """
        async with self.session_factory() as session:
            yield session


# ==========================================
# Global Database Helper Instance
# ==========================================

# Instantiated application wide database resource initialized via configuration profiles
db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
