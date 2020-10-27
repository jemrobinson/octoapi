import json
import requests
from .exceptions import ApiException
from .types import JSONType


class AuthenticatedClient:
    API_BASE_URL = "https://api.octopus.energy/v1"

    def __init__(self, api_key: str) -> None:
        self.session = requests.Session()
        self.session.auth = (api_key, "")

    def request_json(self, path: str, params: dict = {}) -> JSONType:
        """Make a request against the Octopus API"""
        request_url = "/".join([self.API_BASE_URL, path.lstrip("/")])
        try:
            response = self.session.request(
                method="GET", url=request_url, params=params
            )
            print(request_url)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ApiException("Unexpected response exception") from e

        print("response", response)
        print("response.text", response.text)
        print("response.json()", response.json())

        return response.json()
