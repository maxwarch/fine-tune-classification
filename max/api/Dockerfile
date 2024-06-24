FROM python:3.11.0-slim

ENV PYTHONUNBUFFERED 1

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
ENV CACHE_HUGGINGFACE=/home/app/.cache/huggingface
RUN mkdir $APP_HOME
RUN mkdir $CACHE_HUGGINGFACE
WORKDIR $APP_HOME


# copy project
COPY ./main.py $APP_HOME
COPY ./requirements.txt $APP_HOME
COPY ./camembert-tourism-events $APP_HOME/camembert-tourism-events

RUN python -m pip install --upgrade pip 
RUN pip install -r requirements.txt

# chown all the files to the app user
RUN chown -R app:app $APP_HOME
RUN chmod 777 $CACHE_HUGGINGFACE

# change to the app user
USER app

EXPOSE 8001

CMD ["uvicorn", "main:app", "--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "8001"]