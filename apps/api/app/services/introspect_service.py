import feedparser, time
from typing import Any
from sqlmodel import Session
from app.repositories.source_repository import SourceRepo
from app.core.errors import NotFoundError, DisabledError


def _tname(v: Any) -> str:
    if v is None:
        return "NoneType"
    if isinstance(v, time.struct_time):
        return "struct_time"
    return type(v).__name__


def _schema(entry: Any) -> dict[str, str]:
    return {
        str(k): _tname(v) for k, v in (entry.items() if hasattr(entry, "items") else [])
    }


def _preview(entry: Any) -> dict[str, str | None]:
    def take(x: Any, n=220):
        if not isinstance(x, str):
            return None
        x = x.strip()
        return (x[: n - 1] + "…") if len(x) > n else (x or None)

    content_val = None
    content = getattr(entry, "content", None)
    if isinstance(content, list) and content and isinstance(content[0], dict):
        content_val = content[0].get("value")
    return {
        "title": take(getattr(entry, "title", None)),
        "link": take(getattr(entry, "link", None), 140),
        "author": take(getattr(entry, "author", None)),
        "published": take(getattr(entry, "published", None)),
        "summary": take(content_val) or take(getattr(entry, "summary", None)),
    }


class IntrospectService:
    def __init__(self, session: Session) -> None:
        self.repo = SourceRepo(session)

    def run(self, slug: str) -> dict[str, object]:
        src = self.repo.get_by_slug(slug)
        if not src:
            raise NotFoundError("source not found")
        if not src.enabled:
            raise DisabledError("source disabled")

        parsed = feedparser.parse(
            src.feed_url, request_headers={"User-Agent": "Digest/Introspect 0.1"}
        )
        entries = parsed.entries or []

        if not entries:
            return {
                "slug": slug,
                "feed_url": src.feed_url,
                "status": getattr(parsed, "status", None),
                "items": 0,
                "schema": {},
                "namespaces": list(getattr(parsed, "namespaces", {}).keys())
                if hasattr(parsed, "namespaces")
                else [],
                "samples": [],
            }

        N = min(3, len(entries))
        merged: dict[str, str] = {}
        for e in entries[:N]:
            for k, t in _schema(e).items():
                merged[k] = t if k not in merged else (t if merged[k] == t else "mixed")

        return {
            "slug": slug,
            "feed_url": src.feed_url,
            "status": getattr(parsed, "status", None),
            "items": len(entries),
            "schema": dict(sorted(merged.items(), key=lambda kv: kv[0])),
            "namespaces": list(getattr(parsed, "namespaces", {}).keys())
            if hasattr(parsed, "namespaces")
            else [],
            "samples": [
                {"schema": _schema(e), "preview": _preview(e)} for e in entries[:N]
            ],
        }
