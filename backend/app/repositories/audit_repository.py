from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    db_log: AuditLog
):

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return db_log