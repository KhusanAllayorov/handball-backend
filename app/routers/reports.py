from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.models import Assessment, Child, User
from ..schemas.schemas import DomainStats, ReportSummary
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/summary", response_model=ReportSummary)
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessments = (
        db.query(Assessment)
        .filter(Assessment.specialist_id == current_user.id)
        .order_by(Assessment.date.asc())
        .all()
    )

    child_count = (
        db.query(Child)
        .filter(Child.specialist_id == current_user.id)
        .count()
    )

    if not assessments:
        empty = DomainStats(md=0, ac=0, bal=0, total=0)
        return ReportSummary(
            pretest=empty,
            posttest=empty,
            child_count=child_count,
            assessment_count=0,
        )

    def _avg_domain(items):
        if not items:
            return DomainStats(md=0, ac=0, bal=0, total=0)
        n = len(items)
        return DomainStats(
            md=round(sum(
                (a.placing_pegs + a.threading_lace + a.drawing_trail) / 3
                for a in items
            ) / n, 2),
            ac=round(sum(
                (a.catching + a.throwing) / 2
                for a in items
            ) / n, 2),
            bal=round(sum(
                (a.one_board_balance + a.walking_heel_toe + a.hopping_mats) / 3
                for a in items
            ) / n, 2),
            total=round(sum(a.total_raw for a in items) / n, 2),
        )

    half = max(1, len(assessments) // 2)
    pre_items = assessments[:half]
    post_items = assessments[half:]

    return ReportSummary(
        pretest=_avg_domain(pre_items),
        posttest=_avg_domain(post_items),
        child_count=child_count,
        assessment_count=len(assessments),
    )
