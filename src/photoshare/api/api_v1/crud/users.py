from sqlalchemy import select, func
from src.photoshare.core.models import User
from src.photoshare.schemas.user import UserCreate
from src.photoshare.schemas.enums import UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from auth.utils_jwt import hash_password


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> User:
    result = await session.execute(select(func.count(User.id)))
    users_count = result.scalar()
    role = UserRole.ADMIN if users_count == 0 else UserRole.USER
    user = User(
        email=str(user_in.email),
        username=str(user_in.username),
        hashed_password=hash_password(user_in.password),
        role=role
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).filter_by(username=username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

