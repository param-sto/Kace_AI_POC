from config import settings
import requests
import re

class KaceClient:

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.csrf_token = None

        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json",
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
        print(response)
        
        self.authenticated = True
        return response.json()

    

    def authenticate_admin_ui(self):

        # Get login page
        login_page = self.session.get(
            f"{self.base_url}/adminui/",
            verify=False
        )

        # Extract login CSRF token
        match = re.search(
            r'var\s+csrf_token\s*=\s*"([^"]+)"',
            login_page.text
        )

        if not match:
            raise Exception("Unable to find login CSRF token")

        csrf_token = match.group(1)

        payload = {
            "CSRF_TOKEN": csrf_token,
            "LOGIN_NAME": self.username,
            "LOGIN_PASSWORD": self.password,
            "ORGANIZATION": "Default",
            "save": ""
        }

        response = self.session.post(
            f"{self.base_url}/adminui/check_login.php",
            data=payload,
            verify=False
        )

        response.raise_for_status()
        self.authenticated = True


    def get_admin_csrf_token(self):

        response = self.session.get(
            f"{self.base_url}/adminui/summary.php",
            verify=False
        )

        match = re.search(
            r'var\s+csrf_token\s*=\s*"([^"]*)"',
            response.text
        )

        if not match:
            raise Exception("Unable to find CSRF token")

        print(match.group(1))
        return match.group(1)

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
        # headers = {"x-dell-csrf_token": self.csrf_token}
        response = self.session.post(
            url,
            json=data,
            # headers=headers,
            verify=False
        )
        print("=" * 50)
        print(response.text)
        print("=" * 50)
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

    

    def post_form(self, path: str, data: dict):

        if not self.authenticated:
            raise Exception("KACE client not authenticated")

        url = f"{self.base_url}{path}"

        response = self.session.post(
            url,
            data=data,
            verify=False
        )

        print("=" * 50)
        print("STATUS:", response.status_code)
        print("BODY:", repr(response.text[:1000]))
        print("=" * 50)

        response.raise_for_status()

        return response