from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


EvidenceStatus = Literal["draft", "sealed-local", "ready", "submitted", "error"]

PrivacyState = Literal["local-only", "not-submitted", "ready-for-review", "submitted-to-authority"]

CustodyEventType = Literal[
    "capture_started",
    "sealed_local",
    "metadata_reviewed",
    "ready_for_review",
    "submitted_to_review",
    "received_by_authority",
]

HashVerificationResult = Literal["match", "mismatch", "evidence_not_found"]

EvidenceType = Literal[
    "screenshot_placeholder",
    "link_placeholder",
    "text_placeholder",
    "file_placeholder",
    "other",
]

SHA256_MAX_LENGTH = 128
SHORT_HASH_MAX_LENGTH = 24
NOTE_MAX_LENGTH = 4000
EVENT_LABEL_MAX_LENGTH = 160
METADATA_MAX_BYTES = 4096

ALLOWED_STATUS_TRANSITIONS: Dict[EvidenceStatus, List[EvidenceStatus]] = {
    "draft": ["sealed-local", "ready", "error"],
    "sealed-local": ["ready", "error"],
    "ready": ["submitted", "error"],
    "submitted": [],
    "error": ["draft", "sealed-local"],
}


def _hash_format_valid(value: str) -> bool:
    clean = value.removeprefix("sha256:")
    try:
        int(clean, 16)
        return True
    except ValueError:
        return False


class EvidenceItemCreate(BaseModel):
    evidence_type: EvidenceType = Field(...)
    sha256_hash: str = Field(..., max_length=SHA256_MAX_LENGTH)
    short_hash: str = Field(..., max_length=SHORT_HASH_MAX_LENGTH)
    status: EvidenceStatus = Field(default="draft")
    privacy_state: PrivacyState = Field(default="local-only")
    captured_at: datetime = Field(...)
    case_id: Optional[UUID] = None
    platform: Optional[str] = Field(default=None, max_length=80)
    source_url: Optional[str] = Field(default=None, max_length=2048)
    original_filename: Optional[str] = Field(default=None, max_length=240)
    mime_type: Optional[str] = Field(default=None, max_length=120)
    size_bytes: Optional[int] = Field(default=None, ge=0)

    @field_validator("sha256_hash")
    @classmethod
    def validate_hash(cls, v: str) -> str:
        if not _hash_format_valid(v):
            raise ValueError(
                "sha256_hash must be valid hexadecimal with optional sha256: prefix"
            )
        return v

    @field_validator("captured_at")
    @classmethod
    def validate_captured_at_not_future(cls, v: datetime) -> datetime:
        if v > datetime.now(timezone.utc):
            raise ValueError("captured_at cannot be in the future")
        return v


class EvidenceItemUpdate(BaseModel):
    status: Optional[EvidenceStatus] = None
    privacy_state: Optional[PrivacyState] = None
    sealed_at: Optional[datetime] = None
    platform: Optional[str] = Field(default=None, max_length=80)
    source_url: Optional[str] = Field(default=None, max_length=2048)

    @field_validator("sealed_at")
    @classmethod
    def validate_sealed_at_not_future(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v > datetime.now(timezone.utc):
            raise ValueError("sealed_at cannot be in the future")
        return v


class EvidenceItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    case_id: Optional[UUID] = None
    owner_user_id: Optional[UUID] = None
    evidence_code: str
    evidence_type: EvidenceType
    platform: Optional[str] = None
    source_url: Optional[str] = None
    local_file_path: Optional[str] = None
    original_filename: Optional[str] = None
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None
    sha256_hash: str
    short_hash: str
    status: EvidenceStatus
    privacy_state: PrivacyState
    captured_at: datetime
    sealed_at: Optional[datetime] = None
    created_at: datetime


class EvidenceNoteCreate(BaseModel):
    note: str = Field(..., min_length=1, max_length=NOTE_MAX_LENGTH)


class EvidenceNoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    evidence_id: UUID
    author_user_id: Optional[UUID] = None
    note: str
    created_at: datetime


class CustodyEventCreate(BaseModel):
    event_type: CustodyEventType = Field(...)
    event_label: str = Field(..., min_length=1, max_length=EVENT_LABEL_MAX_LENGTH)
    event_hash: Optional[str] = Field(default=None, max_length=SHA256_MAX_LENGTH)
    occurred_at: datetime = Field(...)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("event_hash")
    @classmethod
    def validate_event_hash_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not _hash_format_valid(v):
            raise ValueError(
                "event_hash must be valid hexadecimal with optional sha256: prefix"
            )
        return v

    @field_validator("occurred_at")
    @classmethod
    def validate_occurred_at_not_future(cls, v: datetime) -> datetime:
        if v > datetime.now(timezone.utc):
            raise ValueError("occurred_at cannot be in the future")
        return v

    @field_validator("metadata")
    @classmethod
    def validate_metadata_size(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        import json

        if len(json.dumps(v, default=str).encode("utf-8")) > METADATA_MAX_BYTES:
            raise ValueError(
                f"metadata exceeds maximum serialized size of {METADATA_MAX_BYTES} bytes"
            )
        return v


class CustodyEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    evidence_id: UUID
    actor_user_id: Optional[UUID] = None
    event_type: CustodyEventType
    event_label: str
    event_hash: Optional[str] = None
    occurred_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class HashVerifyRequest(BaseModel):
    submitted_hash: str = Field(..., max_length=SHA256_MAX_LENGTH)
    evidence_id: Optional[UUID] = None

    @field_validator("submitted_hash")
    @classmethod
    def validate_submitted_hash_format(cls, v: str) -> str:
        if not _hash_format_valid(v):
            raise ValueError(
                "submitted_hash must be valid hexadecimal with optional sha256: prefix"
            )
        return v


class HashVerifyResponse(BaseModel):
    evidence_id: Optional[UUID] = None
    submitted_hash: str
    stored_hash: Optional[str] = None
    result: HashVerificationResult
    verified_at: datetime
    warning: str = (
        "Verificación criptográfica de datos sintéticos. No constituye validez legal."
    )


class HashVerificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    evidence_id: Optional[UUID] = None
    submitted_hash: str
    result: HashVerificationResult
    verified_at: datetime


class EvidenceListResponse(BaseModel):
    items: List[EvidenceItemResponse]
    total: int
    limit: int
    offset: int


class NoteListResponse(BaseModel):
    items: List[EvidenceNoteResponse]
    evidence_id: UUID
    total: int
    limit: int
    offset: int


class CustodyEventListResponse(BaseModel):
    events: List[CustodyEventResponse]
    evidence_id: UUID
    chain_length: int


class HashVerificationListResponse(BaseModel):
    items: List[HashVerificationResponse]
    total: int
    limit: int
    offset: int


class MachiyotlErrorDetail(BaseModel):
    field: str
    reason: str


class MachiyotlErrorResponse(BaseModel):
    code: str
    message: str
    details: List[MachiyotlErrorDetail] = Field(default_factory=list)
    trace_id: str = "mch-unknown"
