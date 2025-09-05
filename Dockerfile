FROM python:3.12

ARG WORK_DIR

RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0

WORKDIR ${WORK_DIR}

ADD ./requirements.txt ${WORK_DIR}/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["/bin/bash"]