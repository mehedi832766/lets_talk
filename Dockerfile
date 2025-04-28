FROM python:3.12-slim
COPY . /signLang
WORKDIR /signLang
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 
RUN pip install -r requirements.txt
CMD ["python", "app.py"]