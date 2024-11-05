# Use an official Python image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend code into the container
COPY . .

# Create directories for file uploads and processed output
RUN mkdir -p UPLOAD_DIRECTORY OUTPUT_DIRECTORY

# Expose the port that FastAPI will run on
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
