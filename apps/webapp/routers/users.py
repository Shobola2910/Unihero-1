from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from apps.webapp.deps import db_session
from shared.models import User

router = APIRouter(prefix="/users", tags=["users"])

class ApproveIn(BaseModel):
    tg_id: int

@router.get("")
def list_users(approved: bool | None = Query(default=None), s: Session = Depends(db_session)):
    q = s.query(User)
    if approved is not None:
        q = q.filter_by(approved=approved)
    return [
        {
            "tg_id": u.tg_id,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "phone": u.phone,
            "student_id": u.student_id,
            "approved": u.approved,
            "created_at": str(u.created_at) if u.created_at else None,
        }
        for u in q.order_by(User.created_at.desc().nullslast()).all()
    ]

@router.post("/approve")
def approve_user(payload: ApproveIn, s: Session = Depends(db_session)):
    u = s.query(User).filter_by(tg_id=payload.tg_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.approved = True
    s.add(u); s.commit()
    return {"ok": True, "approved_tg_id": payload.tg_id}
