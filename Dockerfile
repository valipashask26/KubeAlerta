# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the PYTHONPATH
ENV PYTHONPATH /kubealerta

# Create a non-root user to run the application
RUN useradd -ms /bin/bash appuser
USER appuser

# Set the working directory to /app
WORKDIR /kubealerta/kubealerta

# Copy only the requirements file to avoid caching the entire project
COPY --chown=appuser:appuser ./kubealerta/requirements.txt /kubealerta/kubealerta/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY --chown=appuser:appuser ./kubealerta /kubealerta/kubealerta




# Expose the port your app runs on
EXPOSE 5000

# Run main.py when the container launches
CMD ["python", "./kubealerta/main.py"]