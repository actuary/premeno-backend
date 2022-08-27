from django.conf import settings
from pytest import raises
from requests_mock import Mocker

from premeno.risk_api.canrisk.api import CanRisk, CanRiskAPIError


class TestCanRiskAPI:
    @classmethod
    def setup_class(cls):
        cls.tmp_cache = settings.CANRISK_API_CACHE
        settings.CANRISK_API_CACHE = False

    @classmethod
    def teardown_class(cls):
        settings.CANRISK_API_CACHE = cls.tmp_cache

    def test_initialise_correct(self) -> None:
        with Mocker() as mock:
            mock.post(
                "https://www.canrisk.org/auth-token/",
                status_code=200,
                json={"token": "notarealtoken"},
            )
            settings.CANRISK_API_TOKEN = ""
            canrisk = CanRisk("dv21", "password123")
            assert canrisk.user_id == "dv21"
            assert canrisk.api_key == "notarealtoken"
            assert canrisk.session.headers["Authorization"] == "token notarealtoken"

            settings.CANRISK_API_TOKEN = "abc"
            canrisk = CanRisk("dv21", "password123")
            assert canrisk.api_key == settings.CANRISK_API_TOKEN

    def test_no_token_response(self) -> None:
        tmp = settings.CANRISK_API_TOKEN
        settings.CANRISK_API_TOKEN = ""
        with raises(CanRiskAPIError, match="Unable to parse CanRisk API token."):
            with Mocker() as mock:
                mock.post(
                    "https://www.canrisk.org/auth-token/",
                    status_code=200,
                    json={"bloken": "notarealtoken"},
                )

                CanRisk("dv21", "password123")

        settings.CANRISK_API_TOKEN = tmp

    def test_bad_response(self) -> None:
        tmp = settings.CANRISK_API_TOKEN
        settings.CANRISK_API_TOKEN = ""
        with raises(CanRiskAPIError, match="Bad response from CanRisk API:"):
            with Mocker() as mock:
                mock.post(
                    "https://www.canrisk.org/auth-token/",
                    status_code=400,
                    json={"token": "notarealtoken"},
                )
                CanRisk("dv21", "password123")

        settings.CANRISK_API_TOKEN = tmp

    def test_boadicea(self) -> None:
        with Mocker() as mock:
            mock.post(
                "https://www.canrisk.org/auth-token/",
                status_code=200,
                json={"token": "notarealtoken"},
            )
            mock.post(
                "https://www.canrisk.org/boadicea/",
                status_code=200,
                json={"test": "TEST"},
            )
            canrisk = CanRisk("dv21", "password123")
            assert canrisk.boadicea("fakepedigreedata") == {"test": "TEST"}

    def test_cached(self) -> None:
        with Mocker() as mock:
            settings.CANRISK_API_CACHE = True
            mock.post(
                "https://www.canrisk.org/auth-token/",
                status_code=200,
                json={"token": "notarealtoken"},
            )
            canrisk = CanRisk("dv21", "password123")

            mock.post(
                "https://www.canrisk.org/boadicea/",
                status_code=200,
                json={"test": "TEST"},
            )
            assert canrisk.boadicea("fakepedigreedata") == {"test": "TEST"}

            mock.post(
                "https://www.canrisk.org/boadicea/",
                status_code=200,
                json={"test": "TEST_DIFFERENT"},
            )
            # caches the first one
            assert canrisk.boadicea("fakepedigreedata") == {"test": "TEST"}
            settings.CANRISK_API_CACHE = False
