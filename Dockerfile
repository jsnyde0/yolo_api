FROM ultralytics/ultralytics:latest-cpu

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency file first for better caching
COPY pyproject.toml .

# Install dependencies from pyproject.toml
RUN pip install --upgrade pip && \
    pip install -e .

# Download YOLO weights
RUN curl -L -o yolo11n.pt "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
