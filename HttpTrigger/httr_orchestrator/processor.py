# orchestrator/processor.py

from HttpTrigger.httr_jira_connector.api_client import JiraClient
from HttpTrigger.httr_shared.logger_config import logger
import HttpTrigger.httr_shared.settings as settings


def process_jira_operations(issue_key, description, custom_fields=None, raw_fields=None):
    """
    Procesa operaciones con Jira de forma escalable:
    - Cuenta caracteres del campo 'description'.
    - Agrega un comentario automático.
    - Actualiza múltiples campos personalizados según la configuración.
    """
    jira = JiraClient()

    # Asegurar que custom_fields esté definido
    custom_fields = custom_fields or {}

    # 🎯 Lógica 1: calcular longitud de descripción
    character_count = len(description)
    logger.info(f"✍️ Descripción tiene {character_count} caracteres.")

    # 🎯 Componer comentario automático
    comment_message = f"📝 Esta historia tiene {character_count} caracteres en la descripción."

    # 🎯 Ejecutar acciones en Jira
    comment_added = jira.add_comment(issue_key, comment_message)

    # 🎯 Lógica 2: actualizar campo personalizado
    field_key = settings.CUSTOM_FIELDS.get("character_count")
    field_updated = jira.update_custom_field(issue_key, field_key, character_count)

    # 🧱 [Escalable] Aquí podrías procesar otros campos usando custom_fields, por ejemplo:
    # for field_name, field_value in custom_fields.items():
    #     field_id = settings.CUSTOM_FIELDS.get(field_name)
    #     if field_id:
    #         jira.update_custom_field(issue_key, field_id, field_value)

    result = {
        "comment_added": comment_added,
        "field_updated": field_updated,
        "character_count": character_count
    }

    logger.info(f"✅ Resultado procesamiento Jira: {result}")
    return result
