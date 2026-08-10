import re
from bs4 import BeautifulSoup

class emailCleaner:
    def clean_email(self, email_body: str, content_type: str, name: str) -> str:
        """
        Clean the email body by removing HTML tags and extra whitespace.
        """
        if content_type == "html":
            soup = BeautifulSoup(email_body, "html.parser")
            body = soup.get_text("\n").strip()
            signature_markers = [
            "\nRegards,",
            "\nThanks,",
            "\nBest",
            "\nSincerely",
            "\nFrom"
            ]
            for marker in signature_markers:
                if marker.lower() in body.lower():
                    index = body.lower().find(marker.lower())
                    body = body[:index]
            body = re.sub(r"\n,\s*\n+", "\n", body)
            body = re.sub(r"\xa0", " ", body).strip()
            if name in body:
                idx = body.find(name)
                body = body[:idx]
            return body.strip()
        return email_body.strip()
    