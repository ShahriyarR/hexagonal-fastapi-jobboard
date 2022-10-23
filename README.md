# FastAPI JobBoard with Hexagonal Architecture - WIP - Work In Progress

JobBoard project with FastAPI using Hexagonal Architecture.

Rewritten version of: [JobBoard](https://github.com/nofoobar/JobBoard-Fastapi)

## About Hexagonal Architecture

You can read it from original author:

[The Pattern: Ports and Adapters](https://alistair.cockburn.us/hexagonal-architecture/)

Why Hexagonal?

* Easy to implement.
* Highly testable and maintainable code.
* Dependency Inversion, Dependency Injection and SRP in the club.
* Centered domain knowledge.
* The original author is quite friendly :)

## Project folder structure

```sh
src/jobboard/
├── adapters
│   ├── db
│   │   ├── alembic.ini
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── env.py
│   │   │   ├── README
│   │   │   ├── script.py.mako
│   │   │   └── versions
│   │   │       └── 7794fd8602f8_.py
│   │   ├── orm.py
│   │   ├── repository.py
│   │   ├── unit_of_work.py
│   │   └── utils.py
│   └── entrypoints
│       ├── api
│       │   ├── base.py
│       │   ├── __init__.py
│       │   ├── utils.py
│       │   └── v1
│       │       ├── route_jobs.py
│       │       ├── route_login.py
│       │       └── route_users.py
│       ├── application.py
│       ├── __init__.py
│       ├── static
│       │   ├── images
│       │   │   ├── lite.gif
│       │   │   └── logo.png
│       │   └── js
│       │       └── autocomplete.js
│       ├── templates
│       │   ├── auth
│       │   │   └── login.html
│       │   ├── components
│       │   │   ├── alerts.html
│       │   │   ├── cards.html
│       │   │   └── navbar.html
│       │   ├── general_pages
│       │   │   └── homepage.html
│       │   ├── jobs
│       │   │   ├── create_job.html
│       │   │   ├── detail.html
│       │   │   └── show_jobs_to_delete.html
│       │   ├── shared
│       │   │   └── base.html
│       │   └── users
│       │       └── register.html
│       └── webapps
│           ├── auth
│           │   ├── forms.py
│           │   └── route_login.py
│           ├── base.py
│           ├── __init__.py
│           ├── jobs
│           │   ├── forms.py
│           │   └── route_jobs.py
│           └── users
│               ├── forms.py
│               └── route_users.py
├── domain
│   ├── model
│   │   ├── events.py
│   │   ├── __init__.py
│   │   └── model.py
│   ├── ports
│   │   ├── __init__.py
│   │   ├── job_service.py
│   │   ├── messagebus.py
│   │   ├── repository.py
│   │   ├── unit_of_work.py
│   │   └── user_service.py
│   └── schemas
│       ├── jobs.py
│       ├── tokens.py
│       └── users.py
├── __init__.py
└── configurator
    ├── config.py
    ├── containers.py
    ├── hashing.py
    └── security.py

26 directories, 56 files
```



## How to install?

We use flit for the installation:

Install flit:

* `pip install flit==3.7.1`

### Installing project for development

`make install-dev` or `flit install --env --deps=develop --symlink` 

### Installing for general showcase

`make install` or `flit install --env --deps=develop` 

## How to run?

`make run` 

or 

`uvicorn src.jobboard.adapters.entrypoints.application:app --reload`

### Run all tests in verbose

`make test` or `pytest -svv` 


### Run all tests with html coverage

`make test-cov` or `pytest --cov-report html --cov=src tests`

## Database migrations

Generated as:

`make migrations`

or

`alembic -c src/jobboard/adapters/db/alembic.ini revision --autogenerate`

Migrate:

`make migrate`

or

`alembic -c src/jobboard/adapters/db/alembic.ini upgrade head`