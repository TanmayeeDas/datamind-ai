# DataMind AI

**DataMind AI** is an AI-powered data analysis application that lets
users ask questions about structured data using natural language. It
supports PostgreSQL database connections and CSV/Excel uploads, with
query results, summary cards, and interactive visualizations.

> **Project status:** Active development. Some capabilities are
> implemented, while advanced analysis features such as general-purpose
> AI analysis for uploaded files, automatic insight generation,
> forecasting, and conversational follow-ups are planned.

## Features

### PostgreSQL analysis

-   Connect to a PostgreSQL database using connection details.
-   Read database schema information, including tables and columns.
-   Generate PostgreSQL `SELECT` queries from natural-language questions
    using OpenAI GPT-4.1-mini.
-   Validate generated SQL before execution.
-   Display generated SQL and query results in a table.

### CSV and Excel analysis

-   Upload CSV and `.xlsx` files.
-   Display file metadata, including row count and columns.
-   Perform basic question answering on uploaded data:
    -   Count rows.
    -   List columns.
    -   Show the first five rows.
    -   Calculate averages and totals for supported numeric-column
        questions.

The uploaded-file analyzer is currently a basic, incrementally expanding
implementation. It does not yet support arbitrary natural-language
analysis.

### Charts and dashboard

-   Generate bar, line, and pie charts.
-   Select category/X and value/Y columns.
-   Visualize uploaded data or database query results.
-   Display summary cards for revenue, orders, customers, and profit
    when matching fields are present in the available results.

Dashboard summaries are currently heuristic and may be based on returned
query rows rather than the full underlying dataset.

## Technology Stack

  **Layer**             **Technologies**
  --------------------- --------------------------
  Backend API           Python, FastAPI
  Database              PostgreSQL
  AI / SQL generation   OpenAI API, GPT-4.1-mini
  Data processing       Pandas
  SQL validation        SQLGlot
  Visualizations        Plotly
  Frontend              HTML, CSS, JavaScript
  Configuration         `python-dotenv`

## Project Structure

    datamind-ai/
    ├── backend/
    │   ├── app/
    │   │   ├── api/                 # FastAPI route handlers
    │   │   ├── core/                # Configuration and logging
    │   │   ├── database/            # Database connection, schema and query utilities
    │   │   ├── schemas/              # Request/response schemas
    │   │   ├── services/             # LLM, file, chart and analysis services
    │   │   ├── utils/                # SQL validation utilities
    │   │   └── main.py               # FastAPI application
    │   ├── uploads/                  # Local uploaded files (ignored by Git)
    │   ├── .env.example              # Environment variable template
    │   └── requirements.txt
    ├── frontend/
    │   ├── css/
    │   │   └── style.css
    │   ├── js/
    │   │   └── app.js
    │   └── index.html
    ├── .gitignore
    └── README.md

## Requirements

-   Python 3.10 or a compatible Python version supported by the
    dependencies.
-   PostgreSQL database (for database analysis).
-   OpenAI API key (for natural-language SQL generation).
-   A modern web browser.

## Setup and Installation

### 1. Clone the repository

    git clone https://github.com/TanmayeeDas/datamind-ai.git
    cd datamind-ai

### 2. Create and activate a virtual environment

From the project root:

    python3 -m venv venv
    source venv/bin/activate

On Windows PowerShell:

    python -m venv venv
    .\venv\Scripts\Activate.ps1

### 3. Install backend dependencies

    pip install -r backend/requirements.txt

### 4. Configure environment variables

Create a local environment file by copying the example:

    cp backend/.env.example backend/.env

Open `backend/.env` and configure the values required by your local
setup. The application configuration currently reads:

    APP_NAME=DataMind AI
    DEBUG=False
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=your_database_url

-   `OPENAI_API_KEY` is used by the OpenAI client for SQL generation.
-   `DATABASE_URL` is loaded by the configuration module; database
    connection routes may also accept connection details from the
    frontend.
-   `APP_NAME` controls the application name returned by the health
    endpoint.
-   `DEBUG` controls the configured debug flag.

Never commit your actual `.env` file, API keys, database passwords, or
private datasets.

### 5. Start the backend

From the project root, with the virtual environment activated:

    cd backend
    uvicorn app.main:app --reload

The API will normally be available at:

-   API base: `http://127.0.0.1:8000`
-   Interactive API documentation: `http://127.0.0.1:8000/docs`
-   Health endpoint: `http://127.0.0.1:8000/`

Keep the backend terminal running.

### 6. Start the frontend

Open a second terminal from the project root:

    python3 -m http.server 5500 --directory frontend

Then open:

    http://localhost:5500

The frontend uses the Plotly CDN, so chart rendering requires internet
access unless Plotly is served locally.

## Using DataMind AI

### Option A: Analyze a PostgreSQL database

1.  Start the backend and frontend.
2.  Select **PostgreSQL** in the application.
3.  Enter the database host, port, database name, username, and
    password.
4.  Connect to retrieve the database schema.
5.  Ask a question in natural language.
6.  Review the generated SQL and returned data.
7.  Select chart settings and generate a visualization when applicable.

Use a database account with only the permissions needed for analysis,
preferably read-only access.

### Option B: Analyze a CSV or Excel file

1.  Select **CSV / Excel**.
2.  Upload a `.csv` or `.xlsx` file.
3.  Ask a supported question about the uploaded data.
4.  Review the response or table.
5.  Choose chart type and columns to generate a visualization.

The current file-analysis capabilities are limited to basic operations.
Broader question understanding and automated analysis are under
development.

## API Overview

The backend exposes routes for health checks, database connectivity and
schema retrieval, natural-language SQL queries, file uploads and
questions, charts, and dashboard functionality.

For the exact routes, request formats, and response schemas, run the
backend and visit:

    http://127.0.0.1:8000/docs

## Security Notes

-   Keep API keys and database credentials out of source control.
-   Do not commit `.env` files or sensitive uploaded datasets.
-   Use read-only database credentials for analytical workloads.
-   SQL validation is a safeguard, not a guarantee of security. Review
    database permissions, SQL validation, query timeouts, and resource
    limits before exposing the application to untrusted users.
-   The current application is a development project and has not been
    documented or verified as production-hardened.
-   Avoid using sensitive or confidential data unless the deployment and
    data-handling requirements have been reviewed.

## Roadmap

Planned improvements include:

-   LLM-based question interpretation for CSV and Excel analysis, with
    Pandas performing calculations on the data.
-   Grouping, filtering, ranking, and period-over-period comparisons.
-   Automatic chart recommendations.
-   AI-generated summaries and evidence-backed insights.
-   Data profiling, data cleaning, and anomaly detection.
-   Multi-step analysis and contextual follow-up questions.
-   Forecasting, what-if analysis, and downloadable reports.

## Contributing

This is an actively developed project. For changes:

1.  Create a feature branch.
2.  Make and test your changes locally.
3.  Keep credentials and private data out of commits.
4.  Submit a pull request describing the change and how it was tested.

## License

No license has been specified yet. Unless a license is added to this
repository, all rights are reserved by the copyright holder and reuse or
redistribution is not automatically permitted.
