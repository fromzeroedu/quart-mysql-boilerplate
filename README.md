# Quart MySQL Boilerplate

This is a boilerplate for a Quart app that can run as a pipenv, Heroku or Docker application. Requires `python 3.7`.

## Local MySQL server
- Create the application user and password:
  - Logon to MySQL using root user
  - Create the counter database `CREATE DATABASE counter;`
  - Create the counter user `CREATE USER 'counter_user'@'%' IDENTIFIED BY 'counter_password';`
  - Give privileges to counter user `GRANT ALL PRIVILEGES ON counter.* TO 'counter_user'@'%';` and `FLUSH PRIVILEGES;`
- Install pipenv if you don't have it using `pip install pipenv`
- Install the packages: `pipenv install`
- Run the first migration with `pipenv run alembic upgrade head`
  - Subsequent migrations after models changes can be run with `pipenv run alembic revision --autogenerate -m "added counter table field"` with [some caveats](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect).
- Run `pipenv run quart run`
- Open `http://localhost:5000` on your browser
- To open a shell, just do `pipenv run quart shell`
- Run tests by doing `pipenv run pytest`

## Using Docker
- Make sure your folder is being shared within Docker client (Preferences > Resources > File Sharing)
- If you have run `pipenv` locally previously, make sure you delete the local `.venv` folder
- Run `docker-compose up --build`. If there's a timeout error, you can restart the Quart container.
- To do the first migration:
  - `docker-compose run --rm web pipenv run alembic upgrade head`
- Restart using docker-compose and head over to `http://localhost:5000` on your browser
- Run tests by doing `docker-compose run --rm web pipenv run pytest -s`

## Production
- Use Hypercorn `hypercorn --bind 0.0.0.0:$PORT --reload wsgi:app`
