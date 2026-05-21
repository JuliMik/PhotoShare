from sqlalchemy import select, func
from src.photoshare.core.models import User
from src.photoshare.schemas.user import UserCreate
from src.photoshare.schemas.enums import UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils_jwt import hash_password

# ==========================================
# User Creation Operations
# ==========================================


# Registers a new user and dynamically determines their role
async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> User:
    """
    Creates a new user in the database.
    If this is the first user in the database, automatically assigns the ADMIN role.
    Otherwise, defaults to the USER role. Hashes the password before storing.
    """
    # Count existing users to determine if this is the first registration
    result = await session.execute(select(func.count(User.id)))
    users_count = result.scalar()
    role = UserRole.ADMIN if users_count == 0 else UserRole.USER

    # Initialize the User instance with hashed password
    user = User(
        email=str(user_in.email),
        username=str(user_in.username),
        hashed_password=hash_password(user_in.password),
        role=role,
    )

    # Persist the user inside the database session
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


# ==========================================
# User Retrieval Operations
# ==========================================


# Fetches a specific user record using their primary key ID
async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    """
    Retrieves a user record from the database by its primary key ID.
    Returns None if no user matches the given ID.
    """
    return await session.get(User, user_id)


# Fetches a specific user record using their unique username string
async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    """
    Queries the database for a user matching the specified username string.
    Returns the User object if found, otherwise returns None.
    """
    stmt = select(User).filter_by(username=username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
