import azure.functions as func
import json
from orchestrator.procesar_hu import procesar_hu

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        hu = body.get("description")
        issue_key = body.get("issueKey")

        if not hu:
            return func.HttpResponse("Campo 'description' requerido", status_code=400)

        resultado = procesar_hu(hu, issue_key)
        return func.HttpResponse(json.dumps(resultado, ensure_ascii=False), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(f"Error interno: {str(e)}", status_code=500)
