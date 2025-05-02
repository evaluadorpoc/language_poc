#comment to commit anything
import os
import logging
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import azure.functions as func

# Configurar logs
logger = logging.getLogger("azure")
logger.setLevel(logging.INFO)

# Variables de entorno
endpoint = os.getenv("TEXT_ANALYTICS_ENDPOINT")
key = os.getenv("TEXT_ANALYTICS_KEY")

try:
    if not endpoint or not key:
        raise ValueError("Faltan variables de entorno TEXT_ANALYTICS_ENDPOINT o TEXT_ANALYTICS_KEY")

    credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

except Exception as init_error:
    logging.error(f"Error inicializando TextAnalyticsClient: {init_error}")
    text_analytics_client = None  # Para que no se rompa la función

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        hu = body.get("hu")

        if not hu:
            return func.HttpResponse("Campo 'hu' requerido", status_code=400)

        if not text_analytics_client:
            return func.HttpResponse("TextAnalyticsClient no inicializado", status_code=500)

        response = text_analytics_client.extract_key_phrases([hu])[0]

        if response.is_error:
            logging.error(f"Error desde Azure Text Analytics: {response.error}")
            return func.HttpResponse("Error analizando la HU", status_code=502)

        frases = response.key_phrases
        tiene_sujeto = any("usuario" in f.lower() for f in frases)
        tiene_accion = any(word in hu.lower() for word in ["quiero", "puedo", "debo"])
        tiene_resultado = any(word in hu.lower() for word in ["para", "a fin de", "con el fin"])

        resultado = {
            "esValida": tiene_sujeto and tiene_accion and tiene_resultado,
            "detalles": {
                "tieneSujeto": tiene_sujeto,
                "tieneAcción": tiene_accion,
                "tieneResultado": tiene_resultado,
                "frasesClave": frases,
                "huOriginal": hu
            }
        }

        return func.HttpResponse(json.dumps(resultado), mimetype="application/json", status_code=200)

    except Exception as e:
        logging.exception("Error inesperado en LanguagePoC")
        return func.HttpResponse("Error interno del servidor", status_code=500)
