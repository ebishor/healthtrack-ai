from app.auth.security import hash_password, verify_password

# Temporary in-memory store for development only.
# Replace with a persistent database before deployment.
_users: dict[str, dict[str, str]] = {}


def create_user(
    username: str,
    password: str,
    role: str = "clinician",
) -> dict[str, str]:
    """Create a user and store their password hash."""
    if username in _users:
        raise ValueError("Username already exists.")

    user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
    }

    _users[username] = user
    return {"username": username, "role": role}


def authenticate_user(
    username: str,
    password: str,
) -> dict[str, str] | None:
    """Return public user information when credentials are valid."""
    user = _users.get(username)

    if user is None or not verify_password(
        password,
        user["password_hash"],
    ):
        return None

    return {
        "username": user["username"],
        "role": user["role"],
    }