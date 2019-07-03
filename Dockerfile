FROM python:3.7
WORKDIR /app

# Get the build arguments and store them as environment variables.
ARG test_organization_id
ENV GOOGLE_CLOUD_TEST_ORGANIZATION_ID=$test_organization_id
ARG test_project_id
ENV GOOGLE_CLOUD_TEST_PROJECT_ID=$test_project_id

# Copy the credentials file and use it to set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
COPY ./credentials/*.json ./credentials/
ENV GOOGLE_APPLICATION_CREDENTIALS=./credentials/quickstart-credentials.json

# Copy the requirements.txt file and install all dependencies.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files (see .dockerignore).
COPY . .

# Run all tests.
RUN pytest

ENTRYPOINT ["python", "quickstart.py"]
