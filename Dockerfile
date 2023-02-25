# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Install pipenv
RUN pip install pipenv

# Set the working directory to /app
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install dependencies using pipenv
RUN pipenv install --system --deploy

# Copy the current directory contents into the container at /app
COPY . /app

# Configure logging
RUN mkdir logs
RUN touch logs/user_logs.log
RUN chmod 777 logs/user_logs.log

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the Python script
CMD ["pipenv", "run", "python", "juno_solar_bot.py"]
