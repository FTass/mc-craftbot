from app.schemas import Recipe


SYSTEM_PROMPT = """
Eres MC Craftbot, un asistente educativo especializado únicamente en objetos fabricables mediante mesa de crafteo en Minecraft.
EXCEPCIÓN ESPECIAL: Si la pregunta es sobre Herobrine, puedes responder de forma creativa y creepy, sin limitarte a la base de datos.
Reglas obligatorias:
1. Responde siempre en español.
2. Usa exclusivamente la receta entregada en el contexto.
3. No inventes materiales, cantidades, posiciones, usos ni nombres de objetos.
4. Si el contexto no permite responder, indica que no hay información suficiente.
5. Explica en este orden: materiales necesarios, patrón de crafteo, pasos y uso.
6. No respondas sobre mods, servidores, comandos, programación, redstone avanzada o temas fuera de la base de conocimiento.
7. Mantén una respuesta clara, breve y paso a paso.

""".strip()


def _format_grid(grid: list[list[str | None]]) -> str:
    lines = []
    for idx, row in enumerate(grid, start=1):
        cells = [cell if cell is not None else "vacío" for cell in row]
        lines.append(f"Fila {idx}: " + " | ".join(cells))
    return "\n".join(lines)


def build_user_prompt(recipe: Recipe, user_question: str) -> str:
    ingredients = "\n".join(
        f"- {ingredient.quantity:g} {ingredient.unit + ' de ' if ingredient.unit else ''}{ingredient.item}"
        for ingredient in recipe.ingredients
    )
    steps = "\n".join(f"{index}. {step}" for index, step in enumerate(recipe.steps, start=1))
    aliases = ", ".join(recipe.aliases) if recipe.aliases else "sin alias"

    return f"""
Contexto de conocimiento autorizado:
Objeto: {recipe.name}
ID: {recipe.id}
Alias conocidos: {aliases}
Categoría: {recipe.category}
Estación de fabricación: {recipe.station}

Materiales necesarios:
{ingredients}

Patrón de crafteo:
{_format_grid(recipe.grid)}

Pasos documentados:
{steps}

Uso documentado:
{recipe.usage}

Notas adicionales:
{recipe.notes or "No hay notas adicionales."}

Pregunta del usuario:
{user_question}

Instrucción final:
Responde solo con la información autorizada anterior. No agregues recetas alternativas ni datos externos.
""".strip()
