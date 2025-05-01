# jira_connector/api_client.py
import requests
import json
from shared.logger_config import logger
from shared.settings import JIRA_BASE_URL, JIRA_TOKEN, JIRA_EMAIL

class JiraClient:
    def __init__(self):
        self.base_url = JIRA_BASE_URL
        self.auth = (JIRA_EMAIL, JIRA_TOKEN)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        logger.info("✅ JiraClient inicializado correctamente.")

    def add_comment(self, issue_key: str, comment_text: str) -> bool:
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment_text
                            }
                        ]
                    }
                ]
            }
        }
        try:
            response = requests.post(url, headers=self.headers, auth=self.auth, json=payload)
            response.raise_for_status()
            logger.info(f"✅ Comentario agregado en {issue_key}.")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error al agregar comentario en {issue_key}: {e}")
            return False

    def update_custom_field(self, issue_key: str, field_id: str, field_value: int) -> bool:
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        payload = {
            "fields": {
                field_id: str(field_value)
            }
        }

        try:
            response = requests.put(url, headers=self.headers, auth=self.auth, json=payload)
            response.raise_for_status()
            logger.info(f"✅ Campo {field_id} actualizado en {issue_key} con valor {field_value}.")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error al actualizar campo {field_id} en {issue_key}: {e}")
            return False

