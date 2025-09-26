from abc import ABC, abstractmethod

from tabulate import tabulate


class BaseReport(ABC):
    """Абстрактный базовый класс для проектирования отчёта"""

    @abstractmethod
    def generate(self, data: list) -> dict:
        """
        Генерирует отчет на основе данных

        Описывается логика формирования отчёта
        """

    def print_report(self, result: dict) -> None:
        """
        Выводит отчет в консоль в виде таблицы

        +----+---------------------+---------+
        |    |    student_name     |   grade |
        +====+=====================+=========+
        |  1 |   Семенова Елена    |     5   |
        +----+---------------------+---------+
        |  2 |    Власова Алина    |    4.5  |
        """

        if not result:
            print("Нет данных для отображения")
            return

        headers = result.get("headers", [])
        rows = result.get("rows", [])

        print(tabulate(rows, headers=headers, tablefmt="grid", stralign="center"))
