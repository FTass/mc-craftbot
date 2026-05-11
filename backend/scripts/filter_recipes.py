import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
recipes_path = os.path.join(script_dir, '../app/data/recipes.json')
with open(recipes_path, 'r', encoding='utf-8') as f:
    recipes = json.load(f)

filtered = [r for r in recipes if r.get('station') == 'Mesa de crafteo']

with open(recipes_path, 'w', encoding='utf-8') as f:
    json.dump(filtered, f, indent=2, ensure_ascii=False)
