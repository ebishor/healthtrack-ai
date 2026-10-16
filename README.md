# HealthTrack AI

HealthTrack AI is an AI-assisted clinical decision-support web application
designed for healthcare professionals. It accepts structured patient
symptom information and uses a pretrained large language model (LLM)
to generate a structured assessment containing potential diagnoses,
supporting findings, further evaluation suggestions, management
considerations, and potential red flags.

## Project Status

This project is a prototype built for demonstration and learning purposes.
It is not a clinically validated medical system and must not be used as
a substitute for professional medical judgment.

All AI-generated assessments require independent review by a qualified
healthcare professional. The application does not establish definitive
diagnoses or issue treatment orders.

## Technology Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript, Jinja2 templates
- **AI/LLM integration:** OpenAI API using the Responses API
- **Data validation:** Pydantic
- **Authentication:** JWT-based authentication
- **Password security:** Argon2 password hashing via `pwdlib`
- **Authorization:** Role-based access control (RBAC)
- **Logging:** Structured JSON logs with request IDs and rotating log files
- **Testing:** Pytest, FastAPI TestClient, and HTTPX
- **Configuration:** Environment variables loaded from `.env`

## Application Architecture

The application follows a modular backend structure that separates
API endpoints, request validation, authentication, business logic,
and configuration.

```text
healthtrack-ai/
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   └── auth_routes.py
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── security.py
│   │   ├── token.py
│   │   └── user_store.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   └── request_middleware.py
│   ├── schemas/
│   │   ├── assessment.py
│   │   ├── response.py
│   │   └── user.py
│   ├── services/
│   │   ├── llm_service.py
│   │   └── preprocessing.py
│   ├── templates/
│   │   └── index.html
│   └── main.py
├── tests/
├── logs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible newer Python version
- An OpenAI API key with access to the configured model
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd healthtrack-ai


## Running Tests

The project includes automated tests for input preprocessing, request
validation, authentication, authorization, API error handling, request
logging, and privacy-related logging behavior.

Activate the virtual environment and run the complete test suite:

```powershell
python -m pytest -v