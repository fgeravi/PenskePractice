"""A small thread-safe cache with time-based expiration."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from time import monotonic
from typing import Generic, TypeVar


KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


@dataclass
class CacheEntry(Generic[ValueType]):
    """Store a cached value and the time at which it expires."""

    value: ValueType
    expires_at: float


class TTLCache(Generic[KeyType, ValueType]):
    """Store values until their configured time-to-live expires."""

    def __init__(self, default_ttl_seconds: float = 60.0) -> None:
        if default_ttl_seconds <= 0:
            raise ValueError("Default TTL must be greater than zero.")

        self._default_ttl_seconds = default_ttl_seconds
        self._entries: dict[KeyType, CacheEntry[ValueType]] = {}
        self._lock = RLock()

    def set(
        self,
        key: KeyType,
        value: ValueType,
        ttl_seconds: float | None = None,
    ) -> None:
        """Insert or replace a cached value."""

        ttl = self._default_ttl_seconds if ttl_seconds is None else ttl_seconds

        if ttl <= 0:
            raise ValueError("TTL must be greater than zero.")

        entry = CacheEntry(
            value=value,
            expires_at=monotonic() + ttl,
        )

        with self._lock:
            self._entries[key] = entry

    def get(self, key: KeyType) -> ValueType | None:
        """Return a value if it exists and has not expired."""

        with self._lock:
            entry = self._entries.get(key)

            if entry is None:
                return None

            if entry.expires_at <= monotonic():
                del self._entries[key]
                return None

            return entry.value

    def delete(self, key: KeyType) -> bool:
        """Delete a key and return whether it previously existed."""

        with self._lock:
            return self._entries.pop(key, None) is not None

    def clear_expired(self) -> int:
        """Remove every expired entry and return the number removed."""

        current_time = monotonic()

        with self._lock:
            expired_keys = [
                key
                for key, entry in self._entries.items()
                if entry.expires_at <= current_time
            ]

            for key in expired_keys:
                del self._entries[key]

        return len(expired_keys)

    def __contains__(self, key: KeyType) -> bool:
        """Support expressions such as: if key in cache."""

        return self.get(key) is not None

    def __len__(self) -> int:
        """Return the number of active, non-expired entries."""

        self.clear_expired()

        with self._lock:
            return len(self._entries)


def main() -> None:
    session_cache: TTLCache[str, dict[str, object]] = TTLCache(
        default_ttl_seconds=30
    )

    session_cache.set(
        "car-12",
        {
            "driver": "Ryan Blaney",
            "last_lap": 29.88,
        },
    )

    session = session_cache.get("car-12")

    if session is None:
        print("Session was not found.")
    else:
        print(f"Cached driver: {session['driver']}")
        print(f"Cached lap: {session['last_lap']} seconds")

    print(f"Active entries: {len(session_cache)}")


if __name__ == "__main__":
    main()