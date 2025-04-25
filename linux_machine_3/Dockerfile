# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid user prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update packages and install dependencies (including SSH and sudo)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    iputils-ping \
    sudo \
    openssh-server \
    build-essential

# Install Flask
RUN pip3 install Flask

# Create application directory
WORKDIR /app

# Copy application files
COPY . /app

# Create the SUID binary for chown and grant www-data sudo permissions for cat
RUN set -e && \
    echo '#include <unistd.h>' > chown_suid.c && \
    echo 'int main(int argc, char** argv) { return execvp("chown", argv); }' >> chown_suid.c && \
    gcc -o chown_suid chown_suid.c && rm chown_suid.c && \
    chown root:root chown_suid && chmod 4755 chown_suid && mv chown_suid /usr/local/bin/ && \
    echo 'www-data ALL=(ALL) NOPASSWD: /bin/cat' >> /etc/sudoers

# Set ownership and permissions
RUN chown -R www-data:www-data /app

# Set up SSH server
RUN mkdir -p /var/run/sshd && \
    # Ensure PasswordAuthentication is enabled
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    ssh-keygen -A

# Create ansible user
RUN useradd -m -s /bin/bash ansible && \
    echo "ansible:youshouldnthavethispassword" | chpasswd && \
    usermod -aG sudo ansible

# Create the flag
RUN echo "SummitCTF{Ubuntu_3_8239}" > /root/flag.txt

# Copy and set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose ports (5000 for Flask, 22 for SSH)
EXPOSE 5000 22

# Run the application
ENTRYPOINT ["/entrypoint.sh"]