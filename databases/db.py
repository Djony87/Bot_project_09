from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

# Настройка базы данных
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Выодит все логи БД
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Пример модели
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    full_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())

# Асинхронный генератор сессий
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Создание таблиц
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)