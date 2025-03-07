# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Set environment variables to non-interactive to prevent prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && \
    apt-get install -y \
        apache2 \
        php libapache2-mod-php \
        wget \
        tar \
        sudo \
        build-essential \
        git \
        libxml2-dev \
        unzip \
        openssh-server \
        libncurses5-dev \
        libssl-dev \
        && rm -rf /var/lib/apt/lists/*


# Create uploads directory for file uploads
RUN mkdir /var/www/html/uploads

# Change ownership to www-data (Apache user)
RUN chown -R www-data:www-data /var/www/html/uploads

# Set permissions for uploads directory
RUN chmod 755 /var/www/html/uploads

# Copy PHP and HTML files into the container
COPY upload.php /var/www/html/upload.php
COPY index.html /var/www/html/index.html

# Modify PHP configuration to enable file uploads and set limits
RUN sed -i 's/^file_uploads = .*/file_uploads = On/' /etc/php/7.4/apache2/php.ini && \
    sed -i 's/^upload_max_filesize = .*/upload_max_filesize = 10M/' /etc/php/7.4/apache2/php.ini && \
    sed -i 's/^post_max_size = .*/post_max_size = 10M/' /etc/php/7.4/apache2/php.ini && \
    sed -i 's/^;max_execution_time = .*/max_execution_time = 300/' /etc/php/7.4/apache2/php.ini && \
    sed -i 's/^;max_input_time = .*/max_input_time = 300/' /etc/php/7.4/apache2/php.ini

# Enable Apache PHP module
RUN a2enmod php7.4

# Restart Apache to apply changes
RUN service apache2 restart

# Download and install GNU Screen version 4.5.0 from GNU FTP
RUN wget https://ftp.gnu.org/gnu/screen/screen-4.5.0.tar.gz -O /tmp/screen.tar.gz && \
    tar -xzf /tmp/screen.tar.gz -C /usr/src/ && \
    cd /usr/src/screen-4.5.0 && \
    ./configure && make && make install && \
    rm -rf /usr/src/screen-4.5.0 /tmp/screen.tar.gz

# Set 'find' binary as SUID to allow potential privilege escalation
RUN chmod u+s $(which find)

# Configure sudo to allow the www-data user to execute a specific tar command without a password
RUN echo "www-data ALL=(ALL) NOPASSWD: /bin/tar czf /tmp/some.tar.gz *" > /etc/sudoers.d/www-data_tar && \
    chmod 440 /etc/sudoers.d/www-data_tar

# Set up SSH access
RUN mkdir /var/run/sshd
RUN echo 'root:REALLYH4RDP455W0RD:)' | chpasswd


RUN echo 'SummitCTF{Ubuntu_1_FLAG_4823}' > /root/flag.txt

# Expose necessary ports
EXPOSE 80 22

# Set the default command to start Apache and SSH services
CMD service apache2 start && service ssh start && tail -f /dev/null
