FROM php:apache

# Update and install necessary packages
RUN apt-get update && apt-get install -y gcc make coreutils

# Copy the 'funky' script to /bin/funky and make it executable
COPY funky /bin/funky
RUN chmod +x /bin/funky

# Remove 'cat' and 'ls' binaries
RUN rm -f /bin/cat /usr/bin/ls

# Set up the website with 100 random subdirectories
RUN mkdir -p /var/www/html/ && \
    for i in $(seq 1 100); do \
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

RUN echo "SummitCTF{funky_FLAG_432}" > /root/flag.txt

# Expose port 80
EXPOSE 80

# Start Apache in the foreground
CMD ["apache2-foreground"]
