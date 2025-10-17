from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from .source import Source


class Article(SQLModel, table=True):
    __tablename__ = "articles"  # o "articles_norm" si así lo definiste en la migración
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="sources.id", index=True)
    raw_id: str | None = Field(default=None, index=True)
    url: str = Field(index=True)
    url_hash: str = Field(index=True)

    title: str
    author: str | None = None
    published_at: datetime | None = None

    tags_json: list[str] | None = Field(default=None, sa_column=Column(JSONB))

    content_html: str | None = None
    content_html_sanitized: str | None = None
    summary_text: str
    image_url: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    source: "Source" = Relationship(back_populates="articles")
