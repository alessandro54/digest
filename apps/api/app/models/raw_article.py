from datetime import datetime
from app.models.source import Source
from sqlmodel import SQLModel, Column, Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB

class RawArticle(SQLModel, table=True):
    __tablename__ = "raw_articles"
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="sources.id", index=True)
    raw_id: str | None = Field(default=None, index=True)
    url: str = Field(index=True)
    payload_json: dict = Field(sa_column=Column(JSONB, nullable=False))
    fetched_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    source: "Source" = Relationship(back_populates="raw_articles")

