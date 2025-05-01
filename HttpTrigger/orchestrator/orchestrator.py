from validators.description_format_validator import validate_description_format
from validators.description_length_validator import validate_description_length

def orchestrate_validations(issue_data: dict) -> dict:
    """
    Ejecuta todas las validaciones disponibles sobre el campo 'description'.
    """
    validations = {
        "format_validation": validate_description_format(issue_data),
        "length_validation": validate_description_length(issue_data)
    }
    return validations
