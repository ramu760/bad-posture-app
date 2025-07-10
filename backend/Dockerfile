# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy backend code
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]