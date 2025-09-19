"""DB initialization logic"""

import yaml
from pathlib import Path
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy import text, select

from src.bot.db.models import Base
from src.bot.db.models import User


class DatabaseInitializer:
    """Class for DB initialization"""

    def __init__(
            self,
            engine: AsyncEngine,
            session_factory: async_sessionmaker[AsyncSession],
            schema_name: str = "public",
            seeds_path: Path | None = None
    ):
        """Initialize the DatabaseInitializer object

        Args:
            engine (AsyncEngine): async database engine
            session_factory (async_sessionmaker): factory for AsyncSession
            schema_name (str): schema name, default is "public"
            seeds_path (Path | None): path to seed files directory
        """
        self._engine = engine
        self._session_factory = session_factory
        self._schema_name = schema_name
        self._seeds_path = seeds_path or (Path(__file__).parent / "seeds")

        self._seed_map: dict[str, type] = {
            "users.yaml": User,
        }

    async def ensure_schema(self):
        """Create schema if it does not exist

        Returns:
            None
        """
        async with self._engine.begin() as conn:
            await conn.execute(text(
                f"CREATE SCHEMA IF NOT EXISTS {self._schema_name}"
            ))

    async def create_tables(self):
        """Create all tables from Base metadata

        Returns:
            None
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def _load_yaml(self, filename: str) -> list[dict]:
        """Load YAML file as list of dicts

        Args:
            filename (str): yaml file name inside seeds folder

        Returns:
            list[dict]: parsed list of rows
        """
        file_path = self._seeds_path / filename
        if not file_path.exists():
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or []
    
    async def _insert_if_empty(
            self,
            session: AsyncSession,
            model: type,
            data: list[dict]
    ):
        """Insert data into table if it is empty

        Args:
            session (AsyncSession): active database session
            model (type): ORM model class
            data (list[dict]): list of rows to insert

        Returns:
            None
        """
        if not data:
            return
        result = await session.execute(select(model))

        if not result.scalars().first():
            session.add_all(
                [model(**row) for row in data]
            )
    
    async def seed_test_data(self):
        """Seed all test data from YAML files

        Returns:
            None
        """
        async with self._session_factory() as session:
            for filename, model in self._seed_map.items():
                data = self._load_yaml(filename)
                await self._insert_if_empty(
                    session,
                    model,
                    data
                )
            await session.commit()

    async def initialize(self):
        """Run full initialization cycle:
        ensure schema, create tables and seed data

        Returns:
            None
        """
        await self.ensure_schema()
        await self.create_tables()
        await self.seed_test_data()
