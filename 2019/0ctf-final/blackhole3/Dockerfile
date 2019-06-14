FROM ubuntu:16.04
MAINTAINER hen
RUN apt-get update -y && apt-get install -y python3 libseccomp-dev
RUN apt-get update -y && apt-get upgrade -y
COPY --chown=root:10000 ./flag /
RUN mkdir /home/blackhole3 && chown root:10000 /home/blackhole3
COPY --chown=root:10000 blackhole3 libinit.so wrapper.py /home/blackhole3/
RUN groupadd -g 10000 blackhole3 && useradd -N -u 10000 -g 10000 blackhole3 && chmod 750 /home/blackhole3  && chmod 440 /flag
USER 10000:10000
CMD /home/blackhole3/wrapper.py
