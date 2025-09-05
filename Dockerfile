FROM python:3.12

ARG APP_DIR

RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0

WORKDIR ${APP_DIR}

ADD ./requirements.txt ${APP_DIR}/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["/bin/bash"]