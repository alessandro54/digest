from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .source import Source


class RawArticle(SQLModel, table=True):
    __tablename__ = "articles_raw"

    id: int | None = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="sources.id", index=True)
    raw_id: str | None = Field(default=None, index=True)
    url: str = Field(index=True)
    payload_json: dict = Field(sa_column=Column(JSONB, nullable=False))
    fetched_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    source: "Source" = Relationship(back_populates="raw_articles")
