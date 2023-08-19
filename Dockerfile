# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster as builder

# Set the working directory to /app
WORKDIR /tmp

RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.8-slim-buster

RUN apt update && apt install tzdata -y
ENV TZ="Asia/Seoul"

COPY --from=builder /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose port 3000 for the application
EXPOSE 3000

# Start the application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", \
    "main:app", "--bind", "0.0.0.0:3000"]
