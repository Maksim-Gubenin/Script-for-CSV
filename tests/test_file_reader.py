import csv
import os
import sys
import tempfile
from typing import Any, Dict, List

import pytest

from utils.file_reader import read_csv_files

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestFileReader:
    """Тесты для чтения CSV файлов"""

    def test_read_single_valid_file(self) -> None:
        """Тест чтения одного валидного CSV файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(
                ["student_name", "subject", "grade", "teacher_name", "date"]
            )
            writer.writerow(
                ["Иванов Иван", "Математика", "5", "Петров П.П.", "2023-10-10"]
            )
            temp_file = f.name

        try:
            data = read_csv_files([temp_file])
            assert len(data) == 1
            assert data[0]["student_name"] == "Иванов Иван"
            assert data[0]["grade"] == "5"
            assert data[0]["subject"] == "Математика"
        finally:
            os.unlink(temp_file)

    def test_read_multiple_files(self) -> None:
        """Тест чтения нескольких CSV файлов"""
        files: List[str] = []
        try:
            for i in range(2):
                f = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
                writer = csv.writer(f)
                writer.writerow(["student_name", "grade"])
                writer.writerow([f"Студент {i}", f"{i+3}"])
                files.append(f.name)
                f.close()

            data = read_csv_files(files)
            assert len(data) == 2
            assert data[0]["student_name"] == "Студент 0"
            assert data[1]["student_name"] == "Студент 1"
        finally:
            for file in files:
                os.unlink(file)

    def test_file_not_found(self) -> None:
        """Тест обработки отсутствующего файла"""
        with pytest.raises(
            FileNotFoundError, match="Файл nonexistent.csv не существует"
        ):
            read_csv_files(["nonexistent.csv"])

    def test_empty_file(self) -> None:
        """Тест чтения пустого файла (только заголовок)"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(["student_name", "grade"])
            temp_file = f.name

        try:
            data = read_csv_files([temp_file])
            assert len(data) == 0
        finally:
            os.unlink(temp_file)

    def test_file_with_special_characters(self) -> None:
        """Тест чтения файла с специальными символами"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["student_name", "grade"])
            writer.writerow(["Студент с-ёЁ", "5"])
            temp_file = f.name

        try:
            data = read_csv_files([temp_file])
            assert len(data) == 1
            assert data[0]["student_name"] == "Студент с-ёЁ"
        finally:
            os.unlink(temp_file)
