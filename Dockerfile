FROM python:3.9

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY secretkeys.py /app/.
COPY gpt.py /app/app.py
COPY templates /app/templates

EXPOSE 5000

CMD ["python", "app.py"]
