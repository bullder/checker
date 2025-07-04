# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project definition file
COPY pyproject.toml .

# Install dependencies from pyproject.toml
RUN pip install uv && uv pip install --system .

# Copy the rest of the application's code into the container at /app
COPY . .

# Set environment variables
# The user will need to pass these in when running the container
ENV URL_TO_MONITOR=""
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# Run url_monitor.py when the container launches
CMD ["python", "url_monitor.py"]
