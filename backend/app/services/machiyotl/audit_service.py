from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import AuditLog
from app.schemas.machiyotl import SHA256_MAX_LENGTH

HASH_PREFIX_LENGTH = 12
ENTITY_SCHEMA = "machiyotl"

MACHIYOTL_AUDIT_ACTIONS = {
    "EVIDENCE_CREATE": "machiyotl.evidence.create",
    "EVIDENCE_UPDATE": "machiyotl.evidence.update",
    "EVIDENCE_SEAL": "machiyotl.evidence.seal",
    "NOTE_CREATE": "machiyotl.note.create",
    "CUSTODY_CREATE": "machiyotl.custody.create",
    "HASH_VERIFY": "machiyotl.hash.verify",
}

HASH_FIELDS = {"sha256_hash", "submitted_hash", "event_hash"}

FORBIDDEN_METADATA_FIELDS = {
    "note",
    "source_url",
    "local_file_path",
    "original_filename",
} | HASH_FIELDS


class MachiyotlAuditError(ValueError):
    pass


class MachiyotlAuditService:

    def __init__(self, db: Session) -> None:
        self.db = db

    def audit_evidence_create(
        self,
        outcome: str = "success",
        actor_user_id: UUID | None = None,
        entity_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        return self._write_audit(
            action=MACHIYOTL_AUDIT_ACTIONS["EVIDENCE_CREATE"],
            outcome=outcome,
            actor_user_id=actor_user_id,
            entity_table="evidence_items",
            entity_id=entity_id,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def audit_evidence_update(
        self,
        outcome: str = "success",
        actor_user_id: UUID | None = None,
        entity_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        return self._write_audit(
            action=MACHIYOTL_AUDIT_ACTIONS["EVIDENCE_UPDATE"],
            outcome=outcome,
            actor_user_id=actor_user_id,
            entity_table="evidence_items",
            entity_id=entity_id,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def audit_evidence_seal(
        self,
        outcome: str = "success",
        actor_user_id: UUID | None = None,
        entity_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        return self._write_audit(
            action=MACHIYOTL_AUDIT_ACTIONS["EVIDENCE_SEAL"],
            outcome=outcome,
            actor_user_id=actor_user_id,
            entity_table="evidence_items",
            entity_id=entity_id,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def audit_note_create(
        self,
        outcome: str = "success",
        actor_user_id: UUID | None = None,
        entity_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        return self._write_audit(
            action=MACHIYOTL_AUDIT_ACTIONS["NOTE_CREATE"],
            outcome=outcome,
            actor_user_id=actor_user_id,
            entity_table="evidence_notes",
            entity_id=entity_id,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def audit_custody_create(
        self,
        outcome: str = "success",
        actor_user_id: UUID | None = None,
        entity_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        return self._write_audit(
            action=MACHIYOTL_AUDIT_ACTIONS["CUSTODY_CREATE"],
            outcome=outcome,
            actor_user_id=actor_user_id,
            entity_table="custody_events",
            entity_id=entity_id,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def audit_hash_verify(
        self,
        outcome: str = "success",
        actor_user_id: UUID | None = None,
        entity_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        return self._write_audit(
            action=MACHIYOTL_AUDIT_ACTIONS["HASH_VERIFY"],
            outcome=outcome,
            actor_user_id=actor_user_id,
            entity_table="hash_verifications",
            entity_id=entity_id,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def sanitize_metadata(self, metadata: dict | None) -> dict:
        if metadata is None:
            return {}
        safe: Dict[str, Any] = {}
        for key, value in metadata.items():
            if key in FORBIDDEN_METADATA_FIELDS:
                continue
            if isinstance(value, str) and len(value) > SHA256_MAX_LENGTH:
                continue
            safe[key] = value
        for hash_field in HASH_FIELDS:
            hash_value = metadata.get(hash_field)
            if hash_value and isinstance(hash_value, str):
                safe["hash_prefix"] = hash_value[:HASH_PREFIX_LENGTH]
                break
        return safe

    def _write_audit(
        self,
        action: str,
        outcome: str,
        actor_user_id: UUID | None = None,
        entity_table: str | None = None,
        entity_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        safe_metadata = self.sanitize_metadata(metadata)
        audit_log = AuditLog(
            action=action,
            outcome=outcome,
            actor_user_id=actor_user_id,
            entity_schema=ENTITY_SCHEMA,
            entity_table=entity_table,
            entity_id=entity_id,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata_json=safe_metadata,
        )
        self.db.add(audit_log)
        return audit_log
