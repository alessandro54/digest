from sqlmodel import SQLModel
from datetime import datetime


class SourceCreate(SQLModel):
    slug: str
    feed_url: str
    kind: str = "tech"
    enabled: bool = True
    cadence_minutes: int = 60
    timeout_sec: int = 20
    max_retries: int = 3
    priority: int = 0
    notes: str | None = None


class SourceUpdate(SQLModel):
    feed_url: str | None = None
    kind: str | None = None
    enabled: bool | None = None
    cadence_minutes: int | None = None
    timeout_sec: int | None = None
    max_retries: int | None = None
    priority: int | None = None
    notes: str | None = None
    last_run_at: datetime | None = None
