FROM ubuntu:latest
LABEL authors="xelt"

ENTRYPOINT ["top", "-b"]