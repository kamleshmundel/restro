# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

# Copy app code
COPY . .

# DON'T run migrations during build - do it at runtime instead
# RUN uv run alembic upgrade head  # ❌ Remove this line

# Expose port
EXPOSE 8000

# Start the app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]