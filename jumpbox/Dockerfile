FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages and create the guest user
RUN apt-get update && \
    apt-get install -y openssh-server sudo netcat && \
    mkdir /var/run/sshd && \
    useradd -m -s /bin/bash guest && \
    echo 'guest:guest' | chpasswd && \
    echo 'guest ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
