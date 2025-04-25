FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    sqlite3 \
    cron \
    sshpass \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Install Flask
RUN pip3 install flask

# Set working directory
WORKDIR /app

# Copy application files
COPY app.py .
COPY templates templates
COPY scripts scripts
COPY update_flags.py .
COPY cron_update_flags /etc/cron.d/update_flags

RUN chmod +x scripts/update_flags.sh
RUN chmod 0644 /etc/cron.d/update_flags

RUN useradd -m -s /bin/bash ansible && \
    echo "ansible:youshouldnthavethispassword" | chpasswd && \
    usermod -aG sudo ansible

RUN /usr/sbin/sshd &

# Expose the port
EXPOSE 5000 22

# Run the application and start cron
CMD ["/bin/sh", "-c", "/usr/sbin/cron && exec python3 app.py"]
