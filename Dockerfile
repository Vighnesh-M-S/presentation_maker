# Use an official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy backend files
COPY Backend/ /app/

# Copy frontend files
COPY Frontend/ /app/Frontend/

COPY .env /app/.env



# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 9090

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090"]
