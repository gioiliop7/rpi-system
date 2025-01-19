# Use the official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and application code to the container
COPY requirements.txt ./
COPY rpi.py ./
COPY shutdown.sh ./
RUN chmod +x shutdown.sh

RUN apt-get update && apt-get install -y gcc python3-dev
RUN apt-get update && apt-get install -y sudo
RUN apt-get update && apt-get install -y procps


# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "rpi.py"]
