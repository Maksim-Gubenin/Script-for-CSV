import os
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from reports.base_report import BaseReport

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestBaseReport:
    """Тесты базового класса отчета"""

    def test_abstract_method_raises_error(self) -> None:
        """Тест что нельзя создать экземпляр абстрактного класса"""
        with pytest.raises(TypeError):
            BaseReport()  # type: ignore

    def test_concrete_class_must_implement_generate(self) -> None:
        """Тест что конкретный класс должен реализовать generate"""

        class InvalidReport(BaseReport):  # type: ignore
            pass

        with pytest.raises(TypeError):
            InvalidReport()  # type: ignore

    def test_valid_concrete_class(self) -> None:
        """Тест корректной реализации абстрактного класса"""

        class ValidReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {"headers": [], "rows": []}

        report = ValidReport()
        assert hasattr(report, "generate")
        assert hasattr(report, "print_report")

    def test_print_report_empty_data(self) -> None:
        """Тест вывода пустого отчета"""

        class TestReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {}

        report = TestReport()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            report.print_report({})
            output = mock_stdout.getvalue()
            assert "Нет данных для отображения" in output

    def test_print_report_valid_data(self) -> None:
        """Тест вывода валидных данных"""

        class TestReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {}

        report = TestReport()
        test_result = {
            "headers": ["Name", "Grade"],
            "rows": [["John", "5"], ["Jane", "4"]],
        }

        with patch("sys.stdout", new_callable=StringIO):
            with patch("reports.base_report.tabulate") as mock_tabulate:
                report.print_report(test_result)
                mock_tabulate.assert_called_once_with(
                    [["John", "5"], ["Jane", "4"]],
                    headers=["Name", "Grade"],
                    tablefmt="grid",
                    stralign="center",
                )

    def test_print_report_missing_headers(self) -> None:
        """Тест вывода с отсутствующими заголовками"""

        class TestReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {}

        report = TestReport()
        test_result = {"rows": [["Data1", "Data2"]]}

        with patch("sys.stdout", new_callable=StringIO):
            with patch("reports.base_report.tabulate") as mock_tabulate:
                report.print_report(test_result)
                mock_tabulate.assert_called_with(
                    [["Data1", "Data2"]], headers=[], tablefmt="grid", stralign="center"
                )
