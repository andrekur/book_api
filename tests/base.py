from unittest import TestCase
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base
from api.api_start import app
from api.views import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


class BaseAPITest(TestCase):
    client = TestClient(app)

    @classmethod
    def setUp(cls):
        Base.metadata.create_all(bind=engine)
        # create test BD
        app.dependency_overrides[get_db] = override_get_db

    @classmethod
    def tearDown(cls):
        Base.metadata.drop_all(bind=engine)
        # del test BD

    def create_shop(self, shop_data):
        # hardcoding url is wrong ¯\_(ツ)_/¯
        return self.client.post(
            '/shops',
            json={**shop_data}
        )

    def get_shops(self):
        return self.client.get(
            '/shops'
        )
