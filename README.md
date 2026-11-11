# Code Coach

A standalone desktop app for learning Python, C++, and C#. It includes short
lessons, coding challenges, a practice editor, saved drafts, XP, and study
streaks.

## Set up

From this project folder, create and activate a virtual environment, then
install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

## Run

```bash
python -m code_coach
```

Progress is stored locally in `~/.code_coach/progress.json`. The practice
editor saves your work but does not execute it, so use a Python interpreter or
a C++/C# compiler to run and check your solutions.

## Test

```bash
python -m pytest tests
```
