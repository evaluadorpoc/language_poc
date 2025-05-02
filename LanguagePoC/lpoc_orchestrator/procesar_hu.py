from lpoc_validators.evaluador_completo import evaluar_clasico, evaluar_intencion_proposito
from lpoc_jira_connector.enviar_comentario import comentar_en_issue

def procesar_hu(hu: str, issue_key: str = None) -> dict:
    resultado_clasico = evaluar_clasico(hu)

    if resultado_clasico["esValida"]:
        resultado = resultado_clasico
    else:
        resultado_alt = evaluar_intencion_proposito(hu)
        resultado_alt["huOriginal"] = hu
        resultado = resultado_alt

    # Si hay issue_key, intenta comentar en Jira
    if issue_key:
        comentario = generar_comentario(result=resultado)
        exito = comentar_en_issue(issue_key, comentario)
        resultado["comentarioPublicado"] = exito

    return resultado


def generar_comentario(result: dict) -> str:
    detalles = result.get("detalles", {})
    comentario = f"**Evaluación automática de historia de usuario**\n\n"
    comentario += f"- Modalidad detectada: `{result.get('modalidad')}`\n"
    comentario += f"- Resultado: {'✅ Válida' if result.get('esValida') else '❌ Incompleta'}\n"
    comentario += "\n**Detalles:**\n"
    for clave, valor in detalles.items():
        comentario += f"- {clave}: {'Sí' if valor else 'No'}\n"
    return comentario
