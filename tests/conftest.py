import pytest
from fastapi.testclient import TestClient

from back_python_default.app import app
from back_python_default.database import get_session


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


# ...
