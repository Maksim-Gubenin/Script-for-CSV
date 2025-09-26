import argparse
import sys

from reports.report_factory import ReportFactory
from utils.file_reader import read_csv_files


def main() -> None:
    """
    Основная функция приложения

    Принимает список файлов и тип необходимого отчёта.
    Генерирует соответствующий отчёт.
    """

    parser = argparse.ArgumentParser(
        description="Анализ успеваемости студентов",
    )
    parser.add_argument(
        "--files",
        required=True,
        nargs="+",
        help="Пути к CSV файлам через пробел",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=ReportFactory.get_available_reports(),
        help="Тип отчета для генерации",
    )

    args = parser.parse_args()

    try:
        data = read_csv_files(args.files)

        if not data:
            print("Нет данных для анализа")
            return

        report = ReportFactory.get_report(args.report)
        result = report.generate(data)
        report.print_report(result)

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка в данных: {e}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, TypeError, IOError) as e:
        print(f"Ошибка при обработке данных: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
