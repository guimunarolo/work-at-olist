# Olist Challenge

This is an API restful that provides a call events record and a bill report.

The applications was made with `Python 3.6`, `Django 2.0` and hosted at `Heroku`.

> You can see the entire challenge here [Work at Olist](https://github.com/olist/work-at-olist).


## Environment

- Macbook Pro `2017`
- macOS Sierra `10.12.6`
- Atom `1.27.0`
- virtualenv `15.1.0`
- Python `3.6.3`
- Docker `18.03.1-ce` `build 9ee9f40`
- docker-compose `1.21.1` `build 5a3f1a3`


## How to run

With `Docker` and `docker-compose` properly installed and running, execute:

```
make
```

If this was the **first time** you ran the project, you need execute:

```
make migrate
make loaddatta
```

Now you have the project running on [http://localhost:8000](http://localhost:8000) and the database fully started.

If you wanna see the application's logs, run:

```
make logs
```

## Running tests

With the project running, execute:

```
make tests
```
