
import os
import logging
import json
import spacy
import azure.functions as func

# Inicializar modelo spaCy
nlp = spacy.load("es_core_news_md")
logger = logging.getLogger("azure")
logger.setLevel(logging.INFO)

def separar_palabras_concatenadas(palabra):
    return palabra if palabra.islower() or palabra.isupper() else None

def evaluar_clasico(titulo):
    doc = nlp(titulo)
    rol, accion, objetivo = None, None, None

    for token in doc:
        if token.text.lower() == 'como' and token.i + 1 < len(doc):
            siguiente_token = doc[token.i + 1]
            separado = separar_palabras_concatenadas(siguiente_token.text)
            if siguiente_token.pos_ in ["NOUN", "PROPN"] or separado:
                rol = separado if separado else siguiente_token.text
        if token.lemma_ == 'querer' and token.i + 1 < len(doc):
            siguiente_token = doc[token.i + 1]
            if siguiente_token.pos_ == 'VERB':
                accion = siguiente_token.lemma_
            elif siguiente_token.pos_ in ["AUX", "PRON"] and token.i + 2 < len(doc):
                posible_verbo = doc[token.i + 2]
                if posible_verbo.pos_ == "VERB":
                    accion = posible_verbo.lemma_
        if token.text.lower() == 'para' and token.i + 1 < len(doc):
            objetivo = ' '.join([t.text for t in doc[token.i + 1:]])

    if not accion:
        for token in doc:
            if token.pos_ == "VERB" and token.dep_ in ["ROOT", "aux"]:
                accion = token.lemma_
                break

    detalles = {
        "Rol": rol is not None,
        "Acción": accion is not None,
        "Objetivo": objetivo is not None and len(objetivo.split()) > 1 if objetivo else False
    }

    puntuacion = sum(detalles.values())
    return {
        "esValida": puntuacion == 3,
        "modalidad": "clasica" if puntuacion == 3 else "incompleta",
        "detalles": detalles,
        "huOriginal": titulo
    }

def evaluar_intencion_proposito(texto):
    doc = nlp(texto)
    tiene_verbo = False
    tiene_sujeto = False
    tiene_proposito = False
    tiene_alcance = False

    for sent in doc.sents:
        tiene_verbo_en_oracion = False
        tiene_sujeto_en_oracion = False
        tiene_objetivo_en_oracion = False

        for token in sent:
            if token.pos_ == "VERB":
                tiene_verbo = True
                tiene_verbo_en_oracion = True
            if "subj" in token.dep_:
                tiene_sujeto = True
                tiene_sujeto_en_oracion = True
            if token.pos_ == "VERB" and any(child.dep_ in ["obj", "obl"] for child in token.children):
                tiene_proposito = True
                tiene_objetivo_en_oracion = True
            if token.pos_ in ["NOUN", "PROPN"]:
                tiene_alcance = True

        if tiene_verbo_en_oracion and tiene_sujeto_en_oracion and tiene_objetivo_en_oracion:
            break

    puntuacion = sum([tiene_verbo, tiene_sujeto, tiene_proposito, tiene_alcance])
    return {
        "esValida": puntuacion >= 3,
        "modalidad": "intencion_proposito" if puntuacion >= 3 else "incompleta",
        "detalles": {
            "TieneVerbo": tiene_verbo,
            "TieneSujeto": tiene_sujeto,
            "TieneProposito": tiene_proposito,
            "TieneAlcance": tiene_alcance
        }
    }

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        hu = body.get("hu")
        if not hu:
            return func.HttpResponse("Campo 'hu' requerido", status_code=400)

        resultado_clasico = evaluar_clasico(hu)
        if resultado_clasico["esValida"]:
            return func.HttpResponse(json.dumps(resultado_clasico, ensure_ascii=False), mimetype="application/json")

        resultado_alt = evaluar_intencion_proposito(hu)
        resultado_alt["huOriginal"] = hu
        return func.HttpResponse(json.dumps(resultado_alt, ensure_ascii=False), mimetype="application/json")

    except Exception as e:
        logger.error(f"Error en ejecución: {str(e)}")
        return func.HttpResponse("Error interno del servidor", status_code=500)
