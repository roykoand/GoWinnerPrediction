FROM tensorflow/tensorflow:latest-jupyter

LABEL source="https://github.com/Inoxoft/ml-template-repo/blob/main/install/minimal.Dockerfile"

RUN mkdir -p /tf
WORKDIR /tf

# python 3.6.9 
RUN /usr/bin/python3 -m pip install --upgrade pip
ENV PYTHONPATH "${PYTHONPATH}:/tf"

COPY ./requirements.txt .
RUN pip install -r requirements.txt 

