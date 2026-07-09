FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ../requirements.txt .

# Install the packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY Task1.py .

# Expose the port the app runs on
EXPOSE 6000

# VOLUME
VOLUME [ "/data" ]

# Define the command to run the application
CMD ["python", "Task1.py"]