FROM debian:11.2

RUN mkdir /run/sshd
COPY .ssh/ /root/.ssh/
RUN apt update && apt install openssh-server python3 -y && \
    apt clean 
ENTRYPOINT ["/usr/sbin/sshd", "-D", "-e", "-o StrictModes=no"]
