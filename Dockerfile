FROM python:3.12

RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["/bin/bash"]