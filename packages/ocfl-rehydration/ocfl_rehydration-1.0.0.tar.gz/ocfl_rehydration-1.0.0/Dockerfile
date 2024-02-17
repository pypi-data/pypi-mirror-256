FROM python:3.11-slim-buster

RUN DEBIAN_FRONTEND=noninteractive

COPY requirements.txt /app/

RUN apt-get update && \
  apt-get install -y python-dev && \
  pip install --upgrade pip && \
  pip install -r /app/requirements.txt

COPY ./ /app

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:src"
#ENTRYPOINT ["/usr/local/bin/python3", "src/ocfl_rehydration/main.py"]
CMD ["sh", "-c", "cd /app && bash"]
