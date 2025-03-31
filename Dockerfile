FROM python:3.13-slim

WORKDIR /app

# Install PDM
RUN pip install pdm

# Copy project files
COPY pyproject.toml pdm.lock ./
COPY src ./src

# Install dependencies
RUN pdm install --prod

# Set Python path to include the virtual environment
ENV PYTHONPATH=/app/.venv/lib/python3.13/site-packages

# Expose port
EXPOSE 8000

# Run the application
CMD ["pdm", "run", "dev"] 