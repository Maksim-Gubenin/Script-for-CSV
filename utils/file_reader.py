import csv
import os


def read_csv_files(file_paths: list) -> list[dict]:
    """Читает данные из нескольких CSV файлов"""

    all_data = []

    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не существует")

        with open(file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                all_data.append(row)

    return all_data
