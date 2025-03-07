# Dockerfile for the Nuclear Power Plant ICS Simulation

# Use a lightweight Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install necessary Python packages
RUN pip install flask pymodbus==2.5.3 twisted

# Create application directory
WORKDIR /app

# Copy application code
COPY app /app

# Expose necessary ports
EXPOSE 80    
EXPOSE 502   

# Start the application
CMD ["python", "main.py"]
