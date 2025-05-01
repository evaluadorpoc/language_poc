import sys
import os
import logging
import azure.functions as func

# Agregamos HttpTrigger al sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from main import process_request

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🔵 Nueva solicitud recibida.")
    try:
        response = process_request(req)
        logging.info("🟢 Solicitud procesada exitosamente.")
        return response
    except Exception as e:
        logging.error(f"🔴 Error procesando solicitud: {e}", exc_info=True)
        return func.HttpResponse(
            "Error interno en el servidor. Revisar logs.",
            status_code=500
        )
    