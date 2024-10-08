# Use an official Python image
FROM python:3.9-slim

# Set environment variables
ENV DAGSTER_HOME=/opt/dagster/dagster_home

# Create dagster home directory
RUN mkdir -p $DAGSTER_HOME

# Set the working directory inside the container
WORKDIR /opt/dagster

# Copy the current directory (your project) into the container
COPY . .

# Install any necessary dependencies
RUN pip install dagster dagit dagster-postgres

# Expose the port for dagster webserver
EXPOSE 3000

# Run Dagster webserver
CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
