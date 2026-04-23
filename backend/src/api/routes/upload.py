from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile

from src.core.auth import get_current_user
from src.core.response import ok_response
from src.services.auth_service import AuthUser
from src.services.store import store

router = APIRouter()


@router.get("/{upload_id}/file")
def get_uploaded_image_file(upload_id: str) -> Response:
    record = store.get_upload(upload_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "UPLOAD_NOT_FOUND",
                "message": "Uploaded image does not exist.",
                "detail": {"uploaded_image_id": upload_id},
            },
        )

    return Response(
        content=record.content,
        media_type=record.content_type,
        headers={"Content-Disposition": f'inline; filename="{record.filename}"'},
    )


@router.post("/upload")
async def upload_image(
    image: UploadFile = File(...),
    user: AuthUser = Depends(get_current_user),
) -> dict:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_INVALID_PARAM",
                "message": "Only image files are allowed.",
                "detail": {"field": "image"},
            },
        )

    content = await image.read()
    size_bytes = len(content)
    filename = image.filename or "uploaded-image"

    record = store.create_upload(
        user_id=user.user_id,
        filename=filename,
        content_type=image.content_type,
        size_bytes=size_bytes,
        content=content,
    )

    return ok_response(
        {
            "id": record.id,
            "image_url": record.image_url,
            "created_at": record.created_at,
            "analysis": {
                "checksum": record.analysis.checksum,
                "dominant_tone": record.analysis.dominant_tone,
                "dominant_color": record.analysis.dominant_color,
                "style_mood": record.analysis.style_mood,
                "silhouette": record.analysis.silhouette,
                "preferred_categories": list(record.analysis.preferred_categories),
            },
        }
    )
