import sys
import os
import pytest
from fastapi.testclient import TestClient

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"Корень проекта: {project_root}")
if project_root not in sys.path:
    print("Добавляем корень проекта в sys.path")
    sys.path.insert(0, project_root)
else:
    print("Корень проекта уже в sys.path")

from app.main import app
print("Успешно импортирован app.main")


images_dir = "tests/images"


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)
