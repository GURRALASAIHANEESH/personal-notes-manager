# Agents & Orchestration

## Agent Usage

No autonomous agent orchestration was used in this project.

AI was used interactively as a step-by-step coding assistant.
I provided context, reviewed output, and made all decisions before
accepting or modifying any generated code.

---

## Interaction Pattern

Me        ->  Describe feature + constraints
AI        ->  Generate scaffold code
Me        ->  Review every line
Me        ->  Test manually in Postman
Me        ->  Write pytest cases
Me        ->  Fix failures independently
AI        ->  Looked up specific error fixes when stuck

---

## Real Issues Solved Manually

| Problem | Root Cause | Fix Applied |
|---|---|---|
| alembic.ini parse error | PowerShell saved files as UTF-16 BOM | Rewrote all files using Python open() with UTF-8 |
| JWT Subject must be a string | user.id passed as integer | Changed to str(user_id) in jwt_helper.py |
| UNIQUE constraint failed in tests | Transaction rollback failed with SQLite | Replaced with DELETE before each test |
| ModuleNotFoundError in pytest | pytest could not find backend root | Added pythonpath = . to pytest.ini |

---

## Tools Used

| Tool | Role |
|---|---|
| Perplexity AI | Primary assistant - architecture, code, debugging |
| Groq llama-3.1-8b-instant | Runtime AI feature inside the app itself |
| Postman | Manual API testing before writing pytest cases |
