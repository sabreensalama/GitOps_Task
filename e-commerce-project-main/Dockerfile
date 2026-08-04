FROM python:3.8-bullseye

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --upgrade pip==23.0.1 setuptools==57.5.0 wheel==0.38.4

RUN pip install -r requirements.txt

# Copy application source
COPY . .


# Expose application port
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]