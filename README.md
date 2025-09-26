## Обработчик успеваемости студентов
Скрипт для анализа успеваемости студентов на основе CSV-файлов. Обрабатывает данные об оценках студентов и формирует отчеты.

### Установка
Проект использует Poetry для управления зависимостями:

#### Клонирование репозитория
```bash
  git clone https://github.com/Maksim-Gubenin/Script-for-CSV.git
  cd Script-for-CSV
````
#### Установка зависимостей
```bash
  poetry install
```

### Базовый запуск
```bash
    poetry run python main.py --files data1.csv data2.csv --report student-performance
```
#### Параметры командной строки

**--files**: Пути к CSV-файлам с данными (один или несколько)

**--report**: Название отчета (в базовой конфигурации поддерживается student-performance)

### Добавление новых отчетов

Чтобы добавить новый отчет:

1. Создайте класс отчета в модуле reports/

2. Унаследуйте от базового класса Report  (report/report_factory.py)

3. Реализуйте методы:
- generate() - основная логика формирования отчета
- display() - вывод результатов
4. Зарегистрируйте отчет в ReportFactory
- ReportFactory.register_report("new-report", NewReportClass) 