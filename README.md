# 🧠 Digest

**Digest** is a lightweight platform that aggregates and curates the latest content from **tech, startup, and crypto** news sources through RSS feeds.
It provides a **FastAPI backend** for data ingestion and a **SvelteKit admin panel** for managing sources and future automation workflows.

---

## ⚙️ Stack

| Layer | Tech |
|-------|------|
| Backend | **FastAPI**, **SQLModel**, **Poetry**, **PostgreSQL** |
| Frontend | **SvelteKit**, **TypeScript**, **TailwindCSS** |
| Dev tools | **Makefile**, **pnpm**, **Alembic** |

---

## 🚀 Run locally

### 1️⃣ Start the API
```bash
make run-api
```
Runs the FastAPI backend on
👉 **http://localhost:8000**

---

### 2️⃣ Start the Admin UI
```bash
make run-ui
```
Runs the SvelteKit admin panel on
👉 **http://localhost:5173**

---

That’s it — the API and UI connect automatically if you’re running both locally.
