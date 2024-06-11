FROM python:3.10

WORKDIR /mentortest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN ollama --version

RUN ollama start & \
    sleep 5 && \
    ollama pull mxbai-embed-large

COPY . .

EXPOSE 5001

RUN chmod +x /mentortest/start_ollama.sh
ENTRYPOINT ["/mentortest/start_ollama.sh"]

CMD ["python3", "api.py"]

#docker build -t mentor_test_api .
#docker run -p 5001:5001 mentor_test_api 