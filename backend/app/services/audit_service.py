from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog

from app.repositories.audit_repository import create_audit_log


def log_audit_event(
    db: Session,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    metadata: str = None
):

    db_log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata=metadata
    )

    return create_audit_log(
        db=db,
        db_log=db_log
    )