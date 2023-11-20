FROM python:latest


RUN git clone https://github.com/h0-qp/movie-fushar.git /movie
WORKDIR /movie
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r movie/requirements.txt
CMD python3 bot.py
