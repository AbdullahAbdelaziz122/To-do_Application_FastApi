FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml ./
# Create a minimal requirements.txt for pip
RUN echo "fastapi" > requirements.txt && \
    echo "uvicorn[standard]" >> requirements.txt

RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

COPY src ./src
# Build the package wheel
RUN pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:3.12-slim AS runner

WORKDIR /app

# Copy wheels from builder and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy source code (optional, but good for debugging)
COPY src ./src

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]