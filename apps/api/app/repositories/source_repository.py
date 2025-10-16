from __future__ import annotations
from sqlmodel import Session, select
from app.models.source import Source


class SourceRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self, kind: str | None = None, enabled: bool | None = None
    ) -> list[Source]:
        stmt = select(Source)
        if kind is not None:
            stmt = stmt.where(Source.kind == kind)
        if enabled is not None:
            stmt = stmt.where(Source.enabled == enabled)
        stmt = stmt.order_by(Source.priority.desc(), Source.slug.asc())
        return self.session.exec(stmt).all()

    def get_by_slug(self, slug: str) -> Source | None:
        return self.session.exec(select(Source).where(Source.slug == slug)).first()

    def create(self, src: Source) -> Source:
        self.session.add(src)
        self.session.commit()
        self.session.refresh(src)
        return src

    def update(self, src: Source) -> Source:
        self.session.add(src)
        self.session.commit()
        self.session.refresh(src)
        return src

    def delete(self, src: Source) -> None:
        self.session.delete(src)
        self.session.commit()
