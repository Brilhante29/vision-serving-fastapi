FROM python:3.12.13-slim@sha256:423ed6ab25b1921a477529254bfeeabf5855151dc2c3141699a1bfc852199fbf

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV YOLO_CONFIG_DIR=/tmp/ultralytics
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV VISION_MODEL_DIR=/app/models

WORKDIR /app

RUN apt-get update && apt-get install --yes --no-install-recommends libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.13.0+cpu torchvision==0.28.0+cpu

COPY requirements.txt requirements-runtime.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir -r requirements-runtime.lock

COPY src ./src
COPY models ./models
RUN python -m pip install --no-cache-dir --no-deps --no-build-isolation .

RUN useradd --create-home --uid 10001 app \
    && mkdir -p /tmp/ultralytics /tmp/matplotlib \
    && chown -R app:app /app /tmp/ultralytics /tmp/matplotlib
USER 10001

EXPOSE 8000
ENTRYPOINT ["python", "-m", "vision_serving"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8000"]
