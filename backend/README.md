# Backend — MC Craftbot

Backend local para el chatbot de crafteos de Minecraft. Usa FastAPI, una base de conocimiento estructurada en JSON y Ollama con `llama3.2:latest`.

## Ubicación esperada

La estructura correcta del proyecto es:

```text
mc-craftbot/
├── mc-chatbot/   # frontend React/Vite
└── backend/      # este backend
```

## Requisitos

- Python 3.10 o superior.
- Ollama instalado.
- Modelo local `llama3.2:latest` disponible.

Verificar Ollama:

```powershell
ollama list
Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get
```

## Instalación

Desde `mc-craftbot/backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno virtual:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Ejecutar backend

```powershell
uvicorn app.main:app --reload
```

URL local:

```text
http://127.0.0.1:8000
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### GET `/health`

Verifica estado del backend y número de recetas cargadas.

Para revisar también Ollama:

```text
http://127.0.0.1:8000/health?check_ollama=true
```

### GET `/recipes`

Lista todas las recetas cargadas desde `app/data/recipes.json`.

### POST `/chat`

Contrato recomendado desde el frontend:

```json
{
  "message": "¿Cómo hago un pico de madera?"
}
```

Respuesta:

```json
{
  "status": "answered",
  "answer": "...",
  "matched_item": "Pico de madera",
  "matched_recipe_id": "wooden_pickaxe",
  "source": "recipes.json",
  "suggestions": ["Pico de madera"]
}
```

También acepta `question` como alias temporal:

```json
{
  "question": "¿Cómo hago un horno?"
}
```

## Pruebas

Desde `backend`:

```powershell
pytest
python scripts/test_ollama_connection.py
```

Las pruebas unitarias no requieren Ollama porque simulan la respuesta del modelo. El script `test_ollama_connection.py` sí requiere que Ollama esté corriendo.

## Cómo agregar recetas

Editar:

```text
backend/app/data/recipes.json
```

Cada receta debe tener esta estructura mínima:

```json
{
  "id": "wooden_pickaxe",
  "name": "Pico de madera",
  "aliases": ["pico de madera", "pico madera", "wooden pickaxe"],
  "category": "herramienta",
  "station": "mesa de crafteo",
  "ingredients": [
    { "item": "Tablones de madera", "quantity": 3 },
    { "item": "Palos", "quantity": 2 }
  ],
  "grid": [
    ["Tablón", "Tablón", "Tablón"],
    [null, "Palo", null],
    [null, "Palo", null]
  ],
  "steps": ["Abre la mesa de crafteo."],
  "usage": "Sirve para minar piedra y bloques básicos."
}
```

## Variables de entorno opcionales

```powershell
$env:OLLAMA_BASE_URL="http://localhost:11434"
$env:OLLAMA_MODEL="llama3.2:latest"
$env:CORS_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
```
