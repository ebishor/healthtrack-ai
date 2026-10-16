import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import require_roles
from app.schemas.assessment import AssessmentRequest
from app.schemas.response import ClinicalAssessment
from app.services.llm_service import (
    LLMServiceError,
    generate_assessment,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Clinical Assessment"])


@router.post(
    "/assess",
    response_model=ClinicalAssessment,
)
async def assess_symptoms(
    request: AssessmentRequest,
    current_user: dict[str, str] = Depends(
        require_roles("clinician", "admin")
    ),
) -> ClinicalAssessment:
    """Generate an authenticated, AI-assisted clinical assessment."""

    # Record an audit event without logging clinical information.
    logger.info(
        "Authenticated user requested an assessment",
        extra={
            "event": "assessment_requested",
            "user_role": current_user["role"],
        },
    )

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