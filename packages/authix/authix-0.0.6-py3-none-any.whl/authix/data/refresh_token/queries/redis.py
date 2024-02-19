from datetime import timedelta
from typing import Optional
from uuid import UUID

from pydantic import UUID4
from redis import StrictRedis

from authix.data.query_exceptions import QueryResultNotFoundError
from authix.data.refresh_token.refresh_token_queries import RefreshQueries


class RedisRefreshQueries(RefreshQueries):
    def __init__(self, dsn: str) -> None:
        self._redis = StrictRedis.from_url(
            url=dsn,
            encoding="utf-8",
            decode_responses=True,
        )

    async def get_user_id(self, refresh_token: str) -> UUID4:
        user_id: Optional[str] = self._redis.get(refresh_token)
        if user_id is None:
            raise QueryResultNotFoundError
        return UUID(user_id)

    async def add(self, refresh_token: str, user_id: UUID4) -> None:
        self._redis.set(refresh_token, str(user_id), ex=timedelta(weeks=4))

    async def delete(self, refresh_token: str) -> UUID4:
        user_id = await self.get_user_id(refresh_token=refresh_token)
        self._redis.delete(refresh_token)
        return user_id
