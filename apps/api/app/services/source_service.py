from __future__ import annotations
from datetime import datetime
from sqlmodel import Session
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate
from app.repositories.source_repository import SourceRepo
from app.core.errors import NotFoundError, ConflictError


class SourceService:
    def __init__(self, session: Session) -> None:
        self.repo = SourceRepo(session)

    # CRUD
    def list(self, kind: str | None, enabled: bool | None) -> list[Source]:
        return self.repo.list(kind, enabled)

    def get(self, slug: str) -> Source:
        src = self.repo.get_by_slug(slug)
        if not src:
            raise NotFoundError("source not found")
        return src

    def create(self, payload: SourceCreate) -> Source:
        if self.repo.get_by_slug(payload.slug):
            raise ConflictError("slug already exists")
        src = Source(**payload.dict())
        return self.repo.create(src)

    def update(self, slug: str, patch: SourceUpdate) -> Source:
        src = self.get(slug)
        for k, v in patch.dict(exclude_unset=True).items():
            setattr(src, k, v)
        src.updated_at = datetime.utcnow()
        return self.repo.update(src)

    def delete(self, slug: str) -> None:
        src = self.get(slug)
        self.repo.delete(src)
