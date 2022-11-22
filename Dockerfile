FROM python:3.9.15-slim
WORKDIR /app
RUN apt-get update -y && apt-get install make -y

COPY . .
RUN pip install flit==3.7.1
RUN FLIT_ROOT_INSTALL=1 flit install

EXPOSE 8000
CMD make run