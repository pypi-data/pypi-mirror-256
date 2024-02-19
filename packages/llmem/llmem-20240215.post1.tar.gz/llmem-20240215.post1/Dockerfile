from python:3.12.2-slim-bookworm

COPY ./ /src
RUN pip wheel --no-deps /src && pip install  --no-cache-dir llmem*.whl && rm -rf /src

WORKDIR /workspace
ENTRYPOINT [ "uvicorn", "llmem:app", "--host", "0.0.0.0"]