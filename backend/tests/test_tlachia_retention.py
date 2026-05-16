from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.db.models import TlachiaPlatformItem
from app.db.session import create_session
from app.services.tlachia.retention_service import RetentionService
from tests.db_test_utils import migrate_database


def setup_module() -> None:
    migrate_database()


def test_retention_deletes_old_items() -> None:
    run_id = uuid4().hex[:8]
    with create_session() as db:
        old_item = TlachiaPlatformItem(
            id=uuid4(),
            synthetic_id=f"old_demo_{run_id}",
            platform="x",
            source_kind="post",
            created_at=datetime.now(timezone.utc) - timedelta(hours=72),
        )
        new_item = TlachiaPlatformItem(
            id=uuid4(),
            synthetic_id=f"new_demo_{run_id}",
            platform="x",
            source_kind="post",
            created_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        db.add(old_item)
        db.add(new_item)
        db.commit()

        svc = RetentionService(db)
        deleted = svc.apply_retention()
        assert deleted >= 1

        remaining = db.query(TlachiaPlatformItem).filter(
            TlachiaPlatformItem.synthetic_id.in_([f"old_demo_{run_id}", f"new_demo_{run_id}"])
        ).all()
        assert all(item.synthetic_id != f"old_demo_{run_id}" for item in remaining)
