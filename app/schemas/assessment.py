
from pydantic import BaseModel, ConfigDict, Field


class AssessmentRequest(BaseModel):
    """Validated input supplied by a healthcare professional."""

    model_config = ConfigDict(extra="forbid")

    patient_age: int | None = Field(
        default=None,
        ge=0,
        le=120,
        description="Patient age in years",
    )

    symptoms: str = Field(
        min_length=5,
        max_length=3000,
        description="Symptoms reported for the patient",
    )

    symptom_duration: str | None = Field(
        default=None,
        max_length=200,
    )

    relevant_medical_history: str | None = Field(
        default=None,
        max_length=1500,
    )

    current_medications: str | None = Field(
        default=None,
        max_length=1000,
    )

    allergies: str | None = Field(
        default=None,
        max_length=1000,
    )