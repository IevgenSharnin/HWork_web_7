# стартуємо pipenv, доставляємо бібліотеки
pipenv shell
pipenv install faker
pipenv install sqlalchemy
pipenv install alembic
pipenv install psycopg2

# ініцціалізацція alembic
alembic init migrations

# внесення змін до alembic.ini та env.py: щодо підключення до конкретної бази

# підіймаємо posgres-базу через docker
docker compose -f docker-compose.yaml up

# власне пайтон-модуль з ініціалізацією таблицць через SQLAlchemy
# НЕ ЗАПУСКАТИ ОКРЕМО
create_tables.py

# створення міграції БД
alembic revision --autogenerate -m 'Init'

# старт міграції БД
alembic upgrade head

# запуск seed.py для заповнення бази випадковими даними
python seed.py

# запуск my_select.py для виконання запитів
python my_select.py