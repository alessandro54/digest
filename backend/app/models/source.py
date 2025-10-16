# models_source.py
from __future__ import annotations
from sqlmodel import SQLModel, Field
from datetime import datetime


class Source(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    feed_url: str
    kind: str = Field(default="tech")  # "tech" | "crypto" | "dev"
    enabled: bool = Field(default=True)
    cadence_minutes: int = Field(default=60)
    timeout_sec: int = Field(default=20)
    max_retries: int = Field(default=3)
    priority: int = Field(default=0)
    last_run_at: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    notes: str | None = None
