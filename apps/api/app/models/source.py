from typing import TYPE_CHECKING, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .raw_article import RawArticle
    from .article import Article


class Source(SQLModel, table=True):
    __tablename__ = "sources"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True)
    feed_url: str
    kind: str = Field(default="rss")
    enabled: bool = Field(default=True)
    cadence_minutes: int = Field(default=60)
    priority: int = Field(default=1)
    last_run_at: datetime | None = None
    last_status: str | None = None
    last_error: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 👇 Usa List[...] y referencias en string
    raw_articles: List["RawArticle"] = Relationship(back_populates="source")
    articles: List["Article"] = Relationship(back_populates="source")
