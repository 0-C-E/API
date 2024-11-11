# Use the official Python 3.13 image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /

# Copy all files to the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
