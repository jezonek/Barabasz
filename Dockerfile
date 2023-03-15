FROM python:3.9-bullseye
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
COPY . .
ENV OPENAI_API_KEY=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
ENV SIGNAL_WEBSOCKET_RX_ENDPOINT=wss://barabasz.bieda.it/v1/receive/%2B4917658296944
ENV SIGNAL_USER_NR=+4917658296944
ENV SIGNAL_HTTPS_ENDPOINT=https://barabasz.bieda.it
CMD ["python", "-u","src/barabasz.py"]