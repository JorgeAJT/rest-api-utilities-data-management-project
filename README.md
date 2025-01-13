# REST API Final Project

This project is a **REST API** built with **FastAPI** to interact with three main tables in a **PostgreSQL** database. A **Docker** container hosts the database, and any HTTP client can be used to test the API.

## Table of Contents

1. [Overview](#overview)

2. [Technologies](#technologies)

3. [Project Structure](#project-structure)

4. [Prerequisites](#prerequisites)

5. [Installation](#installation)

6. [Running the Project](#running-the-project)

7. [API Usage (Endpoints)](#api-usage-endpoints)

    - [Meter Readings](#meter-readings)
      
    - [Meter Data](#meter-data)
      
    - [Mandate Data](#mandate-data)
      
8. [Contributions](#contributions)

9. [Author](#author)

## Overview
This project provides a **REST API** to manage data for three main database tables:

- **meter_readings**
- **meter_data**
- **mandate_data**

It includes CRUD operations (**C**reate, **R**ead, **U**pdate, **D**elete) for each table.

The API is built with **FastAPI** and organized into different routers for each table. This modular approach keeps the codebase maintainable and scalable.

## Technologies
- **Python 3.x**
- **FastAPI**: Powerful and easy-to-use framework for building APIs.
- **PostgreSQL**: Relational database.
- **psycopg2**: PostgreSQL adapter for Python.
- **Docker**: For running the PostgreSQL database in a container.
- **Uvicorn**: ASGI server to run the FastAPI application.
- **Postman** (or any HTTP client): To test the API endpoints.

## Project Structure

Below is an outline of the main directories and files:

    rest-api-final-project/
    │
    ├── main.py               # Entry point for the FastAPI application
    │
    ├── src/
    │   ├── __init__.py
    │   ├── router.py         # Main router that includes sub-routers for each table
    │   ├── utils/
    │   │   ├── logger.py
    │   │   ├── db_connection.py
    │   │   └── __init__.py
    │   ├── models/
    │   │   ├── response_model.py
    │   │   ├── brand_enum_model.py
    │   │   ├── energy_type_enum.py
    │   │   ├── meter_readings_model.py
    │   │   ├── meter_data_model.py
    │   │   ├── mandate_data_model.py
    │   │   └── __init__.py
    │   ├── meter_readings/
    │   │   ├── get.py
    │   │   ├── post.py
    │   │   ├── put.py
    │   │   ├── delete.py
    │   │   └── __init__.py
    │   ├── meter_data/
    │   │   ├── get.py
    │   │   ├── post.py
    │   │   ├── put.py
    │   │   ├── delete.py
    │   │   └── __init__.py
    │   └── mandate_data/
    │       ├── get.py
    │       ├── post.py
    │       ├── put.py
    │       ├── delete.py
    │       └── __init__.py
    │
    └── requirements.txt       # (Optional) List of required dependencies

Key files:
- **main.py**
  - Application entry point. Creates the `FastAPI` instance and includes the main `api_router`.
  - Runs the app with `uvicorn.run(app, port=8080)` if executed directly.
- **src/router.py**
  - Imports and includes the sub-routers for meter_readings, meter_data, and mandate_data.
- **src/utils/logger.py**
  - Sets up a logger with a predefined format and level.
- **src/utils/db_connection.py**
  - Defines the `db_connection()` function to establish a PostgreSQL connection using `psycopg2`.
- **src/models/**
  - Contains Pydantic models for data validation and serialization:
    - `response_model.py`: A base `Response` model to standardize responses.
    - `brand_enum_model.py`, `energy_type_enum.py`: Enums for brand and energy type fields.
    - `meter_readings_model.py`, `meter_data_model.py`, `mandate_data_model.py`: Request and response models for each table.
- **src/meter_readings, src/meter_data, src/mandate_data**
  - Each folder contains 4 files (`get.py`, `post.py`, `put.py`, `delete.py`) that implement the respective CRUD operations, plus an `__init__.py` that re-exports them as routers.

## Prerequisites
1. **Python 3.x** installed.
2. **PostgreSQL** (latest version recommended)
3. **Docker Desktop** (optional, if running PostgreSQL in a container)

      - For Docker, a sample command might be:
        ```bash
        docker run -d \
          -p 5432:5432 \
          -e POSTGRES_PASSWORD=1234 \
          -v my_db_volume:/var/lib/postgresql/data \
          --name my_postgres_container \
          postgres
      - Make sure the credentials and port match what you have in `db_connection.py`.

5. (Optional) Virtualenv or venv to isolate Python dependencies.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/rest-api-final-project.git
    cd rest-api-final-project
    
2. (Optional) **Create a virtual environment** and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate    # Linux / macOS
    venv\Scripts\activate       # Windows
3. **Install dependencies** (if you have a `requirements.txt`):
    ```bash
    pip install -r requirements.txt
    ```
    Or install manually:
    ```bash
    pip install fastapi uvicorn psycopg2
    ```

## Running the Project

1. Ensure your PostgreSQL database is **running** (locally or via Docker).
   
2. From the project’s root directory, run:
    ```bash
    python main.py
    ```
    By default, the server will start on port **8080**.
   
3. Open your browser or any HTTP client (like Postman) and go to:
    ```bash
    http://localhost:8080
    ```
    FastAPI’s interactive docs are at:
    ```bash
    http://localhost:8080/docs
    ```
    or
    ```bash
    http://localhost:8080/redoc
    ```

## API Usage (Endpoints)
All endpoints return a JSON with a `status_code` and `message` (which can contain data or error details).

### Meter Readings
1. **GET**
    - `GET /meter_readings/{connection_ean_code}`
      
      - Retrieves meter readings filtered by `connection_ean_code`.
    - `GET /meter_readings/?account_id={account_id}&connection_ean_code={connection_ean_code}`
      - Filters by `account_id`, `connection_ean_code`, or both.

2. **POST**
    - `POST /meter_readings/`

      - Creates a new record in `meter_readings`.
        
      - Expects a JSON body matching `MeterReadingsRequest`.

3. **PUT**
    - `PUT /meter_readings/{meter_readings_id}`
      
      - Updates an existing record identified by `meter_readings_id`.
        
      - Expects a JSON body matching `MeterReadingsRequest`.
        
4. **DELETE**
    - `DELETE /meter_readings/{meter_readings_id}`
      
      - Deletes the record identified by `meter_readings_id`.

### Meter Data
1. **GET**
    - `GET /meter_data/{connection_ean_code}`
      
      - Retrieves meter data by `connection_ean_code`.
    - `GET /meter_data/?business_partner_id={business_partner_id}&connection_ean_code={connection_ean_code}`
      - Filters by `business_partner_id`, `connection_ean_code`, or both.
        
2. **POST**
    - `POST /meter_data/`
      
      - Inserts a new record into `meter_data`.
        
      - Expects a JSON body matching `MeterDataRequest`.
        
3. **PUT**
    - `PUT /meter_data/{meter_data_id}`
      
      - Updates an existing record identified by `meter_data_id`.
        
      - Expects a JSON body matching `MeterDataRequest`.
4. **DELETE**
    - `DELETE /meter_data/{meter_data_id}`
      
      - Deletes the record identified by `meter_data_id`.

### Mandate Data
1. **GET**
    - `GET /mandate_data/{business_partner_id}`
      
      - Retrieves mandate data by `business_partner_id`.
    - `GET /mandate_data/?business_partner_id={business_partner_id}&mandate_status={mandate_status}&collection_frequency={collection_frequency}`
      - Filters by `business_partner_id`, `mandate_status`, and optionally by `collection_frequency`.
        
2. **POST**
    - `POST /mandate_data/`
      
      - Creates a new record in `mandate_data`.
        
      - **Important**: `mandate_id` is **not** auto-generated. You must provide it in the request body.
        
3. **PUT**
    - `PUT /mandate_data/{mandate_id}`
      
      - Updates an existing record identified by `mandate_id`.
        
      - Also requires `mandate_id` in the `MandateData` object for consistency.
        
4. **DELETE**
    - `DELETE /mandate_data/{mandate_id}`
      
      - Deletes the record identified by `mandate_id`.

## Contributions

Contributions are welcome! To contribute:

1. Fork this repository.

2. Create a new branch for your feature or fix:
    ```bash
    git checkout -b feature/new-feature

3. Make your changes and commit with descriptive messages:
    ```bash
    git commit -m "Add new feature X"

4. Push the branch to your forked repository:
    ```bash
    git push origin feature/new-feature

5. Create a Pull Request to the main branch of this repository.

6. Wait for maintainers to review and provide feedback.

## Author

:man_technologist: Jorge Jiménez - JorgeAJT :weight_lifting_man:
