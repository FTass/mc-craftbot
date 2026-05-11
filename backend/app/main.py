from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.ollama_client import OllamaClientError, ask_ollama, is_ollama_available
from app.prompt_builder import SYSTEM_PROMPT, build_user_prompt
from app.recipe_store import get_recipe_store
from app.schemas import ChatRequest, ChatResponse, HealthResponse, Recipe


settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend local para MC Craftbot usando FastAPI, base de recetas y Ollama.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
def health(check_ollama: bool = Query(default=False, description="If true, checks Ollama /api/tags.")):
    store = get_recipe_store()
    ollama_available = None
    if check_ollama:
        ollama_available = is_ollama_available()

    return HealthResponse(
        status="ok",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        recipes_loaded=store.count(),
        ollama_model=settings.OLLAMA_MODEL,
        ollama_checked=check_ollama,
        ollama_available=ollama_available,
    )


@app.get("/recipes", response_model=list[Recipe])
def list_recipes():
    return get_recipe_store().recipes


@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: str):
    recipe = get_recipe_store().get_by_id(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada.")
    return recipe


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    user_text = payload.text()
    if not user_text:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")

    store = get_recipe_store()
    recipe, suggestions = store.find(user_text)

    if recipe is None:
        return ChatResponse(
            status="not_found",
            answer=(
                "No tengo información suficiente en la base de conocimiento para responder eso. "
                "Puedo ayudarte con objetos registrados como: " + ", ".join(suggestions) + "."
            ),
            matched_item=None,
            matched_recipe_id=None,
            suggestions=suggestions,
        )

    user_prompt = build_user_prompt(recipe=recipe, user_question=user_text)

    try:
        answer = ask_ollama(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    except OllamaClientError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ChatResponse(
        status="answered",
        answer=answer,
        matched_item=recipe.name,
        matched_recipe_id=recipe.id,
        suggestions=suggestions,
    )
