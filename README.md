apt-get update && apt-get install -y libgl1 libglib2.0-0

python -m rec.one_by_one.main --dataset various_forms_hangul --recipe rec/one_by_one/recipe.yaml