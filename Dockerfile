FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-runtime
WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg python3-pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
