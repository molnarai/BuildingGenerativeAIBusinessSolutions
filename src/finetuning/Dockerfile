FROM nvcr.io/nvidia/pytorch:24.01-py3
RUN mkdir /myapp
WORKDIR /myapp
RUN cd /myapp
COPY ./requirements.txt .
RUN pip3 install -r ./requirements.txt 
# COPY src .
ENTRYPOINT [ "/bin/bash" ]
CMD [ "pwd", ";", "ls -lR" ]
