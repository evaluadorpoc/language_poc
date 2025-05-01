import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('MiNuevaFuncion fue ejecutada correctamente.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hola, {name}!")
    else:
        return func.HttpResponse(
            "Por favor proporciona un parámetro 'name' en la URL o en el cuerpo JSON.",
            status_code=400
        )
