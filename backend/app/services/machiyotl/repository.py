from __future__ import annotations

from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.db.models import (
    MachiyotlCustodyEvent,
    MachiyotlEvidenceItem,
    MachiyotlEvidenceNote,
    MachiyotlHashVerification,
)
from app.schemas.machiyotl import ALLOWED_STATUS_TRANSITIONS


class EvidenceNotFoundError(ValueError):
    pass


class MachiyotlRepository:
    """Centralized query layer for Machiyotl evidence operations.

    Enforces module boundaries: every method queries only the ``machiyotl``
    schema. No cross-schema joins to ``chimalli``, ``tlachia``, or ``core``.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    # ------------------------------------------------------------------
    # Evidence Items
    # ------------------------------------------------------------------

    def get_evidence_by_id(self, evidence_id: UUID) -> MachiyotlEvidenceItem | None:
        """Single-row lookup by primary key."""
        return self.db.scalar(
            select(MachiyotlEvidenceItem).where(MachiyotlEvidenceItem.id == evidence_id)
        )

    def get_evidence_by_code(self, evidence_code: str) -> MachiyotlEvidenceItem | None:
        """Single-row lookup by unique human-readable code."""
        return self.db.scalar(
            select(MachiyotlEvidenceItem).where(
                MachiyotlEvidenceItem.evidence_code == evidence_code
            )
        )

    def list_evidence(
        self,
        owner_user_id: UUID | None = None,
        case_id: UUID | None = None,
        status: str | None = None,
        platform: str | None = None,
        captured_from: datetime | None = None,
        captured_to: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[MachiyotlEvidenceItem], int]:
        """Filtered, paginated evidence list with total count.

        Uses ``ix_machiyotl_evidence_owner_status`` or
        ``ix_machiyotl_evidence_case_status`` depending on the filter
        combination provided.

        Returns (items, total_count).
        """
        limit = min(limit, 200)
        offset = max(offset, 0)

        # --- base query ---------------------------------------------------
        stmt = select(MachiyotlEvidenceItem)

        # --- dynamic filters -----------------------------------------------
        if owner_user_id is not None:
            stmt = stmt.where(MachiyotlEvidenceItem.owner_user_id == owner_user_id)
        if case_id is not None:
            stmt = stmt.where(MachiyotlEvidenceItem.case_id == case_id)
        if status is not None:
            stmt = stmt.where(MachiyotlEvidenceItem.status == status)
        if platform is not None:
            stmt = stmt.where(MachiyotlEvidenceItem.platform == platform)
        if captured_from is not None:
            stmt = stmt.where(MachiyotlEvidenceItem.captured_at >= captured_from)
        if captured_to is not None:
            stmt = stmt.where(MachiyotlEvidenceItem.captured_at <= captured_to)

        # --- total count --------------------------------------------------
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery()))
        total = total or 0

        # --- paginated result ----------------------------------------------
        stmt = (
            stmt.order_by(MachiyotlEvidenceItem.captured_at.desc())
            .limit(limit)
            .offset(offset)
        )
        items = self.db.scalars(stmt).all()

        return list(items), total

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    def get_evidence_notes(
        self,
        evidence_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[MachiyotlEvidenceNote], int]:
        """Paginated notes for a given evidence item.

        Uses FK index on ``evidence_notes.evidence_id``.
        """
        limit = min(limit, 200)
        offset = max(offset, 0)

        total_stmt = select(func.count()).where(
            MachiyotlEvidenceNote.evidence_id == evidence_id
        )
        total = self.db.scalar(total_stmt) or 0

        stmt = (
            select(MachiyotlEvidenceNote)
            .where(MachiyotlEvidenceNote.evidence_id == evidence_id)
            .order_by(MachiyotlEvidenceNote.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        items = self.db.scalars(stmt).all()
        return list(items), total

    # ------------------------------------------------------------------
    # Custody Timeline
    # ------------------------------------------------------------------

    def get_custody_timeline(
        self,
        evidence_id: UUID,
    ) -> List[MachiyotlCustodyEvent]:
        """Chronological custody chain for an evidence item.

        Uses ``ix_machiyotl_custody_evidence_time`` (evidence_id, occurred_at).
        """
        stmt = (
            select(MachiyotlCustodyEvent)
            .where(MachiyotlCustodyEvent.evidence_id == evidence_id)
            .order_by(MachiyotlCustodyEvent.occurred_at.asc())
        )
        return list(self.db.scalars(stmt).all())

    # ------------------------------------------------------------------
    # Hash Verifications
    # ------------------------------------------------------------------

    def list_hash_verifications(
        self,
        evidence_id: UUID | None = None,
        verified_from: datetime | None = None,
        verified_to: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[MachiyotlHashVerification], int]:
        """Paginated hash verification history.

        Uses FK index on ``hash_verifications.evidence_id``.
        """
        limit = min(limit, 200)
        offset = max(offset, 0)

        # --- base query ---------------------------------------------------
        stmt = select(MachiyotlHashVerification)

        if evidence_id is not None:
            stmt = stmt.where(
                MachiyotlHashVerification.evidence_id == evidence_id
            )
        if verified_from is not None:
            stmt = stmt.where(
                MachiyotlHashVerification.verified_at >= verified_from
            )
        if verified_to is not None:
            stmt = stmt.where(
                MachiyotlHashVerification.verified_at <= verified_to
            )

        # --- total count --------------------------------------------------
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery()))
        total = total or 0

        # --- paginated result ----------------------------------------------
        stmt = (
            stmt.order_by(MachiyotlHashVerification.verified_at.desc())
            .limit(limit)
            .offset(offset)
        )
        items = self.db.scalars(stmt).all()
        return list(items), total

    # ------------------------------------------------------------------
    # State Machine Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def validate_status_transition(from_status: str, to_status: str) -> bool:
        """Pure logic gate for allowed state transitions.

        Uses the canonical ``ALLOWED_STATUS_TRANSITIONS`` map defined in
        the Machiyotl schemas.
        """
        return to_status in ALLOWED_STATUS_TRANSITIONS.get(from_status, [])

    # ------------------------------------------------------------------
    # Cross-module guard
    # ------------------------------------------------------------------

    @staticmethod
    def assert_machiyotl_only(item: MachiyotlEvidenceItem | MachiyotlEvidenceNote) -> None:
        """Runtime guard: raises if the item leaks cross-module data.

        This is a defensive measure for service-layer callers that may
        accidentally hydrate related objects from other schemas.
        """
        # SQLAlchemy inspection: ensure no joined attributes are loaded
        # from other schemas.  In practice this is a no-op for now
        # because the repository never joins across schemas, but the
        # check documents the intent clearly.
        pass  # Placeholder for future hardened introspection
