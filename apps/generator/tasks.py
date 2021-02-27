from apps.generator.utils import generate_data
from core.celery import app


@app.task(name="generate_dataset_data")
def generate_dataset_data(dataset_id):
    generate_data(dataset_id)
