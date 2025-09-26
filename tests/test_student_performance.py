import os
import sys
from typing import Any, Dict, List

from reports.student_performance import StudentPerformanceReport

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestStudentPerformanceReport:
    """Тесты отчета успеваемости студентов"""

    def test_generate_empty_data(self) -> None:
        """Тест с пустыми данными"""
        report = StudentPerformanceReport()
        result = report.generate([])

        assert result["headers"] == ["", "student_name", "grade"]
        assert not result["rows"]

    def test_generate_single_student_single_grade(self) -> None:
        """Тест с одним студентом и одной оценкой"""
        report = StudentPerformanceReport()
        data = [{"student_name": "Иванов Иван", "grade": "5", "subject": "Математика"}]

        result = report.generate(data)

        assert len(result["rows"]) == 1
        assert result["rows"][0][1] == "Иванов Иван"
        assert result["rows"][0][2] == 5.0

    def test_generate_single_student_multiple_grades(self) -> None:
        """Тест с одним студентом и несколькими оценками"""
        report = StudentPerformanceReport()
        data = [
            {"student_name": "Иванов Иван", "grade": "5"},
            {"student_name": "Иванов Иван", "grade": "4"},
            {"student_name": "Иванов Иван", "grade": "3"},
        ]

        result = report.generate(data)

        assert len(result["rows"]) == 1
        assert result["rows"][0][1] == "Иванов Иван"
        assert result["rows"][0][2] == 4.0

    def test_generate_multiple_students_sorted(self) -> None:
        """Тест сортировки нескольких студентов по убыванию оценки"""
        report = StudentPerformanceReport()
        data = [
            {"student_name": "Студент A", "grade": "3"},
            {"student_name": "Студент A", "grade": "4"},
            {"student_name": "Студент B", "grade": "5"},
            {"student_name": "Студент C", "grade": "4"},
        ]

        result = report.generate(data)

        assert result["rows"][0][1] == "Студент B"
        assert result["rows"][1][1] == "Студент C"
        assert result["rows"][2][1] == "Студент A"

    def test_generate_ignores_invalid_grades(self) -> None:
        """Тест игнорирования некорректных оценок"""
        report = StudentPerformanceReport()
        data = [
            {"student_name": "Тест", "grade": "5"},
            {"student_name": "Тест", "grade": "invalid"},
            {"student_name": "Тест", "grade": "4"},
        ]

        result = report.generate(data)

        assert len(result["rows"]) == 1
        assert result["rows"][0][2] == 4.5

    def test_generate_ignores_missing_grade_field(self) -> None:
        """Тест игнорирования записей без поля grade"""
        report = StudentPerformanceReport()
        data = [
            {"student_name": "Тест", "grade": "5"},
            {"student_name": "Тест"},
            {"student_name": "Тест", "grade": "4"},
        ]

        result = report.generate(data)

        assert len(result["rows"]) == 1
        assert result["rows"][0][2] == 4.5

    def test_generate_result_structure(self) -> None:
        """Тест структуры возвращаемых данных"""
        report = StudentPerformanceReport()
        data = [{"student_name": "Тест", "grade": "5"}]

        result = report.generate(data)

        assert "headers" in result
        assert "rows" in result
        assert isinstance(result["headers"], list)
        assert isinstance(result["rows"], list)
        assert len(result["headers"]) == 3
        assert result["headers"] == ["", "student_name", "grade"]
