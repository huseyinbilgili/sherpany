# Sherpany Challenge

Build an "events" web application where users can log in, create events and sign up for an
event and withdraw from an event.

#### Any user can list events:
* Sorted so that upcoming events are first.
* List view shows title, date and amount of participants.
* List view shows the owner of the event (as the part of the email before the "@").
* Assume there will be many thousands of events, users and participants per event.
* Any logged in user can create events.
* Logged in user can edit own events.
* Login with email and password.
* Registration with email and password.

## Installation

* Create virtual environment.
```bash
python3.9 -m venv sherpany_venv
```
* Activate virtual environment.
```bash
source sherpany_venv/bin/activate
```

* Install dependencies.
```bash
pip install -r requirements.txt
```

* Run migrations.
```bash
python manage.py migrate
```

* Run project.
```bash
python manage.py runserver
```
* Run tests. We're able to see the coverage in `htmlcov`.
```bash
pytest
```