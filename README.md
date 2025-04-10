# ResumeMatchPro Core

A shared library that provides core functionality for the ResumeMatchPro application, used by various Azure Functions.

## Overview

This library contains shared code and repositories for interacting with Azure Cosmos DB and other services in the ResumeMatchPro ecosystem. It provides a standardized way to handle data access and business logic across different Azure Functions.

## Features

- Azure Cosmos DB integration
- Job Description (JD) repository management
- Shared models and exceptions
- Type-safe data handling with Pydantic

## Project Structure

```
resumematchpro_core/
├── repositories/         # Data access layer
│   ├── models.py        # Data models
│   └── jds_repository.py # Job Description repository
├── shared/              # Shared utilities
│   └── exceptions.py    # Custom exceptions
├── tests/              # Test suite
└── scripts/            # Utility scripts
```

## Requirements

- Python 3.11 or higher
- Azure Cosmos DB
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Development

### Setup

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Testing

Run tests with coverage:
```bash
pytest --cov=repositories --cov=shared
```

### Code Quality

The project uses:
- mypy for static type checking
- ruff for linting
- pytest for testing
- pre-commit hooks for automated code quality checks

## License

This project is licensed under the CC-BY-NC-4.0 License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Create a feature branch from `develop`
2. Make your changes
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request to `develop`

## Versioning

This project uses semantic versioning. See `_version.py` for the current version.
