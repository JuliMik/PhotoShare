from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Absolute pathway referencing the system application root directory
BASE_DIR = Path(__file__).parent.parent


# ==========================================
# Component Specific Configurations
# ==========================================


class RunConfig(BaseModel):
    """
    Sub-model holding parameters defining server engine socket attachments.
    """

    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    """
    Sub-model defining explicit endpoint nesting routes for internal API version 1 modules.
    """

    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    """
    Sub-model orchestrating top-level routing namespaces throughout the gateway layers.
    """

    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseSettings):
    """
    Configuration model orchestrating asynchronous network pool parameters
    and constraints indexing schemas for Alembic migrations.
    """

    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    # Explicit metadata mapping structure maintaining strict unique keys naming syntax
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthJWT(BaseModel):
    """
    Sub-model managing cryptographic token signatures credentials layout
    and lifecycle timing barriers for active security protocols.
    """

    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    # access_token_expire_minutes: int = 3


# ==========================================
# Root Application Settings Composition
# ==========================================


class Settings(BaseSettings):
    """
    Global system root configuration orchestrator compiling infrastructure environment mappings.
    Loads and processes hierarchically formatted custom profile environment attributes automatically.
    """

    model_config = SettingsConfigDict(
        env_file=[
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ],
        case_sensitive=False,
        env_nested_delimiter="__",  # Permits deep structural loading via nested keys (e.g. APP_CONFIG__DB__URL)
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    auth_jwt: AuthJWT = AuthJWT()


# Instantiated immutable application profile tracking environment values across lifecycle threads
settings = Settings()
