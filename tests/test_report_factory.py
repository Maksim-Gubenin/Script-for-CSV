import os
import sys
from typing import List

import pytest

from reports.base_report import BaseReport
from reports.report_factory import ReportFactory
from reports.student_performance import StudentPerformanceReport

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestReportFactory:
    """Тесты фабрики отчетов"""

    def setup_method(self) -> None:
        """Сброс состояния фабрики перед каждым тестом"""
        ReportFactory._reports.clear()
        ReportFactory.register_report("student-performance", StudentPerformanceReport)

    def test_register_and_get_report(self) -> None:
        """Тест регистрации и получения отчета"""
        report = ReportFactory.get_report("student-performance")
        assert isinstance(report, StudentPerformanceReport)
        assert isinstance(report, BaseReport)

    def test_get_unknown_report_raises_error(self) -> None:
        """Тест запроса неизвестного отчета"""
        with pytest.raises(ValueError, match="Неизвестный тип отчета: unknown"):
            ReportFactory.get_report("unknown")

    def test_get_available_reports(self) -> None:
        """Тест получения списка доступных отчетов"""
        available = ReportFactory.get_available_reports()
        assert "student-performance" in available
        assert len(available) == 1

    def test_register_multiple_reports(self) -> None:
        """Тест регистрации нескольких отчетов"""

        class TestReport(BaseReport):
            def generate(self, data: List[dict]) -> dict:
                return {"headers": [], "rows": []}

        ReportFactory.register_report("test-report", TestReport)
        available = ReportFactory.get_available_reports()
        assert "student-performance" in available
        assert "test-report" in available
        assert len(available) == 2

    def test_report_instance_has_required_methods(self) -> None:
        """Тест что созданный отчет имеет необходимые методы"""
        report = ReportFactory.get_report("student-performance")
        assert hasattr(report, "generate")
        assert hasattr(report, "print_report")
        assert callable(report.generate)
        assert callable(report.print_report)
