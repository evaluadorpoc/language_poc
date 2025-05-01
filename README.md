# 🚀 LanguagePoC – Azure Function para evaluación de Historias de Usuario

Este proyecto implementa una Azure Function (`LanguagePoC`) que recibe una historia de usuario (HU) y evalúa su calidad utilizando servicios cognitivos de Azure.

---

## 🧩 Funcionalidad actual

La función expone un endpoint HTTP que recibe un JSON con una historia de usuario y responde con un análisis estructurado.

### 🔁 Flujo básico

```
POST /api/LanguagePoC
```

### 🔷 Ejemplo de entrada:

```json
{
  "hu": "Como usuario quiero guardar mis búsquedas favoritas para volver a ellas después"
}
```

### 🔷 Ejemplo de salida esperada:

```json
{
  "esValida": true,
  "detalles": {
    "tieneSujeto": true,
    "tieneAcción": true,
    "tieneResultado": true,
    "análisis": "La HU es clara, tiene estructura de usuario + acción + objetivo.",
    "score": 0.95
  }
}
```

---

## 🧠 Servicios utilizados

- [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Azure Cognitive Services – Text Analytics](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/overview)
- GitHub Actions para CI/CD
- Postman para pruebas manuales

---

## 🚀 Despliegue

Este proyecto se despliega automáticamente a la Azure Function App:

```
jira-azure-validator.azurewebsites.net
```

Rutas disponibles:

- `POST /api/HttpTrigger`
- `POST /api/LanguagePoC`

---

## 🛠️ Estructura del proyecto

```
├── HttpTrigger/           → Función original
├── LanguagePoC/           → Nueva función cognitiva
├── .github/workflows/     → CI/CD con GitHub Actions
├── host.json              → Config global
├── requirements.txt       → Dependencias Python
├── local.settings.json    → Config local (excluido de Git)
```

---

## 🧪 Probar desde Postman

1. Método: `POST`
2. URL: `https://jira-azure-validator.azurewebsites.net/api/LanguagePoC`
3. Headers:  
   - `Content-Type: application/json`
4. Body:

```json
{
  "hu": "Como usuario quiero visualizar mis métricas para tomar mejores decisiones"
}
```

---

## 🔐 Seguridad

Las funciones pueden requerir API key en ambientes productivos. Actualmente accesible vía URL con código (`?code=...`) incluido automáticamente por Azure.

---

## 👨‍💻 Autor

Paúl Sánchez  
Proyecto desarrollado como parte del PoC 2.0 para evaluación inteligente de historias de usuario en entornos ágiles.

---

## 📄 Licencia

MIT License
