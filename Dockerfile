FROM python:3.12.3

ENV ENVIRONMENT=production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . /app/

RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/*.proto

EXPOSE 50060

# Menjalankan aplikasi
CMD ["python", "main.py"]