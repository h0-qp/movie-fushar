#FROM python:latest


#RUN git clone https://github.com/h0-qp/downloaderstories.git /downloaderstories
#WORKDIR /downloaderstories
#RUN python -m pip install --upgrade pip
#RUN python -m pip install --no-cache-dir -r downloaderstories/requirements.txt
#CMD python3 download_stories_telegram2.py

FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","botStory_5_acc.py"]
#RUN apt-get -qq update && apt-get -qq install -y git wget ffmpeg mediainfo \
# && apt-get clean \
# && rm -rf /var/lib/apt/lists/*