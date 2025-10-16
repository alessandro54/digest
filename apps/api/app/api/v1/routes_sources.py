from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.db.init import get_session
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate
from app.services.source_service import SourceService
from app.services.introspect_service import IntrospectService
from app.core.errors import NotFoundError, ConflictError, DisabledError

router = APIRouter()


def src_svc(session: Session = Depends(get_session)) -> SourceService:
    return SourceService(session)


def intro_svc(session: Session = Depends(get_session)) -> IntrospectService:
    return IntrospectService(session)


@router.get("/", response_model=List[Source])
def list_sources(
    kind: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    svc: SourceService = Depends(src_svc),
):
    return svc.list(kind, enabled)


@router.get("/{slug}", response_model=Source)
def get_source(slug: str, svc: SourceService = Depends(src_svc)):
    try:
        return svc.get(slug)
    except NotFoundError as e:
        raise HTTPException(404, str(e))


@router.post("/", response_model=Source, status_code=201)
def create_source(payload: SourceCreate, svc: SourceService = Depends(src_svc)):
    try:
        return svc.create(payload)
    except ConflictError as e:
        raise HTTPException(409, str(e))


@router.patch("/{slug}", response_model=Source)
def update_source(
    slug: str, patch: SourceUpdate, svc: SourceService = Depends(src_svc)
):
    try:
        return svc.update(slug, patch)
    except NotFoundError as e:
        raise HTTPException(404, str(e))


@router.delete("/{slug}", status_code=204)
def delete_source(slug: str, svc: SourceService = Depends(src_svc)):
    try:
        svc.delete(slug)
        return None
    except NotFoundError as e:
        raise HTTPException(404, str(e))


@router.post("/{slug}/introspect/")
def introspect_source(slug: str, svc: IntrospectService = Depends(intro_svc)):
    try:
        return svc.run(slug)
    except NotFoundError as e:
        raise HTTPException(404, str(e))
    except DisabledError as e:
        raise HTTPException(409, str(e))
