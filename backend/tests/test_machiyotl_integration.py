"""Integration test for the Machiyotl module end-to-end pipeline.

Covers: schema validation → audit trail → DB persistence → metadata safety.
Exercises all Machiyotl artifacts built so far (schemas + audit service) together.
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import select, func

from app.db.models import AuditLog, MachiyotlEvidenceItem
from app.db.session import create_session
from app.schemas.machiyotl import (
    ALLOWED_STATUS_TRANSITIONS,
    CustodyEventCreate,
    EvidenceItemCreate,
    EvidenceItemResponse,
    EvidenceNoteCreate,
    HashVerifyRequest,
)
from app.services.machiyotl.audit_service import (
    HASH_PREFIX_LENGTH,
    MACHIYOTL_AUDIT_ACTIONS,
    MachiyotlAuditService,
)
from tests.db_test_utils import migrate_and_seed_database


VALID_HASH = "9f2a7cd8e18b40a3c6f5e2d1b8a9c0d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0"
VALID_SHORT_HASH = "9f2a7c...d18b40"
NOW = datetime.now(timezone.utc).replace(microsecond=0)
FUTURE = datetime(2099, 1, 1, tzinfo=timezone.utc)


def _make_evidence_create(**overrides):
    defaults = {
        "evidence_type": "screenshot_placeholder",
        "sha256_hash": VALID_HASH,
        "short_hash": VALID_SHORT_HASH,
        "status": "draft",
        "privacy_state": "local-only",
        "captured_at": NOW,
    }
    return EvidenceItemCreate(**(defaults | overrides))


def _count_audit_rows(db, action: str) -> int:
    return db.scalar(
        select(func.count()).select_from(AuditLog).where(AuditLog.action == action)
    )


class TestFullEvidenceLifecycle:
    """Simulates a complete evidence lifecycle: create → seal → ready → note → custody → verify."""

    def test_full_pipeline(self) -> None:
        migrate_and_seed_database()

        with create_session() as db:
            audit = MachiyotlAuditService(db)

            # 1. CREATE — schema validates, audit writes
            create = _make_evidence_create()
            assert create.status == "draft"
            assert create.privacy_state == "local-only"

            audit.audit_evidence_create(
                entity_id="evd-001",
                metadata={
                    "evidence_code": "EVD-2026-INT-001",
                    "evidence_type": create.evidence_type,
                    "status": create.status,
                    "sha256_hash": create.sha256_hash,
                },
            )

            # 2. SEAL — transition d→r d→s-l is valid, audit writes with hash prefix
            assert "sealed-local" in ALLOWED_STATUS_TRANSITIONS["draft"]

            audit.audit_evidence_seal(
                entity_id="evd-001",
                metadata={
                    "from_status": "draft",
                    "to_status": "sealed-local",
                    "sha256_hash": create.sha256_hash,
                },
            )

            # 3. UPDATE — status transition from sealed-local → ready is valid
            assert "ready" in ALLOWED_STATUS_TRANSITIONS["sealed-local"]

            audit.audit_evidence_update(
                entity_id="evd-001",
                metadata={
                    "from_status": "sealed-local",
                    "to_status": "ready",
                },
            )

            # 4. NOTE — schema validates, audit strips content
            note = EvidenceNoteCreate(note="Nota de integración sobre el caso.")
            assert len(note.note) > 0

            audit.audit_note_create(
                entity_id="note-001",
                metadata={
                    "note": "ESTE TEXTO NUNCA DEBE APARECER EN AUDITORIA",
                    "evidence_code": "EVD-2026-INT-001",
                },
            )

            # 5. CUSTODY — schema validates event type
            custody = CustodyEventCreate(
                event_type="sealed_local",
                event_label="Evidencia sellada en prueba de integración",
                occurred_at=NOW,
            )
            assert custody.event_type == "sealed_local"

            audit.audit_custody_create(
                entity_id="cust-001",
                metadata={"event_type": custody.event_type},
            )

            # 6. HASH VERIFY — schema validates hash format
            verify = HashVerifyRequest(submitted_hash="sha256:" + VALID_HASH)
            assert verify.submitted_hash.startswith("sha256:")

            audit.audit_hash_verify(
                entity_id="ver-001",
                metadata={
                    "result": "match",
                    "submitted_hash": verify.submitted_hash,
                },
            )

            db.commit()

        # VERIFY in a fresh session
        with create_session() as db:
            for action in MACHIYOTL_AUDIT_ACTIONS.values():
                count = _count_audit_rows(db, action)
                assert count >= 1, f"Expected at least 1 audit row for action {action}, got {count}"

            note_audit = db.scalar(
                select(AuditLog).where(AuditLog.action == MACHIYOTL_AUDIT_ACTIONS["NOTE_CREATE"])
            )
            assert note_audit is not None
            assert "note" not in note_audit.metadata_json
            assert note_audit.metadata_json["evidence_code"] == "EVD-2026-INT-001"

            seal_audit = db.scalar(
                select(AuditLog).where(AuditLog.action == MACHIYOTL_AUDIT_ACTIONS["EVIDENCE_SEAL"])
            )
            assert seal_audit is not None
            assert seal_audit.metadata_json["hash_prefix"] == VALID_HASH[:HASH_PREFIX_LENGTH]
            assert "sha256_hash" not in seal_audit.metadata_json


class TestSchemaRejection:
    """Schema-level validation rejects bad payloads before any service runs."""

    def test_rejects_invalid_state(self) -> None:
        with pytest.raises(ValidationError):
            _make_evidence_create(status="not-a-real-state")

    def test_rejects_malformed_hash(self) -> None:
        with pytest.raises(ValidationError):
            _make_evidence_create(sha256_hash="not-hex!!!")

    def test_rejects_future_timestamp(self) -> None:
        with pytest.raises(ValidationError):
            _make_evidence_create(captured_at=FUTURE)

    def test_rejects_empty_note(self) -> None:
        with pytest.raises(ValidationError):
            EvidenceNoteCreate(note="")

    def test_rejects_invalid_custody_event_type(self) -> None:
        with pytest.raises(ValidationError):
            CustodyEventCreate(
                event_type="invalid_event_type",
                event_label="Label",
                occurred_at=NOW,
            )

    def test_rejects_invalid_hash_in_verify_request(self) -> None:
        with pytest.raises(ValidationError):
            HashVerifyRequest(submitted_hash="bad-hash-!!!")


class TestStatusTransitionGuard:
    """State machine rules encoded in ALLOWED_STATUS_TRANSITIONS."""

    def test_draft_to_submitted_is_blocked(self) -> None:
        assert "submitted" not in ALLOWED_STATUS_TRANSITIONS["draft"]

    def test_sealed_local_to_submitted_is_blocked(self) -> None:
        assert "submitted" not in ALLOWED_STATUS_TRANSITIONS["sealed-local"]

    def test_submitted_is_terminal(self) -> None:
        assert ALLOWED_STATUS_TRANSITIONS["submitted"] == []

    def test_error_recovers_to_draft(self) -> None:
        assert "draft" in ALLOWED_STATUS_TRANSITIONS["error"]


class TestAuditMetadataSafety:
    """Audit metadata never leaks sensitive fields."""

    def test_note_content_excluded(self) -> None:
        svc = MachiyotlAuditService(db=None)
        safe = svc.sanitize_metadata({
            "note": "contenido sensible que debe excluirse",
            "evidence_code": "EVD-001",
        })
        assert "note" not in safe
        assert safe["evidence_code"] == "EVD-001"

    def test_source_url_excluded(self) -> None:
        svc = MachiyotlAuditService(db=None)
        safe = svc.sanitize_metadata({
            "source_url": "https://private.example.com",
            "status": "draft",
        })
        assert "source_url" not in safe
        assert safe["status"] == "draft"

    def test_local_file_path_excluded(self) -> None:
        svc = MachiyotlAuditService(db=None)
        safe = svc.sanitize_metadata({
            "local_file_path": "/tmp/sensitive.dat",
            "platform": "demo",
        })
        assert "local_file_path" not in safe
        assert safe["platform"] == "demo"

    def test_original_filename_excluded(self) -> None:
        svc = MachiyotlAuditService(db=None)
        safe = svc.sanitize_metadata({
            "original_filename": "victim-screenshot.png",
            "mime_type": "image/png",
        })
        assert "original_filename" not in safe
        assert safe["mime_type"] == "image/png"

    def test_none_metadata_returns_empty(self) -> None:
        svc = MachiyotlAuditService(db=None)
        assert svc.sanitize_metadata(None) == {}


class TestDBPersistence:
    """Data written via audit service is found intact in a fresh session."""

    def test_audit_rows_persist_across_sessions(self) -> None:
        migrate_and_seed_database()
        evidence_id = str(uuid4())

        with create_session() as db:
            MachiyotlAuditService(db).audit_evidence_create(
                entity_id=evidence_id,
                metadata={"evidence_code": "EVD-PERSIST-001", "sha256_hash": VALID_HASH},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == evidence_id)
            )
        assert audit is not None
        assert audit.entity_schema == "machiyotl"
        assert audit.entity_table == "evidence_items"
        assert audit.outcome == "success"
        assert audit.action == MACHIYOTL_AUDIT_ACTIONS["EVIDENCE_CREATE"]
        assert audit.metadata_json["evidence_code"] == "EVD-PERSIST-001"
        assert audit.metadata_json["hash_prefix"] == VALID_HASH[:HASH_PREFIX_LENGTH]


class TestEvidenceItemResponse:
    """Response schema hydrates from ORM-like dicts."""

    def test_from_attributes_hydration(self) -> None:
        evidence_id = uuid4()
        data = {
            "id": evidence_id,
            "case_id": None,
            "owner_user_id": None,
            "evidence_code": "EVD-2026-INT-001",
            "evidence_type": "screenshot_placeholder",
            "platform": "demo",
            "source_url": None,
            "local_file_path": None,
            "original_filename": None,
            "mime_type": None,
            "size_bytes": None,
            "sha256_hash": VALID_HASH,
            "short_hash": VALID_SHORT_HASH,
            "status": "sealed-local",
            "privacy_state": "local-only",
            "captured_at": NOW,
            "sealed_at": NOW,
            "created_at": NOW,
        }
        item = EvidenceItemResponse.model_validate(data)
        assert item.id == evidence_id
        assert item.status == "sealed-local"
        assert item.sha256_hash == VALID_HASH
