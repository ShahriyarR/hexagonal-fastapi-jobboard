# FastAPI JobBoard with Hexagonal Architecture - WIP - Work In Progress

JobBoard project with FastAPI using Hexagonal Architecture.

Rewritten version of: [JobBoard](https://github.com/nofoobar/JobBoard-Fastapi)

## How to run

`make run` 

or 

`uvicorn src.jobboard.adapters.entrypoints.application:app --reload`

## Database migrations

Generated as:

`make migrations`

or

`alembic -c src/jobboard/adapters/db/alembic.ini revision --autogenerate`

Migrate:

`make migrate`

or

`alembic -c src/jobboard/adapters/db/alembic.ini upgrade head`