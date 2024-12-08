# Celery Task Orchestration and Data Collection Framework

## Overview
This repository provides a structured framework to build Python-based services for:
- Task orchestration using Celery and RabbitMQ.
- Data collection from REST APIs and browser-based scraping tools like Selenium or Playwright.
- Seamless integration with MongoDB and OpenSearch for data storage.

The framework emphasizes modularity, fault tolerance, and adherence to code quality standards. It includes abstract classes for common operations and best practices for reliable and maintainable services.

---

## Key Features

### 1. Modular Components
- Abstract base classes for common operations:
  - Database connectors (MongoDB, OpenSearch).
  - Queue publishers and subscribers (RabbitMQ).
  - Data collectors (REST APIs, browser-based scraping).

### 2. Error Handling
- Graceful handling of success and failure states with detailed logging.
- Default or fallback values for missing or invalid data.

### 3. Validation
- **Pydantic schemas** for data validation and type enforcement.

### 4. Automation and Code Quality
- **Git hooks** for pre-commit linting.
- Dependency management using **Poetry**.

### 5. Testing and Documentation
- Unit tests for all modules.
- Clear documentation for every function and class.

---

## Code Structure
```plaintext
.
├── src
│   ├── base
│   │   ├── abstract_api_collector.py
│   │   ├── abstract_scraper.py
│   │   ├── rabbitmq_connector.py
│   │   ├── celery_task_handler.py
│   │   ├── db_connector.py
│   │   └── __init__.py
│   ├── services
│   │   ├── api_collector_service.py
│   │   ├── scraper_service.py
│   │   ├── task_orchestrator.py
│   │   └── __init__.py
│   ├── models
│   │   ├── data_schema.py
│   │   └── __init__.py
│   ├── utils
│   │   ├── logging.py
│   │   └── __init__.py
│   ├── tests
│   │   ├── test_api_collector.py
│   │   ├── test_scraper.py
│   │   ├── test_task_orchestrator.py
│   │   └── __init__.py
│   └── main.py
├── README.md
├── pyproject.toml
├── .pre-commit-config.yaml
└── requirements.txt
```

---

## Getting Started

### Prerequisites
1. Python 3.9+
2. Poetry (for dependency management)
3. RabbitMQ (as a message broker)
4. MongoDB and OpenSearch (for data storage)

### Installation

1. Clone the repository:
```bash
$ git clone <repository_url>
$ cd <repository_name>
```

2. Install dependencies:
```bash
$ poetry install
```

3. Set up pre-commit hooks:
```bash
$ pre-commit install
```

4. Configure environment variables:
```bash
$ cp .env.example .env
```
Modify `.env` with your RabbitMQ, MongoDB, and OpenSearch credentials.

---

## Usage

### Running the Services

1. Start RabbitMQ, MongoDB, and OpenSearch.

2. Launch Celery workers:
```bash
$ celery -A src.main worker --loglevel=info
```

3. Run the main application:
```bash
$ poetry run python src/main.py
```

---

## Testing
Run unit tests using:
```bash
$ pytest
```

---

## Reusability Components (Examples)

### Logging and Performance Time
If another class needs logging or tracing, it can now simply call these utilities:

```python
from src.utils.logging import configure_logger, log_and_trace

class AnotherAPICollector:
    def __init__(self):
        self.logger = configure_logger("AnotherAPICollector")

    def some_method(self):
        start_time = time.time()
        # Simulate some processing
        time.sleep(1)
        log_and_trace(self.logger, "some_method", start_time)

```

---

## Contribution Guidelines
- Follow PEP8 standards.
- Write clear docstrings for every class and function.
- Ensure all new code includes test cases.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Next Steps
- [ ] Implement advanced retry mechanisms for Celery tasks.
- [ ] Add more detailed logging and monitoring.
- [ ] Extend support for additional message brokers and databases.

---
