import os
import sys
from typing import Any, List
from unittest.mock import MagicMock, patch

import pytest

from main import main

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestMain:
    """Тесты основной функции приложения"""

    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_success(self, mock_read_csv: Any, mock_factory: Any) -> None:
        """Тест успешного выполнения main"""
        mock_read_csv.return_value = [{"student_name": "Иванов Иван", "grade": "5"}]

        mock_report_instance = MagicMock()
        mock_report_instance.generate.return_value = {
            "headers": ["№", "Студент", "Оценка"],
            "rows": [["1", "Иванов Иван", "5.0"]],
        }
        mock_factory.get_report.return_value = mock_report_instance
        mock_factory.get_available_reports.return_value = ["student-performance"]

        with patch(
            "sys.argv",
            ["main.py", "--files", "test.csv", "--report", "student-performance"],
        ):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_not_called()

        mock_read_csv.assert_called_with(["test.csv"])
        mock_factory.get_report.assert_called_with("student-performance")
        mock_report_instance.generate.assert_called_once()

    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_file_not_found(self, mock_read_csv: Any, mock_factory: Any) -> None:
        """Тест обработки FileNotFoundError"""
        mock_read_csv.side_effect = FileNotFoundError("Файл не найден")
        mock_factory.get_available_reports.return_value = ["student-performance"]

        with patch(
            "sys.argv",
            [
                "main.py",
                "--files",
                "nonexistent.csv",
                "--report",
                "student-performance",
            ],
        ):
            with patch("sys.exit") as mock_exit:
                with patch("sys.stderr"):
                    main()
                    mock_exit.assert_called_with(1)

    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_value_error(self, mock_read_csv: Any, mock_factory: Any) -> None:
        """Тест обработки ValueError"""
        mock_factory.get_report.side_effect = ValueError("Неизвестный отчет")
        mock_factory.get_available_reports.return_value = ["student-performance"]

        with patch(
            "sys.argv", ["main.py", "--files", "test.csv", "--report", "unknown"]
        ):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_with(1)

    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_empty_data(self, mock_read_csv: Any, mock_factory: Any) -> None:
        """Тест обработки пустых данных"""
        mock_read_csv.return_value = []
        mock_factory.get_available_reports.return_value = ["student-performance"]

        with patch(
            "sys.argv",
            ["main.py", "--files", "empty.csv", "--report", "student-performance"],
        ):
            with patch("sys.exit") as mock_exit:
                with patch("sys.stdout"):
                    main()
                    mock_exit.assert_not_called()

    def test_main_missing_required_arguments(self) -> None:
        """Тест отсутствия обязательных аргументов"""
        with patch("sys.argv", ["main.py"]):
            with pytest.raises(SystemExit):
                main()

    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_key_error(self, mock_read_csv: Any, mock_factory: Any) -> None:
        """Тест обработки KeyError при обработке данных"""
        mock_read_csv.return_value = [{"student_name": "Иванов Иван"}]
        mock_report_instance = MagicMock()
        mock_report_instance.generate.side_effect = KeyError(
            "Отсутствует обязательное поле"
        )
        mock_factory.get_report.return_value = mock_report_instance
        mock_factory.get_available_reports.return_value = ["student-performance"]

        with patch(
            "sys.argv",
            ["main.py", "--files", "test.csv", "--report", "student-performance"],
        ):
            with patch("sys.exit") as mock_exit:
                with patch("sys.stderr"):
                    main()
                    mock_exit.assert_called_with(1)

    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_type_error(self, mock_read_csv: Any, mock_factory: Any) -> None:
        """Тест обработки TypeError при обработке данных"""
        mock_read_csv.return_value = [{"student_name": "Иванов Иван", "grade": "5"}]
        mock_report_instance = MagicMock()
        mock_report_instance.generate.side_effect = TypeError("Неверный тип данных")
        mock_factory.get_report.return_value = mock_report_instance
        mock_factory.get_available_reports.return_value = ["student-performance"]

        with patch(
            "sys.argv",
            ["main.py", "--files", "test.csv", "--report", "student-performance"],
        ):
            with patch("sys.exit") as mock_exit:
                with patch("sys.stderr"):
                    main()
                    mock_exit.assert_called_with(1)

    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_io_error(self, mock_read_csv: Any, mock_factory: Any) -> None:
        """Тест обработки IOError при чтении файлов"""
        mock_read_csv.side_effect = IOError("Ошибка ввода-вывода")
        mock_factory.get_available_reports.return_value = ["student-performance"]

        with patch(
            "sys.argv",
            ["main.py", "--files", "test.csv", "--report", "student-performance"],
        ):
            with patch("sys.exit") as mock_exit:
                with patch("sys.stderr"):
                    main()
                    mock_exit.assert_called_with(1)

    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_generic_exception(
        self, mock_read_csv: Any, mock_factory: Any
    ) -> None:
        """Тест обработки других исключений в блоке обработки данных"""
        mock_read_csv.return_value = [{"student_name": "Иванов Иван", "grade": "5"}]
        mock_report_instance = MagicMock()
        mock_report_instance.generate.side_effect = Exception("Неожиданная ошибка")
        mock_factory.get_report.return_value = mock_report_instance
        mock_factory.get_available_reports.return_value = ["student-performance"]

        with patch(
            "sys.argv",
            ["main.py", "--files", "test.csv", "--report", "student-performance"],
        ):
            with patch("sys.exit"):
                with patch("sys.stderr"):
                    with pytest.raises(Exception):
                        main()
