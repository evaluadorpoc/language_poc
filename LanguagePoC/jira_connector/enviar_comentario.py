import requests
from requests.auth import HTTPBasicAuth
import os

def comentar_en_issue(issue_key: str, comentario: str) -> bool:
    url = f"{os.environ['JIRA_URL']}/rest/api/3/issue/{issue_key}/comment"
    payload = { "body": comentario }

    auth = HTTPBasicAuth(os.environ["JIRA_EMAIL"], os.environ["JIRA_API_TOKEN"])
    headers = { "Accept": "application/json", "Content-Type": "application/json" }

    response = requests.post(url, json=payload, auth=auth, headers=headers)
    return response.status_code in [200, 201]
