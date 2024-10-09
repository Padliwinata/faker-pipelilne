FROM python:3.11-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
COPY . /opt/dagster/app
WORKDIR /opt/dagster/app
RUN touch /opt/dagster/dagster_home/dagster.yaml

RUN pip install dagster-webserver dagster-postgres dagster-aws
RUN pip install ".[dev]"

# Copy your code and workspace to /opt/dagster/app
# COPY workspace.yaml /opt/dagster/app/


ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
# COPY dagster.yaml /opt/dagster/dagster_home/


EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
