import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
recipes_path = os.path.join(script_dir, '../app/data/recipes.json')

with open(recipes_path, 'r', encoding='utf-8') as f:
    recipes = json.load(f)

# Diccionario de reemplazos para los shulker boxes
reemplazos = {
    "Morado shulker box": "shulker box morado",
    "Marrón shulker box": "shulker box marrón",
    "Azul shulker box": "shulker box azul",
    # Agrega los demás colores que encuentres
}

# Función para reemplazar en todos los campos
def reemplazar_en_objeto(obj, reemplazos):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                for viejo, nuevo in reemplazos.items():
                    obj[key] = value.replace(viejo, nuevo)
            else:
                reemplazar_en_objeto(value, reemplazos)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, str):
                for viejo, nuevo in reemplazos.items():
                    obj[i] = item.replace(viejo, nuevo)
            else:
                reemplazar_en_objeto(item, reemplazos)

reemplazar_en_objeto(recipes, reemplazos)

with open(recipes_path, 'w', encoding='utf-8') as f:
    json.dump(recipes, f, indent=2, ensure_ascii=False)

