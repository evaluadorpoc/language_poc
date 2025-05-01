# settings.py
import os

# 📂 Configuración Jira
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
# Field IDs para Jira (NO secretos, valores estáticos)
CUSTOM_FIELDS = {
    "character_count": "customfield_10038"
}
# 📂 Otros settings generales
AZURE_FUNCTIONS_WORKER_RUNTIME = os.getenv("FUNCTIONS_WORKER_RUNTIME")
