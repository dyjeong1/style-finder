from src.services.auth_service import AuthUser


LOCAL_USER = AuthUser(
    user_id="local-user-001",
    email="local@stylematch.dev",
    role="owner",
)


def get_current_user() -> AuthUser:
    return LOCAL_USER
