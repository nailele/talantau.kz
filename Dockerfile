FROM python:3.12-slim

ENV PATH="/root/.local/bin:$PATH"

RUN pip install poetry  && poetry config virtualenvs.create false

WORKDIR /app

COPY . .
RUN poetry lock && poetry install --only main --no-interaction --no-ansi --no-root

CMD ["uvicorn", "talantau.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
