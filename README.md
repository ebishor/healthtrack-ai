
# HealthTrack AI

HealthTrack AI is an AI-assisted clinical decision-support web application built with FastAPI and the OpenAI API. It accepts structured patient symptom information and generates a structured assessment containing potential diagnoses, supporting findings, further evaluation suggestions, management considerations, and potential red flags.

## Project Status

This project is a prototype developed for demonstration and learning purposes. It is not a clinically validated medical system and must not be used as a substitute for professional medical judgment.

- AI-generated assessments must be independently reviewed by a qualified healthcare professional.
- The application does not establish definitive diagnoses or issue treatment orders.
- Use fictional data for demonstrations and testing.
- The prototype does not provide production-grade clinical data storage or a validated clinical workflow.

## Features

- Structured patient assessment form
- LLM-powered assessment generation
- JWT-based clinician authentication
- Role-based access control (RBAC)
- Password hashing using Argon2 via `pwdlib`
- Request validation using Pydantic
- Request IDs and structured JSON logging
- Input preprocessing and error handling
- Automated tests using pytest and FastAPI TestClient

## Technology Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript, Jinja2 templates
- **AI integration:** OpenAI Responses API
- **Validation:** Pydantic
- **Authentication:** JWT access tokens
- **Password security:** Argon2
- **Testing:** pytest, HTTPX
- **Configuration:** Environment variables loaded from `.env`

## Architecture

The application separates API routes, authentication, validation, business logic, and configuration.

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
```

## Prerequisites

- Python 3.11 recommended
- Git
- An OpenAI API key with access to the configured model

## Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/ebishor/healthtrack-ai.git
cd healthtrack-ai
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your local environment file from the example:

```powershell
Copy-Item .env.example .env
```

Open `.env` and fill in the required values:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5-mini
JWT_SECRET_KEY=your_long_random_secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Keep any additional settings already present in `.env.example`. Configure the LLM model using the project's supported configuration.

**Security:** Never commit `.env` or expose API keys and JWT secrets. Use strong, randomly generated secrets and keep them private.

### 5. Start the application

From the project root, run:

```powershell
uvicorn app.main:app --reload
```

Open the application in your browser:

http://127.0.0.1:8000

Interactive API documentation is available at:

http://127.0.0.1:8000/docs

## Using the Application

1. Open the application in your browser.
2. Create a clinician account using the registration panel, or log in with an existing account.
3. Enter fictional patient information in the assessment form.
4. Submit the assessment and review the generated output.
5. Log out to disable access to the assessment form.

Passwords must meet the application's configured validation requirements.

### Authentication and prototype limitations

The application protects assessment requests using JWT authentication and enforces role-based access control.

**Current limitation:** User accounts are stored in memory. Accounts may be lost when the application process restarts. This storage approach is for prototyping and must be replaced with persistent, appropriately secured storage before production use.

## Running Tests

Run the automated test suite from the project root:

```powershell
python -m pytest -v
```

The tests cover input preprocessing, request validation, authentication, authorization, API error handling, request logging, and privacy-related logging behavior.

## Security and Privacy

- Environment secrets are excluded from version control.
- Passwords are hashed rather than stored as plaintext.
- Assessment endpoints require authentication.
- Inputs are validated before processing.
- Logs are designed to avoid recording sensitive assessment content and credentials.
- Use fictional data for demonstrations.

This prototype has not undergone a comprehensive security audit. HTTPS, persistent identity management, production secret management, rate limiting, and additional operational safeguards should be addressed before deployment.

## AI Design and Responsible Use

The application uses a pretrained language model to generate structured assessment suggestions from user-provided information. Structured outputs and input validation help make responses easier to process, but do not guarantee clinical accuracy.

Potential risks include hallucinations, omissions, bias, and unsupported recommendations. Outputs require human review, and the system should not be used to make autonomous clinical decisions.

## Performance and Limitations

Performance depends on model response time, network conditions, and the complexity of the input. No specific latency or concurrent-user capacity is claimed without reproducible load testing.

The prototype does not establish clinical validity, guarantee diagnosis accuracy, or replace professional medical evaluation.

## AI Usage Disclosure

AI assistance was used during development for implementation guidance, debugging, documentation, and test preparation. The resulting code and documentation should be reviewed and verified by the project author.

## License

No license has been specified yet. All rights remain with the copyright holder unless a license is added to this repository.