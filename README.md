# repairshop

## Запуск проекта

1. `git clone <URL>`
2. `py -m venv .venv && .venv\Scripts\Activate.ps1`
3. `py -m pip install -r requirements.txt`
4. `py manage.py migrate`
5. `py manage.py createsuperuser`   ← каждый создаёт своего админа
6. `py manage.py runserver`

Открой http://127.0.0.1:8000/admin

⚠️ `db.sqlite3` не в Git. У каждого своя локальная база.