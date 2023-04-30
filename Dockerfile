FROM python:3.11.2
RUN pip3 install --user aiogram requests
WORKDIR /usr/src/weather/
COPY . /usr/src/weather/
CMD ["python3", "bot.py"]

