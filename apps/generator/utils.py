import csv
import os

from faker import Faker

from apps.generator.services import GeneratorService
from utils.upload_dataset import upload_instance

service = GeneratorService


def generate_data(dataset_id):
    dataset_instance = service.get_dataset_by_id(dataset_id)
    headers = service.get_dataset_headers(dataset_instance)
    row_types = service.get_column_types(dataset_instance)

    filename = (
        f'{dataset_instance.schema.title}-'
        f'{dataset_instance.id}-'
        f'{dataset_instance.rows}.csv'
    )

    path = upload_instance(dataset_instance, filename)
    dataset_instance.file.name = path
    dataset_instance.save(update_fields=['file'])
    csv_file_path = dataset_instance.file.path

    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    with open(csv_file_path, 'at') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()

        for i in range(dataset_instance.rows):
            dataset = {}
            for j in range(len(headers)):
                row = generate_row(header=headers[j], row_type=row_types[j])
                _, value = row.popitem()
                dataset[headers[j]] = value

            writer.writerow(dataset)
    dataset_instance.ready = True
    dataset_instance.save(update_fields=['ready'])


def generate_row(header, row_type):
    row = {
        f'{header}': get_data_type_content(row_type['name'], row_type['from'], row_type['to'])
    }
    return row


def get_data_type_content(name, range_from=None, range_to=None):
    fake = Faker('en_US')
    if not range_to and not range_to:
        range_to = 15
        range_from = 10
    format_name = name.lower().replace(' ', '_')
    fake_types = dict(
        date=fake.date(),
        address=fake.address(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        full_name=f'{fake.first_name()} {fake.last_name()}',
        company_name=fake.company(),
        job=fake.job(),
        integer=fake.pyint(min_value=range_from, max_value=range_to),
        text=fake.sentence(nb_words=(fake.pyint(min_value=range_from, max_value=range_to)))
    )

    return fake_types.get(format_name)
