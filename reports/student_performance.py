from collections import defaultdict

from .base_report import BaseReport


class StudentPerformanceReport(BaseReport):
    """Отчет об успеваемости студентов"""

    def generate(self, data: list) -> dict:
        """
        Генерирует отчет об успеваемости студентов

        Returns:
            Словарь, где под ключом 'headers' заголовки для вывода в консоль,
            а под ключом 'rows' непосредственно студенты и
            рейтинг успеваемости.
        """

        student_grades = defaultdict(list)

        for row in data:
            try:
                student_name = row["student_name"]
                grade = int(row["grade"])
                student_grades[student_name].append(grade)
            except (KeyError, ValueError):
                continue

        student_averages = []
        for student, grades in student_grades.items():
            avg_grade = sum(grades) / len(grades)
            student_averages.append(
                {"student": student, "average_grade": round(avg_grade, 2)}
            )

        student_averages.sort(key=lambda x: x["average_grade"], reverse=True)

        rows = []
        for i, student_data in enumerate(student_averages, 1):
            rows.append(
                [
                    i,
                    student_data["student"],
                    student_data["average_grade"],
                ]
            )

        return {"headers": ["", "student_name", "grade"], "rows": rows}
