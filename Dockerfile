FROM python:2.7
ADD . /restccnu
WORKDIR /restccnu
ENV USER_AGENT_FILE /restccnu/fuckccnu/multiUA/user_agents.txt
ENV REST_MONGO_HOST 123.56.41.13
ENV REST_MONGO_PORT 27020
ENV DSN_KEY https://d438bb8419534626a1eff3f4b79a37eb:75109875b95d490aafd5de57caa9cf7e@sentry.io/101268

RUN pip install --index-url http://pypi.doubanio.com/simple/ -r requirements.txt --trusted-host=pypi.doubanio.com
