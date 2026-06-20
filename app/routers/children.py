from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.models import Child, User
from ..schemas.schemas import ChildCreate, ChildOut, ChildUpdate
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/children", tags=["children"])


@router.get("", response_model=List[ChildOut])
def list_children(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Child).filter(Child.specialist_id == current_user.id).all()


@router.post("", response_model=ChildOut, status_code=201)
def create_child(
    body: ChildCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    child = Child(**body.model_dump(), specialist_id=current_user.id)
    db.add(child)
    db.commit()
    db.refresh(child)
    return child


@router.put("/{child_id}", response_model=ChildOut)
def update_child(
    child_id: int,
    body: ChildUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    child = db.query(Child).filter(
        Child.id == child_id, Child.specialist_id == current_user.id
    ).first()
    if not child:
        raise HTTPException(status_code=404, detail="Bola topilmadi")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(child, field, value)
    db.commit()
    db.refresh(child)
    return child


@router.delete("/{child_id}", status_code=204)
def delete_child(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    child = db.query(Child).filter(
        Child.id == child_id, Child.specialist_id == current_user.id
    ).first()
    if not child:
        raise HTTPException(status_code=404, detail="Bola topilmadi")
    db.delete(child)
    db.commit()
