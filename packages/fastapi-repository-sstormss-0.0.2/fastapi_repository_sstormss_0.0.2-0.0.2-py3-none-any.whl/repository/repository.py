from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select, insert


class BaseRepository(ABC):

    @abstractmethod
    async def create(self, data: dict = None, obj: Any = None):
        raise NotImplementedError

    @abstractmethod
    async def get(self, obj: Any = None):
        raise NotImplementedError

    @abstractmethod
    async def update(self):
        raise NotImplementedError

    @abstractmethod
    async def delete(self):
        raise NotImplementedError

    @abstractmethod
    async def all(self):
        raise NotImplementedError


class MemoryRepository(BaseRepository):

    def __init__(self):
        self.objects = dict()

    async def check(self, obj: str) -> bool:
        if obj in list(self.objects.keys()):
            return False
        return True

    async def create(self, obj: str, data: dict = None) -> bool:
        if await self.check(obj):
            self.objects[obj] = data
            return True
        return False

    async def get(self, obj: str) -> list or bool:
        if obj in list(self.objects.keys()):
            return self.objects[obj]
        else:
            return False

    async def update(self):
        pass

    async def delete(self, obj: str):
        self.objects.pop(obj)
        return True

    async def append(self, obj: str, websocket: str):
        if await self.check(obj):
            return False
        self.objects.get(obj).append(websocket)
        return True

    async def remove(self, obj: str, data: str) -> bool:
        if self.objects.get(obj).remove(data):
            return True
        return False

    async def all(self) -> dict:
        listing = {}
        for i in list(self.objects.keys()):
            listing[i] = self.objects[i]
        # print(listing)
        return listing


class SQLAlchemyRepository(BaseRepository):
    model = None

    async def get(self, session, **filters):
        async with session() as session:
            try:
                obj = await session.scalar(select(self.model).filter_by(**filters))
                return obj
            except Exception:
                return None

    async def create(self, data: dict, session):
        async with session() as session:
            obj = await session.scalar(insert(self.model).returning(self.model), data)
            await session.refresh(obj)
            await session.commit()
            return obj.to_read_model()

    async def update(self, *args, **kwargs):
        pass

    async def delete(self, session, **filters):
        async with session() as session:
            try:
                obj = await session.scalar(select(self.model).filter_by(**filters))
                await session.delete(obj)
                await session.commit()
                return True
            except Exception:
                return False

    async def all(self, session):
        async with session() as session:
            try:
                obj = await session.scalars(select(self.model))
                return obj
            except Exception:
                return None
