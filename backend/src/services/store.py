from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class UploadedImageRecord:
    id: str
    user_id: str
    image_url: str
    filename: str
    content_type: str
    size_bytes: int
    created_at: str


class InMemoryStore:
    def __init__(self) -> None:
        self.uploads: dict[str, UploadedImageRecord] = {}

    def create_upload(
        self,
        user_id: str,
        filename: str,
        content_type: str,
        size_bytes: int,
    ) -> UploadedImageRecord:
        upload_id = str(uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        image_url = f"/mock-storage/{upload_id}-{filename}"

        record = UploadedImageRecord(
            id=upload_id,
            user_id=user_id,
            image_url=image_url,
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            created_at=created_at,
        )
        self.uploads[upload_id] = record
        return record

    def get_upload(self, upload_id: str) -> UploadedImageRecord | None:
        return self.uploads.get(upload_id)


store = InMemoryStore()
