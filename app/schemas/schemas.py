from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# ── Auth ──────────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role_name: str
    mode: str = "specialist"
    clinical: bool = False
    emoji: str = "🧑‍🏫"
    role_description: str = ""


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role_name: str
    mode: str
    clinical: bool
    emoji: str
    role_description: str

    model_config = {"from_attributes": True}


# ── Children ──────────────────────────────────────────────────────────────────

class ChildCreate(BaseModel):
    name: str
    age: int
    color_hex: str = "#FF6B35"
    percentile: str = "—"
    pre_score: int = 0
    post_score: int = 0


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    color_hex: Optional[str] = None
    percentile: Optional[str] = None
    pre_score: Optional[int] = None
    post_score: Optional[int] = None


class ChildOut(BaseModel):
    id: int
    name: str
    age: int
    color_hex: str
    percentile: str
    pre_score: int
    post_score: int

    model_config = {"from_attributes": True}


# ── Assessments ───────────────────────────────────────────────────────────────

class AssessmentCreate(BaseModel):
    child_name: str
    age_years: int = 9
    date: Optional[datetime] = None

    placing_pegs: int
    threading_lace: int
    drawing_trail: int
    catching: int
    throwing: int
    one_board_balance: int
    walking_heel_toe: int
    hopping_mats: int

    # Flutter tomonidan hisoblangan natijalar
    total_raw: int = 0
    total_standard_score: int = 0
    total_percentile: float = 0.0
    zone: str = "green"

    child_id: Optional[int] = None


class AssessmentOut(AssessmentCreate):
    id: int
    specialist_id: int

    model_config = {"from_attributes": True}


# ── Report ────────────────────────────────────────────────────────────────────

class DomainStats(BaseModel):
    md: float
    ac: float
    bal: float
    total: float


class ReportSummary(BaseModel):
    pretest: DomainStats
    posttest: DomainStats
    child_count: int
    assessment_count: int
