import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable

from app.schemas import Recipe
from app.config import get_settings


QUESTION_STOP_PHRASES = [
    "como hago",
    "como hacer",
    "como crafteo",
    "como fabricar",
    "como fabrico",
    "quiero hacer",
    "quiero craftear",
    "necesito hacer",
    "necesito craftear",
    "receta de",
    "materiales para",
    "minecraft",
]


def normalize_text(value: str) -> str:
    """Normalize user text for resilient recipe matching.

    - lowercase
    - remove accents
    - remove punctuation
    - collapse whitespace
    """
    value = value.lower().strip()
    value = "".join(
        char for char in unicodedata.normalize("NFD", value)
        if unicodedata.category(char) != "Mn"
    )
    value = re.sub(r"[^a-z0-9ñ\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def simplify_question(value: str) -> str:
    normalized = normalize_text(value)
    simplified = normalized
    for phrase in QUESTION_STOP_PHRASES:
        simplified = simplified.replace(phrase, " ")
    simplified = re.sub(r"\s+", " ", simplified).strip()
    return simplified or normalized


class RecipeStore:
    """Loads and searches the local crafting knowledge base."""

    def __init__(self, recipes_path: Path | None = None):
        self.recipes_path = recipes_path or get_settings().RECIPES_PATH
        self._recipes: list[Recipe] = []
        self._index: list[tuple[str, Recipe]] = []
        self.load()

    def load(self) -> None:
        if not self.recipes_path.exists():
            raise FileNotFoundError(f"No existe el archivo de recetas: {self.recipes_path}")

        raw = json.loads(self.recipes_path.read_text(encoding="utf-8"))
        self._recipes = [Recipe.model_validate(item) for item in raw]
        self._index = []
        for recipe in self._recipes:
            terms = [recipe.name, recipe.id, *recipe.aliases]
            for term in terms:
                self._index.append((normalize_text(term), recipe))

    @property
    def recipes(self) -> list[Recipe]:
        return self._recipes

    def count(self) -> int:
        return len(self._recipes)

    def get_by_id(self, recipe_id: str) -> Recipe | None:
        recipe_id_norm = normalize_text(recipe_id).replace(" ", "_")
        for recipe in self._recipes:
            if normalize_text(recipe.id).replace(" ", "_") == recipe_id_norm:
                return recipe
        return None

    def suggestions(self, limit: int = 8) -> list[str]:
        return [recipe.name for recipe in self._recipes[:limit]]

    def find(self, user_text: str) -> tuple[Recipe | None, list[str]]:
        """Return the best matching recipe and alternative suggestions.

        The search is intentionally conservative. If confidence is too low, it returns
        None so the chatbot does not invent undocumented recipes.
        """
        query = normalize_text(user_text)
        simplified = simplify_question(user_text)
        if not query:
            return None, self.suggestions()

        candidates: list[tuple[float, Recipe, str]] = []

        for term, recipe in self._index:
            if not term:
                continue

            # Exact match after simplification.
            if simplified == term or query == term:
                candidates.append((100.0, recipe, term))
                continue

            # User sentence contains the full alias/name.
            if term in query:
                candidates.append((90.0 + min(len(term) / 10, 8), recipe, term))
                continue

            # Alias/name contains the simplified object phrase.
            if simplified and simplified in term and len(simplified) >= 4:
                candidates.append((75.0 + min(len(simplified) / 10, 8), recipe, term))
                continue

            # Token subset matching for phrases like "hacer pico madera".
            term_tokens = set(term.split())
            query_tokens = set(simplified.split()) or set(query.split())
            if term_tokens and term_tokens.issubset(query_tokens):
                candidates.append((82.0 + len(term_tokens), recipe, term))
                continue

            # Conservative fuzzy matching.
            ratio = SequenceMatcher(None, simplified, term).ratio()
            if ratio >= 0.78:
                candidates.append((70.0 * ratio, recipe, term))

        if not candidates:
            return None, self.suggestions()

        candidates.sort(key=lambda item: item[0], reverse=True)
        best_score, best_recipe, _ = candidates[0]

        # Avoid weak fuzzy matches.
        if best_score < 55:
            return None, self.suggestions()

        # Generate unique suggestions from top candidates.
        seen = set()
        alternatives: list[str] = []
        for _, recipe, _ in candidates:
            if recipe.name not in seen:
                alternatives.append(recipe.name)
                seen.add(recipe.name)
            if len(alternatives) >= 5:
                break

        return best_recipe, alternatives


# Lazy singleton used by the API.
_store: RecipeStore | None = None


def get_recipe_store() -> RecipeStore:
    global _store
    if _store is None:
        _store = RecipeStore()
    return _store
