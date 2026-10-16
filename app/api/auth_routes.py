from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.token import create_access_token
from app.auth.user_store import authenticate_user, create_user
from app.schemas.user import TokenResponse, UserCreate, UserPublic

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register(user_data: UserCreate) -> UserPublic:
    """Register a clinician account for development."""

    # Public registration must never grant administrator privileges.
    try:
        user = create_user(
            username=user_data.username,
            password=user_data.password,
            role="clinician",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return UserPublic(**user)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:
    """Authenticate a user and return a JWT access token."""

    user = authenticate_user(
        form_data.username,
        form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        username=user["username"],
        role=user["role"],
    )

    return TokenResponse(access_token=token)