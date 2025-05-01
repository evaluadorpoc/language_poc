# HttpTrigger/main.py

import azure.functions as func
from shared.logger_config import logger
from orchestrator.processor import process_jira_operations
from shared.jira_change_utils import field_was_changed

def process_request(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("✅ Nueva solicitud HTTP recibida.")

    try:
        req_body = req.get_json()
        logger.info(f"📥 Cuerpo recibido: {req_body}")
    except ValueError as e:
        logger.error(f"❌ Error al parsear JSON: {e}")
        return func.HttpResponse(
            body='{"success": false, "message": "Invalid JSON payload."}',
            status_code=400,
            mimetype="application/json"
        )

    issue_key = req_body.get("issue", {}).get("key")
    description = req_body.get("issue", {}).get("fields", {}).get("description", "").strip()
    changelog = req_body.get("changelog", {})

    # 🛑 Si no se modificó 'description', no hacemos nada
    if not field_was_changed(changelog, "description"):
        logger.info("🛑 Cambio ignorado: no se modificó el campo 'description'.")
        return func.HttpResponse(
            body='{"success": false, "message": "Field `description` was not changed."}',
            status_code=200,
            mimetype="application/json"
        )

    if not issue_key or not description:
        logger.warning("⚠️ Faltan campos 'issueKey' o 'description'.")
        return func.HttpResponse(
            body='{"success": false, "message": "Missing issueKey or description."}',
            status_code=400,
            mimetype="application/json"
        )

    # ✅ Procesar operación Jira
    jira_result = process_jira_operations(issue_key, description, {}, req_body.get("issue", {}).get("fields", {}))

    response_message = {
        "success": True,
        "message": "Request processed and Jira updated.",
        "jira_result": jira_result,
        "data_received": req_body
    }

    logger.info(f"📤 Respuesta enviada: {response_message}")

    return func.HttpResponse(
        body=str(response_message),
        status_code=200,
        mimetype="application/json"
    )
