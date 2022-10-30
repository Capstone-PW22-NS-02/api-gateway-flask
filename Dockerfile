# Follow Task-0 subtask-1
FROM python:3.8-alpine
WORKDIR /app
COPY ./requirements.txt ./app.py ./
EXPOSE 8080
RUN pip install -r requirements.txt 
CMD ["python","app.py"]