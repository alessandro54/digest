from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate
from app.db.init import get_session

router = APIRouter()


@router.get("/", response_model=List[Source])
def list_sources(
    kind: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    session: Session = Depends(get_session),
):
    stmt = select(Source)
    if kind:
        stmt = stmt.where(Source.kind == kind)
    if enabled is not None:
        stmt = stmt.where(Source.enabled == enabled)
    stmt = stmt.order_by(Source.priority.desc(), Source.slug.asc())
    return session.exec(stmt).all()


@router.get("/{slug}", response_model=Source)
def get_source(slug: str, session: Session = Depends(get_session)):
    src = session.exec(select(Source).where(Source.slug == slug)).first()
    if not src:
        raise HTTPException(404, "Source not found")
    return src


@router.post("/", response_model=Source, status_code=201)
def create_source(payload: SourceCreate, session: Session = Depends(get_session)):
    if session.exec(select(Source).where(Source.slug == payload.slug)).first():
        raise HTTPException(409, "Slug already exists")
    src = Source(**payload.dict())
    session.add(src)
    session.commit()
    session.refresh(src)
    return src


@router.patch("/{slug}", response_model=Source)
def update_source(
    slug: str, patch: SourceUpdate, session: Session = Depends(get_session)
):
    src = session.exec(select(Source).where(Source.slug == slug)).first()
    if not src:
        raise HTTPException(404, "Source not found")
    for k, v in patch.dict(exclude_unset=True).items():
        setattr(src, k, v)
    src.updated_at = datetime.utcnow()
    session.add(src)
    session.commit()
    session.refresh(src)
    return src


@router.delete("/{slug}", status_code=204)
def delete_source(slug: str, session: Session = Depends(get_session)):
    src = session.exec(select(Source).where(Source.slug == slug)).first()
    if not src:
        raise HTTPException(404, "Source not found")
    session.delete(src)
    session.commit()
    return None
