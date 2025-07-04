# URL Change Monitor with Telegram Notifications

[![Quality Checks](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/main.yml/badge.svg?branch=master&event=push&job=quality_checks)](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/main.yml)
[![Docker Image CI](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/main.yml/badge.svg?branch=master&event=push&job=build)](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/main.yml)

This project contains a Python script that monitors a specified URL for any content changes and sends a notification to a Telegram chat when a change is detected.

The project is containerized using Docker and includes a GitHub Actions workflow for continuous integration and deployment.

## Features

- Monitors a single URL for content changes.
- Uses SHA-256 hashing to detect changes efficiently.
- Sends notifications to a specified Telegram chat.
- Configuration via environment variables.
- Linting with `ruff` and type checking with `mypy`.
- Standardized development tasks using `uv` scripts.
- Dockerized for easy deployment.
- CI/CD pipeline using GitHub Actions to build and publish the Docker image.

## Getting Started

### Prerequisites

- Python 3.8+
- `uv` (can be installed via `pip install uv`)
- Docker (for running the containerized application)

### Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a `.env` file:**

    Copy the example file and fill in your specific details.

    ```bash
    cp .env.example .env
    ```

    You will need to edit the `.env` file with your:
    - `URL_TO_MONITOR`
    - `TELEGRAM_BOT_TOKEN`
    - `TELEGRAM_CHAT_ID`

3.  **Set up the environment and install dependencies:**

    This command uses the `setup` target in the `Makefile` to create a virtual environment and install all required dependencies.

    ```bash
    make setup
    ```

### Running the Application

To start the monitoring script, use the following `make` command:

```bash
make run
```

The script will load the environment variables from the `.env` file and begin monitoring the URL.

### Development Tasks

This project uses `ruff` for linting and `mypy` for static type checking. You can run these checks using the provided `make` commands:

- **Run all checks:**
  ```bash
  make check
  ```

- **Run only the linter:**
  ```bash
  make lint
  ```

- **Run only the type checker:**
  ```bash
  make type-check
  ```

## Docker

The application is fully containerized. You can build and run it using Docker.

1.  **Build the Docker image:**

    ```bash
    docker build -t url-monitor .
    ```

2.  **Run the Docker container:**

    Pass your environment variables directly to the `docker run` command.

    ```bash
    docker run -d --restart=always --name url-monitor-app \
      -e URL_TO_MONITOR="https://example.com" \
      -e TELEGRAM_BOT_TOKEN="your_token_here" \
      -e TELEGRAM_CHAT_ID="your_chat_id_here" \
      url-monitor
    ```

## CI/CD

This project uses GitHub Actions to automate the building and publishing of the Docker image.

The workflow is defined in `.github/workflows/main.yml` and has two main jobs:

1.  **`lint`**: This job installs dependencies and runs `ruff` and `mypy` to ensure code quality.
2.  **`build`**: This job depends on the success of the `lint` job. It builds the Docker image and pushes it to the GitHub Container Registry (`ghcr.io`).

The workflow is triggered on every push to the `main` branch.
