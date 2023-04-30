FROM python:3.11.2
WORKDIR /usr/src/weather/
COPY . /usr/src/weather/
RUN pip3 install --user -r requirements.txt 
CMD ["python3", "bot.py"]
