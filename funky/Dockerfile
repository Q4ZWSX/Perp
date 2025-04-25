FROM php:apache

# Update and install necessary packages including openssh-server and sudo
RUN apt-get update && apt-get install -y gcc make coreutils openssh-server sudo && \
    ssh-keygen -A

# Remove 'cat' and 'ls' binaries
RUN rm -f /usr/bin/ls /usr/bin/cat

# Set up the website with 100 random subdirectories
RUN mkdir -p /var/www/html/ && \
    for i in $(seq 1 10000); do \
      dir=$(head /dev/urandom | tr -dc a-z0-9 | head -c12); \
      mkdir "/var/www/html/$dir"; \
    done

# Copy 'shell.php' into a random subdirectory
COPY shell.php /tmp/shell.php
RUN random_dir=$(find /var/www/html/ -mindepth 1 -maxdepth 1 -type d | shuf -n 1); \
    mv /tmp/shell.php "$random_dir/"

# Set permissions for the web directories
RUN chmod -R 755 /var/www/html/

# Copy 'index.php' to the web root
COPY index.php /var/www/html/index.php

# Copy and compile 'root.c' to create the SUID 'root' executable
COPY root.c /tmp/root.c
RUN mkdir -p /backups/shells && \
    gcc /tmp/root.c -o /backups/shells/root && \
    chmod u+s /backups/shells/root && \
    rm /tmp/root.c

# Set up SSH server
RUN mkdir -p /var/run/sshd && \
    # Ensure PasswordAuthentication is enabled
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Create the ansible user
RUN useradd -m -s /bin/bash ansible && \
    echo "ansible:youshouldnthavethispassword" | chpasswd && \
    usermod -aG sudo ansible

# Create the flag
RUN echo "SummitCTF{funkyFLAG_432}" > /root/flag.txt

# Copy and set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose ports 80 and 22
EXPOSE 80 22

# Start the services
ENTRYPOINT ["/entrypoint.sh"]
