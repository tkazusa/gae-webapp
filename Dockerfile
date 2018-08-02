FROM python:3.5.4
MAINTAINER taketoshi.kazusa@gmail.com

# install python depends
COPY Makefile /app/Makefile
COPY webapp /app/webapp
COPY requirements.txt /app/requirements.txt
RUN ls /app
WORKDIR /app

RUN make install

CMD ["/bin/bash"]
