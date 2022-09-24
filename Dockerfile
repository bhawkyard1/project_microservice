FROM python:3.9-slim

WORKDIR /home/ben/code/projects/pipeline_microservices/project/working_dir

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "app", "run", "-h", "0.0.0.0"]