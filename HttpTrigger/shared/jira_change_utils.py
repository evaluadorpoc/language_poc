# shared/jira_change_utils.py

from shared.logger_config import logger

def extract_changed_fields(changelog):
    if not changelog or "items" not in changelog:
        logger.debug("🔍 Changelog vacío o sin estructura válida.")
        return []
    return [item.get("field") for item in changelog["items"] if "field" in item]

def field_was_changed(changelog, field_name):
    changed = field_name in extract_changed_fields(changelog)
    logger.debug(f"📌 ¿'{field_name}' fue modificado?: {'Sí' if changed else 'No'}")
    return changed

def any_field_changed(changelog, field_list):
    changed = set(extract_changed_fields(changelog)) & set(field_list)
    logger.debug(f"📌 ¿Alguno de los campos {field_list} fue modificado?: {'Sí' if changed else 'No'}")
    return bool(changed)
