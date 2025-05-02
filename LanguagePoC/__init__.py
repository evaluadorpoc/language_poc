import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import azure.functions as func
import logging
import json

endpoint = os.getenv("TEXT_ANALYTICS_ENDPOINT")
key = os.getenv("TEXT_ANALYTICS_KEY")

credential = AzureKeyCredential(key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        hu = body.get("hu")

        if not hu:
            return func.HttpResponse("Campo 'hu' requerido", status_code=400)

        # Análisis con Azure
        response = text_analytics_client.extract_key_phrases([hu])[0]
        frases = response.key_phrases if not response.is_error else []

        tiene_sujeto = any("usuario" in f.lower() for f in frases)
        tiene_accion = any(word in hu.lower() for word in ["quiero", "puedo", "debo"])
        tiene_resultado = any(word in hu.lower() for word in ["para", "con el fin", "a fin de"])

        resultado = {
            "esValida": tiene_sujeto and tiene_accion and tiene_resultado,
            "detalles": {
                "tieneSujeto": tiene_sujeto,
                "tieneAcción": tiene_accion,
                "tieneResultado": tiene_resultado,
                "frasesClave": frases
            }
        }

        return func.HttpResponse(json.dumps(resultado), mimetype="application/json")

    except Exception as e:
        logging.exception("Error al procesar HU")
        return func.HttpResponse("Error interno del servidor", status_code=500)
