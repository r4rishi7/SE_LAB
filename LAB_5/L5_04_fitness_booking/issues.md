# Lab 5 — Static Code Analysis Issues

**File analysed:** `gym_system.py`  
**Purpose:** Record the issues identified during manual inspection and static analysis, and document the fix approach.

> Line numbers below refer to the cleaned `gym_system.py` structure currently in the project. If your handout requires line numbers from the original baseline, use the matching line numbers from the unmodified starter file and baseline reports.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Mutable default argument for attendance log | Correctness / Reliability — Medium | 11–14 | Using a list as a default argument can cause the same list to be reused across calls, allowing attendance entries to leak between separate bookings. | Use `None` as the default and create a new list inside the function when no log is supplied. |
| Booking into an unknown class has no defined capacity | Correctness — Medium | 19–22 | A booking for a class absent from the capacity dictionary needs a deliberate policy; silently treating it as capacity zero makes the behaviour unclear to callers. | Check class capacity explicitly and return a clear failure result or define the class capacity before accepting bookings. |
| Negative class capacity can be configured | Input validation — Medium | 31–34 | A negative seat count is invalid configuration and can make booking behaviour confusing. | Reject negative capacities with `ValueError` before updating the capacity dictionary. |
| Cancellation may reference a missing class or member | Reliability — Medium | 25–29 | Removing a member from a nonexistent roster or a roster that does not contain the member can raise `KeyError` or `ValueError`. | Catch only the expected exceptions and print a clear message when there is nothing to cancel. |
| Export file is opened without an explicit encoding | Portability / Reliability — Low | 42–45 | Relying on the platform's default text encoding can cause inconsistent behaviour across environments. | Open the JSON file with `encoding="utf-8"`. |
| Old-export cleanup deletes matching files in the working directory | File handling / Safety — Medium | 48–53 | The cleanup routine deletes every file matching the supplied prefix and a `.json` suffix in the current directory. An overly broad prefix can remove files the user did not intend to delete. | Restrict cleanup to the intended export naming pattern and directory; verify the matched files before deleting them if the pattern can be configured. |
| Walk-in count is converted directly from input | Input validation — Medium | 64–65 | Non-integer input raises `ValueError`; negative counts also do not represent a valid number of guests. | Parse the input with validation and reject negative values with a helpful message. |
| Module uses shared global booking state | Maintainability — Low | 5–7 | Global dictionaries make functions depend on mutable module-level state, which can complicate testing and reuse. | For a larger version, encapsulate capacity and rosters in a class or pass the state explicitly. |

## Verification

Run the three tools from the project directory:

```bash
pylint gym_system.py
bandit -r gym_system.py
flake8 gym_system.py
```

Compare the results with the saved files in `BEFORE/` and `AFTER/`. Do not claim an issue is resolved solely because a report is empty; also run the program and check its booking, cancellation, capacity, and export behaviour.
