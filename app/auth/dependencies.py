from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.token import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> dict[str, str]:
    """Validate the access token and return the authenticated user."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        print("DEBUG decoded payload:", payload)
        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            raise credentials_exception

        return {
            "username": username,
            "role": role,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise credentials_exception from exc


def require_roles(*allowed_roles: str):
    """Create a dependency that restricts access to specified roles."""

    def role_checker(
        current_user: dict[str, str] = Depends(get_current_user),
    ) -> dict[str, str]:
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )

        return current_user

    return role_checker