docker run -it -v ~/prj/paddle-dataset-converter:/app -v /mnt/data1/ai/dataset:/data -w /app python:3.12 bash

apt-get update && apt-get install -y libgl1 libglib2.0-0

pip install -r requirements.txt

python -m rec.one_by_one.main --dataset various_forms_hangul --recipe rec/one_by_one/recipe.yaml