# scripts/seed_sources.py
# Run: poetry run python scripts/seed_sources.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "apps" / "api"))

from datetime import datetime
from typing import Iterable

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.db.init import engine  # your existing engine
from app.models.source import Source  # your SQLModel table

SEED_SOURCES: list[dict[str, str]] = [
    {
        "slug": "techcrunch",
        "feed_url": "https://techcrunch.com/feed/",
        "kind": "tech",
        "notes": "Startups & VC",
    },
    {
        "slug": "the-verge",
        "feed_url": "https://www.theverge.com/rss/index.xml",
        "kind": "tech",
    },
    {"slug": "wired", "feed_url": "https://www.wired.com/feed/rss", "kind": "tech"},
    {
        "slug": "coindesk",
        "feed_url": "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "kind": "crypto",
    },
    {
        "slug": "cointelegraph",
        "feed_url": "https://cointelegraph.com/rss",
        "kind": "crypto",
    },
    {
        "slug": "venturebeat",
        "feed_url": "https://venturebeat.com/feed/",
        "kind": "startups",
    },
    {
        "slug": "hackernews",
        "feed_url": "https://hnrss.org/frontpage",
        "kind": "community",
    },
    {
        "slug": "producthunt",
        "feed_url": "https://www.producthunt.com/feed",
        "kind": "startups",
    },
    {
        "slug": "reddit-programming",
        "feed_url": "https://www.reddit.com/r/programming/.rss",
        "kind": "dev",
    },
    {
        "slug": "arstechnica",
        "feed_url": "http://feeds.arstechnica.com/arstechnica/index",
        "kind": "tech",
    },
]


def seed(sources: Iterable[dict[str, str]]) -> None:
    print("🌱 Seeding sources ...")
    with Session(engine) as session, session.begin():  # single transaction
        # 1) Fetch existing slugs once (fast, ORM)
        want_slugs = [s["slug"] for s in sources]
        existing = set(
            session.exec(select(Source.slug).where(Source.slug.in_(want_slugs))).all()
        )

        created = 0
        for s in sources:
            if s["slug"] in existing:
                print(f"  ↺ exists: {s['slug']}")
                continue

            # 2) Try create (race-safe via IntegrityError)
            obj = Source(
                slug=s["slug"],
                feed_url=s["feed_url"],
                kind=s.get("kind", "tech"),
                enabled=True,
                cadence_minutes=60,
                timeout_sec=20,
                max_retries=3,
                priority=0,
                notes=s.get("notes"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(obj)
            try:
                session.flush()  # forces INSERT now; lets us catch duplicates here
                created += 1
                print(f"  ✅ added: {s['slug']}")
            except IntegrityError:
                # Another process inserted it first → rollback to savepoint & continue
                session.rollback()  # rollback the failed INSERT only; transaction stays open
                print(f"  ↺ raced/exists: {s['slug']}")

    print(f"✅ Done. Created: {created} | Skipped: {len(sources) - created}")


if __name__ == "__main__":
    seed(SEED_SOURCES)
