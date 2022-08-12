from enum import Enum
from http import client

import requests


class CanRiskAPIError(Exception):
    """ Errors using or contacting the canrisk API """


class CancerRateSource(Enum):
    """ Cancer Incidence Rates data source country """
    UK = "UK"


class MutationFreqSource(Enum):
    """ Gene mutation frequencies source country """
    UK = "UK"


BASE_URL = "https://www.canrisk.org"


class CanRisk:
    def __init__(self, username: str, password: str) -> None:
        self.session = requests.Session()
        self.user_id = username
        self.api_key = self._get_api_key(username, password)
        self.session.headers.update({
            "Authorization": f"token {self.api_key}",
        })

    def _get_api_key(self, username: str, password: str) -> str:
        data = {"username": username, "password": password}
        json = self._get_post_response("auth-token/", data=data)

        try:
            return json["token"]
        except KeyError:
            raise CanRiskAPIError("Unable to parse CanRisk API token.")

    def _get_post_response(self, route: str, data: dict = {}) -> dict:
        r = self.session.post(f"{BASE_URL}/{route}", data=data)
        if r.status_code != requests.codes.ok:
            raise CanRiskAPIError("Bad response from CanRisk API: "
                                  f"'{client.responses[r.status_code]}': "
                                  f"{r.text}")

        return r.json()

    def boadicea(self,
                 pedigree_data: str,
                 cancer_rates: CancerRateSource = CancerRateSource.UK,
                 mut_freq: MutationFreqSource = MutationFreqSource.UK) -> dict:
        data = {
            "user_id": self.user_id,
            "cancer_rates": cancer_rates.value,
            "mut_freq": mut_freq.value,
            "pedigree_data": pedigree_data
        }

        return self._get_post_response("boadicea/", data=data)
