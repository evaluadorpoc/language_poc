from shared.logger_config import logger

def validate_description_format(issue_data: dict) -> dict:
    """
    Valida si el campo 'description' comienza con 'Como '.
    """
    description = issue_data.get('description', '').strip()

    if not description:
        logger.warning("⚠️ Validación fallida: 'description' está vacío o no existe.")
        return {
            "passed": False,
            "details": "Missing or empty 'description' field."
        }

    if description.startswith("Como "):
        logger.info("✅ Validación exitosa: 'description' inicia correctamente con 'Como '.")
        return {
            "passed": True,
            "details": "Description starts correctly with 'Como '."
        }
    else:
        logger.warning("⚠️ Validación fallida: 'description' no inicia con 'Como '.")
        return {
            "passed": False,
            "details": "Description does not start with 'Como '."
        }
