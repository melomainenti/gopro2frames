FROM ubuntu:20.04
LABEL authors="melom"

ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y git ffmpeg exiftool build-essential libjpeg-dev wget

RUN apt install -y python3-pip

RUN apt install -y libxml2-dev

RUN apt install -y python3-dev

RUN apt install -y libxslt-dev

RUN apt install -y python3.8-venv

WORKDIR /imagemagick_build/

RUN wget https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.1-44.tar.gz && tar xzf 7.1.1-44.tar.gz && cd ImageMagick-7.1.1-44/

WORKDIR /imagemagick_build/ImageMagick-7.1.1-44/

RUN sh ./configure && make -j && make install && ldconfig /usr/local/lib

WORKDIR /usr/src/app

RUN git clone https://github.com/melomainenti/gopro2frames.git && \
    cd gopro2frames && \
    git clone https://github.com/trek-view/max2sphere && \
    cd max2sphere && \
    make clean && \
    make -f Makefile-Linux && \
    cd .. && \
    git clone https://github.com/trek-view/fusion2sphere && \
    cd fusion2sphere && \
    make -f Makefile && \
    cd /usr/src/app/gopro2frames/

WORKDIR /usr/src/app/gopro2frames

RUN rm -rf max2sphere/docs
RUN rm -rf max2sphere/testframes

RUN rm -rf fusion2sphere/pgm-examples
RUN rm -rf fusion2sphere/testframes
RUN rm -rf fusion2sphere/parameter-examples

RUN git pull

RUN python3 -m venv venv

SHELL ["/bin/bash", "-c"]

RUN source venv/bin/activate && pip3 install -r requirements.txt

#ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/gopro-frame-maker"

CMD bash