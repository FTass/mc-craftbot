from app.recipe_store import get_recipe_store, normalize_text, simplify_question


def test_normalize_text_removes_accents_and_punctuation():
    assert normalize_text("¿Cómo hago una Caña de pescar?") == "como hago una cana de pescar"


def test_simplify_question_removes_common_phrases():
    assert "pico de madera" in simplify_question("¿Cómo hago un pico de madera en Minecraft?")


def test_store_loads_recipes():
    store = get_recipe_store()
    assert store.count() >= 10


def test_find_wooden_pickaxe_from_question():
    store = get_recipe_store()
    recipe, suggestions = store.find("¿Cómo hago un pico de madera?")
    assert recipe is not None
    assert recipe.id == "wooden_pickaxe"
    assert "Pico de madera" in suggestions


def test_find_furnace_from_question():
    store = get_recipe_store()
    recipe, _ = store.find("necesito fabricar un horno")
    assert recipe is not None
    assert recipe.id == "furnace"


def test_unknown_recipe_returns_none():
    store = get_recipe_store()
    recipe, suggestions = store.find("¿Cómo hago una mesa de encantamientos?")
    assert recipe is None
    assert len(suggestions) > 0
