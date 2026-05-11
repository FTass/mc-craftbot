# MC Craftbot - Frontend

Frontend React/Vite para el chatbot de recetas de Minecraft.

## Requisitos

- Node.js compatible con la versión de Vite instalada.
- Backend FastAPI ejecutándose en `http://127.0.0.1:8000`.

## Ejecutar

```powershell
npm install
npm run dev
```

## Configuración del backend

Por defecto el frontend consulta:

```text
http://127.0.0.1:8000/chat
```

Si necesitas cambiarlo, crea un archivo `.env` usando `.env.example` como base:

```text
VITE_CHAT_API_URL=http://127.0.0.1:8000/chat
```

## Build

```powershell
npm run build
```
