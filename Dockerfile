FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    openssh-client openssh-server sudo python3 python3-pip && \
    useradd -m devops && echo "devops:devops" | chpasswd && \
    mkdir -p /var/run/sshd

# SSHD config baseline
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

CMD ["/usr/sbin/sshd","-D"]
