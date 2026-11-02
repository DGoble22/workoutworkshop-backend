# Workout Workshop API

Flask API for [Workout Workshop](https://github.com/DGoble22/workoutworkshop-frontend), a group-built fitness platform. It covers accounts, workouts, coaches, and chat.

## What it does

- Registers users and coaches, checks usernames, and issues JWTs.
- Stores an exercise library and a weekly workout plan. Users can log sets, mark exercises complete, and read weekly stats.
- Lets a user apply to a coach, and lets that coach accept or decline. Coaches keep a client list, a profile, availability, and meal plans.
- Collects coach reviews and reports. Admins approve certifications, dismiss or act on reports, and edit the exercise list.
- Tracks goals, payment details, weight, calories, daily check-ins, and progress photos.
- Sends chat over Socket.IO, with history available over HTTP.
- Publishes API docs through Flasgger.

## Stack

Python, Flask, Flask-SQLAlchemy, PyMySQL, Flask-SocketIO, PyJWT, and Flasgger. GitHub Actions runs the test suite on pushes to `main`, then calls a deploy webhook.

## Run it locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Export the database and auth settings before starting the server:

```bash
DB_HOST=
DB_PORT=3306
DB_USER=
DB_PASSWORD=
DB_NAME=
JWT_SECRET=
```

Table definitions and seed data are in `SQL/`.

```bash
python app.py
```

## API groups

| Prefix | Purpose |
| --- | --- |
| `/auth` | Register, login, change password |
| `/user` | Profile, goals, progress, surveys, chat history |
| `/coach` | Coach profiles, requests, clients, meal plans, reviews |
| `/api/workouts` | Exercise library, plans, logs, weekly stats |
| `/admin` | Applications, reports, exercises, users |

## Tests

The CI job runs:

```bash
coverage run -m unittest discover -p "*_tests.py" tests
```

See `tests/HOWTORUN.md` for local test notes.
