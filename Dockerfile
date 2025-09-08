FROM public.ecr.aws/docker/library/python:3.10-alpine
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]
