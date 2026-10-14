# Lab 5: Static Code Analysis — Fitness Club Class Booking Ledger

## Overview
This lab uses `gym_system.py`, a small fitness-class booking ledger for classes such as Yoga, HIIT, and Spin. It books members up to class capacity, cancels bookings, displays rosters, and exports the roster data to `gym_schedule.json`.

The goal is to inspect the program, use static-analysis tools to identify code-quality and security concerns, document the issues, apply fixes, and compare the reports before and after the changes.

## Tools
- **Pylint** — code quality, naming, conventions, and potential defects
- **Flake8** — style and lint checks
- **Bandit** — checks for common Python security issues

Install the tools in your Python environment:

```bash
python -m pip install pylint flake8 bandit
```

## Run the program
From this directory, run:

```bash
python gym_system.py
```

The program asks for the number of walk-in guests for HIIT. Press Enter to use the default value (`1`), or enter a non-negative integer.

## Run static analysis
Create the baseline reports before making changes, then run the same commands again after the fixes. The repository stores reports in `BEFORE/` and `AFTER/` so that the results can be compared.

```bash
pylint gym_system.py > BEFORE/pylint_report_before.txt
bandit -r gym_system.py > BEFORE/bandit_report_before.txt
flake8 gym_system.py > BEFORE/flake8_report_before.txt
```

After fixing the code:

```bash
pylint gym_system.py > AFTER/pylint_report_after.txt
bandit -r gym_system.py > AFTER/bandit_report_after.txt
flake8 gym_system.py > AFTER/flake8_report_after.txt
```

Run these commands from the project directory. The `BEFORE/` and `AFTER/` folders must exist first.

## Issues and fixes
See [`issues.md`](issues.md) for the issue table, severity, affected lines, descriptions, and proposed fixes.

The final implementation includes improvements such as:
- avoiding a mutable default argument for the attendance log;
- handling missing bookings without crashing;
- rejecting negative class capacities;
- writing JSON with an explicit UTF-8 encoding;
- using a controlled file pattern when removing old JSON exports; and
- adding docstrings and clearer function/variable names.

## Results
The baseline reports are in `BEFORE/`; the final reports are in `AFTER/`. Compare the reports to confirm which findings were resolved. The final version previously achieved a Pylint score of **10.00/10**, Bandit reported **no issues**, and Flake8 produced no output. Re-run the tools in your environment to verify these results for the current files and tool versions.

## Deliverables
- `gym_system.py` — cleaned program
- `issues.md` — documented issue table
- `reflection.md` — answers to the four reflection questions in the lab handout
- `BEFORE/` and `AFTER/` — static-analysis reports

## Notes
- `gym_schedule.json` is generated when the program runs and is excluded from version control.
- The Python virtual environment is excluded from version control.
- The program should retain its booking, cancellation, roster display, and JSON-export functionality after the fixes.
