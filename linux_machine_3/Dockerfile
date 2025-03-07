# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid user prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update packages and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    iputils-ping \
    sudo

# Install Flask
RUN pip3 install Flask

# Create application directory
WORKDIR /app

# Copy application files
COPY . /app

# Expose port
EXPOSE 5000

# Create the SUID binary for chown and grant www-data sudo permissions for cat
RUN set -e && \
    apt-get update && \
    apt-get install -y build-essential && \
    echo '#include <unistd.h>' > chown_suid.c && \
    echo 'int main(int argc, char** argv) { return execvp("chown", argv); }' >> chown_suid.c && \
    gcc -o chown_suid chown_suid.c && rm chown_suid.c && \
    chown root:root chown_suid && chmod 4755 chown_suid && mv chown_suid /usr/local/bin/ && \
    echo 'www-data ALL=(ALL) NOPASSWD: /bin/cat' >> /etc/sudoers

# Set ownership and permissions
RUN chown -R www-data:www-data /app

RUN echo "SummitCTF{Ubuntu_3_8239}" > /root/flag.txt

# Run the application as the www-data user
USER www-data

# Run the application
CMD ["python3", "app.py"]
