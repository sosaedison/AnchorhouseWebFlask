# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim as dependencies

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH /app
ENV FLASK_APP /app/anchorwebflask/app.py

# Create and set working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# Create edisonarchives user to run application
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" edisonarchives \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" edisonarchives

# Create container healthcheck
HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD curl --fail http://localhost:8080/status || exit 1


RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

FROM dependencies as debug
ENV FLASK_ENV development
ENV FLASK_DEBUG 1

USER edisonarchives
ENTRYPOINT ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "8080"]

FROM dependencies as production
ENV FLASK_ENV production


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "anchorwebflask.app:app"]
USER edisonarchives
ENTRYPOINT ["./start_app.sh"]
