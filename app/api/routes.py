from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from app.schemas.assessment import AssessmentRequest
from app.schemas.response import ClinicalAssessment
from app.services.llm_service import (
    LLMServiceError,
    generate_assessment,
)

router = APIRouter(prefix="/api", tags=["Clinical Assessment"])


@router.post(
    "/assess",
    response_model=ClinicalAssessment,
)
async def assess_symptoms(
    request: AssessmentRequest,
) -> ClinicalAssessment:
    """Generate AI-assisted clinical decision support."""

    try:
        return await generate_assessment(request)

    except LLMServiceError as exc:
        message = str(exc)

        if "not configured" in message.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=message,
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=message,
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc