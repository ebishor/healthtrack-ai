from pydantic import BaseModel, Field


class PotentialDiagnosis(BaseModel):
    name: str = Field(description="Name of a possible diagnosis")
    reasoning: str = Field(
        description="Brief explanation of why it may be considered"
    )
    urgency: str = Field(
        description="Suggested urgency for clinician assessment"
    )
    supporting_findings: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)


class ClinicalAssessment(BaseModel):
    summary: str
    potential_diagnoses: list[PotentialDiagnosis]
    further_evaluation: list[str]
    management_considerations: list[str]
    red_flags: list[str]
    disclaimer: str