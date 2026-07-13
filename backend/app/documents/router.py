from uuid import UUID

from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.db.session import get_db
from app.documents.schemas import DocumentResponse
from app.documents.service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=201,
)
def upload_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db),) -> DocumentResponse:
    service = DocumentService(db)

    document = service.upload_document(
        file=file,
        owner=current_user,
    )

    return DocumentResponse.model_validate(document)

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentResponse:
    service = DocumentService(db)

    document = service.get_user_document(
        document_id=document_id,
        owner_id=current_user.id,
    )

    return DocumentResponse.model_validate(document)

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session =Depends(get_db),
) -> Response:
    service = DocumentService(db)

    service.delete_user_document(
        document_id=document_id,
        owner_id=current_user.id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)