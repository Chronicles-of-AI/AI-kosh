# FROM python:3.8.7 as builder
# RUN apt-get update && apt-get upgrade -y
# COPY requirements.txt requirements.txt
# RUN python -m pip install -r requirements.txt

# FROM ubuntu:20.04
# RUN apt-get update && apt-get install python3 -y
# COPY --from=builder /root/.local/lib/python3.8/site-packages /usr/local/lib/python3.8/dist-packages
# COPY . /app
# WORKDIR /app
# RUN chmod 777 run.sh
# ENTRYPOINT [ "/bin/bash" ]
# CMD ["run.sh"]

FROM python:3.8.7 as builder
RUN apt-get update && apt-get upgrade -y
COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt

# FROM ubuntu:20.04
# RUN apt-get update && apt-get install python3 -y
# COPY --from=builder /root/.local/lib/python3.8/site-packages /usr/local/lib/python3.8/dist-packages

RUN chmod 777 run.sh
ENTRYPOINT [ "/bin/bash" ]
CMD ["run.sh"]