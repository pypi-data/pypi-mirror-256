from uuid import UUID

from pydantic import NonNegativeInt
from tinydb import Query, TinyDB

from .base import BaseEngine


class TinyDBEngine(BaseEngine):
    db: TinyDB
    path: str
    table: str

    def __init__(self, path: str, table: str) -> None:
        self.db = TinyDB(path)
        self.table = table

    def _get(self, resource_id: UUID, raise_exception: bool = True) -> dict:
        try:
            result = self.db.table(self.table).search(Query().resource_id == str(resource_id))
            assert result or not raise_exception, "not found"
        except AssertionError as exception:
            raise self.exception(self.status.HTTP_404_NOT_FOUND, exception.args[0]) from exception
        else:
            return result[0] if len(result) else {}

    async def insert_one(self, resource_id: UUID, resource_obj: dict) -> dict:
        self.db.table(self.table).insert({"resource_id": str(resource_id), "resource_obj": resource_obj})
        return {"id": resource_id, **resource_obj}

    async def select_one(self, resource_id: UUID) -> dict:
        result = self._get(resource_id)
        return {"id": resource_id, **result["resource_obj"]}

    async def update_one(self, resource_id: UUID, resource_obj: dict) -> dict:
        self._get(resource_id)
        self.db.table(self.table).update({"resource_obj": resource_obj}, Query().resource_id == str(resource_id))
        return {"id": resource_id, **resource_obj}

    async def delete_one(self, resource_id: UUID) -> None:
        self._get(resource_id)
        self.db.table(self.table).remove(Query().resource_id == str(resource_id))
        return

    async def select_many(self, skip: NonNegativeInt = 0, limit: NonNegativeInt = 100) -> list[dict]:
        return [{"id": result["resource_id"], **result["resource_obj"]} for result in self.db.table(self.table).all()][
            skip:limit
        ]
