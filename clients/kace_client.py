from config import settings
import requests

class KaceClient:

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password

        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-kace-api-version": "5"
        })

        self.authenticated = False

    def authenticate_kace(self):
        """
        Authenicate with KACE SMA.
        """
        url = f"{self.base_url}/ams/shared/api/security/login"

        payload = {
            "userName": self.username,
            "password": self.password
        }
        response = self.session.post(
            url,
            json=payload,
            verify=False
        )     

        response.raise_for_status()

        self.authenticated = True
        return response.json()

    def get(self, path: str, params: dict | None = None):
        """
        GET request.
        """
        if not self.authenticated:
            raise Exception("KACE client not authorized")
        url = f"{self.base_url}{path}"

        response = self.session.get(
            url,
            params=params,
            verify=False
        )

        response.raise_for_status()
        return response.json()

    def post(self, path: str, data: dict | None = None):

        if not self.authenticated:
            raise Exception("KACE client not authenticated")

        url = f"{self.base_url}{path}"

        response = self.session.post(
            url,
            json=data,
            verify=False
        )

        response.raise_for_status()
        return response.json()

    def put(self, path: str, data: dict | None = None):
        if not self.authenticated:
            raise Exception("KACE client not authenticated")

        url = f"{self.base_url}{path}"

        response = self.session.put(
            url,
            json=data,
            verify=False
        )

        response.raise_for_status()
        return response.json()

    