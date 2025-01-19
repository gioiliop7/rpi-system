# Use the official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and application code to the container
COPY requirements.txt ./
COPY rpi.py ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "rpi.py"]
