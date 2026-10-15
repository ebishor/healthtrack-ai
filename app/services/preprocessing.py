
import re
import unicodedata
from typing import Any

from app.schemas.assessment import AssessmentRequest


def clean_text(value: str | None) -> str | None:
    """Normalize text without changing its medical meaning."""

    if value is None:
        return None

    # Normalize Unicode representations.
    value = unicodedata.normalize("NFKC", value)

    # Replace control characters with spaces.
    value = "".join(
        " " if unicodedata.category(char).startswith("C") else char
        for char in value
    )

    # Collapse repeated whitespace and trim both ends.
    value = re.sub(r"\s+", " ", value).strip()

    # Normalize empty optional fields to None.
    return value or None


def preprocess_assessment(
    request: AssessmentRequest,
) -> dict[str, Any]:
    """Convert validated input into a clean, structured payload."""

    symptoms = clean_text(request.symptoms)

    if not symptoms or len(symptoms) < 5:
        raise ValueError(
            "Please provide a meaningful description of symptoms."
        )

    return {
        "patient_age": request.patient_age,
        "symptoms": symptoms,
        "symptom_duration": clean_text(request.symptom_duration),
        "relevant_medical_history": clean_text(
            request.relevant_medical_history
        ),
        "current_medications": clean_text(request.current_medications),
        "allergies": clean_text(request.allergies),
    }