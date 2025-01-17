FROM ubuntu:latest
LABEL authors="louisliu"

ENTRYPOINT ["top", "-b"]