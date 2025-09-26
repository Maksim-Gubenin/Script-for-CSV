from typing import Dict, List, Type

from reports.base_report import BaseReport
from reports.student_performance import StudentPerformanceReport


class ReportFactory:
    """Фабрика для создания отчетов"""

    _reports: Dict[str, Type[BaseReport]] = {}

    @classmethod
    def get_report(cls, report_name: str) -> BaseReport:
        """Создает экземпляр отчета по имени"""
        report_class = cls._reports.get(report_name)
        if not report_class:
            raise ValueError(f"Неизвестный тип отчета: {report_name}")
        return report_class()

    @classmethod
    def get_available_reports(cls) -> List[str]:
        """Возвращает список доступных отчетов"""
        return list(cls._reports.keys())

    @classmethod
    def register_report(cls, report_name: str, report_class: Type[BaseReport]) -> None:
        """Регистрирует новый тип отчета"""
        cls._reports[report_name] = report_class


# Регистрация отчетов
ReportFactory.register_report("student-performance", StudentPerformanceReport)
