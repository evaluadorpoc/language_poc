from shared.logger_config import logger

def validate_description_length(issue_data: dict) -> dict:
    """
    Valida que el campo 'description' tenga al menos 10 caracteres.
    """
    description = issue_data.get('description', '').strip()

    if len(description) >= 10:
        logger.info(f"✅ Validación exitosa: longitud de 'description' es {len(description)} caracteres.")
        return {
            "passed": True,
            "details": f"Description length is acceptable ({len(description)} characters)."
        }
    else:
        logger.warning(f"⚠️ Validación fallida: longitud de 'description' es {len(description)} caracteres.")
        return {
            "passed": False,
            "details": f"Description too short ({len(description)} characters)."
        }
