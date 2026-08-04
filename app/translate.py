import requests
from flask_babel import _

from app import app


def translate(text: str, source_language: str, dest_language: str) -> str:
    key = app.config.get("MS_TRANSLATOR_KEY")
    region = app.config.get("MS_TRANSLATOR_REGION")

    if not key:
        return _("Error: the translation service is not configured.")

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    if region:
        headers["Ocp-Apim-Subscription-Region"] = region

    params = {
        "api-version": "3.0",
        "from": source_language,
        "to": dest_language,
    }

    body = [
        {
            "Text": text
        }
    ]

    try:
        response = requests.post(
            "https://api.cognitive.microsofttranslator.com/translate",
            params=params,
            headers=headers,
            json=body,
            timeout=10,
        )
    except requests.RequestException:
        return _("Error: the translation service could not be reached.")

    if response.status_code != 200:
        return _("Error: the translation service failed.")

    result = response.json()
    return result[0]["translations"][0]["text"]