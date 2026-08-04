# Speak Ukrainian UI Test Automation

This repository contains a Python-based UI test automation project for the Speak Ukrainian web application. The project uses Selenium with a page-object style structure to keep test code maintainable and organized.

## Project overview

The test suite is organized around:

- `tests/` for test cases
- `pages/` for page objects and reusable UI components
- `fixtures/` for shared test fixtures
- `api/` for API-related helpers (currently placeholder structure)
- `data/` for configuration files and environment setup

## Prerequisites

- Python 3.12+
- pip
- A supported browser installed locally (Chrome/Edge are commonly used)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd speak-ukrainian-5341
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. create a `.env` (example in `.env.example`) file in the root directory and add the following environment variables :

   ```text
   BASE_UI_URL=https://speak-ukrainian.org.ua/
   BASE_API_URL=https://api.speak-ukrainian.org.ua/
   IMPLICITY_WAIT=10
   EXPLICIT_WAIT=10
   HEADLESS=TRUE
   USER_NAME=user
   USER_PASSWORD=password
   USER_EMAIL=user@email.com
   ```
## Running tests

Run the test suite with:

```bash
python -m pytest
```

The project is configured to generate Allure results by default via `pytest.ini`.

## Code quality checks

Run linting with:

```bash
python -m ruff check .
```

## Repository structure

```text
.
├── api/
├── data/
├── fixtures/
├── pages/
│   ├── components/
│   └── modals/
├── tests/
├── pytest.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Notes

The current repository includes a minimal example test and a basic page-object foundation. As the project grows, new page objects, components, and tests should be added under the existing structure to keep the suite consistent.
