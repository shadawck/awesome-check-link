FROM python:3-alpine
LABEL name awesome-check-link
LABEL src "https://github.com/remiflavien1/awesome-check-link"
LABEL dockerfile fractalizers
RUN pip3 install awesome-check-link
ENTRYPOINT ["aclinks"]
CMD ["-h"]