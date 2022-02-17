FROM python:3.9-slim

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH "$PATH:/root/.local/bin/"

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.in-project true && \
    poetry install

ENV MUSIC_ROOT "/music-uploads"
ENV DESTINATION "/library"

CMD ["poetry", "run", "python", "yt-sorter.py"]