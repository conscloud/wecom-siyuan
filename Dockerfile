FROM python:3.8

WORKDIR /app

RUN apk update && \
    apk add tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY . .

CMD ["python", "app.py"]

