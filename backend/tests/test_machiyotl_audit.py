from uuid import uuid4

from sqlalchemy import select

from app.db.models import AuditLog
from app.db.session import create_session
from app.services.machiyotl.audit_service import (
    ENTITY_SCHEMA,
    FORBIDDEN_METADATA_FIELDS,
    HASH_PREFIX_LENGTH,
    MACHIYOTL_AUDIT_ACTIONS,
    MachiyotlAuditService,
)
from tests.db_test_utils import migrate_and_seed_database


NOW_ISO = "2026-05-15T14:35:00Z"
EXPECTED_ACTIONS = {
    "EVIDENCE_CREATE",
    "EVIDENCE_UPDATE",
    "EVIDENCE_SEAL",
    "NOTE_CREATE",
    "CUSTODY_CREATE",
    "HASH_VERIFY",
}


class TestActionConstants:
    def test_all_expected_actions_defined(self) -> None:
        assert EXPECTED_ACTIONS.issubset(MACHIYOTL_AUDIT_ACTIONS.keys())

    def test_all_actions_follow_naming_convention(self) -> None:
        for action in MACHIYOTL_AUDIT_ACTIONS.values():
            assert action.startswith("machiyotl.")
            assert len(action.split(".")) == 3

    def test_no_duplicate_action_values(self) -> None:
        values = list(MACHIYOTL_AUDIT_ACTIONS.values())
        assert len(values) == len(set(values))


class TestAuditEvidenceCreate:
    def test_writes_audit_row_with_expected_fields(self) -> None:
        migrate_and_seed_database()
        evidence_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_evidence_create(
                entity_id=evidence_id,
                metadata={"evidence_code": "EVD-DEMO-001", "sha256_hash": "a" * 64},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == evidence_id)
            )
            assert audit is not None
            assert audit.action == MACHIYOTL_AUDIT_ACTIONS["EVIDENCE_CREATE"]
            assert audit.entity_schema == ENTITY_SCHEMA
            assert audit.entity_table == "evidence_items"
            assert audit.outcome == "success"
            assert audit.metadata_json["evidence_code"] == "EVD-DEMO-001"

    def test_hash_is_sanitized_to_prefix(self) -> None:
        migrate_and_seed_database()
        evidence_id = str(uuid4())
        full_hash = "a" * 64

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_evidence_create(
                entity_id=evidence_id,
                metadata={"sha256_hash": full_hash},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == evidence_id)
            )
            assert audit is not None
            assert audit.metadata_json["hash_prefix"] == full_hash[:HASH_PREFIX_LENGTH]
            assert "sha256_hash" not in audit.metadata_json


class TestAuditEvidenceUpdate:
    def test_writes_audit_with_status_transition_metadata(self) -> None:
        migrate_and_seed_database()
        evidence_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_evidence_update(
                entity_id=evidence_id,
                metadata={"from_status": "draft", "to_status": "sealed-local"},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == evidence_id)
            )
            assert audit is not None
            assert audit.action == MACHIYOTL_AUDIT_ACTIONS["EVIDENCE_UPDATE"]
            assert audit.entity_table == "evidence_items"
            assert audit.metadata_json["from_status"] == "draft"
            assert audit.metadata_json["to_status"] == "sealed-local"


class TestAuditEvidenceSeal:
    def test_writes_audit_with_hash_prefix(self) -> None:
        migrate_and_seed_database()
        evidence_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_evidence_seal(
                entity_id=evidence_id,
                metadata={"event_type": "sealed_local", "sha256_hash": "b" * 64},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == evidence_id)
            )
            assert audit is not None
            assert audit.action == MACHIYOTL_AUDIT_ACTIONS["EVIDENCE_SEAL"]
            assert audit.metadata_json["event_type"] == "sealed_local"
            assert audit.metadata_json["hash_prefix"] == "b" * HASH_PREFIX_LENGTH


class TestAuditNoteCreate:
    def test_note_content_is_excluded_from_metadata(self) -> None:
        migrate_and_seed_database()
        note_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_note_create(
                entity_id=note_id,
                metadata={
                    "note": "Contenido sensible que nunca debe aparecer en auditoría",
                    "evidence_code": "EVD-DEMO-002",
                },
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == note_id)
            )
            assert audit is not None
            assert audit.action == MACHIYOTL_AUDIT_ACTIONS["NOTE_CREATE"]
            assert audit.entity_table == "evidence_notes"
            assert "note" not in audit.metadata_json
            assert audit.metadata_json["evidence_code"] == "EVD-DEMO-002"

    def test_note_exists_flag_can_be_set(self) -> None:
        migrate_and_seed_database()
        note_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_note_create(
                entity_id=note_id,
                metadata={"note_exists": True},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == note_id)
            )
            assert audit.metadata_json["note_exists"] is True


class TestAuditCustodyCreate:
    def test_writes_audit_with_event_type_metadata(self) -> None:
        migrate_and_seed_database()
        event_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_custody_create(
                entity_id=event_id,
                metadata={"event_type": "sealed_local"},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == event_id)
            )
            assert audit is not None
            assert audit.action == MACHIYOTL_AUDIT_ACTIONS["CUSTODY_CREATE"]
            assert audit.entity_table == "custody_events"
            assert audit.metadata_json["event_type"] == "sealed_local"


class TestAuditHashVerify:
    def test_writes_audit_with_result_metadata(self) -> None:
        migrate_and_seed_database()
        verification_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_hash_verify(
                entity_id=verification_id,
                metadata={"result": "match", "submitted_hash": "c" * 64},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == verification_id)
            )
            assert audit is not None
            assert audit.action == MACHIYOTL_AUDIT_ACTIONS["HASH_VERIFY"]
            assert audit.entity_table == "hash_verifications"
            assert audit.metadata_json["result"] == "match"
            assert audit.metadata_json["hash_prefix"] == "c" * HASH_PREFIX_LENGTH


class TestAuditFailureOutcome:
    def test_writes_audit_with_failure_outcome(self) -> None:
        migrate_and_seed_database()
        evidence_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_evidence_create(
                outcome="failure",
                entity_id=evidence_id,
                metadata={"error": "invalid_hash_format"},
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == evidence_id)
            )
            assert audit is not None
            assert audit.outcome == "failure"
            assert audit.metadata_json["error"] == "invalid_hash_format"


class TestMetadataSanitization:
    def test_strips_forbidden_fields_completely(self) -> None:
        service = MachiyotlAuditService(db=None)
        raw = {
            "note": "texto sensible",
            "source_url": "https://example.com/private",
            "local_file_path": "/tmp/evidence.dat",
            "original_filename": "captura.png",
            "evidence_code": "EVD-001",
            "status": "draft",
        }
        safe = service.sanitize_metadata(raw)
        for field in FORBIDDEN_METADATA_FIELDS:
            assert field not in safe, f"forbidden field {field} leaked"
        assert safe["evidence_code"] == "EVD-001"
        assert safe["status"] == "draft"

    def test_preserves_hash_prefix(self) -> None:
        service = MachiyotlAuditService(db=None)
        full_hash = "f" * 64
        safe = service.sanitize_metadata({"sha256_hash": full_hash})
        assert "sha256_hash" not in safe
        assert safe["hash_prefix"] == full_hash[:HASH_PREFIX_LENGTH]
        assert len(safe["hash_prefix"]) == HASH_PREFIX_LENGTH

    def test_excludes_oversized_values(self) -> None:
        service = MachiyotlAuditService(db=None)
        safe = service.sanitize_metadata({"safe_field": "x" * 200})
        assert "safe_field" not in safe

    def test_handles_none_metadata(self) -> None:
        service = MachiyotlAuditService(db=None)
        safe = service.sanitize_metadata(None)
        assert safe == {}


class TestAuditWithoutActor:
    def test_audit_works_without_actor(self) -> None:
        migrate_and_seed_database()
        evidence_id = str(uuid4())

        with create_session() as db:
            svc = MachiyotlAuditService(db)
            svc.audit_evidence_create(
                entity_id=evidence_id,
                actor_user_id=None,
            )
            db.commit()

        with create_session() as db:
            audit = db.scalar(
                select(AuditLog).where(AuditLog.entity_id == evidence_id)
            )
            assert audit is not None
            assert audit.actor_user_id is None
            assert audit.outcome == "success"
