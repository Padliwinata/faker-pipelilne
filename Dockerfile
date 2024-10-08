# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /opt/dagster

# Copy the current directory contents into the container at /opt/dagster
COPY . .

# Install Dagster and necessary packages
RUN pip install dagster dagster-postgres

# Create the Dagster home directory
RUN mkdir -p /opt/dagster/dagster_home

# Set environment variables
ENV DAGSTER_HOME=/opt/dagster/dagster_home

# Expose port for Dagster webserver
EXPOSE 3000

# Command to run Dagster webserver
CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
