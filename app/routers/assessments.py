from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.models import Assessment, User
from ..schemas.schemas import AssessmentCreate, AssessmentOut
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("", response_model=list[AssessmentOut])
def list_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Assessment)
        .filter(Assessment.specialist_id == current_user.id)
        .order_by(Assessment.date.desc())
        .all()
    )


@router.post("", response_model=AssessmentOut, status_code=201)
def create_assessment(
    body: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = body.model_dump()
    if data.get("date") is None:
        data["date"] = datetime.now(timezone.utc)
    assessment = Assessment(**data, specialist_id=current_user.id)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


@router.delete("/{assessment_id}", status_code=204)
def delete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    a = db.query(Assessment).filter(
        Assessment.id == assessment_id,
        Assessment.specialist_id == current_user.id,
    ).first()
    if a:
        db.delete(a)
        db.commit()
