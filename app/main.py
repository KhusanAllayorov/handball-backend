from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from .database import engine, Base
from .models import models  # noqa: F401 — trigger table registration
from .routers import auth, children, assessments, reports, static_content

Base.metadata.create_all(bind=engine)


def _run_migrations() -> None:
    """Mavjud jadvalga yetishmayotgan ustunlarni qo'shadi.

    `create_all` mavjud jadvalga yangi ustun qo'shmaydi, shuning uchun
    `password_plain` kabi keyin qo'shilgan ustunlarni qo'lda ALTER qilamiz.
    SQLite va PostgreSQL ikkalasida ham ishlaydi.
    """
    inspector = inspect(engine)
    user_columns = {c["name"] for c in inspector.get_columns("users")}
    if "password_plain" not in user_columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN password_plain VARCHAR"))


_run_migrations()

app = FastAPI(
    title="Handball Coordination API",
    description="DCD bolalar uchun mini-gandbol metodik ekotizimi — backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # prod da Flutter app URL ga o'zgartiring
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(children.router)
app.include_router(assessments.router)
app.include_router(reports.router)
app.include_router(static_content.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Handball Coordination API v1.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
