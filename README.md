# MDS — задания и решения

Учебные материалы [Netology-DS/MDS](https://github.com/Netology-DS/MDS), исходная версия `3059236b56be24ea9eb87253dd9aab304965c33c`.
Копия владельца: [JakimPit/MDS](https://github.com/JakimPit/MDS).

В `MDS-new` находятся решения HW_1–HW_9 и итоговой HW_X: вычисления, пояснения, графики и проверки математических результатов. Решения подготовлены AI по запросу владельца. Это не evidence самостоятельного освоения курса.

## Запуск в VS Code на Windows

Открой папку репозитория. Для ноутбуков нужны расширения Microsoft Python и Jupyter. Выбери ядро `.venv/Scripts/python.exe`, затем **Run All**.

Создание окружения на другом компьютере (Python 3.12):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Повторная проверка всех решений:

```powershell
.\.venv\Scripts\python.exe verify_notebooks.py
```

Результаты запуска сохраняются в ноутбуках и `verification.json`. Список точных версий зависимостей — `requirements-lock.txt`. `solve_notebooks.py` воспроизводит заполнение шаблонов и сбрасывает outputs изменяемых ячеек; после него повтори проверку.

В оптимизации явно указаны область поиска и критерий качества. В HW_7 сравнение на одном seed — отдельный эксперимент, а не универсальный рейтинг методов. В HW_9 результаты иллюстрируют ЦПТ на распределении с конечной дисперсией.

Документация методов: [curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html), [differential_evolution](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html).
