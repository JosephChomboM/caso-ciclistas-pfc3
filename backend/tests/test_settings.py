import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_reject_short_secret():
    with pytest.raises(ValidationError):
        Settings(jwt_secret="short", _env_file=None)


def test_production_requires_postgres_and_https():
    with pytest.raises(ValidationError):
        Settings(environment="production", jwt_secret="x" * 40, _env_file=None)


def test_no_wildcard_cors():
    with pytest.raises(ValidationError):
        Settings(jwt_secret="x" * 40, cors_origins=["*"], _env_file=None)
