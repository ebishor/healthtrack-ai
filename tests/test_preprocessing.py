
import pytest
from pydantic import ValidationError

from app.schemas.assessment import AssessmentRequest
from app.services.preprocessing import (
    clean_text,
    preprocess_assessment,
)


def test_clean_text_normalizes_whitespace():
    result = clean_text(
        "  Patient has FEVER \n and   persistent cough.  "
    )

    assert result == "Patient has FEVER and persistent cough."


def test_clean_text_handles_empty_values():
    assert clean_text(None) is None
    assert clean_text("   ") is None


def test_preprocess_returns_structured_data():
    request = AssessmentRequest(
        patient_age=35,
        symptoms="  Fever   and persistent cough  ",
        symptom_duration="  3 days ",
    )

    result = preprocess_assessment(request)

    assert result == {
        "patient_age": 35,
        "symptoms": "Fever and persistent cough",
        "symptom_duration": "3 days",
        "relevant_medical_history": None,
        "current_medications": None,
        "allergies": None,
    }


def test_negative_age_is_rejected():
    with pytest.raises(ValidationError):
        AssessmentRequest(
            patient_age=-1,
            symptoms="Fever and cough",
        )


def test_blank_symptoms_are_rejected_after_cleaning():
    request = AssessmentRequest(
        symptoms="     ",
    )

    with pytest.raises(ValueError):
        preprocess_assessment(request)